import {
  FlagshipPersistenceSnapshot,
  SecondaryFindingSnapshot,
  ThirdFindingCategoryDrift,
} from "@/lib/types";

export interface FlagshipPersistenceSummary {
  dominantTopMarketId: string;
  dominantTopMarketTitle: string;
  persistenceRate: number;
  averageTopShare: number;
  minTopShare: number;
  maxTopShare: number;
}

export interface SecondaryFindingSummary {
  averageAsymmetryGap: number;
  positiveWindowShare: number;
  positiveWindowCount: number;
}

export interface ThirdFindingSummary {
  dominantCategory: string;
  dominantDrift: number;
  increasingCategories: number;
  decreasingCategories: number;
}

function round(value: number): number {
  return Math.round(value * 10000) / 10000;
}

export function summarizeFlagshipPersistence(
  snapshots: FlagshipPersistenceSnapshot[]
): FlagshipPersistenceSummary {
  const counts = new Map<string, { title: string; count: number }>();
  for (const row of snapshots) {
    const existing = counts.get(row.top_market_id);
    if (existing) {
      existing.count += 1;
    } else {
      counts.set(row.top_market_id, { title: row.top_market_title, count: 1 });
    }
  }

  let dominantTopMarketId = "";
  let dominantTopMarketTitle = "";
  let dominantCount = 0;
  for (const [marketId, entry] of counts.entries()) {
    if (entry.count > dominantCount) {
      dominantTopMarketId = marketId;
      dominantTopMarketTitle = entry.title;
      dominantCount = entry.count;
    }
  }

  const topShares = snapshots.map((row) => row.top_share_of_total_gap);
  const averageTopShare = topShares.reduce((sum, value) => sum + value, 0) / Math.max(topShares.length, 1);

  return {
    dominantTopMarketId,
    dominantTopMarketTitle,
    persistenceRate: round(dominantCount / Math.max(snapshots.length, 1)),
    averageTopShare: round(averageTopShare),
    minTopShare: round(Math.min(...topShares)),
    maxTopShare: round(Math.max(...topShares)),
  };
}

export function summarizeSecondaryFinding(
  snapshots: SecondaryFindingSnapshot[]
): SecondaryFindingSummary {
  const asymmetryValues = snapshots.map((row) => row.asymmetry_gap);
  const positiveWindowCount = asymmetryValues.filter((value) => value > 0).length;
  const averageAsymmetryGap =
    asymmetryValues.reduce((sum, value) => sum + value, 0) / Math.max(asymmetryValues.length, 1);

  return {
    averageAsymmetryGap: round(averageAsymmetryGap),
    positiveWindowShare: round(positiveWindowCount / Math.max(snapshots.length, 1)),
    positiveWindowCount,
  };
}

export function summarizeThirdFinding(driftRows: ThirdFindingCategoryDrift[]): ThirdFindingSummary {
  const sorted = [...driftRows].sort((a, b) => Math.abs(b.drift) - Math.abs(a.drift));
  const dominant = sorted[0];
  const increasingCategories = driftRows.filter((row) => row.drift > 0).length;
  const decreasingCategories = driftRows.filter((row) => row.drift < 0).length;

  return {
    dominantCategory: dominant?.category ?? "",
    dominantDrift: round(Math.abs(dominant?.drift ?? 0)),
    increasingCategories,
    decreasingCategories,
  };
}
