# 06 — Value Stream Map: ration-pack assembly

**Conclusion first (O): the constraint is not assembly speed.** At the volumes this market actually tenders, the line runs ~2 hours a day. The constraints are **component lead time, shelf-life/rotation, working capital and certification**. That finding should change how you spend capex: buy reliability and traceability, not throughput.

---

## 1. Demand sizing — establish takt before drawing anything

**(F, Addendum A / TED)** Known demand signals:
- Ration contract (re-run): **€711,375** — TED 456343-2026
- Prior year's equivalent award: **€102,636** — TED 110041-2025
- MO SR food DNS: stated value **€13,166,370**, issuing continuous small call-offs — individual awards observed at **€4,680** and **€6,900**

**(R) Unit economics assumption — flag this as unverified until the BOM is built:** a 24-hour, 3,600 kcal, 14-menu STANAG 2937 pack sells at **€25–35**. This is the load-bearing number in this document. It comes out of the "Cost the Pack" sprint (`01`), not from this file.

| Scenario | Annual value | Packs/yr @ €28 | Packs/day @ 250 d | Takt time (1 shift, 7.5 h) |
|---|---|---|---|---|
| DNS call-offs only | €150,000 | 5,360 | 21 | **21 min/pack** |
| Ration contract won | €711,375 | 25,400 | 102 | **4.4 min/pack** |
| Both + municipal (Addendum A 2030 base) | €1,600,000 | 57,100 | 228 | **1.97 min/pack** |

**(O) Read the takt column and then read it again.** Even at the 2030 base case, takt is ~2 minutes per pack. A single semi-automatic kitting station with two operators achieves 30–60 seconds per pack **(R)**. **You are 2–4× over-capacity on day one with the cheapest possible line.** Anyone selling you a high-speed automated line for this demand profile is selling you idle capacity.

---

## 2. Current state — how Slovakia buys rations today

**(F)** The 2025 contract was won by **EXIMA spol. s r.o.** — a Banská Bystrica foreign-trade company representing international manufacturers, 10–19 employees, €1.919m revenue, **€11,209 net profit** (0.6% net margin). It is a trading firm, not a producer.
**(R)** The value stream is therefore an **import-and-repack** stream:

```
CURRENT STATE — import & repack (R, inferred)

 MO SR ──tender──► TRADER ──PO──► FOREIGN MANUFACTURER(S)
                      │                     │
                      │              ┌──────▼───────┐
                      │              │   PRODUCE    │  LT 4–8 wk
                      │              │   (abroad)   │
                      │              └──────┬───────┘
                      │                     │  ▼▼▼ inventory in transit
                      │              ┌──────▼───────┐
                      │              │  FREIGHT/    │  LT 1–2 wk
                      │              │  CUSTOMS     │
                      │              └──────┬───────┘
                      │                     │  ▼▼▼ inventory at 3PL
                      │              ┌──────▼───────┐
                      │              │  RELABEL /   │  LT 1 wk
                      │              │  REPACK      │
                      │              └──────┬───────┘
                      │                     │
                      └────────────────► DELIVER ──► MO SR

 Total lead time (R):        6–11 weeks
 Value-adding time (R):      ~2–4 % of that
 Euro leakage:               ~100 % of component value leaves Slovakia (F, Addendum A §2.2)
 Observed failure mode (F):  0 bids at the raised 2026 spec — the stream could not respond
```

**(O) The diagnostic finding.** The current stream's dominant waste is not motion or defects — it is **waiting** and **transport**, plus the strategic waste of *unused domestic capability*. When the buyer raised the spec, the stream had no way to reconfigure, because nobody in it controls the recipe. That is why there were zero bids. **A stream whose only lever is a foreign purchase order cannot respond to a spec change.** That is your entry.

---

## 3. Future state — domestic assembly

```
FUTURE STATE — domestic assembly (target)

                         ┌──────────────────────────────────────┐
                         │  TENDER WATCHER (automated, §10)     │
                         │  TED · ÚVO · JOSEPHINE · eZakazky    │
                         └───────────────┬──────────────────────┘
                                         │ daily digest
 MO SR / MV SR / ────tender/call-off──► YOU  ◄──── rolling forecast ────┐
 SŠHR / municipality                     │                             │
                                         │ kanban pull per component   │
        ┌────────────────┬───────────────┼──────────────┬──────────────┘
        │                │               │              │
 ┌──────▼──────┐ ┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼────────┐
 │ DRY BAKERY  │ │ RETORT /     │ │ ACCESSORY   │ │ OUTER PACK / │
 │ crispbread  │ │ CANNED MEAL  │ │ sachets,    │ │ film, carton │
 │ SK co-packer│ │ SK co-packer │ │ utensils,   │ │              │
 │ LT 2–3 wk   │ │ LT 3–4 wk    │ │ heaters     │ │ LT 1–2 wk    │
 │ MOQ ██      │ │ MOQ ███      │ │ LT 2–4 wk   │ │              │
 └──────┬──────┘ └───────┬──────┘ └──────┬──────┘ └─────┬────────┘
        └────────────────┴───────┬───────┴──────────────┘
                                 │  ▼▼ component buffer (target 3–4 wk cover)
                    ┌────────────▼─────────────┐
                    │  GOODS-IN + QC + LOT REG │  C/T 15 min/pallet
                    └────────────┬─────────────┘
                    ┌────────────▼─────────────┐
                    │  KIT / ASSEMBLE          │  C/T 30–60 s/pack
                    │  14 menu variants        │  C/O 10–15 min (menu change)
                    └────────────┬─────────────┘
                    ┌────────────▼─────────────┐
                    │  SEAL · CODE · CHECKWEIGH│  C/T 5–10 s/pack
                    │  · METAL DETECT          │  FPY target ≥99.5 %
                    └────────────┬─────────────┘
                    ┌────────────▼─────────────┐
                    │  CASE PACK · PALLETISE   │  C/T 2 min/case
                    │  · LABEL (SSCC)          │
                    └────────────┬─────────────┘
                    ┌────────────▼─────────────┐
                    │  DISPATCH / HOLD & ROTATE│  Tier 2: rotation engine
                    └────────────┬─────────────┘
                                 ▼
                             CUSTOMER

 Target total lead time (R):      3–5 weeks (component-limited)
 Assembly throughput time (R):    <1 day for a 5,000-pack call-off
 Domestic content:                target ≥70 % of component value
```

