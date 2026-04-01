# 3-Minute Demo Script

## 0:00 - 0:20 Problem framing

MacroFair identifies macro prediction contracts where crowd odds diverge from a fundamentals-aware fair-value estimate. It is a calibration-first research product, not an execution bot.

## 0:20 - 1:20 Screener walkthrough

Open the home page and highlight the core columns:

- contract
- platform
- market probability
- fair probability
- gap
- confidence

Use search and filters to narrow contracts, then sort by gap to surface largest dislocations.

## 1:20 - 2:20 Detail and explainability

Open a contract detail page. Show:

- market vs fair-value headline cards
- market probability history chart
- linked macro series chart
- factor contribution panel and narrative summary

Explain that confidence accounts for liquidity, spread, and mapping stability.

## 2:20 - 2:50 Methodology and trust

Visit methodology page and summarize the deterministic pipeline:

1. read-only ingestion
2. canonical normalization
3. feature engineering
4. combined model + calibration
5. scoring + explanations

## 2:50 - 3:00 Validation and close

Mention full quality gates and proof pack:

- `tsc`
- `vitest`
- `pytest`
- `playwright`

Close with one insight example from the top-ranked dislocation.
