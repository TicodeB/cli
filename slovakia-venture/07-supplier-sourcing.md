# 07 — Supplier & Co-packer Sourcing

**Conclusion first (O):** your supply base is the business. At Tier 1 you own a kitting cell and a certificate; the **product** is made by other people's factories. That means co-packer selection is not procurement, it is **strategy** — and the biggest single risk in the model is that a co-packer decides to sell direct.

**(F, Addendum A adversarial section):** *"Kitting has no moat: the moment you prove the market, Bonavita or a Polish assembler with an existing IFS certificate takes it, because they already own the hardest input."* That critique is largely correct. §4 below is how you blunt it.

---

## 1. Component architecture

A 24-hour 3,600 kcal STANAG 2937 pack decomposes into six sourcing families **(R)** — confirm against the actual spec:

| Family | Typical contents | Shelf life needed | Source type |
|---|---|---|---|
| **A — Dry bakery** | Crispbread, rusks, biscuits, energy bars | 12–24 mo | SK/CZ co-packer |
| **B — Wet main meals** | Retort pouches or cans; meat at lunch **and** dinner per the 2026 spec **(F)** | 24–36 mo | SK canner / retort producer |
| **C — Spreads & accompaniments** | Pâté, jam, cheese spread, honey sachets | 18–24 mo | SK canner / sachet filler |
| **D — Beverages & drink powders** | Instant coffee/tea, isotonic powder, purification tablets | 24–36 mo | EU sachet filler |
| **E — Confectionery & energy** | Chocolate (heat-stable), glucose, chewing gum | 12–18 mo | EU |
| **F — Non-food accessories** | Spoon, wet wipe, matches, flameless heater, bag, menu card | n/a | EU / import |

**(O) Design instruction that will save you more than any negotiation:** maximise **common components across the 14 menus**. Only families B and C should vary by menu; A, D, E and F should be near-identical. §06 §4 shows combinatorial inventory is the #1 operational risk — this is where you eliminate it, at the design stage, for free.

---

## 2. Named starting points

**(F)** Established from Addendum A's competitor map and this session's search. **Nothing below is a confirmed co-packing relationship** — these are targets, not partners.

### Family A — dry bakery
| Company | Basis | Note |
|---|---|---|
| **Bonavita** | **(F)** Topoľčany plant + two CZ plants; the incumbent SK crispbread producer | **(O) First call and biggest risk simultaneously** — best capability, and the most likely to bypass you |
| **Pekáreň Takáč a syn s.r.o.** | **(F)** produces bread, sweet/salty pastries and **durable baked goods** (trvanlivé pečivo) | Smaller, likelier to accept private-label work |
| CZ/PL knäckebrot lines | **(F, Addendum A)** | Price benchmark + second source |
| Imports: Wasa, Racio, Dr. Schär | **(F)** present in SK retail | Benchmark only; branded, unlikely to co-pack |

**(F) Useful technical fact for the spec:** knäckebrot must contain **max 10% moisture**, which is what gives it very long storage life. That makes family A the easiest shelf-life family and a sensible first component to lock.

### Family B/C — wet meals, canned
| Company | Basis | Note |
|---|---|---|
| **Tauris** | **(F)** established supplier to state canteens | Meat processing scale |
| **Mecom** | **(F)** same | Meat processing scale |
| **Ryba Košice** | **(F)** same | Canned fish/pâté; **(R)** closest to retort capability |
| **(O) Gap to test** | **(F, Addendum A)** these players run "fresh/frozen logic, not 3–5 year shelf life" | **The critical unknown: can any SK producer hit 24–36 months?** If not, family B is imported and the domestic-content story weakens |

### Freeze-dried — a gap worth noting
**(F)** Polish **LYOFOOD**, Czech brands, and SK fruit-only players (**Brix**, **Nutiva**). **(F, Addendum A/R)** There is **no Slovak savoury freeze-dried meal capacity**. **(O)** Import initially; this is a Tier 3 manufacturing opportunity later, and a good story for a JTF "new and emerging sectors" application (`05` §2).

---

## 3. The RFQ pack

`templates/rfq-copacker.md` is ready to send. It asks the five things that actually decide viability, in order:

1. **MOQ** per SKU and per production run
2. **Lead time** from PO to goods-ready, and **slot availability** (can you book capacity?)
3. **Achievable shelf life** under stated storage conditions — *with evidence*
4. **Certification held** (HACCP / IFS / BRCGS / FSSC, with scope and expiry)
5. **Private-label willingness** and whether they will supply against a **frame agreement** rather than spot POs

