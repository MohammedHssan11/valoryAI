import { afterEach, describe, expect, it, vi } from "vitest";
import { exchangeFirebaseToken } from "./tokenExchange";

describe("exchangeFirebaseToken", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("posts the Firebase ID token to the backend token exchange endpoint", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(
        JSON.stringify({
          access_token: "valorai-jwt",
          token_type: "bearer",
          expires_in: 3600,
          user: {
            id: 1,
            external_subject: "firebase-user",
            display_name: "Firebase User",
          },
        }),
        { status: 200, headers: { "Content-Type": "application/json" } },
      ),
    );
    vi.stubGlobal("fetch", fetchMock);

    const result = await exchangeFirebaseToken("firebase-id-token");

    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/v1/auth/token-exchange",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ firebase_id_token: "firebase-id-token" }),
      }),
    );
    expect(result.access_token).toBe("valorai-jwt");
    expect(result.user.display_name).toBe("Firebase User");
  });

  it("surfaces backend token exchange errors", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ detail: "Invalid Firebase token" }), {
          status: 401,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    await expect(exchangeFirebaseToken("bad-token")).rejects.toThrow("Invalid Firebase token");
  });
});
