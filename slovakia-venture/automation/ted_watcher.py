#!/usr/bin/env python3
"""TED tender watcher.

Polls the EU TED API for notices matching a CPV allow-list, scores them for
relevance, and emits a daily digest. Deduplicates against local state so a
notice is reported once.

    python3 ted_watcher.py              # live query
    python3 ted_watcher.py --dry-run    # offline, uses fixtures/, no network

NOTE: the live request/response shape could not be verified when this was
written (api.ted.europa.eu was unreachable from the build environment).
Parsing is deliberately tolerant. Run live once and adjust FIELD_MAP if the
field names differ; nothing else should need to change.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
STATE_DIR = HERE / "state"
FIXTURES = HERE / "fixtures"

# Map our internal names -> candidate keys in the TED response. First hit wins.
FIELD_MAP = {
    "notice_id": ("notice-identifier", "publication-number", "ND", "id"),
    "title": ("notice-title", "title", "TI", "name"),
    "buyer": ("buyer-name", "organisation-name-buyer", "AA", "contracting-authority"),
    "country": ("buyer-country", "place-of-performance-country", "CY", "country"),
    "cpv": ("classification-cpv", "cpv", "PC", "main-cpv"),
    "value": ("total-value", "estimated-value", "value", "TV"),
    "deadline": ("deadline-receipt-tender", "deadline", "DT", "submission-deadline"),
    "published": ("publication-date", "PD", "date-published"),
    "url": ("links", "notice-url", "url"),
}


def load_config(path: pathlib.Path | None = None) -> dict:
    return json.loads((path or HERE / "config.json").read_text(encoding="utf-8"))


def _first(record: dict, keys: tuple[str, ...]):
    """Return the first present, non-empty value among keys."""
    for key in keys:
        if key in record and record[key] not in (None, "", [], {}):
            return record[key]
    return None


def _flatten(value) -> str:
    """TED returns many fields as lists or language-keyed dicts."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return " ".join(_flatten(v) for v in value if v)
    if isinstance(value, dict):
        for lang in ("eng", "en", "slk", "sk"):
            if lang in value:
                return _flatten(value[lang])
        return " ".join(_flatten(v) for v in value.values() if v)
    return str(value)


def _to_float(value) -> float | None:
    text = _flatten(value).replace(",", "").replace(" ", "")
    if not text:
        return None
    cleaned = "".join(ch for ch in text if ch.isdigit() or ch == ".")
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


def _to_date(value) -> dt.date | None:
    text = _flatten(value)[:10]
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y%m%d"):
        try:
            return dt.datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def normalise(record: dict) -> dict:
    out = {name: _flatten(_first(record, keys)) for name, keys in FIELD_MAP.items()}
    out["value_eur"] = _to_float(_first(record, FIELD_MAP["value"]))
    out["deadline_date"] = _to_date(_first(record, FIELD_MAP["deadline"]))
    return out


def score(notice: dict, cfg: dict, today: dt.date) -> tuple[int, list[str], bool]:
    """Relevance score 0-100, the reasons (so a filter can be debugged), and
    whether any subject-matter signal was found at all.

    Subject matter is a GATE, not just points. Country, value band and a
    comfortable deadline are attributes almost every notice has; on their own
    they must never be enough to surface one. Without a CPV or keyword hit the
    notice is not about our subject and is dropped regardless of score.
    """
    points, reasons = 0, []

    cpv_text = notice.get("cpv", "")
    matched = [c for c in cfg["cpv_allow"] if c[:5] in cpv_text or c in cpv_text]
    if matched:
        points += 40
        reasons.append(f"CPV match {','.join(sorted(set(matched)))}")

    haystack = f"{notice.get('title', '')} {notice.get('buyer', '')}".lower()
    hits = [k for k in cfg["keywords_boost"] if k.lower() in haystack]
    if hits:
        points += min(25, 8 * len(hits))
        reasons.append(f"keywords {','.join(hits)}")

    has_subject_signal = bool(matched or hits)

    country = notice.get("country", "").upper()
    if any(c in country for c in cfg["buyer_countries"]):
        points += 15
        reasons.append(f"country {country}")

    value = notice.get("value_eur")
    if value is not None and cfg["min_value_eur"] <= value <= cfg["max_value_eur"]:
        points += 10
        reasons.append(f"value {value:,.0f} EUR in band")

    deadline = notice.get("deadline_date")
    if deadline:
        days = (deadline - today).days
        if days < cfg["min_days_to_deadline"]:
            points -= 30
            reasons.append(f"only {days}d to deadline")
        else:
            points += 10
            reasons.append(f"{days}d to deadline")

    if not has_subject_signal:
        reasons.append("no CPV or keyword match — not our subject")

    return max(0, min(100, points)), reasons, has_subject_signal


