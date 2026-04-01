import { describe, expect, it } from "vitest";

import { DEMO_MARKETS } from "@/lib/demo-data";
import { filterAndSortMarkets } from "@/lib/market-utils";

describe("filterAndSortMarkets", () => {
  it("filters by platform and category", () => {
    const rows = filterAndSortMarkets(DEMO_MARKETS, {
      search: "",
      platform: "Polymarket",
      category: "inflation",
      sortBy: "gap"
    });

    expect(rows).toHaveLength(1);
    expect(rows[0]?.market_id).toBe("poly-cpi-jun-2026-over-3");
  });

  it("sorts by confidence", () => {
    const rows = filterAndSortMarkets(DEMO_MARKETS, {
      search: "",
      platform: "all",
      category: "all",
      sortBy: "confidence"
    });

    expect(rows[0]?.confidence).toBeGreaterThanOrEqual(rows[1]?.confidence ?? 0);
  });

  it("searches by title", () => {
    const rows = filterAndSortMarkets(DEMO_MARKETS, {
      search: "recession",
      platform: "all",
      category: "all",
      sortBy: "gap"
    });

    expect(rows).toHaveLength(1);
    expect(rows[0]?.market_id).toBe("kalshi-recession-q4-2026");
  });
});
