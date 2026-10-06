# 13 — MVP: Samples → Conversations → Contracts → Assembly

**Your sequence is correct and I am not going to improve it.** Samples before contracts, contracts before assembly. That is the discipline that keeps capex behind demand, and it is the same logic as Gate 1. This file makes it executable.

**Conclusion first (O): the MVP is not a machine. It is ~€5k of bench equipment plus a documentation pack.** The thing that gates your first contract is not throughput — it is **shelf-life evidence**, and §4 shows the asset-light model largely dissolves that problem, which is the single most useful finding in this file.

---

## 1. The sequence, with the interlocks

```
  PHASE 0  ──────────  PHASE 1  ──────────  PHASE 2  ──────────  PHASE 3
  SAMPLES              CONVERSATIONS        CONTRACTS            ASSEMBLY
  €3–8k                €0–2k                €0                   €95–120k
  4–8 weeks            2–6 months           1–6 months           post-Gate 1
     │                     │                    │                    │
  hand-built           sample sent,         framework or         MVP-1 line
  20–50 packs          tasted, specced      call-off won         ordered
     │                     │                    │                    │
     └─ needs: component ──┴─ needs: a story ───┴─ needs: capacity ──┘
        shelf-life docs       and a reference       you can prove

  GATE 0 (30/06/2027) sits between Phase 1 and 2: >=EUR50k invoiced + 1 state reference
  GATE 1 (31/12/2027) sits between Phase 2 and 3: >=2 co-packing agreements
                                                  + >=EUR300k demand
                                                  + grant decision in hand
```

**(O) The important property of this diagram: no phase funds the next one with your money.** Phase 0 is a month's salary. Phase 1 costs postage and travel. Phase 2 costs nothing but time. Only Phase 3 is capital, and by then a contract pays for it.

---

## 2. The daily quota — derived, not assumed

You asked for machinery to fulfil a daily quota. The quota is not a given; it falls out of which contract you win. From `06` §1, at an assumed **€28/pack (R, unverified)**:

| Scenario | Annual value | Packs/yr | **Packs/day** (250 d) | Takt (7.5 h shift) |
|---|---|---|---|---|
| Sample phase | — | 20–50 **total** | **~2** | irrelevant |
| DNS call-offs only | €150,000 | 5,360 | **21** | 21 min/pack |
| **Ration contract won** | €711,375 | 25,400 | **102** | **4.4 min/pack** |
| Both + municipal (2030) | €1,600,000 | 57,100 | 228 | 2.0 min/pack |

**Design the MVP line for ~102 packs/day.** That is the first real contract and the honest planning target.

**(R) What 102/day actually requires:** two operators in a U-cell at a conservative **1 pack/minute** produce 102 packs in **under two hours**. A single semi-automatic sealing station keeps up without effort.

> **(O) Read that twice before buying anything.** The binding daily quota is achievable in a fifth of one shift. Throughput is not your constraint and never becomes one until Tier 3. Every euro spent on speed is a euro not spent on the things that actually gate contracts: traceability, checkweighing, and shelf-life evidence.

---

## 3. MVP-0 — the sample kit (buy this now)

**Purpose:** build 20–50 compliant, documented, presentable packs by hand. No line, no premises beyond a clean compliant space.

| # | Item | Why | Cost **(R)** |
|---|---|---|---|
| 1 | Stainless bench + food-grade surfaces | Hygiene baseline | €300–700 |
| 2 | **Impulse / bar sealer** (bench, 400–600 mm) | Seals outer pouches and bags | €150–500 |
| 3 | **Bench vacuum sealer** (chamber, small) | Only if you seal anything yourself | €600–2,000 |
| 4 | **Calibrated bench scale** (0.1 g) + platform scale | Fill weights, declared net weight | €200–600 |
| 5 | **Label printer** (thermal transfer, roll) | FIC-compliant labels, lot codes, GS1 | €300–900 |
| 6 | **Date/lot coder** (hand-held or via label) | Lot + best-before on every pack | €100–400 |
| 7 | Hand-held barcode scanner | Lot capture into the traceability system | €80–200 |
| 8 | Heat gun / shrink equipment (optional) | Presentation | €80–250 |
| 9 | Hygiene kit: handwash, PPE, sanitiser, pest-proof bins | Mandatory for food handling | €200–500 |
| 10 | Sample shipping: insulated cartons, void fill, tamper seals | Samples must arrive intact and sealed | €150–400 |
| 11 | **Traceability system** (`automation/`, already built) | Lot genealogy from pack one | €0 |
| 12 | Metal detection | **Not at sample stage.** Declare the control as a Phase 3 measure | €0 |
| | **Total** | | **€2,160–6,450** |

