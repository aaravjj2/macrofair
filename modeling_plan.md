# Modeling Plan

## Objective

Estimate a fair-value probability for each macro prediction market, then rank the size and quality of the divergence between market-implied probability and fair value.

## Modeling philosophy

Keep the first version simple, testable, and explainable.

Do not start with a heavy black-box model.

## Baselines

### Baseline 1: market-only baseline
Use only:
- current market probability
- time to resolution
- spread
- recent momentum
- platform

Purpose:
- quantify how much fundamentals add beyond the market itself

### Baseline 2: fundamentals-only baseline
Use:
- mapped macro features
- release timing
- regime variables

Purpose:
- quantify how much structure exists outside crowd price

### Baseline 3: combined fair-value model
Use:
- market microstructure features
- macro features
- event timing
- regime features
- platform features

## Candidate models

Start with:
- logistic regression
- gradient boosting classifier/regressor
- isotonic calibration on top
- optional monotonic constraints where sensible

## Feature families

### Market features
- current probability
- recent return / movement
- realized volatility
- spread
- depth proxy
- volume
- open interest
- platform

### Horizon features
- hours to resolution
- day of week
- release proximity
- whether settlement is within 24h / 72h / 7d

### Macro features
Depends on category:
- CPI trend
- unemployment trend
- fed funds / treasury curve
- labor surprise context
- inflation surprise context
- financial conditions proxies

### Regime features
- recent macro volatility
- platform liquidity regime
- pre/post major releases
- high uncertainty regime indicator

## Labels and training set

Use historically resolved markets wherever possible.

If a direct label is sparse:
- start with nearest settled analogs
- use category-specific resolved subsets
- document every mapping assumption

## Evaluation

Primary:
- Brier score
- log loss
- calibration error
- reliability plots

Secondary:
- ranking quality for large later-closing gaps
- subgroup performance by category, platform, and horizon

## Mispricing score

Core definition:
`gap = market_probability - fair_probability`

Adjusted score may include:
- confidence
- spread penalty
- low-liquidity penalty
- mapping confidence
- time-to-resolution scaling

## Explainability

Use:
- coefficient tables for linear models
- SHAP or feature contribution approximations for tree models
- plain-language narrative templates

## Research findings we want to test

- low-liquidity contracts are less calibrated
- pre-release windows create persistent overreaction or underreaction
- cross-platform disagreement is informative
- some market categories are systematically noisier than others

## Guardrails

- no claim of guaranteed profits
- no claim that model "beats the market" globally unless proven
- every result tied to a backtest artifact
