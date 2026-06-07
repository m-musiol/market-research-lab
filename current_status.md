# market-research-lab — Current Status

**Last updated:** 2026-06-07
**Owner:** Marc Musiol (Hamburg, Germany)

---

## Project Context

This is a **career-transition project** toward an Alternative Data Analyst
role in quantitative finance. Marc is currently a Data Scientist at pilot
Hamburg (4 days/week) and has a 12-18 month learning runway. The
GitHub repo `m-musiol/market-research-lab` doubles as a public portfolio.

**Public repo:** https://github.com/m-musiol/market-research-lab
**Private notes repo:** https://github.com/m-musiol/market-research-lab-notes

---

## What's Done

### Infrastructure
- Python 3.12 via uv, PostgreSQL 18 local, Jupyter via VS Code
- Repo structure: `framework/`, `sources/`, `shared/`, `notes/`, `data/`
- Database schema with three tables:
  - `market_data` — OHLCV for tradeable assets
  - `volatility_metrics` — derived volatility values
  - `source_signals` — long-format storage for non-OHLCV signals
- API access verified: Alpaca, FRED, PostgreSQL
- Migration pattern in place (`shared/sql/001_*`, `002_*`)

### Target Variable
- SPY Garman-Klass annualized volatility, computed and stored
- 4,112 trading days from 2010-01-04 to 2026-05-08
- Calibrated against close-to-close baseline (ratio 0.74, within
  theoretical 0.6-0.8 range)

### Protocol
- **Current version: v0.2.** Layer 1 now requires an effect-size
  threshold (max(|r|, |ρ|) ≥ 0.10, Cohen's small-effect convention)
  alongside p < 0.05. Granger causality demoted from gating to
  supporting indicator. Both Pearson and Spearman reported, with
  discrepancies flagged. Rationale documented in protocol §5.1.1.
- §4 clarifies that for parameter-free models the 2023 validation
  period is held out but left unused (excluded from both train and
  test). Both existing verdicts document this explicitly.

### Sources Evaluated

**Source 01 — VIX:** PASSES Layers 1-2
- Pearson r = 0.72, Spearman ρ = 0.68
- Granger causality at lags 1, 5, 10 all highly significant
- OOS R² = 0.46 vs naive baseline 0.31 (improvement +0.15)
- Diebold-Mariano p = 0.003
- Calibration test successful — pipeline correctly detects strong signal

**Source 02 — Treasury yield curve (10Y-2Y spread):** FAILS Layer 2
- Pearson r = -0.04 (significant by p-value, negligible by effect size)
- OOS R² = -0.10 vs naive baseline 0.32 (improvement -0.42, catastrophic)
- Diebold-Mariano p = 0.004 (spread model significantly *worse* than naive)
- Honest negative — pipeline correctly detects absence of signal
- Note: under v0.2's effect-size threshold, this source would now fail
  Layer 1 directly (|r| = 0.04 < 0.10), not only Layer 2

---

## Source 03 — In Progress (Reconnaissance Phase)

**Source:** Polymarket Fed-path market, evaluated under protocol v0.2.

**Decisions locked in:**
- **Approach:** univariate, single market (Approach C). Composite
  (Approach B) and stitched short-lived markets (Approach A) deferred
  to future sources.
- **Market:** "How many Fed rate cuts in 2025" — one specific binary
  sub-market, to be chosen during reconnaissance based on which kept
  p meaningfully bounded away from 0 and 1 through the year.
- **Daily price p_t:** last trade of UTC day.
- **Primary predictor:** p_t · (1 − p_t) — Bernoulli variance
  (market uncertainty).
- **Secondary predictor (sensitivity):** Δp_t = p_t − p_{t-1}.
- **Rejected:** raw p_t (wrong directional hypothesis), entropy H(p_t)
  (redundant with variance).

**Documented caveats (in `sources/03_polymarket_fed/README.md`):**
- Cuts-only truncation — immaterial for 2025 (hike probability ≈ 0
  all year), but matters for other years. See
  `notes/02_source_selection_principles.md`.
- Sample size at protocol floor (n ≈ 250).
- Layer 2 will be underpowered — single-year market means the OOS
  test split is well under 250 obs. Layer 2 result will be indicative,
  not conclusive.

**Data access:** Polymarket CLOB API `/prices-history` endpoint
(public, no auth). Workflow: Gamma API to find market + token IDs →
CLOB for daily price series → aggregate to daily UTC-close.

**Next steps:**
1. Reconnaissance script — list sub-markets of "How many Fed rate cuts
   in 2025", pull each daily price series, plot to pick the most
   informative sub-market.
2. Lock chosen sub-market's market/token IDs into the README.
3. Write `fetch.py` — idempotent, writes to `source_signals` with
   `source_name = 'polymarket_fed_2025'`.
4. Begin Layer 1 analysis (Pearson, Spearman, Granger as supporting).

---

## Open Items

- **None blocking.** The three methodology-review issues raised on
  2026-06-07 (protocol/verdict split inconsistency, verdict arithmetic
  gaps, Source 03 sample-size tension) are all resolved.

---

## Working Style

- **Step-by-step verification.** Small steps, confirm each works before
  moving on. No large code dumps. Marc applies edits manually in VS Code
  and pushes via PowerShell; provide full file content for replacements,
  then explicit open → edit → commit → push commands.
- **Inline English corrections.** Marc is improving his English by using
  it for technical work. Correct mistakes inline as short notes, not
  separate blocks.
- **German on demand.** For conceptual deep-dives Marc may request a
  German explanation. Switch language without resistance, mark the mode.
- **Honest about uncertainty.** When something is genuinely unknown,
  name it as such instead of giving a confident-sounding default.
- **Session-end ritual.** At the end of every working session, remind
  Marc to update two files:
  1. `notes/glossary.md` (English, public — for new project terms)
  2. `Formelsammlung_Finanzen_Statistik.md` in the private notes repo
     (German, personal — for new formulas and concepts with worked
     examples)

---

## Technical Skills Snapshot

**Strong:**
- Python (pandas, polars, numpy, scipy, sklearn, statsmodels)
- SQL (PostgreSQL, joins, schema design)
- Git workflow basics

**Building:**
- Quant methodology (Garman-Klass, Diebold-Mariano, walk-forward
  validation — newly learned through this project)
- Financial market microstructure (currently reading Harris
  "Trading and Exchanges")
- Time-series statistics (Granger causality, persistence, regime
  effects)

**Improving alongside:**
- Technical English (writing, conversation)

**Limited / not addressed yet:**
- Backtesting frameworks (vectorbt, zipline)
- GARCH and volatility-specific models
- Options pricing
- Prediction-market data handling (starting with Source 03)