**(O) Add ~€1–3k for HACCP documentation and RVPS registration** (`03` §3) and the sample phase is **under €8,000 all-in**. That is the entire cost of becoming a supplier who can be taken seriously.

**(O) What you can and cannot claim from a hand-built sample.** You can claim: composition, calorie value, net weights, labelling compliance, lot traceability, and that the pack physically works. You **cannot** claim your own shelf life — see §4. Do not write a shelf-life figure on a sample label that you cannot evidence; a defence or reserve buyer will ask for the data, and a number you cannot support is worse than no number.

---

## 4. The hidden critical path: shelf-life evidence

**(O) This is the item that sinks naive entrants, and nobody in your source documents flagged it.**

A ration or reserve buyer does not buy a recipe. They buy a **guaranteed remaining life**, often 24–36 months, written into the contract and audited.

**(F)** The evidence standard: accelerated shelf-life testing (ASLT) speeds up data collection, but **conditions must be tailored to the product and results should be confirmed with real-time studies** — real-time testing provides the most accurate representation and is often required to validate accelerated results. **(F)** The classic military-ration work tests storage at multiple temperatures over 24 months with sensory panels on a 9-point hedonic scale.

**The naive reading: you need two years of data before you can sell. That would kill the venture.**

### Why the asset-light model dissolves this

**(O) You are not the manufacturer, and that is the point.**

| Who owns the problem | What they must hold |
|---|---|
| **Your co-packers** | Validated shelf-life data for *their* components — they already have it, because they already sell those products with best-before dates |
| **You** | Component **certificates of analysis** and **shelf-life declarations**, plus evidence that *your assembly and outer packaging do not compromise* component life |

**(R) Consequences, and they are large:**
1. **The pack's shelf life is the shortest component's remaining life** at the moment of assembly. That is an arithmetic statement derived from supplier declarations, not a study you must run.
2. **Your own validation scope shrinks to the assembly step** — does the outer pack introduce moisture, light, odour transfer or physical damage? That is a small, cheap study, not a two-year programme.
3. **Component selection becomes the lever.** Choosing a crispbread at ≤10% moisture **(F)** with a 24-month declared life and a retort meal with 36 months gives you a 24-month pack without running a single long-term trial.
4. **It makes the RFQ question in `07` §3 the highest-value question you ask.** "What shelf life can you guarantee, under what storage conditions, and is it evidenced by real-time or accelerated data?" That one question determines what you can contractually promise.

> **(O) So the sequence is: collect supplier shelf-life evidence → derive the pack's achievable life → only then put a figure in front of a buyer.** Running your own 24-month study is a Tier 3 activity, for when you manufacture.

**Action:** add a **Shelf-Life Evidence File** to the documentation pack in §5 — one page per component, naming the supplier, the declared life, the storage conditions and whether the basis is real-time or accelerated.

---

## 5. The sample pack — what you actually send

**(O) The physical pack is the easy half. The documentation is what converts a sample into a conversation about a contract.**

### Send, in one carton
1. **1–2 complete 24-hour packs**, sealed, coded, labelled as you would supply them.
2. **One opened display set** — components laid out, so they do not have to destroy a sealed sample to see it.
3. **A one-page spec sheet**: menu, kcal/day, macronutrient split, net weights, pack dimensions, pallet configuration, declared shelf life **with its basis**, storage conditions.
4. **Compliance folder**: HACCP summary, RVPS registration number, component certificates of analysis, the **Shelf-Life Evidence File** (§4), allergen declaration, FIC-compliant label proof.
5. **Domestic-content statement**: which components are Slovak, by value. **(F, Addendum A)** Current ration supply is import-and-repack, so this is a real differentiator with political tailwind.
6. **A one-page covering letter.** Not marketing. What it is, what you can supply, in what volume, by when, and one question asking what would have to be true for them to trial it.

### Do not send
- Unsealed or hand-labelled packs. They read as amateur and they fail audit optics.
- A shelf-life claim without evidence (§4).
- A price, in the first contact, unless they asked. You do not yet know the specification; a wrong price anchors you badly.
- Anything implying you already hold a certification you do not (`03` §5 explains how to answer the certification screen honestly).

**(R) Budget: €150–400 per sample dispatch** including carriage. **Send 10–15.** Total under €5,000 including the build.

---

## 6. Market research: who the buyers actually are

**(O) Tiered by how reachable they are, not by how large.** Every row below is grounded in a published procurement notice or statute rather than inference, which is unusual for a market map and is the reason to trust the ordering.

