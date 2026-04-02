import {
  FLAGSHIP_PERSISTENCE_SNAPSHOTS,
  SECONDARY_FINDING_SNAPSHOTS,
} from "@/lib/findings-data";
import {
  summarizeFlagshipPersistence,
  summarizeSecondaryFinding,
} from "@/lib/findings-utils";
import { describe, expect, it } from "vitest";

describe("findings-utils", () => {
  it("summarizes flagship persistence deterministically", () => {
    const first = summarizeFlagshipPersistence(FLAGSHIP_PERSISTENCE_SNAPSHOTS);
    const second = summarizeFlagshipPersistence(FLAGSHIP_PERSISTENCE_SNAPSHOTS);

    expect(first).toEqual(second);
    expect(first.dominantTopMarketId).toBe("poly-cpi-jun-2026-over-3");
    expect(first.persistenceRate).toBe(1);
    expect(first.averageTopShare).toBeGreaterThan(0.6);
  });

  it("summarizes platform asymmetry deterministically", () => {
    const first = summarizeSecondaryFinding(SECONDARY_FINDING_SNAPSHOTS);
    const second = summarizeSecondaryFinding(SECONDARY_FINDING_SNAPSHOTS);

    expect(first).toEqual(second);
    expect(first.averageAsymmetryGap).toBeGreaterThan(0);
    expect(first.positiveWindowShare).toBe(1);
  });
});
