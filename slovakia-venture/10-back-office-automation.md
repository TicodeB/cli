# 10 — Back-Office Automation

**Conclusion first (O): build exactly two things now, and nothing else.** A **tender watcher** and a **rotation/expiry engine**. Both are in `automation/`, both run on stdlib Python with no dependencies, and both have offline tests. Everything else — CRM, ERP, BI dashboards — is premature and would be automating a business that does not yet exist.

**(F, Addendum A Improvement 6)** The watcher is also a saleable product: *"Build it once for yourself; licence it to other small suppliers."* Modelled at €99–399/month × 40 customers = €48–190k/year at near-100% gross margin. **(O) I agree with the logic and would flag one thing: do not let the software become the business.** It is a hedge and a cash-flow bridge, not the thesis. Addendum A's own premortem — *"you never left Tier 0"* — applies doubly to a founder with software skills and a hard operational problem to solve.

---

## 1. Architecture

```
┌─ SENSE ─────────────────────────────────────────────────────────┐
│ TED API (EU-wide)  ·  ÚVO/EVO  ·  JOSEPHINE  ·  eZakazky (MO SR)│
│ EKS  ·  ERANET  ·  MIRRI/eGrant calls  ·  Program Slovensko      │
│                    ↓ poll daily, dedupe by notice id            │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─ FILTER & SCORE ────────────────────────────────────────────────┐
│ CPV allow-list · buyer allow-list · value band · deadline ≥ 7 d │
│ relevance score → HIGH / WATCH / IGNORE                          │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─ NOTIFY ────────────────────────────────────────────────────────┐
│ 06:30 daily digest: new HIGH · closing in 7 d · awards to rivals│
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─ RESPOND (human gate) ──────────────────────────────────────────┐
│ Draft the qualification pack from stored artefacts:             │
│   ÚVO ZHS extract · §32 evidence · HACCP cert · references      │
│   insurance · financials · signed declarations                  │
│ → YOU REVIEW → submit                                            │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─ DELIVER & PROVE ───────────────────────────────────────────────┐
│ Lot genealogy · pack BOM per lot · expiry register              │
│ ROTATION ENGINE → what ships next, what must move, what is at   │
│ risk of write-off                                                │
└──────────────────────────────────────────────────────────────────┘
```

**(O) The human gate is architectural, not decorative.** Never auto-submit a bid or auto-send a first contact. The cost of a wrong automated submission to a state buyer — an unintended binding offer — vastly exceeds the labour saved.

---

## 2. Build order

| # | Component | Effort **(R)** | When | Why this order |
|---|---|---|---|---|
| 1 | **TED watcher** | 1 weekend | **Now** | **(F, Addendum A)** *"You will be the best-informed supplier in the district within 30 days, for the cost of a weekend"* |
| 2 | **Rotation/expiry engine** | 2–3 days | Before first stock | Expiry is the eighth waste (§06). Retrofitting traceability is what makes certification expensive |
| 3 | ÚVO / JOSEPHINE / eZakazky scrapers | 1 week | Q1 2027 | Slovak sub-threshold contracts never reach TED. **This is where the small call-offs live** |
| 4 | Qualification-pack generator | 3 days | After first 3 bids | Automate only once you know what is actually asked for every time |
| 5 | Lot genealogy / traceability | 1 week | Before Tier 1 | Audit evidence, and the Tier 2 product |
| 6 | Cost/quote model per pack | 2 days | "Cost the Pack" sprint | Turns the BOM into bid prices at volume breaks |
| 7 | CRM / ERP / BI | — | **Not yet** | **(O) Premature. A spreadsheet is correct at this scale** |

**Total infrastructure cost (R): €5–15/month.** A small VPS, or a laptop with a scheduled task.

---

## 3. What is built here

### `automation/ted_watcher.py`
Polls the **TED API v3** search endpoint for the CPV allow-list, scores notices, and emits a digest.

