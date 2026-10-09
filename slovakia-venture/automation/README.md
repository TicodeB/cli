# automation/

Stdlib Python 3.10+. No dependencies, no paid APIs, no LLM calls in the loop.

```bash
python3 test_automation.py                       # 25 offline tests
python3 ted_watcher.py --dry-run --no-state      # offline demo
python3 ted_watcher.py                           # live TED query
python3 rotation_calendar.py --ledger fixtures/stock_sample.csv --min-life-pct 75
```

| File | Purpose |
|---|---|
| `ted_watcher.py` | Polls TED for CPV matches, scores HIGH/WATCH/IGNORE, dedupes, emits a digest |
| `rotation_calendar.py` | Shelf-life status by remaining-life %, contract-clause breach flag, FEFO pick list |
| `config.json` | CPV allow-list, buyer countries, value band, scoring thresholds |
| `fixtures/` | Sample data for offline tests |
| `state/` | `seen.json` (dedupe) and `last_run.json` (heartbeat) — gitignored |

**Scoring is gated, not purely additive.** A notice with no CPV and no keyword match is
IGNORE regardless of country, value or deadline. Without that gate, generic attributes
alone scored 35/100 and irrelevant notices reached the digest — caught by
`test_ted_scoring`.

**Monitoring:** `state/last_run.json` is the heartbeat. No digest by 08:00 means the
watcher is broken — silence is the failure mode, so the digest always prints how many
notices were fetched versus filtered.

**Not verified against the live TED API.** `api.ted.europa.eu` was 403 at the network
egress proxy when this was written. Parsing is defensive and tolerates missing fields
and both response shapes. Run live once and adjust `FIELD_MAP` if field names differ.

Cron:
```
30 6 * * 1-5 cd /path/to/automation && /usr/bin/python3 ted_watcher.py >> digest.log 2>&1
```
