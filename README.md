# market-research-lab

A public research lab building a transparent, reproducible framework for
evaluating whether alternative data sources carry predictive information
about financial markets.

The lab is not trying to discover trading alpha. It is building a
**comparative evaluation methodology** and documenting a structured
verdict for each source tested. Negative results are as valuable as
positive ones.

---

## Why this exists

Hedge funds and asset managers spend significant resources evaluating
non-traditional data sources (prediction markets, satellite imagery,
sentiment data, web traffic, etc.) before integrating any of them into
investment processes. The hard part is not finding sources — it's
distinguishing real signal from statistical artifact.

This repo applies a consistent four-layer evaluation protocol to a
growing set of alternative data candidates, documenting the methodology
openly and the findings honestly.

---

## What's in the repo
market-research-lab/
├── framework/
│   └── evaluation_protocol.md      Scientific standard — read first
├── sources/
│   ├── 01_vix/                     CBOE Volatility Index — calibration source
│   └── 02_yield_curve/             10Y-2Y Treasury spread — honest negative
├── shared/
│   ├── sql/                        Versioned database migrations
│   ├── fetch_market_data.py        OHLCV ingestion
│   └── compute_volatility.py       Garman-Klass volatility computation
├── notes/
│   ├── glossary.md                 Living glossary of project terms
│   └── 01_volatility_*.md          Methodology notes
└── CLAUDE.md                       Project briefing for AI/human collaborators

---

## Evaluation Protocol (v0.1)

Every source is evaluated against the same protocol:

| Layer | Question | Tests |
|-------|----------|-------|
| **1. Association** | Is there *any* measurable relationship? | Pearson, Spearman, Granger causality |
| **2. Predictive value** | Does it work on unseen data? | Walk-forward, OOS R², Diebold-Mariano |
| **3. Economic significance** | Could it generate exploitable returns after costs? | Sharpe, max drawdown, hit rate |
| **4. Robustness** | Does it hold across regimes? | Regime splits, temporal stability, outlier sensitivity |

Graduated rigor: layers 1-2 for the first 3 sources, layers 1-3 for
sources 4-5, all 4 layers from source 6 onward. Full details in
[`framework/evaluation_protocol.md`](framework/evaluation_protocol.md).

---

## Sources evaluated

| # | Source | Result | Verdict |
|---|--------|--------|---------|
| 01 | [VIX](sources/01_vix/) | Passes Layers 1-2 | Robust predictive signal (calibration test successful) |
| 02 | [Treasury yield curve (10Y-2Y)](sources/02_yield_curve/) | Fails Layer 2 | Statistically detectable but practically negligible; actively harmful OOS at daily horizon |

Each source folder contains its README (hypothesis), fetch code,
analysis notebook, and a structured verdict.

---

## Tech stack

- Python 3.12, managed with [uv](https://github.com/astral-sh/uv)
- PostgreSQL 18 for time-series storage
- Standard scientific stack: pandas, polars, scipy, statsmodels, scikit-learn
- Data sources: yfinance, Alpaca Markets, FRED, with more to follow

---

## Reproducibility

All data fetching code is committed; data files themselves are not.
A fresh checkout reproduces results via:

```bash
uv sync
psql -U postgres -d quant_research -f shared/sql/001_create_schema.sql
psql -U postgres -d quant_research -f shared/sql/002_create_source_signals.sql
uv run python shared/fetch_market_data.py SPY 2010-01-01
uv run python shared/compute_volatility.py SPY
uv run python sources/01_vix/fetch.py
uv run python sources/02_yield_curve/fetch.py
```

Then run the analysis notebooks in each source folder.

---

## Status

Active research project. Updated roughly weekly. Started May 2026.

---

## License

MIT — see [LICENSE](LICENSE)

## Disclaimer

This is educational and research-oriented work. Nothing in this repo
constitutes investment advice. No live trading is performed against any
signal documented here.