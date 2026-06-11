import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { AuthProvider } from "@/auth/AuthProvider";
import { AuthSessionManager } from "@/auth/authSessionManager";
import { APP_ROUTES } from "@/navigation/routes";
import { AuthScreen } from "./AuthScreen";
import { ProtectedRoute } from "./ProtectedRoute";

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

function renderProtectedRoute(manager: AuthSessionManager, initialEntry = APP_ROUTES.broker) {
  return render(
    <AuthProvider manager={manager}>
      <MemoryRouter initialEntries={[initialEntry]}>
        <Routes>
          <Route path={APP_ROUTES.login} element={<AuthScreen />} />
          <Route element={<ProtectedRoute />}>
            <Route path={APP_ROUTES.broker} element={<div>Broker workspace</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    </AuthProvider>,
  );
}

describe("ProtectedRoute", () => {
  it("redirects anonymous users to login", async () => {
    const manager = new AuthSessionManager({
      storage: new MemoryStorage(),
      getCurrentFirebaseUser: async () => null,
    });

    renderProtectedRoute(manager);

    expect(await screen.findByText("Welcome Back")).toBeInTheDocument();
  });

  it("renders protected content when a restorable ValorAI session exists", async () => {
    const storage = new MemoryStorage();
    storage.setItem("valorai_access_token", "stored-jwt");
    storage.setItem("valorai_access_token_expires_at", new Date(Date.now() + 3_600_000).toISOString());
    storage.setItem(
      "valorai_user_metadata",
      JSON.stringify({ id: 1, external_subject: "firebase-user", display_name: "Firebase User" }),
    );
    const manager = new AuthSessionManager({
      storage,
      getCurrentFirebaseUser: async () => null,
    });

    renderProtectedRoute(manager);

    expect(await screen.findByText("Broker workspace")).toBeInTheDocument();
  });
});
