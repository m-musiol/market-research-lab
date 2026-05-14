# CLAUDE.md

Project instruction file. Auto-loaded by Claude Code; also serves as
onboarding context for any fresh AI session or human collaborator.

---

## Project

**Name:** market-research-lab

**Goal:** A transparent, reproducible framework for evaluating whether
alternative data sources carry predictive information about financial
markets. The lab is not trying to discover trading alpha — it is
building a comparative evaluation methodology and documenting a verdict
for each source tested.

**Owner:** Marc Musiol (Hamburg, Germany)

**Career context:** This project is a deliberate 12-18 month skill-
building investment toward a role as an Alternative Data Analyst in
quantitative finance. The repo doubles as a public portfolio. Code
quality, methodological rigor, and clear documentation matter as much
as results.

---

## Tech Stack

- **Language:** Python 3.12, managed with `uv`
- **Database:** PostgreSQL 18 (local), database name `quant_research`
- **Key libraries:** pandas, polars, duckdb, scipy, statsmodels,
  scikit-learn, matplotlib, psycopg2, yfinance
- **Notebooks:** Jupyter via VS Code
- **Secrets:** stored in `.env` (gitignored), never committed

---

## Repository Structure

market-research-lab/
├── CLAUDE.md                    <- this file
├── framework/
│   └── evaluation_protocol.md   <- the scientific standard, READ FIRST
├── sources/
│   └── NN_<name>/               <- one folder per evaluated source
│       ├── README.md            <- hypothesis + plan
│       ├── fetch.py             <- data acquisition
│       ├── analysis.ipynb       <- statistical tests + visualization
│       └── verdict.md           <- structured final verdict
├── shared/                      <- reusable code + SQL migrations
│   ├── sql/                     <- numbered schema migrations
│   ├── fetch_market_data.py
│   └── compute_volatility.py
├── notes/                       <- methodology notes + glossary
└── data/                        <- gitignored, never committed

---

## Core Conventions

1. **The evaluation protocol is authoritative.** Before any source
   evaluation, read `framework/evaluation_protocol.md`. Every
   methodological choice must conform to it (target variable, time
   horizon, data splits, four-layer hierarchy).

2. **Every source gets a verdict.** Negative results
   (no predictive value) are as valuable as positive ones and are
   documented with the same rigor.

3. **No look-ahead bias, ever.** Predictor data at day t may only be
   used to predict targets at day t+1 or later. Target shifting and
   train/test splits must be chronological.

4. **Reproducibility.** All data fetching code is committed. Data files
   are not. A fresh machine should reproduce results after `uv sync`
   plus running the fetch scripts.

5. **Idempotent data writes.** All database writes use UPSERT semantics
   so scripts can be safely re-run.

6. **Commit discipline.** Small, focused commits with clear messages.
   The commit history is part of the portfolio.

---

## Current Status

- **Infrastructure:** complete (tooling, DB schema, API access verified)
- **Target variable:** SPY Garman-Klass volatility, computed and stored
- **Sources evaluated:**
  - Source 01 — VIX: PASSES Layers 1-2 (calibration test successful)
- **Next:** Source 02 (candidate: Treasury yield curve, or Polymarket)

---

## Working Style Notes

- Proceed in small, verifiable steps; confirm each works before moving on.
- Prefer problem framing ("how should we handle X?") over imperatives.
- Keep explanations grounded; this project is also a learning vehicle.