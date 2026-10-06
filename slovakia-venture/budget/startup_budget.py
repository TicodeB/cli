#!/usr/bin/env python3
"""Startup budget for the Slovakia ration/preparedness venture.

Phases 0-2 are the real startup cost. Phase 3 (the MVP-1 line) is gated on
Gate 1 and is deliberately NOT part of the startup number.

All figures are (R) planning ranges unless marked (F) in 15-startup-budget.md.

    python3 startup_budget.py
"""
from __future__ import annotations

PHASE0 = [
    # (item, low, high, note)
    ("s.r.o. incorporation (seat in RS district)", 220, 850, "(F)"),
    ("Food trade licence (zivnost)", 7, 30, "(R)"),
    ("RVPS food-business registration", 0, 100, "(R)"),
    ("UVO ZHS register of economic operators", 0, 100, "(R)"),
    ("NCAGE + NSPA Source File", 0, 0, "(F) free"),
    ("Procurement platform accounts", 0, 0, "free"),
    ("Accountancy setup + first 3 months", 300, 900, "(R)"),
    ("Irish tax opinion (HoldCo + Entrepreneur Relief)", 400, 900, "(R)"),
    ("HACCP system documentation + food hygiene training", 800, 2500, "(R)"),
    ("Premises: approved-kitchen hire, ~60 h over 8 weeks", 900, 2400, "(R)"),
    ("MVP-0 bench equipment (13 S3)", 2160, 6450, "(R)"),
    ("Error-proofing: nest trays + evidence camera (14 S8)", 500, 2100, "(R)"),
    ("Sample components, ~50 packs bought retail", 1250, 1750, "(R)"),
    ("Sample packaging + carriage, 12 dispatches", 480, 1440, "(R)"),
    ("Liability + product insurance, year 1", 300, 900, "(R)"),
    ("Website + company email", 0, 500, "(R)"),
    ("Travel: co-packers, buyers, MH SR / MIRRI", 400, 1200, "(R)"),
]

PHASE1 = [
    ("Approved-kitchen hire, 6 months light use", 1200, 3600, "(R)"),
    ("Travel + buyer meetings", 1000, 3000, "(R)"),
    ("Scan-to-close interlock build (14 S3)", 1500, 4000, "(R)"),
    ("JTF grant consultant (12 S5 action 8)", 2000, 6000, "(R)"),
    ("Accountancy, 6 months", 900, 1800, "(R)"),
    ("Trial-order components (working capital)", 2000, 6000, "(R)"),
]

PHASE2 = [
    ("Working capital for first call-off (state pays ~60 d)", 5000, 20000, "(R)"),
    ("Bid costs / certificates / possible bid bond", 0, 2000, "(R)"),
]

PHASE3_GATED = [
    ("MVP-1 minimum viable line (08 S1)", 95000, 120000, "(R) GATED on Gate 1"),
    ("Premises lease + fit-out delta", 5000, 20000, "(R) GATED"),
]


def show(title: str, rows: list, running: list) -> tuple[int, int]:
    print(f"\n{title}")
    print("-" * 86)
    print(f"{'ITEM':<58}{'LOW':>10}{'HIGH':>10}  TAG")
    print("-" * 86)
    lo = hi = 0
    for item, a, b, note in rows:
        lo += a
        hi += b
        print(f"{item:<58}{a:>10,}{b:>10,}  {note}")
    print("-" * 86)
    print(f"{'SUBTOTAL':<58}{lo:>10,}{hi:>10,}")
    running.append((title, lo, hi))
    return lo, hi


def main() -> None:
    running: list = []
    show("PHASE 0 - setup + samples (weeks 1-8)", PHASE0, running)
    show("PHASE 1 - conversations + trials (months 3-9)", PHASE1, running)
    show("PHASE 2 - first contracts (months 9-18)", PHASE2, running)

    startup_lo = sum(lo for _, lo, _ in running)
    startup_hi = sum(hi for _, _, hi in running)

    print("\n" + "=" * 86)
    print("STARTUP TOTAL (phases 0-2, everything before any production capex)")
    print("=" * 86)
    for title, lo, hi in running:
        print(f"  {title.split(' - ')[0]:<20}{lo:>12,}{hi:>12,}")
    print(f"  {'TOTAL':<20}{startup_lo:>12,}{startup_hi:>12,}")

    p0 = running[0]
    print(f"\n  Cash needed to send the first sample (Phase 0 only): "
          f"EUR {p0[1]:,} - {p0[2]:,}")
    print(f"  Cash needed to reach Gate 0 (Phases 0-1):            "
          f"EUR {p0[1]+running[1][1]:,} - {p0[2]+running[1][2]:,}")

    print("\n" + "=" * 86)
    print("GATED - NOT part of the startup budget")
    print("=" * 86)
    g_lo = g_hi = 0
    for item, a, b, note in PHASE3_GATED:
        g_lo += a
        g_hi += b
        print(f"{item:<58}{a:>10,}{b:>10,}  {note}")
    print(f"{'SUBTOTAL (post-Gate 1, grant/loan funded)':<58}{g_lo:>10,}{g_hi:>10,}")

    print(f"\nFor comparison: the original dossier plan opened with EUR 600,000 of")
    print(f"plant capex. This reaches a first state invoice for "
          f"EUR {startup_lo:,}-{startup_hi:,},")
    print(f"i.e. {600000/startup_hi:.0f}-{600000/startup_lo:.0f}x less, with the line still "
          f"fully specified behind Gate 1.")


if __name__ == "__main__":
    main()
