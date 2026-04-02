import { afterEach, describe, expect, it, vi } from "vitest";

import { resolveZerveStatus } from "@/lib/zerve-status";

const originalFetch = global.fetch;
const originalEnv = { ...process.env };

afterEach(() => {
  global.fetch = originalFetch;
  process.env = { ...originalEnv };
  vi.restoreAllMocks();
});

describe("resolveZerveStatus", () => {
  it("falls back to deterministic env status when backend base URL is absent", async () => {
    process.env.MACROFAIR_API_BASE_URL = "";
    process.env.ZERVE_ENABLED = "false";

    const status = await resolveZerveStatus();

    expect(status.source).toBe("env-fallback");
    expect(status.enabled).toBe(false);
    expect(status.mode).toBe("demo");
  });

  it("uses backend status when API base URL is configured", async () => {
    process.env.MACROFAIR_API_BASE_URL = "https://api.example.test";
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        enabled: true,
        configured: true,
        mode: "demo",
        base_url: "https://api.example.test",
        project_id: "project-123",
        api_key_configured: true,
        note: "Configured",
      }),
    } as unknown as Response);

    const status = await resolveZerveStatus();

    expect(status.source).toBe("backend");
    expect(status.enabled).toBe(true);
    expect(status.configured).toBe(true);
    expect(status.baseUrl).toBe("https://api.example.test");
    expect(status.projectId).toBe("project-123");
  });
});
