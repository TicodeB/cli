#!/usr/bin/env python3
"""Verify Addendum_A_Model_LIVE.xlsx against the source workbook's figures.

LibreOffice cannot open xlsx files in the build container (no Java), so the
formulas cannot be recalculated here. Instead this re-implements the model
logic in Python and checks it against the hardcoded numbers in the source
Addendum_A_Model.xlsx, flagging every intentional divergence.

    python3 verify_live_model.py
"""
from __future__ import annotations

import pathlib
import sys

from openpyxl import load_workbook

HERE = pathlib.Path(__file__).resolve().parent
MODEL = HERE / "Addendum_A_Model_LIVE.xlsx"
FAILURES: list[str] = []


def check(name: str, got, expected, tol: float = 1.5, note: str = "") -> None:
    ok = abs(got - expected) <= tol
    mark = "PASS" if ok else "FAIL"
    extra = f"  ({note})" if note else ""
    print(f"  {mark}  {name:<46} {got:>12,.0f} vs {expected:>12,.0f}{extra}")
    if not ok:
        FAILURES.append(name)


def inputs() -> dict:
    ws = load_workbook(MODEL)["Assumptions"]
    out = {}
    for r in range(5, 34):
        label, value = ws.cell(row=r, column=1).value, ws.cell(row=r, column=2).value
        if label and isinstance(value, (int, float)):
            out[label] = value
    return out


def main() -> int:
    a = inputs()
    marginal = (a["Irish income tax — higher rate"] + a["USC — top band"] + a["PRSI"])
    target = a["Target net income"] * 12
    payout = a["Dividend payout ratio"]
    cit = a["Corporate tax — standard rate"]

    print("Income bridge (source: Addendum_A_Model.xlsx Income_Bridge_Revised)")
    for label, rate, own, expect in (
        ("7% Slovak, 70% owned", a["Slovak dividend withholding (credited)"], 0.70, 194443),
        ("Irish marginal, 70% owned", marginal, 0.70, 378309),
        ("Irish marginal, 100% owned", marginal, 1.00, 264816),
    ):
        pbt = target / (1 - rate) / own / payout / (1 - cit)
        check(f"PBT needed — {label}", pbt, expect)

    print("\nP&L (source: PL_AssetLight)")
    revenue = [162000, 668000, 1316000, 2124000, 2800000]
    margin = [0.13, 0.21, 0.25, 0.27, 0.28]
    overheads = [28000, 110000, 190000, 280000, 350000]
    interest = [0, 6000, 6000, 5000, 4000]
    grant = [0, 10000, 10000, 10000, 10000]
    line, rack, period = (a["Capex — container kitting line"],
                          a["Capex — racking + WMS"], a["Depreciation period"])
    depreciation = [0, line / period] + [(line + rack) / period] * 3
    source_pbt = [-6940, 14280, 123000, 278480, 420000]

    for i, year in enumerate((2027, 2028, 2029, 2030, 2031)):
        pbt = (revenue[i] * margin[i] - overheads[i]
               - depreciation[i] + grant[i] - interest[i])
        note = "INTENTIONAL: source depreciates the 2029 racking from 2028" if year == 2028 else ""
        check(f"PBT {year}", pbt, source_pbt[i],
              tol=6000 if year == 2028 else 1.5, note=note)

    print("\nExit value (source: Exit_Value)")
    limit = a["Entrepreneur Relief lifetime limit"]
    er, std, mult = (a["Irish CGT — Entrepreneur Relief rate"],
                     a["Irish CGT — standard rate above limit"], a["EBITDA multiple at exit"])
    for ebitda, own, expect in ((250000, 0.70, 787500), (250000, 1.00, 1125000),
                                (400000, 1.00, 1685000), (434000, 0.70, 1362730)):
        share = ebitda * mult * own
        cgt = min(share, limit) * er + max(0, share - limit) * std
        check(f"Net to you — EBITDA {ebitda:,} @ {own:.0%}", share - cgt, expect)

    print("\nFunding portfolio (source: Funding_Portfolio)")
    ws = load_workbook(MODEL)["Funding_Portfolio"]
    probs = [ws.cell(row=r, column=5).value for r in range(5, 19)
             if isinstance(ws.cell(row=r, column=5).value, (int, float))]
    at_least_one = 1.0
    for p in probs:
        at_least_one *= (1 - p)
    at_least_one = 1 - at_least_one
    print(f"  INFO  {len(probs)} instruments, P(at least one) = {at_least_one:.4f}")
    if at_least_one < 0.90:
        FAILURES.append("portfolio below 90%")

    print("\nSector scoring v2 (weights must sum to 100%)")
    ws = load_workbook(MODEL)["Sector_Scoring_v2"]
    weights = [ws.cell(row=5, column=c).value for c in range(2, 9)]
    total = sum(w for w in weights if isinstance(w, (int, float)))
    check("Weight total", total * 100, 100, tol=0.01)

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILED: {', '.join(FAILURES)}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
