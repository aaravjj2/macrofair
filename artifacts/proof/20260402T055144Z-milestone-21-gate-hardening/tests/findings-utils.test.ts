import {
  FLAGSHIP_PERSISTENCE_SNAPSHOTS,
  SECONDARY_FINDING_SNAPSHOTS,
  THIRD_FINDING_CATEGORY_DRIFT,
} from "@/lib/findings-data";
import {
  summarizeFlagshipPersistence,
  summarizeSecondaryFinding,
  summarizeThirdFinding,
} from "@/lib/findings-utils";
import { describe, expect, it } from "vitest";

describe("findings-utils", () => {
  it("summarizes flagship persistence deterministically", () => {
    const first = summarizeFlagshipPersistence(FLAGSHIP_PERSISTENCE_SNAPSHOTS);
    const second = summarizeFlagshipPersistence(FLAGSHIP_PERSISTENCE_SNAPSHOTS);

    expect(first).toEqual(second);
    expect(first.dominantTopMarketId).toBe("poly-cpi-jun-2026-over-3");
    expect(first.persistenceRate).toBeCloseTo(0.9167, 4);
    expect(first.averageTopShare).toBeGreaterThan(0.5);
  });

  it("summarizes platform asymmetry deterministically", () => {
    const first = summarizeSecondaryFinding(SECONDARY_FINDING_SNAPSHOTS);
    const second = summarizeSecondaryFinding(SECONDARY_FINDING_SNAPSHOTS);

    expect(first).toEqual(second);
    expect(first.averageAsymmetryGap).toBeGreaterThan(0);
    expect(first.positiveWindowShare).toBe(1);
  });

  it("summarizes third finding deterministically", () => {
    const first = summarizeThirdFinding(THIRD_FINDING_CATEGORY_DRIFT);
    const second = summarizeThirdFinding(THIRD_FINDING_CATEGORY_DRIFT);

    expect(first).toEqual(second);
    expect(first.dominantCategory).toBe("inflation");
    expect(first.dominantDrift).toBeGreaterThan(0.3);
    expect(first.increasingCategories).toBeGreaterThan(0);
    expect(first.decreasingCategories).toBeGreaterThan(0);
  });
});