### Lead-time ladder

| Stream | Current **(R)** | Future **(R)** | Mechanism |
|---|---|---|---|
| Order → delivery | 6–11 wk | **3–5 wk** | Domestic co-packers replace import + customs |
| Spec change → revised pack | months / impossible | **2–3 wk** | You control the recipe and the co-packer relationship |
| Reorder of a single component | 4–8 wk | **2–4 wk** | Kanban pull on named domestic suppliers |
| Emergency release (Tier 2) | n/a | **hours** | Stock already held and rotated |

**(O) The Tier 2 row is the whole strategic point.** Nobody else in this market can offer *hours*. That is not a lead-time improvement, it is a different product — and it is what a national reserve buyer is actually purchasing.

---

## 4. The seven wastes, applied honestly

| Waste | Where it will appear in *your* stream | Countermeasure |
|---|---|---|
| **Inventory** | Component buffers across 14 menu types × 12–18 SKUs = combinatorial stock. **This is your #1 risk** | Common-component design: maximise shared items across menus. Target ≤40 distinct SKUs for 14 menus **(R)** |
| **Waiting** | Co-packer MOQs and production slots | Frame agreements with scheduled slots, not spot POs |
| **Defects** | Wrong item in pack; missing item; wrong date code | Checkweigh **every** pack against a menu-specific target weight — catches ~90% of kitting errors for ~€6k **(R)** |
| **Over-processing** | Buying automation for 2-minute takt | See §1. Buy the cheapest reliable line |
| **Transport** | Multi-site co-packing means components converge from 3–5 locations | Consolidate inbound; prefer co-packers within ~200 km |
| **Motion** | Hand-kitting layout | U-shaped cell, components at waist height, one-piece flow per pack |
| **Over-production** | Building packs to stock against an unwon tender | **Build to order only** until Tier 2 gives you a paid reason to hold stock |

**(O) An eighth waste, specific to this product: expiry.** A ration pack is a depreciating asset with a hard cliff. Shelf life is inventory with a fuse. Every day of stock cover is a day of remaining life consumed. This is why the rotation engine in `10` is not a nice-to-have — it *is* the Tier 2 product.

---

## 5. KPIs — what to measure from pack one

Keep it to six. **(O)** Your instinct will be to build the full OEE stack; resist it until there is a line to measure.

| KPI | Definition | Target **(R)** | Why this one |
|---|---|---|---|
| **First-pass yield** | Packs passing checkweigh + detection first time / total | ≥99.5% | The only quality number a defence buyer asks about |
| **Pack completeness audit** | Random packs fully opened & itemised, per 500 | 100% correct | Checkweigh misses same-weight substitutions |
| **On-time-in-full (OTIF)** | Call-offs delivered complete by due date | ≥98% | This is what wins the *next* call-off |
| **Component cover** | Days of stock by component | 21–28 days | Below → stockout; above → expiry + capital |
| **Remaining shelf life at dispatch** | % of total life left when it ships | ≥85% | Buyers reject short-dated stock. Protects Tier 2 |
| **Landed cost per pack** | Fully absorbed cost incl. labour & overhead | Track vs. bid price | The number the whole business turns on |

**(O) Deliberately excluded: OEE.** With a 2-minute takt and a 2-hour day, availability and performance are meaningless — you would be measuring a machine that is idle by design. Measure OEE from Tier 3, when a line is the constraint. Measuring it now would produce an impressive dashboard describing nothing.

---

## 6. Verification actions
1. **Build the pack BOM** (`01`, "Cost the Pack"). Every number in this file is downstream of it.
2. Get **real MOQs and lead times** from the three co-packers — replace the **(R)** estimates in §3.
3. Obtain the **menu specification** from the tender documents: how many distinct SKUs do 14 menus actually require? This sets the inventory risk in §4.
4. Confirm **required shelf life** in the spec (24 / 36 / 60 months?). It drives component choice, co-packer choice and the entire Tier 2 economics.
5. Re-derive takt once the real price per pack is known. If the pack sells at €18 rather than €28, every volume in §1 rises by 55%.
