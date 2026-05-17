# Evaluation Protocol

This document defines the standardized methodology used to evaluate
alternative data sources as predictors of financial market behavior.
Every source documented in this lab is evaluated against this protocol.
The protocol is designed to evolve, but changes are versioned and noted.

**Version:** 0.2
**Last updated:** 2026-05-17

---

## 1. Mission

The goal of this lab is not to discover trading alpha. It is to build
a transparent, reproducible framework for assessing whether a given
alternative data source carries predictive information about financial
markets — and under what conditions. Each source receives a structured
verdict, regardless of outcome. Negative results are as valuable as
positive ones.

---

## 2. Target Variable

### 2.1 Primary Target: Realized Volatility of SPY

- **Asset:** SPDR S&P 500 ETF (ticker: SPY)
- **Data source:** Daily OHLCV from yfinance / Alpaca
- **Volatility metric:** Daily Garman-Klass volatility estimator
  - Chosen over close-to-close return standard deviation because it
    incorporates intraday range information and has lower variance.
- **Formula:**

  σ²_GK = 0.5 * (ln(High/Low))² − (2*ln(2)−1) * (ln(Close/Open))²

- **Units:** Reported in annualized percentage points (multiply daily
  variance by 252, take square root, multiply by 100).

### 2.2 Secondary Target (added later)

- **Direction of SPY daily return:** binary, sign(close[t+1] − close[t])
- Used for evaluating sources after the methodology has been validated
  on the volatility target.

---

## 3. Time Horizon

### 3.1 Primary Horizon

- **Forecast horizon:** Volatility on day t+1, predicted using
  source data available up to end of day t.
- All source data must be timestamped and lagged correctly to prevent
  look-ahead bias. If a source publishes at 4 PM ET, it cannot be used
  to predict the same day.

### 3.2 Secondary Horizon (added later)

- 5-day-ahead average volatility (smoother, less noise)
- Useful for sources with weekly or slower update cadence

---

## 4. Data Splitting Rules

To prevent overfitting and look-ahead bias, all evaluations use
chronological splitting:

- **Training period (in-sample):** earliest available data through 2022-12-31
- **Validation period:** 2023-01-01 through 2023-12-31
- **Test period (out-of-sample, held out):** 2024-01-01 through latest

The test period is **never used** for model selection or threshold
tuning. It is only touched once, when reporting final out-of-sample
results.

For walk-forward validation, the training window is rolled forward
in monthly steps starting from 2023-01-01.

---

## 5. The Four-Layer Evaluation Hierarchy

Every source is evaluated through up to four layers. A source must
pass each layer before advancing. Failure at any layer ends the
evaluation; the source receives a verdict at that level.

### Layer 1: Statistical Association

**Question:** Is there any measurable relationship between the source
signal and future volatility — both statistically detectable and
large enough to matter?

**Tests applied (gating):**
- Pearson correlation between source signal and t+1 volatility
- Spearman rank correlation (robust to non-linear monotonic relationships)

**Tests applied (supporting, non-gating):**
- Granger causality test at lags 1, 5, 10 days — reported for context
  and interpretation; see §5.1.1 for why these are not pass/fail.

