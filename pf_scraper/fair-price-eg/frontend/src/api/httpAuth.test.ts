import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AxiosError, type AxiosAdapter, type AxiosResponse } from "axios";
import { authSessionManager } from "@/auth/authSessionManager";
import { http } from "./http";

const originalAdapter = http.defaults.adapter;

function storeSession(token: string, expiresInMs = 3_600_000) {
  sessionStorage.setItem("valorai_access_token", token);
  sessionStorage.setItem("valorai_access_token_expires_at", new Date(Date.now() + expiresInMs).toISOString());
  sessionStorage.setItem(
    "valorai_user_metadata",
    JSON.stringify({ id: 1, external_subject: "firebase-user", display_name: "Firebase User" }),
  );
}

function okResponse(config: Parameters<AxiosAdapter>[0]): AxiosResponse {
  return {
    data: { ok: true },
    status: 200,
    statusText: "OK",
    headers: {},
    config,
  };
}

describe("http auth interceptor", () => {
  beforeEach(async () => {
    sessionStorage.clear();
    await authSessionManager.logout();
    vi.restoreAllMocks();
  });

  afterEach(async () => {
    http.defaults.adapter = originalAdapter;
    sessionStorage.clear();
    await authSessionManager.logout();
    vi.restoreAllMocks();
  });

  it("injects the ValorAI bearer token into protected API requests", async () => {
    storeSession("stored-jwt");
    await authSessionManager.restoreSession();
    const adapter = vi.fn(async (config: Parameters<AxiosAdapter>[0]) => okResponse(config));
    http.defaults.adapter = adapter;

    await http.get("/v1/copilot/workspaces");

    expect(adapter).toHaveBeenCalledTimes(1);
    expect(adapter.mock.calls[0][0].headers.get("Authorization")).toBe("Bearer stored-jwt");
  });

  it("renews and retries once after a 401 response", async () => {
    storeSession("old-jwt");
    await authSessionManager.restoreSession();
    vi.spyOn(authSessionManager, "renewSession").mockResolvedValue("fresh-jwt");
    vi.spyOn(authSessionManager, "getValidAccessToken")
      .mockResolvedValueOnce("old-jwt")
      .mockResolvedValue("fresh-jwt");
    const seenHeaders: Array<string | undefined> = [];
    const adapter = vi.fn(async (config: Parameters<AxiosAdapter>[0]) => {
      const authorization = config.headers.get("Authorization");
      seenHeaders.push(typeof authorization === "string" ? authorization : undefined);
      if (seenHeaders.length === 1) {
        throw new AxiosError("Unauthorized", "ERR_BAD_REQUEST", config, undefined, {
          data: { detail: "expired" },
          status: 401,
          statusText: "Unauthorized",
          headers: {},
          config,
        });
      }
      return okResponse(config);
    });
    http.defaults.adapter = adapter;

    await http.get("/v1/copilot/workspaces");

    expect(seenHeaders).toEqual(["Bearer old-jwt", "Bearer fresh-jwt"]);
  });

  it("marks access denied state on 403 responses", async () => {
    storeSession("stored-jwt");
    await authSessionManager.restoreSession();
    http.defaults.adapter = vi.fn(async (config: Parameters<AxiosAdapter>[0]) => {
      throw new AxiosError("Forbidden", "ERR_BAD_REQUEST", config, undefined, {
        data: { detail: "forbidden" },
        status: 403,
        statusText: "Forbidden",
        headers: {},
        config,
      });
    });

    await expect(http.get("/v1/broker/reason")).rejects.toMatchObject({ status: 403 });

    expect(authSessionManager.snapshot.accessDenied).toBe("You do not have permission to perform this action.");
  });
});
