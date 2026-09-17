# 11 — Model Reconciliation: where your four documents disagree

**Inputs read in full (17/09/2026):** `Slovakia_Land_and_Venture_Dossier.docx` (15/09) · `Venture_Financial_Model.xlsx` (15/09) · `Addendum_A_Defence_CivilDefence.docx` (16/09) · `Addendum_A_Model.xlsx` (16/09).

**Conclusion first (O):** the two halves of your advice set contradict each other, and you cannot act on both. The dossier's own scoring model ranks the shelf-stable bakery **#1 of 6**; Addendum A rejects it as the entry point. §2 shows the disagreement is **not** a matter of opinion — it is caused by a missing column in the scoring sheet, and it resolves with arithmetic.

Separately, §1 is a defect you should fix before relying on the newer model at all.

---

## 1. `Addendum_A_Model.xlsx` contains zero formulas

Measured directly from the file:

| Workbook | Formula cells | Total cells | Verdict |
|---|---|---|---|
| `Venture_Financial_Model.xlsx` | **336** | 52,034 | A real model. `Assumptions` drives `P&L` → `Income_Bridge` → `Funding` |
| `Addendum_A_Model.xlsx` | **0** | 632 | **A static picture of a model** |

**(F)** Every number in the Addendum A workbook — the revised income bridge, the asset-light P&L, the tier ladder, the funding probabilities, the exit values — is a typed constant. Nothing recalculates.

**(O) Why this matters more than it sounds.** Addendum A's own method depends on flexing these numbers:
- *"Re-rate them after your first grant consultant meeting"* (funding probabilities)
- Gate 1 tests ≥€300k contracted demand — you will want to see what that does to the P&L
- *"the €25–35 per pack is the load-bearing number"* — it appears nowhere as an input you can change
- The Irish tax correction is the single most valuable item in the document, and the 52.2% rate is hardcoded in three places. **(F)** PRSI is noted in that same sheet as rising to **4.35% from 10/2026** — so the headline 52.2% is already going stale, and nothing will update when it does.

The original model does this properly: *"Blue cells on the Assumptions sheet are inputs — change them and every other sheet recalculates."* The newer, more correct analysis was delivered in a weaker container.

**Traces of it are already visible.** In `Exit_Value`, the "Years of €90k target" column reads 5.2, 8.8, 15.1 where the arithmetic gives **5.25, 8.75, 15.14** (verified independently) — one cell is stored as `8.800000000000001`. Cosmetic, and it changes no decision, but it is the signature of hand-typed numbers rather than computed ones.

**And one substantive error that a live model would not have made.** `PL_AssetLight` charges depreciation of a flat **€20,000 from 2028** — that is €160,000 ÷ 8 years, i.e. the full capex programme. But the €40,000 racking/WMS is not bought until **2029** (the sheet says so itself, two rows below). The model therefore **depreciates an asset a year before it is purchased**.

| Year | Source depreciation | Charged as incurred | Source PBT | Corrected PBT |
|---|---|---|---|---|
| 2028 | €20,000 | **€15,000** | €14,280 | **€19,280** |
| 2029+ | €20,000 | €20,000 | unchanged | unchanged |

**(O)** A €5,000 swing in one year changes no gate and no decision — the point is not the money. The point is that a hardcoded sheet has no mechanism to catch this, whereas a formula reading a capex-by-year input cannot make the error at all.

**→ Action:** rebuild it as a live model. `models/Addendum_A_Model_LIVE.xlsx` in this repo does that — same structure, same numbers, but formula-driven from a single `Assumptions` sheet. See §5.

---

## 2. The contradiction, and what actually causes it

### The two verdicts
| Document | Verdict on the €600k shelf-stable bakery |
|---|---|
| Dossier §6 + `Sector_Scoring` | **Recommended.** Score **3.85/5**, rank **1 of 6** |
| Addendum A §3 | **Rejected as the entry point.** *"Do not make it the front door"* |