def classify(points: int, cfg: dict, has_subject_signal: bool) -> str:
    if not has_subject_signal:
        return "IGNORE"
    if points >= cfg["high_score_threshold"]:
        return "HIGH"
    return "WATCH" if points >= 30 else "IGNORE"


def fetch_live(cfg: dict) -> list[dict]:
    expert = " OR ".join(f'classification-cpv="{c}"' for c in cfg["cpv_allow"])
    payload = {
        "query": expert,
        "fields": sorted({k for keys in FIELD_MAP.values() for k in keys}),
        "limit": cfg.get("page_size", 100),
        "page": 1,
    }
    request = urllib.request.Request(
        cfg["api_url"],
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        body = json.loads(response.read().decode("utf-8"))
    if isinstance(body, list):
        return body
    for key in ("notices", "results", "items", "data"):
        if isinstance(body.get(key), list):
            return body[key]
    return []


def load_seen() -> set[str]:
    path = STATE_DIR / "seen.json"
    if not path.exists():
        return set()
    try:
        return set(json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError):
        return set()


def save_seen(seen: set[str]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / "seen.json").write_text(json.dumps(sorted(seen)), encoding="utf-8")


def write_heartbeat(fetched: int, reported: int) -> None:
    """Silence is the failure mode: record every run so absence is detectable."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / "last_run.json").write_text(
        json.dumps(
            {
                "ran_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                "fetched": fetched,
                "reported": reported,
            }
        ),
        encoding="utf-8",
    )


def build_digest(records: list[dict], cfg: dict, seen: set[str], today: dt.date) -> tuple[str, list[dict]]:
    scored, skipped_seen = [], 0
    for record in records:
        notice = normalise(record)
        if not notice["notice_id"]:
            continue
        if notice["notice_id"] in seen:
            skipped_seen += 1
            continue
        points, reasons, signal = score(notice, cfg, today)
        notice.update(score=points, band=classify(points, cfg, signal), reasons=reasons)
        scored.append(notice)

    keep = [n for n in scored if n["band"] != "IGNORE"]
    keep.sort(key=lambda n: -n["score"])

    lines = [
        f"TED DIGEST — {today.isoformat()}",
        "=" * 60,
        f"fetched {len(records)} · already seen {skipped_seen} · "
        f"scored {len(scored)} · reportable {len(keep)}",
        "",
    ]
    if not keep:
        lines.append("No new relevant notices.")
        lines.append("NOTE: zero reportable is not the same as zero published —")
        lines.append("check the counts above before assuming a quiet week.")
    for notice in keep:
        deadline = notice["deadline_date"].isoformat() if notice["deadline_date"] else "?"
        value = f"{notice['value_eur']:,.0f} EUR" if notice["value_eur"] else "value n/a"
        lines += [
            f"[{notice['band']}] {notice['score']}/100  {notice['notice_id']}",
            f"  {notice['title'][:100]}",
            f"  buyer: {notice['buyer'][:70]}  |  {value}  |  deadline: {deadline}",
            f"  why: {'; '.join(notice['reasons'])}",
            "",
        ]
    return "\n".join(lines), scored


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="use fixtures, no network")
    parser.add_argument("--no-state", action="store_true", help="do not read/write seen state")
    args = parser.parse_args(argv)

    cfg = load_config()
    today = dt.date.today()

    if args.dry_run:
        records = json.loads((FIXTURES / "ted_sample.json").read_text(encoding="utf-8"))
    else:
        try:
            records = fetch_live(cfg)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            print(f"TED fetch failed: {exc}", file=sys.stderr)
            print("Watcher did NOT run successfully — treat as an alert.", file=sys.stderr)
            return 2

    seen = set() if args.no_state else load_seen()
    digest, scored = build_digest(records, cfg, seen, today)
    print(digest)

    if not args.no_state:
        save_seen(seen | {n["notice_id"] for n in scored})
    write_heartbeat(len(records), sum(1 for n in scored if n["band"] != "IGNORE"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
