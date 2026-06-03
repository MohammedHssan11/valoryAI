type AppEnvironment = "dev" | "testing" | "staging" | "production";

function readEnv(key: string, fallback: string): string {
  const value = import.meta.env[key];
  return typeof value === "string" && value.trim().length > 0 ? value.trim() : fallback;
}

function readNumberEnv(key: string, fallback: number): number {
  const value = Number(import.meta.env[key]);
  return Number.isFinite(value) && value > 0 ? value : fallback;
}

function trimTrailingSlash(value: string): string {
  return value.endsWith("/") ? value.slice(0, -1) : value;
}

function normalizeEnvironment(value: string): AppEnvironment {
  const normalized = value.trim().toLowerCase();
  if (normalized === "test") return "testing";
  if (normalized === "prod") return "production";
  if (normalized === "stage") return "staging";
  if (normalized === "testing" || normalized === "staging" || normalized === "production" || normalized === "dev") {
    return normalized;
  }
  return "dev";
}

const appEnv = normalizeEnvironment(readEnv("VITE_APP_ENV", "dev"));

export const appConfig = {
  appEnv,
  isProduction: appEnv === "production",
  apiBaseUrl: trimTrailingSlash(readEnv("VITE_API_BASE_URL", "http://localhost:8000")),
  requestTimeoutMs: readNumberEnv("VITE_API_TIMEOUT_MS", 20000),
};
