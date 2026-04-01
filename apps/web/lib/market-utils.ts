import { MarketSummary } from "@/lib/types";

export type MarketSort = "gap" | "confidence" | "time";

export interface MarketFilters {
  search: string;
  platform: string;
  category: string;
  sortBy: MarketSort;
}

export function filterAndSortMarkets(markets: MarketSummary[], filters: MarketFilters): MarketSummary[] {
  const searchTerm = filters.search.trim().toLowerCase();

  const filtered = markets.filter((market) => {
    const matchesSearch = searchTerm.length === 0 || market.title.toLowerCase().includes(searchTerm);
    const matchesPlatform = filters.platform === "all" || market.platform === filters.platform;
    const matchesCategory = filters.category === "all" || market.category === filters.category;
    return matchesSearch && matchesPlatform && matchesCategory;
  });

  const sorted = [...filtered];
  if (filters.sortBy === "confidence") {
    sorted.sort((left, right) => right.confidence - left.confidence);
  } else if (filters.sortBy === "time") {
    sorted.sort(
      (left, right) =>
        new Date(left.resolution_time).getTime() - new Date(right.resolution_time).getTime()
    );
  } else {
    sorted.sort((left, right) => Math.abs(right.gap) - Math.abs(left.gap));
  }

  return sorted;
}