### The dossier's scoring weights
**(F)** From `Sector_Scoring`: Fit with skills **0.25** · Demand security **0.20** · Low capital need **0.15** · Grant eligibility **0.15** · Margin **0.15** · Speed to cash **0.10**.

Bakery scores 5, 4, 2, 5, 3, 3 → **3.85**. Verified: 1.25+0.80+0.30+0.75+0.45+0.30 = 3.85 ✓

### Scoring Addendum A's ladder on the dossier's own weights
**(R) My scores**, same 1–5 scale, same weights:

| Option | Fit | Demand | Low capital | Grant | Margin | Speed | **Score** |
|---|---|---|---|---|---|---|---|
| Shelf-stable bakery (dossier) | 5 | 4 | 2 | 5 | 3 | 3 | **3.85** |
| Tier 2 — reserve service | 4 | 5 | 4 | 3 | 4 | 2 | **3.85** |
| Tier 1 — kitting | 4 | 4 | 4 | 4 | 3 | 3 | **3.75** |
| Tier 0 — broker | 4 | 4 | 5 | 2 | 2 | 5 | **3.65** |

**(O) Read that honestly: on the dossier's own framework, the bakery still wins — or at best ties.** Addendum A's rejection of it is *not supported* by the scoring model it inherited. If you were to arbitrate between the two documents using the only quantitative tool either of them gives you, the bakery survives.

### So which is right? The scoring model is incomplete.

**(O) The framework has no criterion for the thing that actually kills ventures: capital committed before the first euro of revenue, and whether that capital is recoverable.**

"Low capital need" at 15% is a weak proxy, and there is no downside or reversibility criterion at all. That omission is exactly what Addendum A's premortem attacks — *"the hall was rented from month one and burned €22k of dead rent... the plant ran at 35% utilisation"* — and what the Downside case proves, where the company **never makes a profit in any year through 2031** (**F**, `P&L` rows 38–44: PBT is negative in all five years).

Add one column — **Reversibility: how much of the committed capital survives failure** — at a 20% weight, scaling the existing six by 0.8 so the weights still sum to 1.00:

| Option | Reversibility **(R)** | Rationale | **Rescored** |
|---|---|---|---|
| Tier 0 — broker | **5** | <€5k at risk; nothing to unwind | **3.92** |
| Tier 1 — kitting | **4** | Container line has resale value **(F, Addendum A)** | **3.80** |
| Tier 2 — reserve service | 3 | Racking + WMS partly recoverable | **3.68** |
| Shelf-stable bakery | **1** | Hall fit-out and certification are unrecoverable | **3.28** |

**The ranking inverts, and the bakery falls to last.** That is the reconciliation: Addendum A is right, but for a reason its own document never states quantitatively, and the dossier's scoring sheet is what needs correcting — not just its conclusion.

> **(O) This is the single most useful thing in this file.** Two advisors disagreeing is a stalemate you cannot resolve by re-reading them. One missing column in a spreadsheet is a defect you can fix in ten minutes, after which the two documents agree.

---

## 3. The original plan already failed its own test

**(F)** Before any Irish tax correction, `Income_Bridge` in the original workbook computes:

| | Base | Downside | Upside |
|---|---|---|---|
| Profit before tax needed | €194,443 | €226,850 | €181,480 |
| Company PBT in 2030 (from P&L) | €181,600 | −€66,064 | €455,843 |
| **Headroom / shortfall** | **−€12,843** | **−€292,914** | +€274,363 |

**(O)** The Base case misses the target in 2030 by its own arithmetic, and only clears €7,500/month in **2031** (€10,524/mo). The Downside case pays **no dividend in any year**. So the recommended venture reached the stated goal in exactly one year out of five, in one scenario out of three — at a 7% tax rate that does not apply to you.

Apply the Irish correction and PBT needed rises from €194,443 to **€378,309** at 70% ownership. The Base case peaks at €181,600. **It is not close: the plan needs roughly twice the company it models.** Addendum A says this; the original workbook's own shortfall cell already implied it.

---

## 4. Three things to check before you rely on any of it

