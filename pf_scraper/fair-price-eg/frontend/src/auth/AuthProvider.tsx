import * as React from "react";
import {
  authSessionManager,
  type AuthSnapshot,
  type AuthSessionManager,
} from "./authSessionManager";

interface AuthContextValue extends AuthSnapshot {
  isAuthenticated: boolean;
  restoreSession: () => Promise<void>;
  signIn: (email: string, password: string) => Promise<string>;
  signUp: (email: string, password: string, displayName?: string) => Promise<string>;
  sendPasswordReset: (email: string) => Promise<void>;
  logout: () => Promise<void>;
  clearAccessDenied: () => void;
}

const AuthContext = React.createContext<AuthContextValue | null>(null);

function contextFromSnapshot(manager: AuthSessionManager, snapshot: AuthSnapshot): AuthContextValue {
  return {
    ...snapshot,
    isAuthenticated: manager.isAuthenticated,
    restoreSession: () => manager.restoreSession(),
    signIn: (email, password) => manager.signIn(email, password),
    signUp: (email, password, displayName) => manager.signUp(email, password, displayName),
    sendPasswordReset: (email) => manager.sendPasswordReset(email),
    logout: () => manager.logout(),
    clearAccessDenied: () => manager.clearAccessDenied(),
  };
}

interface AuthProviderProps {
  children: React.ReactNode;
  manager?: AuthSessionManager;
}

export function AuthProvider({ children, manager = authSessionManager }: AuthProviderProps) {
  const [snapshot, setSnapshot] = React.useState<AuthSnapshot>(manager.snapshot);

  React.useEffect(() => manager.subscribe(setSnapshot), [manager]);

  React.useEffect(() => {
    void manager.restoreSession();
  }, [manager]);

  const value = React.useMemo(() => contextFromSnapshot(manager, snapshot), [manager, snapshot]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider.");
  }
  return context;
}
