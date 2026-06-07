# Source Selection Principles

Cross-source methodology notes about *choosing* which data source or
instrument to evaluate — distinct from the evaluation protocol, which
governs *how* a chosen source is tested.

These principles accumulate as evaluations expose them. Each entry
names the principle, the reasoning, and the source that surfaced it.

---

## 1. Directional vs. level-based markets for capturing uncertainty

**Principle.** A directional binary market (e.g. "any rate cut by
year-end") only captures the full uncertainty of a variable when the
real-world debate is confined to that one direction. When outcomes
span both directions (e.g. the Fed might hike *or* cut), a directional
market truncates the distribution and understates uncertainty. In
those cases a level-based market (e.g. "Fed funds rate above X% at
year-end") is the more complete instrument.

**Reasoning.** The predictor we care about is uncertainty about the
underlying variable. A binary "will it go up?" market collapses to
near-certainty whenever the market agrees on direction — even if there
is still genuine uncertainty about *magnitude*. Magnitude uncertainty
is invisible to a one-sided directional market but fully visible to a
level-based or multi-outcome market.

**Surfaced by.** Source 03 (Polymarket Fed-path, 2025). The chosen
"how many cuts in 2025" market is directional (cuts only). For 2025
this is immaterial because hike probability was negligible all year,
so the truncation loses no meaningful mass. But the same instrument
applied to a hiking-cycle year (e.g. 2022) or a mixed-expectation
year would systematically understate Fed-policy uncertainty. Choose
the instrument to match the year's policy regime.

**Practical rule.** Before selecting a directional market as an
uncertainty proxy, check whether the real-world outcome space for the
evaluation period is genuinely one-sided. If not, prefer a
level-based or multi-outcome market.