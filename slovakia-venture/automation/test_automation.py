#!/usr/bin/env python3
"""Offline tests for the automation scripts. No network, no dependencies.

    python3 test_automation.py
"""
from __future__ import annotations

import datetime as dt
import json
import pathlib
import sys

import rotation_calendar as rc
import ted_watcher as tw

HERE = pathlib.Path(__file__).resolve().parent
FAILURES: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name} {detail}")
        FAILURES.append(name)


def test_ted_normalisation() -> None:
    print("ted_watcher: normalisation")
    records = json.loads((HERE / "fixtures" / "ted_sample.json").read_text(encoding="utf-8"))
    notice = tw.normalise(records[0])
    check("extracts notice id", notice["notice_id"] == "456343-2026", notice["notice_id"])
    check("prefers English title", "Combat food rations" in notice["title"], notice["title"])
    check("parses value", notice["value_eur"] == 711374.83, str(notice["value_eur"]))
    check("parses deadline", notice["deadline_date"] == dt.date(2026, 10, 21))
    check("flattens cpv list", "15894100" in notice["cpv"], notice["cpv"])


def test_ted_scoring() -> None:
    print("ted_watcher: scoring and filtering")
    cfg = tw.load_config()
    records = json.loads((HERE / "fixtures" / "ted_sample.json").read_text(encoding="utf-8"))
    today = dt.date(2026, 9, 17)
    digest, scored = tw.build_digest(records, cfg, seen=set(), today=today)
    by_id = {n["notice_id"]: n for n in scored}

    check("ration tender is HIGH", by_id["456343-2026"]["band"] == "HIGH",
          str(by_id["456343-2026"]["score"]))
    check("food DNS is HIGH", by_id["351086-2026"]["band"] == "HIGH",
          str(by_id["351086-2026"]["score"]))
    check("office furniture is IGNORE", by_id["999001-2026"]["band"] == "IGNORE",
          str(by_id["999001-2026"]["score"]))
    check("near-deadline notice penalised",
          by_id["999002-2026"]["score"] < by_id["456343-2026"]["score"])
    check("scores carry reasons", all(n["reasons"] for n in scored))
    check("digest reports counts", "fetched 4" in digest, digest.splitlines()[2])
    check("IGNORE excluded from digest", "999001-2026" not in digest)


def test_ted_dedupe() -> None:
    print("ted_watcher: deduplication")
    cfg = tw.load_config()
    records = json.loads((HERE / "fixtures" / "ted_sample.json").read_text(encoding="utf-8"))
    today = dt.date(2026, 9, 17)
    digest, _ = tw.build_digest(records, cfg, seen={"456343-2026"}, today=today)
    check("seen notice suppressed", "456343-2026" not in digest)
    check("seen count reported", "already seen 1" in digest)


def test_ted_empty_is_visible() -> None:
    print("ted_watcher: empty result is distinguishable")
    cfg = tw.load_config()
    digest, _ = tw.build_digest([], cfg, seen=set(), today=dt.date(2026, 9, 17))
    check("states no new notices", "No new relevant notices." in digest)
    check("warns zero != quiet", "not the same as zero published" in digest)


def test_rotation_bands() -> None:
    print("rotation_calendar: status bands")
    as_of = dt.date(2026, 9, 17)
    rows = rc.load_ledger(HERE / "fixtures" / "stock_sample.csv")
    assessed = {r["lot"]: r for r in (rc.assess(row, as_of, 75.0) for row in rows)}

    check("expired lot detected", assessed["L2023-220"]["status"] == "EXPIRED",
          assessed["L2023-220"]["status"])
    check("short-dated crispbread flagged",
          assessed["L2024-041"]["status"] in {"CRITICAL", "ROTATE_NOW"},
          assessed["L2024-041"]["status"])
    check("fresh kit is OK", assessed["L2026-014"]["status"] == "OK",
          assessed["L2026-014"]["status"])
    check("remaining pct computed", 0 <= assessed["L2025-008"]["remaining_pct"] <= 100)


def test_rotation_contract_clause() -> None:
    print("rotation_calendar: contract minimum-life clause")
    as_of = dt.date(2026, 9, 17)
    rows = rc.load_ledger(HERE / "fixtures" / "stock_sample.csv")
    row = next(r for r in rows if r["lot"] == "L2024-113")

    lenient = rc.assess(row, as_of, min_life_pct=10.0)
    strict = rc.assess(row, as_of, min_life_pct=95.0)
    check("passes a lenient clause", not lenient["breaches_contract"])
    check("fails a strict clause", strict["breaches_contract"])
    check("status unaffected by clause", lenient["status"] == strict["status"])


def test_rotation_fefo_order() -> None:
    print("rotation_calendar: FEFO ordering")
    as_of = dt.date(2026, 9, 17)
    rows = rc.load_ledger(HERE / "fixtures" / "stock_sample.csv")
    text = rc.report(rows, as_of, 75.0)
    lines = [l for l in text.splitlines() if l.startswith("L20")]
    expiries = [l[46:58].strip() for l in lines]
    check("listed first-expiry-first", expiries == sorted(expiries), str(expiries))
    check("write-off warning shown", "WRITE-OFF RISK" in text)


def test_rotation_bad_input() -> None:
    print("rotation_calendar: input validation")
    try:
        rc.assess({"lot": "X", "product": "p", "qty": "1",
                   "produced": "2026-01-01", "expiry": "2025-01-01"},
                  dt.date(2026, 9, 17), 75.0)
        check("rejects expiry before production", False, "no error raised")
    except ValueError:
        check("rejects expiry before production", True)


def main() -> int:
    for test in (
        test_ted_normalisation,
        test_ted_scoring,
        test_ted_dedupe,
        test_ted_empty_is_visible,
        test_rotation_bands,
        test_rotation_contract_clause,
        test_rotation_fefo_order,
        test_rotation_bad_input,
    ):
        test()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILED: {', '.join(FAILURES)}")
        return 1
    print("All tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
