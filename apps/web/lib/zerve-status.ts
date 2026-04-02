type ZerveStatusSource = "backend" | "env-fallback";

export interface ZerveStatusView {
  integration: "zerve";
  enabled: boolean;
  configured: boolean;
  mode: string;
  baseUrl: string;
  projectId: string;
  apiKeyConfigured: boolean;
  source: ZerveStatusSource;
  backendChecked: boolean;
  note: string;
}

function parseBool(value: string | undefined): boolean {
  if (!value) {
    return false;
  }
  return ["1", "true", "yes", "on"].includes(value.trim().toLowerCase());
}

function buildEnvFallbackStatus(): ZerveStatusView {
  const enabled = parseBool(process.env.ZERVE_ENABLED);
  const baseUrl = (process.env.ZERVE_BASE_URL ?? "").trim();
  const projectId = (process.env.ZERVE_PROJECT_ID ?? "").trim();
  const apiKeyConfigured = Boolean((process.env.ZERVE_API_KEY ?? "").trim());
  const configured = enabled && Boolean(baseUrl) && Boolean(projectId) && apiKeyConfigured;

  return {
    integration: "zerve",
    enabled,
    configured,
    mode: process.env.MACROFAIR_MODE ?? "demo",
    baseUrl: enabled ? baseUrl : "",
    projectId: enabled ? projectId : "",
    apiKeyConfigured,
    source: "env-fallback",
    backendChecked: false,
    note: enabled
      ? configured
        ? "Zerve appears configured from server-side env."
        : "Zerve enabled but missing required server-side env."
      : "Zerve integration disabled by default. Demo mode remains active.",
  };
}

export async function resolveZerveStatus(): Promise<ZerveStatusView> {
  const fallback = buildEnvFallbackStatus();
  const apiBaseUrl = (process.env.MACROFAIR_API_BASE_URL ?? "").trim().replace(/\/$/, "");

  if (!apiBaseUrl) {
    return fallback;
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 1200);

  try {
    const response = await fetch(`${apiBaseUrl}/api/v1/integrations/zerve/status`, {
      method: "GET",
      cache: "no-store",
      signal: controller.signal,
    });

    if (!response.ok) {
      return {
        ...fallback,
        backendChecked: true,
        note: "Backend status endpoint was unreachable. Falling back to local env status.",
      };
    }

    const payload = await response.json();
    return {
      integration: "zerve",
      enabled: Boolean(payload.enabled),
      configured: Boolean(payload.configured),
      mode: String(payload.mode ?? "demo"),
      baseUrl: String(payload.base_url ?? ""),
      projectId: String(payload.project_id ?? ""),
      apiKeyConfigured: Boolean(payload.api_key_configured),
      source: "backend",
      backendChecked: true,
      note: String(payload.note ?? "Backend status loaded."),
    };
  } catch {
    return {
      ...fallback,
      backendChecked: true,
      note: "Backend status fetch failed. Falling back to local env status.",
    };
  } finally {
    clearTimeout(timeout);
  }
}
