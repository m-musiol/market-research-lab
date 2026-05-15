# Glossary

Living glossary of terms encountered while building this lab.
Terms are added as they appear in evaluations, methodology notes,
and reading. Each entry: one sentence, plain language.

---

## Financial Concepts

**VIX** — The "fear gauge" of Wall Street, derived from S&P 500 option
prices, expressing the market's expected 30-day forward volatility.

**Realized volatility** — Volatility actually observed in past price
movements, as opposed to *implied* volatility forecast by options.

**Garman-Klass volatility** — A daily volatility estimator that uses a
day's open, high, low, and close prices, more efficient than simple
close-to-close volatility but blind to overnight gaps.

**Close-to-close volatility** — The standard textbook volatility metric,
computed as the standard deviation of daily log returns based only on
closing prices.

**Volatility persistence** — The empirical observation that turbulent
trading days tend to be followed by turbulent days; volatility clusters
in time.

**OHLCV** — Standard daily price record consisting of Open, High, Low,
Close, and Volume.

**Sharpe Ratio** — A measure of risk-adjusted return, computed as excess
return divided by return volatility.

---

## Statistical Concepts

**Pearson correlation** — Measures the strength of a *linear*
relationship between two numeric series, on a scale from -1 to +1.

**Spearman rank correlation** — Like Pearson, but compares the *ranks*
of values instead of the values themselves, making it robust to outliers.

**Granger causality** — Tests whether one series X contains information
about the *future* of another series Y, beyond what Y's own past
already explains.

**Lag** — The time offset used in a test (lag 1 = "1 day ago", lag 5 =
"5 days ago").

**p-value** — The probability that the observed result arose by pure
chance; smaller values indicate stronger evidence (typical threshold:
< 0.05).

**F-statistic** — A test statistic from regression analysis; in the
Granger test it measures how much adding X improves the forecast of Y.

**R²** — The fraction of *variance in the target* a model explains;
0 = nothing explained, 1 = perfect prediction.

**RMSE (Root Mean Squared Error)** — The typical magnitude of a model's
forecast errors, in the same units as the target variable.

**Linear regression** — A simple model of the form `y = a * x + b` that
finds the best straight-line relationship between an input and output.

**Diebold-Mariano test** — Tests whether the difference in forecast
accuracy between two models is *statistically significant* or just
random.

**Effect size** — A measure of the *magnitude* of an observed relationship,
independent of sample size; distinct from statistical significance, which
measures only whether the effect is distinguishable from zero.

**Significance vs. effect size** — A relationship can be statistically
significant (p < 0.05) but have a tiny effect size; with large samples,
even microscopic effects become "significant" while remaining practically
meaningless.

---

## Methodology Concepts

**Look-ahead bias** — The methodological error of accidentally using
information from the *future* in a forecast, leading to falsely
optimistic results.

**Out-of-sample test** — Training a model on older data and evaluating
it on *unseen newer data* to measure its true predictive power.

**In-sample vs. out-of-sample** — In-sample = data the model was
trained on; out-of-sample = data the model has not seen during training.

**Naive baseline** — A simple comparison forecast (e.g., "tomorrow will
be like today") that any more sophisticated model must beat.

**Walk-forward validation** — A method where the model is repeatedly
retrained on a *rolling time window* and tested on the period immediately
after.

**Calibration test** — A deliberate test against a *known answer* to
verify that a methodology works, before applying it to questions
where the answer is unknown.

**Forecast pair** — A data pair (predictor at day t, target at day t+1)
that forms the basic unit of any predictive analysis.

**Layer (in this protocol)** — One of the four hierarchical evaluation
stages (association → out-of-sample → economic → robustness) through
which each source is tested.

**Graduated rigor** — The strategy of starting with only basic layers
on early sources and adding more layers as the methodology matures.

**Verdict** — The structured final summary of a source evaluation,
formatted like a mini research memo, which is the actual research
output of each evaluation.

**Regime mismatch** — When the data distribution in the training period
differs structurally from the test period (e.g. training on a normal
yield curve, testing on an inverted one), causing models to extrapolate
into unfamiliar territory and often fail catastrophically.

**Honest negative** — A clean evaluation result showing that a candidate
source has no predictive value, which is as scientifically valuable as
a positive result and a sign of a well-functioning evaluation framework.

---

## Engineering / Database Concepts

**JOIN (SQL)** — A database operation that links rows from two tables
through a *shared column* (here: `date`).

**UPSERT** — A database operation that *inserts or updates* a record
depending on whether it already exists, preventing duplicates.

**Idempotent** — Property of a script meaning that running it multiple
times produces the *same end result* without causing harm.

**Composite primary key** — A primary key composed of *multiple columns
combined* (here: `ticker + date`) that enforces uniqueness at the
database level.

**Migration (database)** — A versioned SQL file that documents *schema
changes* and makes them reproducible (`001_create_schema.sql`, etc.).

**Migration pattern** — The convention of storing schema changes in
*numbered SQL files* (001_, 002_, …) so they apply in order.

**Repository (repo)** — A versioned project folder whose entire change
history is preserved in Git.

**Commit** — A single saved snapshot of the code with a description, like
a checkpoint in the version history.

---

## Career / Industry Concepts

**Hedge Fund (in the quant context)** — An investment fund that often
trades using data-driven strategies and non-traditional data sources;
a primary employer category for Alternative Data Analysts.

**Alternative Data Analyst** — A role focused on finding, validating,
and integrating non-traditional data sources (satellite, sentiment,
prediction markets, etc.) into financial forecasting workflows.

**Quant Researcher** — A role focused on developing quantitative trading
models, often requiring deep mathematical or statistical training.