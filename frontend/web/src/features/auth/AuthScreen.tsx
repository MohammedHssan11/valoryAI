import * as React from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { GlassCard } from "@/components/ui/glass";
import { useAuth } from "@/auth/AuthProvider";
import { isFirebaseConfigured } from "@/auth/firebaseClient";
import { DEFAULT_AUTHENTICATED_ROUTE } from "@/navigation/routes";

type AuthMode = "login" | "signup" | "reset";

function modeTitle(mode: AuthMode): string {
  if (mode === "signup") return "Create Account";
  if (mode === "reset") return "Reset Password";
  return "Welcome Back";
}

function reasonMessage(search: string): string | null {
  const reason = new URLSearchParams(search).get("reason");
  if (reason === "expired") return "Your session expired. Sign in again to continue.";
  if (reason === "denied") return "Access denied for that protected workflow.";
  return null;
}

export function AuthScreen() {
  const auth = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mode, setMode] = React.useState<AuthMode>("login");
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [displayName, setDisplayName] = React.useState("");
  const [notice, setNotice] = React.useState<string | null>(reasonMessage(location.search));
  const [error, setError] = React.useState<string | null>(null);
  const from = (location.state as { from?: { pathname?: string } } | null)?.from?.pathname ?? DEFAULT_AUTHENTICATED_ROUTE;
  const configured = isFirebaseConfigured();
  const busy = auth.status === "loading";

  React.useEffect(() => {
    setNotice(reasonMessage(location.search));
  }, [location.search]);

  if (auth.isAuthenticated) {
    return <Navigate to={from} replace />;
  }

  const submit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setNotice(null);

    try {
      if (mode === "reset") {
        await auth.sendPasswordReset(email);
        setNotice("Password reset email sent.");
        setMode("login");
        return;
      }

      if (mode === "signup") {
        await auth.signUp(email, password, displayName);
      } else {
        await auth.signIn(email, password);
      }
      navigate(from, { replace: true });
    } catch (submitError) {
      setError(
        submitError instanceof Error && submitError.message
          ? submitError.message
          : "ValorAI could not establish an authenticated session.",
      );
    }
  };

  return (
    <main className="flex min-h-screen w-full items-center justify-center bg-background px-4 py-12 text-on-background">
      <GlassCard className="w-full max-w-md p-6">
        <div className="mb-8 text-center">
          <div className="mb-4 flex items-center justify-center gap-2 text-primary-fixed-dim">
            <span className="material-symbols-outlined text-3xl" style={{ fontVariationSettings: "'FILL' 1" }}>
              blur_on
            </span>
            <span className="font-headline-lg-mobile text-2xl text-primary">VALORAI</span>
          </div>
          <h1 className="font-headline-lg-mobile text-2xl text-on-surface">{modeTitle(mode)}</h1>
          <p className="mt-2 text-sm text-on-surface-variant">Authenticate to unlock protected intelligence workflows.</p>
        </div>

        {!configured && (
          <div className="mb-4 rounded-lg border border-error/30 bg-error-container/25 px-4 py-3 text-sm text-on-error-container">
            Firebase web configuration is missing. Add the `VITE_FIREBASE_*` values before signing in.
          </div>
        )}

        {(notice || auth.error) && (
          <div className="mb-4 rounded-lg border border-primary/20 bg-primary/10 px-4 py-3 text-sm text-primary">
            {notice ?? auth.error}
          </div>
        )}

        {error && (
          <div className="mb-4 rounded-lg border border-error/30 bg-error-container/25 px-4 py-3 text-sm text-on-error-container">
            {error}
          </div>
        )}

        <form className="space-y-4" onSubmit={submit}>
          {mode === "signup" && (
            <label className="block">
              <span className="mb-1 block text-xs uppercase text-on-surface-variant">Name</span>
              <input
                className="w-full rounded-lg border border-white/10 bg-surface-container-lowest px-4 py-3 text-on-surface outline-none transition-colors focus:border-primary/60"
                autoComplete="name"
                value={displayName}
                onChange={(event) => setDisplayName(event.target.value)}
              />
            </label>
          )}

          <label className="block">
            <span className="mb-1 block text-xs uppercase text-on-surface-variant">Email</span>
            <input
              className="w-full rounded-lg border border-white/10 bg-surface-container-lowest px-4 py-3 text-on-surface outline-none transition-colors focus:border-primary/60"
              type="email"
              autoComplete="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </label>

          {mode !== "reset" && (
            <label className="block">
              <span className="mb-1 block text-xs uppercase text-on-surface-variant">Password</span>
              <input
                className="w-full rounded-lg border border-white/10 bg-surface-container-lowest px-4 py-3 text-on-surface outline-none transition-colors focus:border-primary/60"
                type="password"
                autoComplete={mode === "signup" ? "new-password" : "current-password"}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
              />
            </label>
          )}

          <Button type="submit" className="w-full" disabled={!configured || busy}>
            {busy ? "CONNECTING" : mode === "reset" ? "SEND RESET" : mode === "signup" ? "CREATE ACCOUNT" : "SIGN IN"}
          </Button>
        </form>

        <div className="mt-6 flex flex-wrap items-center justify-center gap-3 text-sm text-on-surface-variant">
          {mode !== "login" && (
            <button type="button" className="text-primary-fixed-dim" onClick={() => setMode("login")}>
              Back to sign in
            </button>
          )}
          {mode === "login" && (
            <>
              <button type="button" className="text-primary-fixed-dim" onClick={() => setMode("signup")}>
                Create account
              </button>
              <span aria-hidden="true">/</span>
              <button type="button" className="text-primary-fixed-dim" onClick={() => setMode("reset")}>
                Reset password
              </button>
            </>
          )}
        </div>
      </GlassCard>
    </main>
  );
}