**Pass thresholds:**
- Sample size ≥ 250 observations
- max(|r|, |ρ|) ≥ 0.10 (Cohen's small-effect convention)
- Corresponding p-value < 0.05 for whichever of r or ρ clears the
  effect-size threshold

Both r and ρ must be reported regardless of which clears the threshold.
A large gap between them (e.g. r = 0.04 but ρ = 0.18, or vice versa)
should be flagged and discussed in the verdict, as it indicates a
non-linear or outlier-driven relationship that will need careful
treatment at Layer 2.

**Failure verdict:** "No statistically detectable association of
meaningful magnitude."

#### 5.1.1 Why the Effect-Size Requirement and Granger Demotion

Protocol v0.1 specified only p-value thresholds for Layer 1. The
Source 02 evaluation (10Y-2Y Treasury spread, 2026-05-13) exposed
the gap: with n = 4,081, Pearson r = -0.04 produced p = 0.008, easily
crossing p < 0.05. Yet r² ≈ 0.0017 means the spread explained roughly
0.17% of the variance in next-day volatility — practically negligible.
The source then failed Layer 2 catastrophically (OOS R² of -0.42 vs.
naive baseline), confirming the in-sample "signal" was an artifact of
sample size rather than a real relationship.

v0.2 closes this gap in two coordinated ways. First, Pearson and
Spearman now require a minimum effect size of 0.10 in addition to
statistical significance. The 0.10 threshold matches Cohen's
small-effect convention and sits well outside the confidence interval
width at our typical sample sizes (CI half-width ≈ 0.031 at n = 4,000),
so a measured value of 0.10 is comfortably distinguishable from noise.
Second, Granger causality is demoted from a gating to a supporting
indicator: its F-statistics suffer from the same large-n significance
inflation, and they are additionally sensitive to lag choice and
stationarity assumptions that the protocol does not currently require
sources to validate. An incremental-R² threshold for Granger may be
revisited in a future protocol version once a concrete case motivates
specific design choices.

The general principle behind both changes: p-value alone is not a
sufficient gate. Layer 1 in v0.2 requires substantive evidence that
a relationship is both real and meaningful before a source advances
to out-of-sample testing.

### Layer 2: Out-of-Sample Predictive Value

**Question:** Does the relationship hold on data not used to discover it?

**Tests applied:**
- Walk-forward validation with monthly retraining
- Out-of-sample R² of a simple linear forecasting model using only
  the source signal as input
- Comparison vs. naive baseline (yesterday's volatility as forecast)
- Threshold: out-of-sample R² > naive baseline by ≥ 0.02 with
  statistically significant Diebold-Mariano test (p < 0.10)

**Failure verdict:** "Statistically associated in-sample but does not
generalize out-of-sample. Likely artifact of in-sample fitting."

### Layer 3: Economic Significance

**Question:** Could this signal generate exploitable returns after costs?

**Tests applied:**
- Construct a simple long/short volatility strategy based on the signal
  (e.g., long VXX when signal predicts high vol, short when low)
- Compute Sharpe ratio, max drawdown, hit rate
- Apply realistic transaction costs (5 bps per trade for liquid ETFs)
- Threshold: cost-adjusted Sharpe > 0.5 over the test period

**Failure verdict:** "Statistically predictive but not economically
exploitable. Useful as a feature within a larger model, not as a
standalone signal."

### Layer 4: Robustness

**Question:** Does the signal work in different market conditions?

**Tests applied:**
- Regime split: high-volatility regime (VIX > 20) vs. low-volatility regime (VIX ≤ 20)
- Temporal stability: signal strength in first third, middle third,
  last third of test period
- Outlier sensitivity: re-run analysis after removing top 5 most
  extreme volatility days
- Threshold: signal must remain statistically significant in at
  least 2 out of 3 regime/period splits

**Failure verdict:** "Predictive in some conditions but unstable.
Use with regime-conditioning."

**Pass verdict at Layer 4:** "Robust predictive signal."

---

## 6. Graduated Rigor Schedule

To allow for methodological learning, layers are introduced
incrementally across the first sources evaluated:

| Source # | Layers Applied |
|----------|----------------|
| 1-3      | Layers 1-2     |
| 4-5      | Layers 1-3     |
| 6+       | Layers 1-4     |

Earlier evaluations will be revisited and upgraded once Layer 4
methodology is mature.

---

## 7. The Verdict Template

Every source's `verdict.md` file must include the following sections:

1. **Source description** (1-2 paragraphs)
2. **Data acquisition method** and any preprocessing applied
3. **Sample period** and number of observations
4. **Layer-by-layer results** with key statistics
5. **Final verdict** — one of:
   - No statistically detectable association
   - In-sample only, no generalization
   - Predictive but not economically exploitable
   - Predictive in some regimes only
   - Robust predictive signal
6. **Limitations and caveats**
7. **Recommendation** — under what conditions, if any, this source
   would be worth integrating into a multi-factor model

---

## 8. Reproducibility Requirements

For every evaluation:

- All raw data fetching code committed to the repo
- All preprocessing code committed and deterministic (fixed random seeds)
- Notebooks must run end-to-end on a fresh machine after `uv sync`
- Data files themselves are not committed (gitignored), but fetching
  code must reproduce them from the source
- Results are reported in absolute terms with confidence intervals,
  not just point estimates

---

## 9. What This Protocol Does NOT Address

For honesty:

- This protocol does not constitute investment advice
- All evaluations are educational and reproducible research
- No live trading is performed against any signal here
- The methodology has known limitations (notably: inability to
  evaluate sources that affect markets through behavioral feedback
  loops, where measurement itself changes the system)
- Layer 1 is a linear and monotonic filter (Pearson and Spearman
  only). Sources hypothesized to be predictive through non-linear
  mechanisms — threshold effects, U-shapes, regime-conditional
  relationships — are not adequately evaluated by Layer 1 v0.2.
  Adding non-linear association tests (mutual information, distance
  correlation) is deferred until a concrete source motivates the
  specific design choices involved.

---

## 10. Versioning

This protocol is versioned. When changes are made, the version
number is incremented and a brief changelog entry is added below.

### Changelog

- **0.2 (2026-05-17):** Layer 1 amendment. Added effect-size
  threshold (max(|r|, |ρ|) ≥ 0.10) alongside the existing p-value
  requirement. Demoted Granger causality from gating to supporting
  indicator. Required dual reporting of Pearson and Spearman with
  discrepancy flagging. Added §5.1.1 documenting the rationale.
  Added explicit acknowledgement of linear/monotonic limitation in §9.
  Motivated by Source 02 (yield curve) evaluation.
- **0.1 (initial):** First version, defining baseline framework.