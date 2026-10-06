#!/usr/bin/env python3
"""Lean-start one-off cost and monthly run-rate, with three staffing options.

Slovak payroll constants are 2026 figures (F) — see 16-lean-start-and-first-hire.md
for sources. Change them here when they move; nothing is hardcoded elsewhere.

    python3 lean_monthly.py
"""
from __future__ import annotations

# --- Slovak constants, 2026 (F) ------------------------------------------------
MIN_WAGE_MONTH = 915.00        # EUR gross, from 01/01/2026
MIN_WAGE_HOUR = 5.259          # EUR at 40 h/week
EMPLOYER_RATE = 0.362          # 25.2% social + 11% health
LIVING_MIN_ADULT = 295.22      # from 01/07/2026 (was 284.13 to 30/06/2026)
S50_CONTRIB_24M = 1291.17      # para 50, jobseeker registered >=24 months, 2026
DPC_MAX_H_WEEK = 10            # dohoda o pracovnej cinnosti, avg per employer

# --- One-off setup (the user's own list) --------------------------------------
ONE_OFF = [
    ("s.r.o. incorporation",                     220,   850, "(F)"),
    ("Food trade licence + RVPS registration",     7,   130, "(R)"),
    ("Bank account opening",                       0,    50, "(R)"),
    ("Domain (.sk) + first year hosting",         40,    75, "(R) you build the site"),
    ("Certification prep: HACCP docs + training", 800,  2500, "(R)"),
    ("Manual batch coder (hand-held)",           100,   400, "(R)"),
    ("Barcode / label printer (hand-held)",      300,   900, "(R)"),
    ("Computer",                                   0,   900, "(R) 0 if you have one"),
    ("Calibrated bench scale",                   200,   600, "(R)"),
    ("Kit nest trays (14 menus) + evidence camera", 500, 2100, "(R) 14 S8"),
    ("Marketing materials + print",              300,  1000, "(F) your cap"),
    ("Sample components, ~50 packs",            1250,  1750, "(R)"),
    ("Sample packaging + carriage, 12 dispatches", 480, 1440, "(R)"),
    ("UVO ZHS registration",                       0,   100, "(R)"),
    ("NCAGE + NSPA Source File",                   0,     0, "(F) free"),
]

# --- Monthly run-rate, excluding staff ----------------------------------------
MONTHLY_BASE = [
    ("Premises: approved-kitchen hire",          200,   750, "(R)"),
    ("Utilities share",                           50,   250, "(R)"),
    ("Accountancy",                               50,   120, "(R)"),
    ("Insurance (liability + product), instalments", 25,  75, "(R)"),
    ("Bank account fees",                          5,    20, "(R)"),
    ("Phone + internet",                          20,    45, "(R)"),
    ("Domain + hosting (amortised)",               3,     7, "(R)"),
    ("Van hire, ~3 days/month",                  120,   250, "(R)"),
    ("Fuel + travel",                             80,   200, "(R)"),
    ("Consumables: film, labels, cartons",        40,   150, "(R)"),
]


def band(rows):
    return sum(r[1] for r in rows), sum(r[2] for r in rows)


def table(title, rows):
    print(f"\n{title}")
    print("-" * 92)
    print(f"{'ITEM':<46}{'LOW':>9}{'HIGH':>9}  NOTE")
    print("-" * 92)
    for item, lo, hi, note in rows:
        print(f"{item:<46}{lo:>9,}{hi:>9,}  {note}")
    lo, hi = band(rows)
    print("-" * 92)
    print(f"{'SUBTOTAL':<46}{lo:>9,}{hi:>9,}")
    return lo, hi


def staffing():
    print("\n\nSTAFFING OPTIONS — monthly employer cost")
    print("=" * 92)
    rows = []

    # A. Solo
    rows.append(("A. You only, no staff", 0.0, 0.0,
                 "Correct for Phase 0 per 09 S2"))

    # B. para 51 graduate practice
    rows.append(("B. para 51 absolventska praxa, 20 h/week", 0.0, 0.0,
                 f"UPSVaR pays the graduate EUR{LIVING_MIN_ADULT:.2f}/mo + "
                 f"accident ins. <=EUR15. YOU PAY NOTHING"))

    # C. dohoda (DPC) at the jobseeker earnings ceiling
    dpc_hours = LIVING_MIN_ADULT / MIN_WAGE_HOUR
    dpc_gross = LIVING_MIN_ADULT
    dpc_cost = dpc_gross * (1 + EMPLOYER_RATE)
    rows.append(("C. Dohoda (DPC) at the on-register earnings cap",
                 dpc_cost, dpc_cost,
                 f"EUR{dpc_gross:.2f} gross = {dpc_hours:.0f} h/mo at min hourly; "
                 f"person STAYS on the register"))

    # D. full minimum wage employee
    full_cost = MIN_WAGE_MONTH * (1 + EMPLOYER_RATE)
    rows.append(("D. Full-time employee at minimum wage",
                 full_cost, full_cost,
                 f"EUR{MIN_WAGE_MONTH:,.2f} gross + {EMPLOYER_RATE:.1%} = "
                 f"EUR{full_cost:,.2f} cost of labour"))

    # E. full employee with para 50 offset
    net_first = full_cost - S50_CONTRIB_24M
    rows.append(("E. Full-time + para 50 subsidy (first month)",
                 net_first, net_first,
                 f"EUR{S50_CONTRIB_24M:,.2f} contribution for a jobseeker "
                 f"registered >=24 months"))

    print(f"{'OPTION':<48}{'EUR/MONTH':>12}  NOTE")
    print("-" * 92)
    for name, lo, hi, note in rows:
        val = f"{lo:,.2f}" if lo == hi else f"{lo:,.0f}-{hi:,.0f}"
        print(f"{name:<48}{val:>12}")
        print(f"{'':<48}{'':>12}  {note}")
    return rows


def main():
    o_lo, o_hi = table("ONE-OFF SETUP (lean start)", ONE_OFF)
    m_lo, m_hi = table("MONTHLY RUN-RATE, before any staff", MONTHLY_BASE)
    staff = staffing()

    print("\n\nTOTAL MONTHLY, BY STAFFING OPTION")
    print("=" * 92)
    for name, lo, hi, _ in staff:
        print(f"{name:<48}{m_lo+lo:>10,.0f} - {m_hi+hi:>9,.0f}  EUR/month")

    print("\n" + "=" * 92)
    print(f"ONE-OFF to open the doors : EUR {o_lo:,} - {o_hi:,}")
    print(f"Month 1 all-in (solo)     : EUR {o_lo+m_lo:,} - {o_hi+m_hi:,}")
    print(f"6 months solo runway      : EUR {o_lo+6*m_lo:,} - {o_hi+6*m_hi:,}")
    print("=" * 92)


if __name__ == "__main__":
    main()