### 4.1 The 60% grant assumption is a ceiling, not an offer
**(F, dossier)** *"Grants there can cover up to 60% of the investment for a small firm"* — from the EC regional aid map 2022–27: Stredné Slovensko 40% + 20pp small-enterprise bonus. The model then assumes **50%** grant share of a €600k capex, i.e. **€300,000**.

**(F, my research)** Under the national **regional investment aid** regime (Act 57/2018 / Reg. 195/2018), maximum intensity is **25%** for western districts and **35%** for all others — Rimavská Sobota being in the latter.

**(O) These are not contradictory — they are different instruments.** The 60% is a state-aid *ceiling* under the GBER regional aid map; the 25/35% are the maxima the national investment-aid scheme actually awards. Which applies depends entirely on which programme funds you. **Banking 50% of a €600k capex on the ceiling rather than on a specific programme's terms is the most consequential unverified assumption in the whole model.**

**Sensitivity:** if the grant lands at 35% instead of 50% → €210k not €300k → a **€90,000 hole** in a stack whose investor tranche is only €100k. That nearly doubles the equity you must raise and pushes dilution well past the modelled 30%.
**→ Action:** name the specific programme before using any intensity figure.

### 4.2 The pack price is load-bearing and unverified
**(R)** Addendum A's entire asset-light P&L rests on a €25–35 pack price that was never sourced. §06 of this package shows takt and volumes swing ~55% between €18 and €28. The "Cost the Pack" sprint exists to close this; nothing downstream is reliable until it does.

### 4.3 TED 456343-2026 is still unknown
**(F)** `Tender_Evidence` records the €711k re-run with deadline **21/07/2026** — two months ago. Whether it attracted a bid is not in any of the four documents and could not be checked from this environment (TED is 403 at the egress proxy). If it was awarded at that price, the "market cannot supply" thesis weakens materially.

---

## 5. What was rebuilt

`models/Addendum_A_Model_LIVE.xlsx` — the Addendum A workbook as a working model:
- A single **`Assumptions`** sheet holding every input as a named, editable cell: Irish marginal rate components, ownership %, payout ratio, Slovak CIT, pack price, revenue lines, margins, overheads, capex, grant probabilities, exit multiple, CGT bands.
- **`Income_Bridge_Revised`**, **`PL_AssetLight`**, **`Exit_Value`** and **`Funding_Portfolio`** recomputed by formula from those inputs.
- **`Sector_Scoring_v2`** — the dossier's scoring sheet with the **Reversibility** column added and weights as inputs, so §2 can be re-run with your own judgement rather than mine.
- Values reconciled against the hardcoded originals by `models/verify_live_model.py`, which re-implements the logic independently and asserts it against the source figures. **All checks pass**; the only divergence is the depreciation correction above, and it is flagged as intentional rather than silently absorbed.
- The funding sheet's `P(at least one)` uses a plain `PRODUCT` over a helper column rather than `PRODUCT(IF(...))` — the array form needs Ctrl+Shift+Enter in pre-dynamic-array Excel and returns a wrong number without it, silently.

Run the check yourself:
```bash
python3 models/build_live_model.py     # rebuild
python3 models/verify_live_model.py    # 13 assertions against the source
```

**(O) Change one cell — PRSI to 4.35%, ownership to 100%, the pack price to €22 — and every sheet responds.** That is what the newer analysis deserved and did not get.

---

## 6. What I'd attack next if I were you

1. **Fix the scoring sheet, not the argument.** Add the Reversibility column, put your own numbers in it, and let the two documents stop contradicting each other. Ten minutes.
2. **Name the grant programme before trusting any intensity.** 60% vs 35% is a €90k swing on the original plan and it is currently an assumption, not a fact.
3. **Open TED 456343-2026.** Still the cheapest decisive fact available.
4. **Treat the land as closed.** €2,107 total indicative value across seven parcels **(F)**, and the Martin parcels were offered €1,400 against ~€2,500 paid — selling now books a loss. Both documents agree it is admin, not strategy. Stop spending strategic attention on it beyond filing the tax returns and settling parcel 3797.
