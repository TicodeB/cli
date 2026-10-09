# 08 — Tier 1 Container Kitting Line: BOM, sourcing, capex

**Conclusion first (O):** buy **used, semi-automatic, and under-specified on speed**. §06 showed takt is ~2 minutes per pack even in the 2030 base case; a €35k flow-wrapper running at 60 packs/minute would sit idle 97% of the time. Spend the money on **traceability, checkweighing and detection** — the three things a defence or reserve buyer audits — and on **containerisation**, which preserves resale value and dodges site lock-in.

**Budget envelope (F, Addendum A):** €120,000–180,000 for the Tier 1 line, versus €600,000 for the original fitted hall.

---

## 1. Bill of materials

Prices are **(R)** — used-market ranges from the channels in §3, to be replaced by actual quotes. "Used" assumes refurbished with a warranty from a dealer, not an auction gamble.

### Core process equipment

| # | Item | Spec for this application | New **(R)** | Used **(R)** | Priority |
|---|---|---|---|---|---|
| 1 | **Horizontal flow-wrapper (HFFS)** | 30–60 packs/min is ample; servo preferred for repeatability | €45–90k | **€15–35k** | Essential |
| 2 | **Checkweigher** | Menu-specific target weights, reject gate, data logging | €12–25k | **€4–9k** | **Essential — see note** |
| 3 | **Metal detector** (in-line) | Ferrous/non-ferrous/stainless, auto-reject | €10–18k | **€6–12k** | Essential |
| 4 | **Date/batch coder** | Thermal transfer (TTO) or CIJ; must print lot + best-before | €6–14k | **€3–7k** | Essential |
| 5 | **Vacuum / MAP pouch sealer** | Only if you seal wet components yourself | €18–40k | **€6–20k** | Conditional |
| 6 | **Tray/pouch heat sealer** (semi-auto) | For sub-assemblies | €8–16k | €3–7k | Conditional |
| 7 | **Shrink tunnel + L-sealer** | Outer bundling | €9–18k | **€4–9k** | Useful |
| 8 | **Conveyors + kitting benches** | U-cell, stainless, height-adjustable | €10–20k | **€3–8k** | Essential |
| 9 | **Label printer + applicator** | GS1-128 / SSCC for pallets | €5–12k | **€2–5k** | Essential |
| 10 | **Pallet stretch wrapper** | Semi-automatic turntable | €5–10k | **€2–5k** | Useful |
| 11 | **Platform + bench scales, calibrated** | Legal-for-trade where needed | €2–5k | €1–2.5k | Essential |
| | **Subtotal, used** | | | **€49–119k** | |

> **(O) The checkweigher is the highest-ROI machine on this list and the one most often skipped.** §06 §4 shows it catches ~90% of kitting errors for ~€6k used. A single incomplete ration pack found by a military customer costs more in credibility than the machine costs in cash. Buy it before the shrink tunnel, before the pouch sealer, before anything optional.
>
> **(O) X-ray instead of metal detection?** €25–45k new, €12–25k used **(R)**. It finds glass, stone, bone and dense plastic that a metal detector misses. **Not at Tier 1** — but if a spec demands it, that is a contract-price conversation, not a capex decision.

### Containerisation and fit-out

| # | Item | Notes | Cost **(R)** |
|---|---|---|---|
| 12 | **2 × 40ft containers, food-grade conversion** | Insulated, hygienic panel lining, coved food-safe flooring, sealed penetrations | **€20–40k** |
| 13 | Electrical fit-out | 3-phase distribution, IP-rated, emergency stops, ≥40 kVA design | €8–15k |
| 14 | HVAC + dehumidification | Dry goods need humidity control, not cooling | €5–12k |
| 15 | Hand-wash, changing, hygiene barrier | Mandatory for food handling | €3–7k |
| 16 | Lighting (shatterproof), pest-proofing | Audit requirements | €2–4k |
| 17 | **Pallet racking** | Component buffer, ~150–300 pallet positions | €5–15k |
| 18 | Fire, first aid, signage, PPE | | €2–4k |
| | **Subtotal** | | **€45–97k** |

### Systems

| # | Item | Notes | Cost **(R)** |
|---|---|---|---|
| 19 | **Lot/traceability + rotation system** | See `10`. Build, don't buy, at this scale | €3–10k |
| 20 | Barcode scanners, label stock, tablets | | €2–4k |
| | **Subtotal** | | **€5–14k** |

### Capex build-up

| Configuration | Total **(R)** | Comment |
|---|---|---|
| **Minimum viable** — items 1,2,3,4,8,9,11,12,13,15,16,19,20, single container | **€95–120k** | Kits and seals pre-packed components. **(O) Start here** |
| **Target Tier 1** — adds 7,10,17, second container | **€125–160k** | Matches Addendum A's €120–180k envelope |
| **Extended** — adds 5,6, X-ray | **€180–230k** | **(O) Only against a spec that demands it and a contract that pays for it** |

---

## 2. What *not* to buy, and why

**(O)** This list will save more money than the sourcing list below.