### Tier A — reachable now, small, repeating
| Buyer | Evidence | Entry |
|---|---|---|
| **MO SR food & drink DNS** | **(F)** €13,166,370 system, permanently open; observed call-offs of **€4,680** and **€6,900** | Join the DNS (`04` §2.2) |
| **ÚV SR food DNS** | **(F)** €3,205,868 | Join |
| **Regional / VÚC food DNS** (e.g. Žilina €14.27m) | **(F)** | Join; check BB region |
| **Municipalities, schools, social care in RS district** | **(F)** EU 72-hour household guidance pushes civil-protection duties down to municipalities | Direct visit — start with Ožďany |

### Tier B — the prize, harder
| Buyer | Evidence | Note |
|---|---|---|
| **MO SR combat rations** | **(F)** €711,375 tendered 29/05/2026; **zero bids**; re-run 02/07/2026 | Spec may be unbuildable at the price — cost it before bidding (`01`) |
| **SŠHR** (state material reserves) | **(F)** ochraňovateľ mechanism pays contracted holders; **(F)** 30–60 day complete-ration doctrine | The Tier 2 annuity. Infožiadosť already drafted (`templates/`) |

### Tier C — export, once you have a reference
| Buyer | Evidence |
|---|---|
| **Polish police / military** | **(F)** full daily ration framework, TED 649047-2025 |
| **Romanian MoD** | **(F)** long-shelf-life foods, TED 652183-2025 |
| **North Macedonia MoD** | **(F)** one-day dry ration type A, TED 651196-2025 |
| **Norwegian municipalities** | **(F)** Narvik stand-by warehouse for freeze-dried food, TED 234765-2025 — the reserve-service model already procured |
| **Finnish municipalities** | **(F)** Rovaniemi dry goods & preserves framework, TED 385803-2025 |
| **Irish Defence Forces** | **(F)** contracts at SME scale: €139k canvas, €140k trailers, €290k spares |

### Tier D — institutional, slow
NSPA (needs NCAGE + Source File, `04` §3) · humanitarian and NGO buyers · EU-level stockpiling.

**(F) An honest caveat on the EU layer.** The EU Stockpiling Strategy (COM(2025) 528) creates an EU stockpiling network, a public–private Preparedness Task Force, and commits to identifying stock gaps and expanding EU-level stockpiles — but the Commission's framing covers critical raw materials, medical countermeasures and energy equipment, with food and water **"possibly"** in scope. **(O) So do not build a plan on EU-level food procurement. Build it on national and municipal buyers, who are already tendering today, and treat the EU layer as upside.**

