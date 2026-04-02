# 3-Minute Demo Script

## 0:00 - 0:20 Problem framing

MacroFair identifies macro prediction contracts where crowd odds diverge from a fundamentals-aware fair-value estimate. It is a calibration-first research product, not an execution bot.

Lead sentence:

"MacroFair finds where crowd odds and deterministic fair value disagree, then ranks and explains the most meaningful dislocations."

## 0:20 - 1:20 Screener walkthrough

Open the home page and highlight, in order:

1. Hero value proposition
2. Featured dislocation card
3. Flagship finding strip
4. Ranked screener table

Call out this computed headline:

- "Here is the top dislocation": CPI June 2026 contributes 69.82% of total absolute dislocation mass and is 3.146x larger than #2.

Then highlight the core table columns:

- contract
- platform
- market probability
- fair probability
- gap
- confidence

Use search and filters to narrow contracts, then sort by gap to surface largest dislocations.

## 1:20 - 2:20 Detail and explainability

Open a contract detail page. Show:

- title + platform/category context
- market vs fair-value headline cards
- gap + confidence
- market probability history chart
- linked macro series chart
- factor contribution panel and narrative summary

Click through to methodology from the detail page.

Explain that confidence accounts for liquidity, spread, and mapping stability.

## 2:20 - 2:50 Methodology and trust

Visit methodology page and summarize the deterministic pipeline:

1. read-only ingestion
2. canonical normalization
3. feature engineering
4. combined model + calibration
5. scoring + explanations

Then explicitly call out:

- what fair value means
- what confidence means
- deterministic demo mode behavior
- limitations
- how to interpret positive vs negative gap

Then show the findings evidence layer:

- "Here is why this is not just a one-time artifact": dominant top dislocation persists in 11/12 deterministic snapshots.
- "Here is a second complementary analytical result": platform gap asymmetry is positive in 12/12 snapshots (Polymarket mean gaps above Kalshi).
- "Here is a third complementary analytical result": inflation category share rises by 30.66 points from first to last snapshot.

## 2:50 - 3:00 Validation and close

Mention full quality gates and proof pack:

- `tsc`
- `vitest`
- `pytest`
- `playwright`

Optionally show integration readiness in findings view:

- Zerve integration is optional and disabled by default.
- Backend status confirms whether server-side configuration is present.
- Core demo behavior is unchanged without any key.

Close with three linked messages:

1. Current top dislocation.
2. Persistence across snapshots.
3. Complementary platform asymmetry evidence.
4. Category-share drift evidence.