- Configuration in `automation/config.json` — CPV codes, buyer countries, value band.
- Deduplicates against `automation/state/seen.json` so a notice is reported once.
- Scores each notice HIGH / WATCH / IGNORE.
- `--dry-run` runs against the bundled fixture with **no network**, so it is testable anywhere.

> **(R) Not verified against the live API.** `ted.europa.eu` and `api.ted.europa.eu` were both **403 at the network egress proxy** from the build environment, so the request/response shape could not be confirmed against production. The parsing layer is deliberately defensive — it tolerates missing fields and both `{"notices": [...]}` and bare-list responses. **First action on your machine: run it live and adjust `FIELD_MAP` if the field names differ.** Everything else will work unchanged.

### `automation/rotation_calendar.py`
The Tier 2 engine, and the reason `05` calls reserve-holding an annuity.

- Reads a stock ledger CSV (lot, product, qty, produced, expiry, location, customer).
- Computes remaining shelf-life **percentage**, not just days — because buyers reject short-dated stock on a percentage basis.
- Classifies: `OK` → `ROTATE_SOON` → `ROTATE_NOW` → `CRITICAL` → `EXPIRED`.
- Flags stock breaching a contractual minimum-remaining-life clause **before** it becomes a write-off.
- Emits a FEFO (first-expiry-first-out) pick list.

### `automation/test_automation.py`
Offline tests for both. No network, no dependencies. `python3 automation/test_automation.py`.

---

## 4. Data you must capture from day one

**(O) This is the part people skip and then pay for during their first audit.** Capture it even while you are a broker with no warehouse — it costs nothing now and is expensive to reconstruct.

| Entity | Fields | Why |
|---|---|---|
| **Lot** | lot id, product, co-packer, production date, expiry, qty, input lots | Traceability one-step-back **(EU 178/2002 Art. 18)** |
| **Pack build** | pack id, menu variant, component lot ids, build date, operator | Recall scope in minutes, not days |
| **Movement** | from, to, date, qty, reason, document ref | Stock accuracy + audit trail |
| **Customer commitment** | contract, min remaining life %, response time, held qty | Drives the rotation engine |
| **Tender** | notice id, buyer, CPV, deadline, decision, outcome, reason | Your win/loss learning loop |

**(O) The last row is the one everyone omits and it is the most valuable.** Recording *why* you did not bid, and why you lost, is the only way a small supplier gets systematically better at tendering. After 20 entries it will tell you exactly which buyers and CPV codes are worth your time.

---

## 5. Verification and control — the non-negotiables

Every automated system in this venture needs four things (your own automation-bias rule, applied to itself):

| Control | Implementation here |
|---|---|
| **Verification** | Offline tests in `test_automation.py`; run before every change |
| **Monitoring** | The watcher writes a heartbeat to `state/last_run.json`. **If no digest arrives by 08:00, assume it is broken.** Silence is the failure mode |
| **Fallback** | Manual weekly check of TED + ÚVO. **(O) Keep doing this for the first month even after automation works** — it is how you learn whether the filters are wrong |
| **Cost control** | Stdlib only, no paid APIs, no LLM calls in the loop. Fixed ~€5–15/month |

**(O) The specific failure mode to design against: a filter that is too narrow and silently returns nothing.** An empty digest looks identical to a quiet week. The digest therefore always reports **how many notices were fetched and how many were filtered out**, so zero results are visibly distinguishable from zero notices.

---

## 6. Verification actions
1. Run `ted_watcher.py` **live** from your own machine and correct `FIELD_MAP` against the real response.
2. Confirm the **CPV allow-list** against the actual ration tender notice — Addendum A's codes are a starting point, not a verified list.
3. Add the **Slovak platforms** (ÚVO, JOSEPHINE, eZakazky). **(O) These matter more than TED for your first year**, because sub-threshold Slovak call-offs — the €4,680 and €6,900 awards — never appear in TED.
4. Decide the **contractual minimum remaining shelf life %** with the first Tier 2 customer; it is the single most important parameter in the rotation engine.
5. Run both scripts on a schedule and confirm the heartbeat before relying on them.