| Don't buy | Why | Instead |
|---|---|---|
| High-speed automated line (>100 packs/min) | 97% idle at real takt (§06) | Semi-auto, 30–60/min |
| Robotic pick-and-place kitting cell | €80–200k; 14 menu variants means constant re-teaching. Changeover kills the business case | Two operators in a U-cell |
| A retort autoclave | That is Tier 3 manufacturing, €150k+, plus pressure-vessel regime | Buy retort meals from a co-packer (`07`) |
| Freeze-dryer | Tier 3+, capital-intensive; **(F)** no Slovak savoury lyo capacity exists, which is a *sourcing* opportunity before it is a manufacturing one | Import initially |
| A bakery line | **(F)** This is the €600k Phase 3 asset Addendum A gates behind contracts | Buy crispbread from Bonavita or equivalent |
| New rather than used | 50–70% premium for capability you will not use | Refurbished with dealer warranty |

---

## 3. Sourcing channels — verified live

**(F)** Channels confirmed to carry used food packaging equipment in the SK/CZ/DE market:

| Channel | What it has | Best for |
|---|---|---|
| **[Machineseeker](https://www.machineseeker.com/Packaging-machinery/ci-13)** | **1,834+ used packaging machine listings**; separate vacuum/shrink category | Widest EU inventory; dealer warranties |
| **[Bazoš.sk — stroje](https://stroje.bazos.sk/inzeraty/baliac%C3%AD-stroj/)** | New and refurbished packaging machines for meat, dairy, gastro | Cheapest SK finds; **(O) caveat emptor, no warranty** |
| **[Kabek (CzechTrade)](https://kabek.czechtrade.sk/pouzite-baliace-stroje)** | Used **horizontal** and vertical packaging machines, shrink-film overwrappers | Exactly the HFFS class you need; CZ proximity |
| **[GPR.sk](https://gpr.sk/sk/vakuove-baliace-stroje/)** | Vacuum packers from benchtop to continuous, food-industry focus | Item 5 if needed |
| **[Pekastroj.sk](https://www.pekastroj.sk/48-baliace-stroje-balicky)** | Bakery-sector packaging machines | Bakery-adjacent formats |
| **[Truck1.sk](https://www.truck1.sk/priemyselne-stroje/baliace-stroje)** | Industrial packaging machines | Secondary sweep |

### Buying protocol **(O)** — non-negotiable for used equipment
1. **Never buy unseen.** Demand a video of the machine running product, or attend a witnessed run.
2. **Demand a trial with your film and your pack format.** Flow-wrappers are format-specific; a machine that ran biscuits may not handle a bulky kit.
3. **Check spare-parts availability and control-system age.** A 2005 machine with an obsolete PLC is a paperweight when the drive fails. **(R) Prefer post-2012.**
4. **Confirm CE marking and a Declaration of Conformity.** Without it you cannot lawfully commission it and no insurer will cover it.
5. **Budget 10–15% of purchase price for commissioning, spares and format parts.** This is the line everyone forgets.
6. **Get three quotes on every item ≥€5k.**

---

## 4. Why containers, restated

**(F, Addendum A)** The container strategy converts the fatal fixed cost — a hall lease signed before revenue — into a movable asset with resale value: *"If the venture fails, a container line sells; a hall fit-out does not."*

**(R)** Three additional advantages worth stating explicitly:
1. **Grant site-lock defence.** Grants impose 3–5 year durability at the funded site. A movable unit gives a genuine argument for relocation if a site fails — though the grant's own clause still binds, so read it (`05` §7).
2. **Deployability becomes a product.** The same unit is Tier 4 — *"containerised field bakery/kitchen/packing units, sold or leased"* to armed forces and humanitarian agencies **(F, Addendum A)**. You are building a demonstrator while you build capacity.
3. **Phased commitment.** Start with one container and add the second when volume justifies it, instead of fitting out 400 m² on day one.

**(R) The honest counter-argument:** containers are cramped, harder to keep clean at the corners, and a food auditor will scrutinise the panel joints and floor coving. Budget for a **proper** conversion (item 12 at the upper end, €40k) rather than a shipping container with a coat of paint. A cheap conversion will fail an audit and cost more than the saving.

---

## 5. Procurement sequence — tied to the gates

| Phase | Trigger | Action | Spend |
|---|---|---|---|
| **Now → Gate 1** | — | **Quotes only.** Two used-line packages + two container-conversion quotes, for the business case | €0 |
| **Gate 1 passed** (31/12/2027) | ≥2 co-packing agreements + ≥€300k demand + grant decision | Order **minimum viable** configuration | €95–120k |
| **+6 months** | Volume confirmed | Add items 7, 10, 17, second container | €30–40k |
| **Spec-driven** | A tender demands it, priced in | X-ray, pouch sealing | €25–70k |

**(F/O) The rule that overrides all of the above:** *no binding orders before grant approval* (`05` §7). Quotes are free and do not prejudice eligibility. A purchase order does.

---

## 6. Verification actions
1. Get **two full used-line package quotes** (items 1–4, 8, 9, 11) and **two container-conversion quotes**. This replaces every **(R)** in §1 and is required for the Tier 1 business case regardless of funding route.
2. Confirm the **pack format and dimensions** from the tender spec before quoting a flow-wrapper — film width and bag length are the first questions any supplier asks.
3. Confirm whether the spec requires **metal detection or X-ray**, and whether it mandates in-line 100% checkweighing.
4. Check the **robotisation/automation voucher** (**F, Addendum A:** €3–30k at up to 85%) against items 1, 2 and 3 — it may fund the automation module specifically.
5. Confirm **reserved electrical capacity** at any candidate site against the ≥40 kVA design figure (`02` §3).