**(O) Question 4 is the one that pays for the whole exercise.** If your co-packers hold IFS or BRCGS for the manufactured components, you may be able to hold **only HACCP** for the assembly step — see `03` §5. That is the single largest certification saving available to this business model and it is a direct consequence of going asset-light. Ask it explicitly and get the certificate scope in writing.

**(O) Question 5 reveals the strategic risk.** A co-packer who refuses private label is telling you they intend to own the customer. Note it and find a second source.

---

## 4. Blunting the "no moat" critique

The moat is not kitting. Four defences, in descending strength **(O)**:

1. **Tier 2 is the moat.** **(F, Addendum A):** *"a multi-year reserve-holding contract with rotation obligations is genuinely sticky, because switching it means moving physical national stock."* A co-packer can undercut you on a pack; they cannot casually take over custody of national reserves. **This is why `05` funds Tier 1 only as the path to Tier 2.**
2. **Two suppliers per component family, always.** **(F, Addendum A risk table):** *"Two suppliers per component; own the certification and the brand, never one input."* Single-sourcing family A to Bonavita hands them the business.
3. **Own the buyer relationship and the compliance burden.** Co-packers are manufacturers; they generally do not want tender paperwork, traceability packs, or 60-day state payment terms. That administrative load is unglamorous and it is genuinely your value-add.
4. **Own the specification.** If the pack is designed by you against the buyer's spec — including the common-component architecture in §1 — a competitor must re-engineer it, not just quote it.

**(O) The honest limit:** none of these is a strong moat at Tier 1 alone. This is why Gate 1 exists and why Tier 1 without a Tier 2 path should not be funded.

---

## 5. The agentic sourcing workflow

You asked for agentic supplier search. Here is the design; the implementation belongs with the automation in `10`.

```
┌─ SEED ────────────────────────────────────────────────────┐
│ CPV codes · SK NACE codes for food manufacturing          │
│ Component families A–F · geography ≤300 km of RS          │
└───────────────────────┬───────────────────────────────────┘
                        ▼
┌─ DISCOVER ────────────────────────────────────────────────┐
│ • ÚVO / TED award history: who already WINS food          │
│   contracts to SK state buyers? (proven compliance)       │
│ • FinStat / ORSR: NACE 10.xx in BB, KE, NR, TT regions    │
│ • Trade directories, Zoznam.sk, sector associations       │
│ • Retail private-label labels: "produced for" = a co-packer│
└───────────────────────┬───────────────────────────────────┘
                        ▼
┌─ ENRICH ──────────────────────────────────────────────────┐
│ FinStat: revenue, headcount, profit, filing discipline    │
│ Certification registers: IFS / BRCGS / FSSC directories   │
│ Capacity signals: recent capex news, job ads, plant size  │
└───────────────────────┬───────────────────────────────────┘
                        ▼
┌─ SCORE (weighted) ────────────────────────────────────────┐
│ shelf-life capability 25 · certification 20 · private-    │
│ label willingness 20 · MOQ fit 15 · distance 10 ·         │
│ financial stability 10                                    │
└───────────────────────┬───────────────────────────────────┘
                        ▼
┌─ ACT (human gate) ────────────────────────────────────────┐
│ Auto-draft RFQ per supplier → YOU REVIEW → send           │
│ Log responses to the supplier register; diary follow-ups  │
└───────────────────────────────────────────────────────────┘
```

**(O) Two design rules, both learned the hard way in automation projects:**
- **The human gate is mandatory before anything is sent.** A first-contact email to a potential strategic partner is not a job for an unattended agent. Auto-*draft*, never auto-*send*.
- **Supplier discovery via public award history is the highest-signal source and almost nobody uses it.** A company already winning food contracts to Slovak state buyers has proven it can handle the paperwork, the payment terms and the audit. That is worth more than a slick website.

**(O) The best sourcing input of all is free and non-digital:** ask the buyer. In the "Cost the Pack" sprint, ask MO SR procurement which Slovak producers have supplied components historically. They will often tell you.

---

## 6. Verification actions
1. **Family B is the make-or-break question:** can *any* Slovak producer deliver a retort meal at 24–36 months shelf life? Call Ryba Košice, Tauris and Mecom and ask directly. If the answer is no across the board, the domestic-content story needs rewriting before it goes into a grant application.
2. Confirm **Bonavita's** private-label position — and identify a second dry-bakery source before you rely on them.
3. Get the **certificate scope documents** (not just the logo) from every shortlisted co-packer.
4. Pull the **ÚVO/TED award history** for food CPV codes to SK state buyers over 3 years. That list *is* your qualified supplier long-list.
5. Confirm the **flameless heater** source (family F) — it is a specialist item, often dual-use regulated **(R)**, and it can quietly become a single point of failure in the BOM.
