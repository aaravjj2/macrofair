# Submission Summary (300 words)

MacroFair is a calibration-first mispricing detector for macro prediction markets. It compares crowd-implied probabilities from Polymarket and Kalshi with a deterministic fair-value estimate informed by macro signals and market microstructure. The goal is not automated execution. The goal is transparent ranking and explainability for where crowd odds and fundamentals disagree most.

In V1, MacroFair focuses on inflation, Fed decisions, unemployment, recession, and GDP contracts. A read-only ingestion layer loads fixture-backed snapshots from both platforms and linked FRED series in deterministic demo mode. A normalization layer maps each contract into a canonical schema and taxonomy with explicit mapping confidence. The feature pipeline then computes market, macro, and event-timing features in a reproducible way.

The fair-value engine combines a baseline market-aware model with a fundamentals-only model, then applies a deterministic calibration layer to reduce edge overconfidence. MacroFair computes dislocation gap, confidence, and actionability score, then ranks live contracts. For every contract, it returns a structured explanation payload including top factors, factor contributions, confidence notes, and warning flags.

The product ships with a typed FastAPI backend and a Next.js frontend designed for quick judge comprehension. The home screener immediately shows contract, platform, market probability, fair probability, gap, and confidence. Detail pages provide history charts, macro context, and explanation panels. Methodology and limits are clearly documented.

Quality gates are strict: TypeScript checks, frontend unit tests, backend unit tests, and Playwright E2E all run with zero retries and single-worker deterministic settings. Each milestone is accompanied by proof artifacts under `artifacts/proof/<timestamp>-<milestone>/`, including manifest files, reports, screenshots, and demo video capture.

MacroFair demonstrates a production-structured, explainable macro calibration workflow packaged for hackathon judging and extensible beyond demo fixtures.
