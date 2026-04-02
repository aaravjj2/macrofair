import { describe, expect, it } from "vitest";

import { DEMO_MARKETS } from "@/lib/demo-data";
import { computeFlagshipFinding } from "@/lib/flagship-finding";

describe("computeFlagshipFinding", () => {
  it("computes a deterministic top dislocation narrative", () => {
    const finding = computeFlagshipFinding(DEMO_MARKETS);

    expect(finding.topMarketId).toBe("poly-cpi-jun-2026-over-3");
    expect(finding.topShareOfTotalGap).toBeGreaterThan(0.25);
    expect(finding.headlineFinding).toMatch(/contributes/i);
  });
});
