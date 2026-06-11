import * as React from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "@/auth/AuthProvider";
import { APP_ROUTES } from "@/navigation/routes";

function LoadingSession() {
  return (
    <main className="flex min-h-screen w-full items-center justify-center bg-background px-4 text-on-background">
      <div className="flex items-center gap-3 rounded-lg border border-white/10 bg-surface/70 px-5 py-4 text-sm text-on-surface-variant">
        <span className="h-2 w-2 animate-pulse rounded-full bg-primary-fixed-dim" />
        Loading ValorAI session
      </div>
    </main>
  );
}

function AccessDeniedState() {
  const auth = useAuth();

  return (
    <main className="flex min-h-screen w-full items-center justify-center bg-background px-4 text-on-background">
      <div className="max-w-md rounded-lg border border-error/30 bg-error-container/20 p-6 text-center">
        <span className="material-symbols-outlined text-3xl text-error">lock</span>
        <h1 className="mt-3 text-xl text-on-surface">Access denied</h1>
        <p className="mt-2 text-sm text-on-surface-variant">
          {auth.accessDenied ?? "You do not have permission to perform this action."}
        </p>
        <button
          type="button"
          className="mt-5 rounded-lg border border-primary/30 px-4 py-2 text-sm text-primary-fixed-dim"
          onClick={auth.clearAccessDenied}
        >
          Return to workspace
        </button>
      </div>
    </main>
  );
}

export function ProtectedRoute() {
  const auth = useAuth();
  const location = useLocation();

  if (auth.status === "uninitialized" || auth.status === "loading") {
    return <LoadingSession />;
  }

  if (auth.status === "expired") {
    return <Navigate to={`${APP_ROUTES.login}?reason=expired`} replace state={{ from: location }} />;
  }

  if (!auth.isAuthenticated) {
    return <Navigate to={APP_ROUTES.login} replace state={{ from: location }} />;
  }

  if (auth.accessDenied) {
    return <AccessDeniedState />;
  }

  return <Outlet />;
}