**Sources:** [COM(2025) 528 — EU Stockpiling Strategy](https://civil-protection-humanitarian-aid.ec.europa.eu/document/download/c57d4067-1900-4616-9239-ca4598b55d69_en?filename=COM_2025_528_1_EN_ACT_combined.pdf) · [Commission — crisis readiness](https://commission.europa.eu/news-and-media/news/strengthening-crisis-readiness-and-health-security-2025-07-09_en) · [Council document ST-11407-2025](https://data.consilium.europa.eu/doc/document/ST-11407-2025-INIT/en/pdf)

---

## 7. Marketing strategy

**(O) You are not running a marketing campaign. You are running a qualification process.** These buyers do not respond to brand; they respond to compliance, references and availability. Spend accordingly: nearly nothing on visual identity, nearly everything on documentation and presence in the procurement systems.

### Positioning — one sentence
> **A Slovak assembler of complete, certified, shelf-stable ration and civil-preparedness packs, built from domestic components, with guaranteed availability.**

**(O) Every word in that sentence is doing work.** *Slovak* and *domestic components* answer the import-and-repack status quo. *Complete* answers the buyer who wants a pack, not a component. *Certified* answers the screen. *Guaranteed availability* is the Tier 2 annuity and the thing nobody else offers.

### On the "Europe is prepping" narrative — use it carefully
**(F) The demand signals are real and citable:** EU Preparedness Union Strategy (03/2025) with 72-hour household guidance; the first-ever EU Stockpiling Strategy (07/2025); Slovakia's SAFE allocation of €2.31bn; a Slovak MoD ration tender that grew 6.9× in a year and received zero bids.

**(O) But three rules on how you say it:**
1. **Lead with food security and civil preparedness, not war.** It is the same market, it is how the EU's own documents frame it, and it keeps grant assessors and municipal officials comfortable (`12` §4).
2. **Never sell urgency you cannot evidence.** These buyers read the same strategies you do and are unimpressed by alarm. Cite the notice numbers instead — a zero-bid tender is more persuasive than any adjective.
3. **Keep the site and the customer list discreet.** **(F, Addendum A)** There was a thwarted arson plot against a Slovak drone facility in 08/2026. Once you are defence-adjacent, operational discretion is a real control, not theatre.

### Channels, in order of return **(R)**
| Rank | Channel | Why |
|---|---|---|
| 1 | **Procurement systems** — MO SR DNS, ÚVO ZHS, eZakazky, JOSEPHINE, EVO, EKS | Where the money is actually spent. Free. `04` |
| 2 | **Direct sampling** to named buyers (§5, §6) | The only thing that converts a cold entity into a trial |
| 3 | **Municipal route** — ZMOS meetings, district office, civil-protection officers | Small repeating orders; buyers who rarely switch once they trust you |
| 4 | **The tender watcher** (`automation/ted_watcher.py`) | Being first to see a call is a marketing advantage |
| 5 | A credible one-page website + company email | Hygiene factor. Buyers check you exist. **(R) €0–500** |
| 6 | Defence/preparedness trade events | **(F)** Trade-fair vouchers exist; only once you have a reference |
| 7 | Paid advertising | **(O) Zero. Nobody buys state rations from an advert** |

### Outreach cadence
| Week | Action |
|---|---|
| 1 | Finalise spec sheet + compliance folder. Build 10 sample packs |
| 2 | Dispatch to 5 Tier A buyers. Log each in the tender/CRM register (`10` §4) |
| 3 | Follow up by phone — **not email**. Ask the one question: *what would have to be true for you to trial this?* |
| 4 | Dispatch to 5 Tier B/C buyers. Send the SŠHR concept note (`templates/koncepcia-rraas.md`) |
| 5–8 | Second follow-up. Convert any interest into a written trial scope |
| ongoing | Log every outcome, including every refusal and its reason (`10` §4) |

> **(O) Record the refusals.** After twenty entries the register tells you which buyers and which CPV codes are worth your time. That is the whole market-research programme, and it costs nothing but discipline.

---

## 8. From sample to contract

| Step | What it is | What it needs from you |
|---|---|---|
| 1 | Sample received, acknowledged | §5 pack |
| 2 | **Technical evaluation** — spec vs their requirement | Shelf-Life Evidence File (§4), allergen and nutrition data |
| 3 | **Trial order** — small, often unadvertised | Ability to supply 20–200 packs reliably. MVP-0 does this |
| 4 | **Qualification** — registration, references, financials | `04`: ÚVO ZHS, DNS entry, MO SR qualification system |
| 5 | **Call-off or framework award** | Priced bid with a real landed cost (`01`, "Cost the Pack") |
| 6 | **Supply** | Only here does MVP-1 (§9) get ordered |

**(O) Step 3 is the one people miss.** A trial order is usually small, sometimes informal, and almost never worth the money by itself. Take it anyway: it is the reference that unlocks Gate 0, and a state buyer who has bought from you once is a different prospect entirely.

---

## 9. MVP-1 — the first-contract line (do not buy yet)

Trigger: **Gate 1** (31/12/2027) — ≥2 co-packing agreements, ≥€300k contracted or high-probability demand, grant decision in hand.

Scope: the **minimum viable** configuration from `08` §1 — flow-wrapper, **checkweigher**, metal detector, coder, conveyors/benches, label printer, scales, one container, electrical, hygiene, traceability. **€95–120k (R)**.

**(O) At 102 packs/day the priority order inside that budget is not throughput. It is, in order: checkweigher (catches ~90% of kitting errors for ~€6k used), traceability, metal detection, then speed — which you will never need.** `08` §2 lists what not to buy and why.

---

## 10. Risks specific to this phase

| Risk | Likelihood **(R)** | Mitigation |
|---|---|---|
| **Shelf-life claim cannot be evidenced** | **High if ignored** | §4. Collect supplier declarations before quoting any figure |
| Samples sent, no reply | High | Phone follow-up in week 3. Email alone has very low return with institutional buyers |
| Co-packer won't supply small sample quantities | Medium | Buy retail for the first samples; declare the sourcing honestly. Switch to co-packer supply at trial stage |
| Buyer asks for certification you lack | Medium | `03` §5: HACCP + traceability + written commitment to certify within 6 months of award, priced into the bid |
| Price anchored too low in an early conversation | Medium | Do not quote before the pack BOM exists |
| Pack price assumption (€28) is wrong | **High — unverified** | `01` "Cost the Pack". Every quota figure in §2 moves with it |
| Drifting in sampling and never closing | Medium | Gate 0 at 30/06/2027 is the stop rule: ≥€50k invoiced + one state reference |

---

## 11. Verification actions
1. **Build the pack BOM** (`01`). Every number in §2 depends on it.
2. **Ask all three co-packers the shelf-life question** (§4, `07` §3) and collect written declarations. This is the critical path.
3. **Confirm the required shelf life** in the MO SR ration spec — 24, 36 or 60 months changes component selection entirely.
4. **Confirm RVPS treats a pre-packed kitting operation as registration, not approval** (`03` §6).
5. **Open TED 456343-2026** — still the cheapest decisive fact available, and it tells you whether Tier B is live.
