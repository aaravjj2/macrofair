import { FlagshipPersistenceSnapshot, SecondaryFindingSnapshot } from "@/lib/types";

export const FLAGSHIP_SNAPSHOT_HEADLINE =
  "In the latest deterministic snapshot, CPI June 2026 contributes 69.82% of absolute dislocation mass and is 3.146x larger than #2.";

export const LONGITUDINAL_WINDOW_NAME = "flagship-persistence-window-v1";

export const FLAGSHIP_PERSISTENCE_SNAPSHOTS: FlagshipPersistenceSnapshot[] = [
  {
    snapshot_id: "2026-03-28-close",
    label: "2026-03-28 close",
    as_of: "2026-03-28T23:55:00Z",
    top_market_id: "poly-cpi-jun-2026-over-3",
    top_market_title: "US CPI YoY (Jun 2026) above 3.0%",
    top_share_of_total_gap: 0.559,
    top_to_second_ratio: 1.851,
    herfindahl_index: 0.4124,
  },
  {
    snapshot_id: "2026-03-29-close",
    label: "2026-03-29 close",
    as_of: "2026-03-29T23:55:00Z",
    top_market_id: "poly-cpi-jun-2026-over-3",
    top_market_title: "US CPI YoY (Jun 2026) above 3.0%",
    top_share_of_total_gap: 0.5957,
    top_to_second_ratio: 2.329,
    herfindahl_index: 0.4303,
  },
  {
    snapshot_id: "2026-03-30-close",
    label: "2026-03-30 close",
    as_of: "2026-03-30T23:55:00Z",
    top_market_id: "poly-cpi-jun-2026-over-3",
    top_market_title: "US CPI YoY (Jun 2026) above 3.0%",
    top_share_of_total_gap: 0.6418,
    top_to_second_ratio: 2.519,
    herfindahl_index: 0.4824,
  },
  {
    snapshot_id: "2026-03-31-close",
    label: "2026-03-31 close",
    as_of: "2026-03-31T23:55:00Z",
    top_market_id: "poly-cpi-jun-2026-over-3",
    top_market_title: "US CPI YoY (Jun 2026) above 3.0%",
    top_share_of_total_gap: 0.6982,
    top_to_second_ratio: 3.146,
    herfindahl_index: 0.5398,
  },
];

export const SECONDARY_FINDING_SNAPSHOTS: SecondaryFindingSnapshot[] = [
  {
    snapshot_id: "2026-03-28-close",
    label: "2026-03-28 close",
    as_of: "2026-03-28T23:55:00Z",
    polymarket_mean_gap: 0.0651,
    kalshi_mean_gap: -0.0146,
    asymmetry_gap: 0.0797,
  },
  {
    snapshot_id: "2026-03-29-close",
    label: "2026-03-29 close",
    as_of: "2026-03-29T23:55:00Z",
    polymarket_mean_gap: 0.0645,
    kalshi_mean_gap: -0.0151,
    asymmetry_gap: 0.0796,
  },
  {
    snapshot_id: "2026-03-30-close",
    label: "2026-03-30 close",
    as_of: "2026-03-30T23:55:00Z",
    polymarket_mean_gap: 0.0661,
    kalshi_mean_gap: -0.0106,
    asymmetry_gap: 0.0767,
  },
  {
    snapshot_id: "2026-03-31-close",
    label: "2026-03-31 close",
    as_of: "2026-03-31T23:55:00Z",
    polymarket_mean_gap: 0.063,
    kalshi_mean_gap: -0.0078,
    asymmetry_gap: 0.0708,
  },
];

export const SECONDARY_FINDING_ONE_SENTENCE =
  "Across the deterministic window, Polymarket contracts are consistently priced further above fair value than Kalshi contracts on average.";
