#!/usr/bin/env python3
"""Shelf-life rotation engine (Tier 2).

A ration pack is a depreciating asset with a hard cliff. This computes
remaining shelf life as a PERCENTAGE of total life — which is how buyers
actually accept or reject stock — flags lots before they become write-offs,
and emits a FEFO (first-expiry-first-out) pick list.

    python3 rotation_calendar.py --ledger fixtures/stock_sample.csv
    python3 rotation_calendar.py --ledger <csv> --min-life-pct 75 --as-of 2026-09-17
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import pathlib
import sys

# Remaining-life percentage thresholds, evaluated in order.
BANDS = (
    (0.00, "EXPIRED"),
    (0.15, "CRITICAL"),
    (0.30, "ROTATE_NOW"),
    (0.50, "ROTATE_SOON"),
)
REQUIRED_COLUMNS = {"lot", "product", "qty", "produced", "expiry"}


def parse_date(text: str) -> dt.date:
    return dt.datetime.strptime(text.strip(), "%Y-%m-%d").date()


def load_ledger(path: pathlib.Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return []
    missing = REQUIRED_COLUMNS - set(rows[0])
    if missing:
        raise ValueError(f"ledger missing columns: {', '.join(sorted(missing))}")
    return rows


def assess(row: dict, as_of: dt.date, min_life_pct: float) -> dict:
    produced, expiry = parse_date(row["produced"]), parse_date(row["expiry"])
    total_days = (expiry - produced).days
    remaining_days = (expiry - as_of).days

    if total_days <= 0:
        raise ValueError(f"lot {row['lot']}: expiry is not after production date")

    remaining_pct = max(0.0, remaining_days / total_days)

    status = "OK"
    for threshold, label in BANDS:
        if remaining_pct <= threshold:
            status = label
            break

    # A lot can be perfectly saleable in general but already fail a specific
    # contract's minimum-remaining-life clause. That is the expensive surprise.
    breaches_contract = remaining_pct * 100 < min_life_pct

    return {
        "lot": row["lot"],
        "product": row["product"],
        "qty": int(float(row["qty"])),
        "location": row.get("location", ""),
        "customer": row.get("customer", ""),
        "expiry": expiry,
        "total_days": total_days,
        "remaining_days": remaining_days,
        "remaining_pct": round(remaining_pct * 100, 1),
        "status": status,
        "breaches_contract": breaches_contract,
    }


def report(rows: list[dict], as_of: dt.date, min_life_pct: float) -> str:
    assessed = sorted(
        (assess(r, as_of, min_life_pct) for r in rows),
        key=lambda a: a["expiry"],  # FEFO
    )

    lines = [
        f"ROTATION REPORT — as of {as_of.isoformat()}",
        f"contractual minimum remaining life: {min_life_pct:.0f}%",
        "=" * 78,
        f"{'LOT':<14}{'PRODUCT':<20}{'QTY':>7}{'EXPIRY':>12}{'LIFE%':>7}  STATUS",
        "-" * 78,
    ]
    for item in assessed:
        flag = " !CONTRACT" if item["breaches_contract"] else ""
        lines.append(
            f"{item['lot']:<14}{item['product'][:19]:<20}{item['qty']:>7}"
            f"{item['expiry'].isoformat():>12}{item['remaining_pct']:>7.1f}"
            f"  {item['status']}{flag}"
        )

    action = [a for a in assessed if a["status"] != "OK" or a["breaches_contract"]]
    at_risk_units = sum(a["qty"] for a in action)

    lines += [
        "-" * 78,
        f"lots: {len(assessed)} · needing action: {len(action)} · units at risk: {at_risk_units:,}",
        "",
        "FEFO PICK LIST (ship these first):",
    ]
    if action:
        for item in action:
            reason = item["status"] if item["status"] != "OK" else "below contract minimum"
            lines.append(
                f"  {item['lot']:<14} {item['qty']:>6} units  "
                f"{item['location'] or '-':<12} → {reason}"
            )
    else:
        lines.append("  nothing requires rotation.")

    expired = [a for a in assessed if a["status"] == "EXPIRED"]
    if expired:
        lines += ["", f"** WRITE-OFF RISK: {len(expired)} lot(s) already expired **"]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", required=True, type=pathlib.Path)
    parser.add_argument("--as-of", default=dt.date.today().isoformat())
    parser.add_argument(
        "--min-life-pct",
        type=float,
        default=75.0,
        help="contractual minimum remaining shelf life, percent (default 75)",
    )
    args = parser.parse_args(argv)

    try:
        rows = load_ledger(args.ledger)
    except (OSError, ValueError) as exc:
        print(f"cannot read ledger: {exc}", file=sys.stderr)
        return 2
    if not rows:
        print("ledger is empty — nothing to assess.", file=sys.stderr)
        return 1

    print(report(rows, parse_date(args.as_of), args.min_life_pct))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
