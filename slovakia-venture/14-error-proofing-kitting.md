# 14 — Error-Proofing: stopping omissions and doublings

**The question:** how do you stop an operator forgetting an item or putting two in?

**Conclusion first (O): not with attention, training or a checkweigher.** A checkweigher — the control everyone reaches for — is **blind to 9 of 20 components** in a typical pack. The answer is a **physical kit nest** (prevents the error) plus **scan-to-close** (detects what the nest cannot), with weight as a third net and a destructive audit to prove the system works. Total cost at your volume: **€2–6k**, not €20k.

---

## 1. The four error modes

| # | Mode | Cause **(R)** | Customer consequence |
|---|---|---|---|
| **1** | **Omission** — item missing | Interruption mid-pack; batch-picking losing count | Short-delivery claim; failed audit |
| **2** | **Doubling** — two of one item | Batch-picking; re-starting an interrupted pack | Cost leak; crowds the pack; may break the seal |
| **3** | **Substitution** — wrong item | Similar packaging; adjacent bins | **Allergen risk.** The serious one |
| **4** | **Menu cross-contamination** — components of menu A in menu B | Changeover between 14 variants | Spec non-compliance; whole-lot rejection |

**(O) Mode 4 is the one specific to your product and the one most often under-controlled.** With 14 menu variants, changeover is the highest-risk moment of the day — not steady running.

---

## 2. Why a checkweigher is not the answer

Modelled in `automation/weight_detectability.py` — re-run it against your real BOM once `01` "Cost the Pack" produces it.

**Model:** a representative 1,091 g / 20-component pack, each component at ±3% fill tolerance (3σ), checkweigher repeatability ±0.5 g. Pack weight **1σ = 4.63 g**, so a practical reject window is **±13.9 g**.

| Verdict | Count | Components |
|---|---|---|
| **Detectable (≥6σ)** | **9 / 20** | Both retort meals (65σ), crispbread (27σ), pâté (16σ), biscuit (13σ), chocolate (11σ), drink powder (7.6σ), heater (7.6σ), cheese spread (6.5σ) |
| Marginal (3–6σ) | 2 / 20 | Jam (5.4σ), honey (4.3σ) |
| **Blind (<3σ)** | **9 / 20** | Sugar, wet wipe, purification tablets, matches, spoon, gum, coffee, tea, salt/pepper |

**(R) The nine weight-blind components are 36 g — 3.3% of pack mass.** A missing coffee sachet is **0.4σ**. Statistically invisible. So is a doubled one.

**Worse: errors cancel.** `+1 jam (25 g) / −1 honey (20 g)` nets **5 g = 1.1σ — invisible**. The pack is wrong in two ways and weighs almost exactly right.

> **(O) So weight is a genuinely good *second* net — it catches every error that matters by mass, cheaply and at 100% inspection. It is a bad *primary* control.** Buy it (`08` §1 item 2, ~€6k used) and keep it. Just do not believe it is sufficient.

---

## 3. The control hierarchy — strongest first

**(O) Each level is roughly an order of magnitude more reliable than the one below. Spend from the top.**

| Level | Control | Catches | Cost **(R)** |
|---|---|---|---|
| **1. Eliminate** | **Common-component architecture** — maximise items shared across all 14 menus so only the main meal and spread vary | Removes mode 4 almost entirely. Free, decided at design time | **€0** |
| **2. Prevent (physical)** | **Kit nest / cavity tray** — a thermoformed or foam insert with exactly one cavity per component | **Modes 1 and 2, for every component regardless of weight.** An empty cavity is visible; a doubled item will not fit | **€300–1,500** |
| **3. Prevent (flow)** | **One-piece flow.** Build one pack start-to-finish. Never batch-pick | Mode 2 at source — doubling is almost always a batch-picking artefact | **€0** |
| **4. Detect (identity)** | **Scan-to-close** — barcode every component; the label will not print until all N are scanned exactly once | **All four modes**, including substitution and same-weight errors | **€1,500–4,000** |
| **5. Detect (mass)** | **Checkweigher**, menu-specific target, 100% inspection | The 9–11 heavy components | €4,000–9,000 used |
| **6. Detect (foreign body)** | Metal detector | Not a kitting control — a contamination control | €6,000–12,000 used |
| **7. Verify** | **Destructive audit** — open and itemise sampled packs (§6) | Proves levels 1–6 are working | labour only |
| **8. Procedural** | Standard work, recipe card per menu, changeover checklist | Supports the above | €0 |
| **9. Training / attention** | — | **Weakest. Never the primary control** | — |

### The kit nest is the single highest-value item here
**(O) It is cheap, it needs no power, no software, no validation and no calibration — and it is the only control that works equally on a 300 g retort pouch and a 1 g salt sachet.** An operator cannot "forget" a cavity that is staring at them, and cannot double into a cavity that holds one. For a hand-built sample phase it is the *entire* detection system.

Practical form: a laser-cut foam or thermoformed ABS tray per menu, cavity-shaped to each component, with the menu code engraved. Change menu → change tray. **That also solves mode 4**: the wrong component physically does not fit the wrong cavity.

### Scan-to-close is the right second investment
You already own most of it: the label printer and scanner are in `13` §3 and `08` §1. The missing piece is the interlock logic — perhaps 200 lines against the traceability schema in `10` §4. **(O) The rule that matters: the system prints the pack label only when the scan set is exactly complete.** The label becomes the certificate, and an unlabelled pack cannot ship.

---

## 4. Computer vision — the honest answer

You asked specifically. **(O) It is the technically correct tool and the wrong purchase at your volume — but there is a cheap version of it you should absolutely buy.**

