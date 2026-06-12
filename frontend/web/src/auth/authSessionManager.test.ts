import { beforeEach, describe, expect, it, vi } from "vitest";
import { AuthSessionManager } from "./authSessionManager";
import type { FirebaseUserLike } from "./firebaseClient";
import type { TokenExchangeResult, ValorUser } from "./tokenExchange";

class MemoryStorage {
  private values = new Map<string, string>();

  getItem(key: string): string | null {
    return this.values.get(key) ?? null;
  }

  setItem(key: string, value: string): void {
    this.values.set(key, value);
  }

  removeItem(key: string): void {
    this.values.delete(key);
  }
}

const user: ValorUser = {
  id: 7,
  external_subject: "firebase-user",
  display_name: "Firebase User",
};

const exchangeResult: TokenExchangeResult = {
  access_token: "valorai-jwt",
  token_type: "bearer",
  expires_in: 3600,
  user,
};

function fakeFirebaseUser(idToken = "firebase-id-token"): FirebaseUserLike {
  return {
    uid: "firebase-user",
    email: "user@example.com",
    displayName: "Firebase User",
    getIdToken: vi.fn().mockResolvedValue(idToken),
  };
}

describe("AuthSessionManager", () => {
  let storage: MemoryStorage;
  let now: number;

  beforeEach(() => {
    storage = new MemoryStorage();
    now = Date.parse("2026-06-10T12:00:00Z");
  });

  it("restores an unexpired ValorAI JWT from browser session storage", async () => {
    storage.setItem("valorai_access_token", "stored-jwt");
    storage.setItem("valorai_access_token_expires_at", new Date(now + 3_600_000).toISOString());
    storage.setItem("valorai_user_metadata", JSON.stringify(user));

    const manager = new AuthSessionManager({
      storage,
      now: () => now,
      getCurrentFirebaseUser: vi.fn(),
    });

    await manager.restoreSession();

    expect(manager.snapshot.status).toBe("authenticated");
    expect(manager.snapshot.accessToken).toBe("stored-jwt");
    expect(manager.snapshot.user?.display_name).toBe("Firebase User");
  });

  it("exchanges the active Firebase ID token when the stored JWT is expired", async () => {
    storage.setItem("valorai_access_token", "expired-jwt");
    storage.setItem("valorai_access_token_expires_at", new Date(now - 1_000).toISOString());
    storage.setItem("valorai_user_metadata", JSON.stringify(user));

    const firebaseUser = fakeFirebaseUser();
    const exchange = vi.fn().mockResolvedValue(exchangeResult);
    const manager = new AuthSessionManager({
      storage,
      now: () => now,
      getCurrentFirebaseUser: vi.fn().mockResolvedValue(firebaseUser),
      exchangeFirebaseToken: exchange,
    });

    await manager.restoreSession();

    expect(firebaseUser.getIdToken).toHaveBeenCalledWith(true);
    expect(exchange).toHaveBeenCalledWith("firebase-id-token");
    expect(manager.snapshot.accessToken).toBe("valorai-jwt");
    expect(storage.getItem("valorai_access_token")).toBe("valorai-jwt");
  });

  it("signs in with Firebase and stores the exchanged ValorAI session", async () => {
    const manager = new AuthSessionManager({
      storage,
      now: () => now,
      signInFirebase: vi.fn().mockResolvedValue(fakeFirebaseUser()),
      getCurrentFirebaseUser: vi.fn().mockResolvedValue(fakeFirebaseUser("fresh-firebase-token")),
      exchangeFirebaseToken: vi.fn().mockResolvedValue(exchangeResult),
    });

    await manager.signIn("user@example.com", "password");

    expect(manager.snapshot.status).toBe("authenticated");
    expect(storage.getItem("valorai_access_token")).toBe("valorai-jwt");
    expect(storage.getItem("valorai_user_metadata")).toContain("Firebase User");
  });

  it("cleans up ValorAI and Firebase state on logout", async () => {
    storage.setItem("valorai_access_token", "stored-jwt");
    storage.setItem("valorai_access_token_expires_at", new Date(now + 3_600_000).toISOString());
    storage.setItem("valorai_user_metadata", JSON.stringify(user));
    const signOut = vi.fn().mockResolvedValue(undefined);
    const manager = new AuthSessionManager({
      storage,
      now: () => now,
      signOutFirebase: signOut,
    });

    await manager.restoreSession();
    await manager.logout();

    expect(signOut).toHaveBeenCalled();
    expect(manager.snapshot.status).toBe("anonymous");
    expect(storage.getItem("valorai_access_token")).toBeNull();
  });
});
