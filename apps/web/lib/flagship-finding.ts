import { FlagshipFinding, MarketSummary } from "@/lib/types";

export function computeFlagshipFinding(markets: MarketSummary[]): FlagshipFinding {
  const ranked = [...markets].sort((left, right) => Math.abs(right.gap) - Math.abs(left.gap));
  const totalAbsoluteGap = ranked.reduce((sum, market) => sum + Math.abs(market.gap), 0);

  const top = ranked[0];
  const second = ranked[1];
  const topAbsoluteGap = Math.abs(top?.gap ?? 0);
  const topShare = totalAbsoluteGap === 0 ? 0 : topAbsoluteGap / totalAbsoluteGap;
  const secondAbsoluteGap = Math.abs(second?.gap ?? 0);
  const topToSecondRatio = secondAbsoluteGap === 0 ? 0 : topAbsoluteGap / secondAbsoluteGap;

  const herfindahlIndex = ranked.reduce((sum, market) => {
    const share = totalAbsoluteGap === 0 ? 0 : Math.abs(market.gap) / totalAbsoluteGap;
    return sum + (share * share);
  }, 0);

  return {
    headlineFinding: `${top.title} contributes ${(topShare * 100).toFixed(1)}% of demo dislocation mass, ${topToSecondRatio.toFixed(1)}x larger than #2.`,
    question: "How concentrated are dislocations in the deterministic demo snapshot?",
    method: "Rank by absolute gap and compute each market's share of total absolute gap.",
    result: `Top absolute gap ${(topAbsoluteGap * 100).toFixed(1)} pts with HHI ${herfindahlIndex.toFixed(3)}.`,
    topMarketId: top.market_id,
    topMarketTitle: top.title,
    topAbsoluteGap,
    topShareOfTotalGap: topShare,
    topToSecondRatio,
    herfindahlIndex
  };
}