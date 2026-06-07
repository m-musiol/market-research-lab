# Source 03 — Polymarket Fed-Path Market

**Status:** Reconnaissance phase
**Protocol version:** v0.2
**Layers planned:** 1, 2 (per graduated rigor schedule for Source #3)

## Hypothesis

Higher market uncertainty about Fed policy predicts higher SPY
realized volatility on day t+1.

The Fed-path market is plausibly linked to equity volatility through
monetary policy uncertainty: when the market is undecided about the
Fed's actions, the resulting macroeconomic uncertainty should
transmit to equity-market volatility.

The hypothesis as stated is symmetric — uncertainty about hikes
matters as much as uncertainty about cuts. For 2025 specifically, a
cuts-only market is empirically a sufficient instrument because the
market-implied probability of any hike was negligible throughout the
year, so the truncation to "cuts only" loses no meaningful
distributional mass. In a hiking-cycle year (e.g. 2022), or a
mixed-expectation year, a level-based rate market would be the
more complete instrument.

## Source

- **Platform:** Polymarket (prediction market)
- **Market:** "How many Fed rate cuts in 2025" — one specific
  binary sub-market, to be chosen during reconnaissance based on
  which sub-market kept p meaningfully bounded away from 0 and 1
  throughout the year.
- **Data API:** Polymarket CLOB API, `/prices-history` endpoint
  (public, no authentication)

## Predictor construction

- **Daily price:** last trade of UTC day
- **Primary predictor:** p_t * (1 - p_t) — Bernoulli variance,
  interpreted as market uncertainty
- **Secondary predictor (sensitivity analysis):** Δp_t = p_t - p_{t-1}
  — daily change in market price, testing whether *shocks* (not levels)
  drive volatility

### Rejected transformations

- **Raw p_t:** encodes a directional hypothesis (higher p → higher
  or lower vol) that lacks theoretical justification. The hypothesis
  here is uncertainty-driven, not direction-driven.
- **Binary entropy H(p_t):** empirically near-identical to p(1-p)
  (correlation > 0.99 for typical data); variance chosen as the more
  interpretable of the two.

## Approach

Univariate, single market (Approach C in candidate framing). Future
sources may revisit composite/aggregate signals across multiple
markets (Approach B) or stitched short-lived markets (Approach A).

## Sample period

- **Source data:** Calendar year 2025, from market listing through
  resolution
- **Target:** SPY Garman-Klass volatility, t+1
- **Joined sample size:** estimated ~250 observations (right at
  protocol v0.2 minimum). Sample-size tightness will be acknowledged
  in the verdict.

## Known limitations

- **Cuts-only truncation.** The chosen market prices only cuts, not
  the full universe of Fed actions (cuts, hold, hike). For 2025 this
  is empirically immaterial — hike probabilities were near zero
  throughout the year. Source-selection in other years should
  re-evaluate this choice.
- **Sample size at protocol floor.** With n ≈ 250, the standard error
  of r is approximately 1/√250 ≈ 0.063, so a measured r near the
  v0.2 threshold of 0.10 will have a 95% CI that includes zero.
  Layer 1 conclusions will be appropriately hedged.
- **Layer 2 will be underpowered.** Because this is a single
  calendar-year market (~250 total observations), the chronological
  test split for Layer 2 will contain well under 250 observations —
  likely under 100. Source 03 can therefore produce a clean Layer 1
  result but only a tentative Layer 2 result. The verdict will treat
  Layer 2 as indicative, not conclusive, and flag that a multi-year
  or stitched-market design (Approach A/B) would be needed for a
  properly powered out-of-sample test.

## Open questions

- Which specific sub-market to use (e.g. "Exactly 1 cut", "Exactly 2
  cuts", etc.) — pending reconnaissance.
- How Polymarket handles thin-trading days (no trades at all). May
  need forward-fill logic; will document choice in fetch.py.