### As a detection control: no, not yet
| | |
|---|---|
| **What it would do** | Photograph the open nest before sealing; verify presence and identity of all components at once |
| **Industrial system cost (R)** | **€15,000–40,000+** — camera, lens, controlled lighting, controller, software licence, integration, validation |
| **DIY / edge-AI cost (R)** | €1,500–4,000 in hardware (fixed camera, light panel, mini-PC, trained model) |
| **Why not at 102 packs/day** | The nest (€300–1,500) prevents what vision would detect, and scan-to-close (€1,500–4,000) detects identity more reliably than a model you must train |
| **The hidden cost** | **Validation.** A defence or reserve buyer will not accept a homemade classifier as a primary control without documented false-negative rates on a held-out test set, lighting-stability evidence and a revalidation procedure on every menu change. That is months of work, not a weekend |
| **Where accuracy actually comes from** | **(R) Fixturing and lighting, not the model.** A nest tray plus consistent lighting does most of the work — at which point you own a nest and may not need the camera |

**(O) Revisit vision at Tier 3**, when volumes are 10× and a line stoppage costs real money. Then it earns its keep.

### As an evidence control: yes, buy this now
**(O) Decouple the two uses. You do not need the camera to *decide* — you need it to *prove*.**

A fixed camera photographing every open nest before sealing, with the image stored against the pack ID, costs **€200–600** and gives you:
- A complete photographic record of every pack you ever shipped
- An instant answer to "your pack was missing X" — you open the photo
- Audit evidence that is extremely persuasive during certification
- A labelled dataset accumulating from day one, so that **if** you later want real vision inspection, the training data already exists

> **(O) This is the best €400 in the whole error-proofing budget.** It is not detection; it is an unarguable record. Most disputes with institutional buyers are not about whether you can detect errors — they are about who is right after the fact.

---

## 5. Why doubling specifically happens, and the two rules that stop it

**(R) Doubling is almost never carelessness. It has two structural causes:**

1. **Batch-picking.** Operator grabs ten jam sachets and distributes them across ten packs. Any interruption and the count is lost — and the error lands in one pack as a double and another as an omission, which is exactly the **cancelling error that weight cannot see** (§2).
2. **Resuming an interrupted pack.** Operator stops mid-pack, returns, cannot recall which items are already in, and tops up.

**Two rules, both free:**
- **One-piece flow.** One pack completed before the next begins. No component touches more than one pack.
- **An interrupted pack is scrapped to rework, never resumed.** It goes to a marked red tray, is emptied and rebuilt. **(O) Make this explicit and blameless in the SOP** — if an operator fears being blamed for the interruption, they will guess instead, and guessing is what puts the error in the customer's hands.

---

## 6. Verification: the destructive audit

**(O) Every control above can fail silently. The audit is what tells you.**

| Parameter | Recommendation **(R)** |
|---|---|
| Method | Open the pack, itemise against the menu spec, record every discrepancy |
| Rate, first 3 months | **1 in 50**, and **the first and last pack of every menu changeover** |
| Rate, steady state | 1 in 200, changeover packs always |
| Record | Pack ID, operator, menu, time, discrepancy type (mode 1–4) |
| Escalation | **Any mode-3 (substitution) finding stops the line** until root cause is found — it is the allergen risk |
| Cost | Labour plus the scrapped pack |

**(O) Audit the changeover packs religiously.** With 14 menus, changeover is where mode 4 lives, and a changeover error contaminates a whole sub-lot rather than one pack.

**(R) On formal AQL sampling plans:** once a customer specifies an AQL, use the sampling plan their contract names (ISO 2859-1 or equivalent) rather than your own rate. **Verify the required AQL in the tender documents** — do not assume one.

---

## 7. What to measure

Carried from `06` §5, with the kitting-specific additions:

| KPI | Target **(R)** | Why |
|---|---|---|
| **First-pass yield** | ≥99.5% | The number a defence buyer asks for |
| **Pack completeness audit** | 100% correct | The only control that sees weight-blind errors |
| **Errors by mode (1–4)** | trend to zero | Tells you *which* control is failing, not just that one is |
| **Changeover error rate** | 0 | Isolates mode 4 |
| **Scan-to-close override count** | **0** | **(O) The most important number here.** If operators are overriding the interlock, you have no interlock |

> **(O) Watch the override count above all.** Every poka-yoke dies the same death: someone adds a bypass for a "special case", and within a month the bypass is the normal path. If overrides are non-zero, fix the reason — never the operator.

---

## 8. Recommended stack

| Phase | Controls | Cost **(R)** |
|---|---|---|
| **Phase 0 — samples (hand-built)** | Common-component design · **kit nest per menu** · one-piece flow · bench scale check · **evidence camera** · 100% audit (volumes are tiny) | **€500–2,100** |
| **Phase 1 — trial orders** | Add scan-to-close · audit 1-in-50 | +€1,500–4,000 |
| **Phase 3 — MVP-1 line** | Add checkweigher (100%) · metal detector · formal audit plan | +€10,000–21,000 |
| **Tier 3** | Revisit vision inspection | — |

**(O) Note what is absent from Phase 0: nothing electronic except a scale and a cheap camera.** The protection comes from a foam tray and a rule about not resuming interrupted packs. That is the honest answer to your question, and it is why this is solvable before you hire anyone.

---

## 9. Verification actions
1. **Build the real BOM** (`01`) and re-run `automation/weight_detectability.py`. Your blind list will differ from the model.
2. **Design the common-component architecture before quoting any menu** (`07` §1) — level 1 of the hierarchy is free only if you do it first.
3. **Get a quote for nest trays** — laser-cut foam and thermoformed ABS, 14 menu variants.
4. **Confirm the required AQL and audit regime** in the tender documents.
5. **Specify the scan-to-close interlock** against the traceability schema in `10` §4 before writing any code.
