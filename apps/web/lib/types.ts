export type Platform = "Polymarket" | "Kalshi";
export type Category = "inflation" | "fed" | "unemployment" | "recession" | "gdp";

export interface MarketSummary {
  market_id: string;
  platform: Platform;
  title: string;
  category: Category;
  market_probability: number;
  fair_probability: number;
  gap: number;
  confidence: number;
  liquidity_score: number;
  resolution_time: string;
  updated_at: string;
  actionability_score: number;
  rank: number;
}

export interface HistoryPoint {
  timestamp: string;
  probability: number;
  volume: number;
  spread: number;
}

export interface MacroSeriesPoint {
  timestamp: string;
  value: number;
  vintage_date: string;
  source: string;
}

export interface ExplainPayload {
  top_factors: string[];
  factor_contributions: Record<string, number>;
  model_notes: string;
  confidence_notes: string;
  warning_flags: string[];
  narrative_summary: string;
}

export interface MarketDetail extends MarketSummary {
  description: string;
  sub_category: string;
  status: string;
  mapping_confidence: number;
  target_variable: string;
  macro_series_id: string;
  history: HistoryPoint[];
  linked_macro_series: MacroSeriesPoint[];
  explanation: ExplainPayload;
}

export interface FlagshipFinding {
  headlineFinding: string;
  question: string;
  method: string;
  result: string;
  topMarketId: string;
  topMarketTitle: string;
  topAbsoluteGap: number;
  topShareOfTotalGap: number;
  topToSecondRatio: number;
  herfindahlIndex: number;
}
