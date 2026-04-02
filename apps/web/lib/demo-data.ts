import { MarketDetail, MarketSummary } from "@/lib/types";

const DETAILS: MarketDetail[] = [
  {
    market_id: "poly-cpi-jun-2026-over-3",
    platform: "Polymarket",
    title: "US CPI YoY (Jun 2026) above 3.0%",
    description: "Resolves yes if BLS CPI YoY for June 2026 prints above 3.0%.",
    category: "inflation",
    sub_category: "cpi",
    status: "open",
    market_probability: 0.64,
    fair_probability: 0.4959,
    gap: 0.1441,
    confidence: 0.8357,
    liquidity_score: 0.74,
    resolution_time: "2026-07-14T12:30:00Z",
    updated_at: "2026-03-31T23:55:00Z",
    actionability_score: 0.1224,
    rank: 1,
    mapping_confidence: 0.89,
    target_variable: "CPI_YOY",
    macro_series_id: "CPIAUCSL",
    history: [
      { timestamp: "2026-03-27T12:00:00Z", probability: 0.6, volume: 81300, spread: 0.035 },
      { timestamp: "2026-03-28T12:00:00Z", probability: 0.61, volume: 85400, spread: 0.034 },
      { timestamp: "2026-03-29T12:00:00Z", probability: 0.62, volume: 89100, spread: 0.033 },
      { timestamp: "2026-03-30T12:00:00Z", probability: 0.63, volume: 97800, spread: 0.032 },
      { timestamp: "2026-03-31T23:55:00Z", probability: 0.64, volume: 128500, spread: 0.03 }
    ],
    linked_macro_series: [
      { timestamp: "2025-12-01", value: 315.21, vintage_date: "2026-03-31", source: "FRED" },
      { timestamp: "2026-01-01", value: 316.12, vintage_date: "2026-03-31", source: "FRED" },
      { timestamp: "2026-02-01", value: 317.08, vintage_date: "2026-03-31", source: "FRED" }
    ],
    explanation: {
      top_factors: ["macro_signal_divergence", "horizon_pressure", "liquidity_adjustment"],
      factor_contributions: {
        macro_signal_divergence: -0.055,
        market_momentum: -0.005,
        liquidity_adjustment: 0.048,
        horizon_pressure: -0.022
      },
      model_notes: "Baseline blend of market microstructure and mapped macro signals.",
      confidence_notes: "Confidence 0.89 reflects deep liquidity and stable mapping.",
      warning_flags: [],
      narrative_summary: "Crowd odds remain above the baseline fair value after accounting for cooling inflation momentum."
    }
  },
  {
    market_id: "kalshi-fed-sep-2026-cut",
    platform: "Kalshi",
    title: "Fed cuts target rate by Sep 2026",
    description: "Resolves yes if Fed target range upper bound is lower than current by Sep 2026.",
    category: "fed",
    sub_category: "rates",
    status: "open",
    market_probability: 0.49,
    fair_probability: 0.4956,
    gap: -0.0056,
    confidence: 0.8828,
    liquidity_score: 0.69,
    resolution_time: "2026-09-17T18:00:00Z",
    updated_at: "2026-03-31T23:55:00Z",
    actionability_score: 0.0048,
    rank: 4,
    mapping_confidence: 0.91,
    target_variable: "FED_FUNDS_PATH",
    macro_series_id: "FEDFUNDS",
    history: [
      { timestamp: "2026-03-27T12:00:00Z", probability: 0.45, volume: 65500, spread: 0.023 },
      { timestamp: "2026-03-28T12:00:00Z", probability: 0.46, volume: 68200, spread: 0.023 },
      { timestamp: "2026-03-29T12:00:00Z", probability: 0.47, volume: 71500, spread: 0.022 },
      { timestamp: "2026-03-30T12:00:00Z", probability: 0.48, volume: 77800, spread: 0.022 },
      { timestamp: "2026-03-31T23:55:00Z", probability: 0.49, volume: 99500, spread: 0.02 }
    ],
    linked_macro_series: [
      { timestamp: "2025-12-01", value: 5.33, vintage_date: "2026-03-31", source: "FRED" },
      { timestamp: "2026-01-01", value: 5.33, vintage_date: "2026-03-31", source: "FRED" },
      { timestamp: "2026-02-01", value: 5.33, vintage_date: "2026-03-31", source: "FRED" }
    ],
    explanation: {
      top_factors: ["macro_signal_divergence", "market_momentum", "liquidity_adjustment"],
      factor_contributions: {
        macro_signal_divergence: 0.044,
        market_momentum: 0.007,
        liquidity_adjustment: 0.038,
        horizon_pressure: -0.019
      },
      model_notes: "Baseline blend of market microstructure and mapped macro signals.",
      confidence_notes: "Confidence 0.87 remains high due to stable spread and mapping.",
      warning_flags: [],
      narrative_summary: "Model fair value is above crowd odds as easing signals accumulate in rates and macro inputs."
    }
  },
  {
    market_id: "poly-unemp-dec-2026-over-4_5",
    platform: "Polymarket",
    title: "US unemployment above 4.5% by Dec 2026",
    description: "Resolves yes if BLS unemployment rises above 4.5% by Dec 2026.",
    category: "unemployment",
    sub_category: "labor",
    status: "open",
    market_probability: 0.42,
    fair_probability: 0.3742,
    gap: 0.0458,
    confidence: 0.8283,
    liquidity_score: 0.62,
    resolution_time: "2026-12-05T13:30:00Z",
    updated_at: "2026-03-31T23:55:00Z",
    actionability_score: 0.037,
    rank: 2,
    mapping_confidence: 0.87,
    target_variable: "UNRATE",
    macro_series_id: "UNRATE",
    history: [
      { timestamp: "2026-03-27T12:00:00Z", probability: 0.44, volume: 41100, spread: 0.022 },
      { timestamp: "2026-03-28T12:00:00Z", probability: 0.44, volume: 44200, spread: 0.022 },
      { timestamp: "2026-03-29T12:00:00Z", probability: 0.43, volume: 50100, spread: 0.021 },
      { timestamp: "2026-03-30T12:00:00Z", probability: 0.43, volume: 56100, spread: 0.021 },
      { timestamp: "2026-03-31T23:55:00Z", probability: 0.42, volume: 70800, spread: 0.02 }
    ],
    linked_macro_series: [
      { timestamp: "2025-12-01", value: 4.2, vintage_date: "2026-03-31", source: "FRED" },
      { timestamp: "2026-01-01", value: 4.3, vintage_date: "2026-03-31", source: "FRED" },
      { timestamp: "2026-02-01", value: 4.3, vintage_date: "2026-03-31", source: "FRED" }
    ],
    explanation: {
      top_factors: ["macro_signal_divergence", "horizon_pressure", "liquidity_adjustment"],
      factor_contributions: {
        macro_signal_divergence: -0.033,
        market_momentum: -0.003,
        liquidity_adjustment: 0.024,
        horizon_pressure: -0.011
      },
      model_notes: "Baseline blend of market microstructure and mapped macro signals.",
      confidence_notes: "Confidence 0.84 is moderate due to medium liquidity depth.",
      warning_flags: [],
      narrative_summary: "Crowd pricing is slightly above baseline fair value, with labor trend data still softening slowly."
    }
  },
  {
    market_id: "kalshi-recession-q4-2026",
    platform: "Kalshi",
    title: "US recession declared by Q4 2026",
    description: "Resolves yes if NBER dates recession start before end of Q4 2026.",
    category: "recession",
    sub_category: "business-cycle",
    status: "open",
    market_probability: 0.31,
    fair_probability: 0.32,
    gap: -0.01,
    confidence: 0.798,
    liquidity_score: 0.55,
    resolution_time: "2027-01-31T23:59:59Z",
    updated_at: "2026-03-31T23:55:00Z",
    actionability_score: 0.0077,
    rank: 3,
    mapping_confidence: 0.78,
    target_variable: "RECESSION_RISK",
    macro_series_id: "USREC",
    history: [
      { timestamp: "2026-03-27T12:00:00Z", probability: 0.28, volume: 35100, spread: 0.045 },
      { timestamp: "2026-03-28T12:00:00Z", probability: 0.29, volume: 36900, spread: 0.044 },
      { timestamp: "2026-03-29T12:00:00Z", probability: 0.29, volume: 40100, spread: 0.043 },
      { timestamp: "2026-03-30T12:00:00Z", probability: 0.3, volume: 44100, spread: 0.042 },
      { timestamp: "2026-03-31T23:55:00Z", probability: 0.31, volume: 55200, spread: 0.04 }
    ],
    linked_macro_series: [
      { timestamp: "2025-12-01", value: 0, vintage_date: "2026-03-31", source: "FRED" },
      { timestamp: "2026-01-01", value: 0, vintage_date: "2026-03-31", source: "FRED" },
      { timestamp: "2026-02-01", value: 0, vintage_date: "2026-03-31", source: "FRED" }
    ],
    explanation: {
      top_factors: ["macro_signal_divergence", "liquidity_adjustment", "horizon_pressure"],
      factor_contributions: {
        macro_signal_divergence: 0.05,
        market_momentum: 0.006,
        liquidity_adjustment: 0.01,
        horizon_pressure: -0.009
      },
      model_notes: "Baseline blend of market microstructure and mapped macro signals.",
      confidence_notes: "Confidence 0.78 is damped by wider spread and weaker mapping confidence.",
      warning_flags: ["WIDE_SPREAD"],
      narrative_summary: "Macro risk factors imply higher recession odds than crowd prices, but spread quality lowers trust."
    }
  },
  {
    market_id: "poly-gdp-q3-2026-below-1_5",
    platform: "Polymarket",
    title: "US real GDP growth (Q3 2026) below 1.5%",
    description: "Resolves yes if BEA advance Q3 2026 GDP SAAR is below 1.5%.",
    category: "gdp",
    sub_category: "growth",
    status: "open",
    market_probability: 0.46,
    fair_probability: 0.4609,
    gap: -0.0009,
    confidence: 0.8433,
    liquidity_score: 0.59,
    resolution_time: "2026-10-29T12:30:00Z",
    updated_at: "2026-03-31T23:55:00Z",
    actionability_score: 0.0007,
    rank: 5,
    mapping_confidence: 0.82,
    target_variable: "GDP_GROWTH",
    macro_series_id: "A191RL1Q225SBEA",
    history: [
      { timestamp: "2026-03-27T12:00:00Z", probability: 0.43, volume: 26500, spread: 0.024 },
      { timestamp: "2026-03-28T12:00:00Z", probability: 0.44, volume: 28400, spread: 0.024 },
      { timestamp: "2026-03-29T12:00:00Z", probability: 0.45, volume: 31600, spread: 0.023 },
      { timestamp: "2026-03-30T12:00:00Z", probability: 0.45, volume: 34900, spread: 0.023 },
      { timestamp: "2026-03-31T23:55:00Z", probability: 0.46, volume: 43700, spread: 0.02 }
    ],
    linked_macro_series: [
      { timestamp: "2025-10-01", value: 2.1, vintage_date: "2026-03-31", source: "FRED" },
      { timestamp: "2026-01-01", value: 1.8, vintage_date: "2026-03-31", source: "FRED" },
      { timestamp: "2026-04-01", value: 1.6, vintage_date: "2026-03-31", source: "FRED" }
    ],
    explanation: {
      top_factors: ["macro_signal_divergence", "market_momentum", "liquidity_adjustment"],
      factor_contributions: {
        macro_signal_divergence: 0.033,
        market_momentum: 0.004,
        liquidity_adjustment: 0.018,
        horizon_pressure: -0.013
      },
      model_notes: "Baseline blend of market microstructure and mapped macro signals.",
      confidence_notes: "Confidence 0.81 is moderate because depth is thinner than top contracts.",
      warning_flags: [],
      narrative_summary: "Fair value sits above market pricing as growth nowcasts trend lower than consensus."
    }
  }
];

export const DEMO_MARKETS: MarketSummary[] = DETAILS.map((market) => ({
  market_id: market.market_id,
  platform: market.platform,
  title: market.title,
  category: market.category,
  market_probability: market.market_probability,
  fair_probability: market.fair_probability,
  gap: market.gap,
  confidence: market.confidence,
  liquidity_score: market.liquidity_score,
  resolution_time: market.resolution_time,
  updated_at: market.updated_at,
  actionability_score: market.actionability_score,
  rank: market.rank
}));

export const DEMO_MARKETS_BY_ID: Record<string, MarketDetail> = DETAILS.reduce((acc, market) => {
  acc[market.market_id] = market;
  return acc;
}, {} as Record<string, MarketDetail>);

export const DEMO_METADATA = {
  mode: "demo",
  version: "0.1.0",
  last_refresh: "2026-03-31T23:55:00Z",
  model_version: "combined-v1",
  schema_version: "1.0.0"
};
