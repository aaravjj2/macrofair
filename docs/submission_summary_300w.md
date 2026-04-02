# Submission Summary (300 words)

MacroFair is a calibration-first mispricing detector for macro prediction markets. It compares crowd-implied probabilities from Polymarket and Kalshi with a deterministic fair-value estimate informed by macro signals and market microstructure. The goal is not automated execution; the goal is transparent ranking and explainability for where crowd odds and fundamentals disagree most.

In V1, MacroFair focuses on inflation, Fed decisions, unemployment, recession, and GDP contracts. A read-only ingestion layer loads fixture-backed snapshots from both platforms and linked FRED series in deterministic demo mode. A normalization layer maps each contract into a canonical schema and taxonomy with explicit mapping confidence. The feature pipeline then computes market, macro, and event-timing features in a reproducible way.

The fair-value engine combines a baseline market-aware model with a fundamentals-only model, then applies a deterministic calibration layer to reduce edge overconfidence. MacroFair computes dislocation gap, confidence, and actionability score, then ranks live contracts. For every contract, it returns a structured explanation payload including top factors, factor contributions, confidence notes, and warning flags.

The product ships with a typed FastAPI backend and a Next.js frontend designed for judge-speed comprehension. The homepage leads with a featured dislocation and flagship finding card before the ranked table. In the latest deterministic snapshot, the CPI June 2026 contract contributes 69.82% of total absolute dislocation mass and is 3.146x larger than the second-ranked gap. This gives a memorable headline and a concrete path into the detail view.

To make that claim durable, MacroFair adds a committed longitudinal snapshot window and recomputes concentration metrics across timestamps. The top dislocation persists as the same contract in 4/4 deterministic snapshots (100% persistence), with top-share ranging from 55.90% to 69.82%. This shows the flagship narrative is not a one-time artifact.

MacroFair also adds a second deterministic finding: platform gap asymmetry. Across the same snapshot window, Polymarket mean signed gaps are above Kalshi mean signed gaps in 4/4 snapshots, with average asymmetry of 7.67 points. This complements concentration with a cross-platform structural lens.

Detail pages provide market vs fair value, gap/confidence context, trend charts, macro context, and factor-level explanation. Methodology explicitly defines fair value, confidence, deterministic demo mode behavior, interpretation rules, and limitations.

Quality gates are strict: TypeScript checks, frontend unit tests, backend unit tests, and Playwright E2E all run with zero retries and single-worker deterministic settings. Each milestone is accompanied by proof artifacts under `artifacts/proof/<timestamp>-<milestone>/`, including manifest files, reports, screenshots, and demo video capture.

MacroFair demonstrates a production-structured, explainable macro calibration workflow with a clear analytical narrative: identify where the crowd and a deterministic fair value disagree, prioritize the biggest dislocations, and explain why.
