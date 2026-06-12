import {
  getCurrentFirebaseUser,
  sendFirebasePasswordReset,
  signInFirebase,
  signOutFirebase,
  signUpFirebase,
  type FirebaseUserLike,
} from "./firebaseClient";
import { AuthSessionError, exchangeFirebaseToken, type TokenExchangeResult, type ValorUser } from "./tokenExchange";

export type AuthSessionStatus = "uninitialized" | "loading" | "anonymous" | "authenticated" | "expired";

export interface AuthSnapshot {
  status: AuthSessionStatus;
  accessToken: string | null;
  expiresAt: string | null;
  user: ValorUser | null;
  error: string | null;
  accessDenied: string | null;
}

interface StoredSession {
  accessToken: string;
  expiresAt: string;
  user: ValorUser;
}

interface StorageLike {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
  removeItem(key: string): void;
}

interface AuthSessionDependencies {
  storage?: StorageLike;
  now?: () => number;
  exchangeFirebaseToken?: (firebaseIdToken: string) => Promise<TokenExchangeResult>;
  getCurrentFirebaseUser?: () => Promise<FirebaseUserLike | null>;
  signInFirebase?: (email: string, password: string) => Promise<FirebaseUserLike>;
  signUpFirebase?: (email: string, password: string, displayName?: string) => Promise<FirebaseUserLike>;
  sendPasswordReset?: (email: string) => Promise<void>;
  signOutFirebase?: () => Promise<void>;
}

const ACCESS_TOKEN_KEY = "valorai_access_token";
const EXPIRES_AT_KEY = "valorai_access_token_expires_at";
const USER_METADATA_KEY = "valorai_user_metadata";
const REFRESH_WINDOW_MS = 60_000;

function browserSessionStorage(): StorageLike | undefined {
  if (typeof window === "undefined") return undefined;
  return window.sessionStorage;
}

function safeParseSession(storage: StorageLike | undefined): StoredSession | null {
  if (!storage) return null;
  try {
    const accessToken = storage.getItem(ACCESS_TOKEN_KEY);
    const expiresAt = storage.getItem(EXPIRES_AT_KEY);
    const userRaw = storage.getItem(USER_METADATA_KEY);
    if (!accessToken || !expiresAt || !userRaw) return null;
    const user = JSON.parse(userRaw) as ValorUser;
    return { accessToken, expiresAt, user };
  } catch {
    return null;
  }
}

function messageForError(error: unknown): string {
  if (error instanceof AuthSessionError) return error.message;
  if (error instanceof Error && error.message.trim()) return error.message;
  return "ValorAI could not establish an authenticated session.";
}

function emptySnapshot(): AuthSnapshot {
  return {
    status: "uninitialized",
    accessToken: null,
    expiresAt: null,
    user: null,
    error: null,
    accessDenied: null,
  };
}

export class AuthSessionManager {
  private readonly storage?: StorageLike;
  private readonly now: () => number;
  private readonly exchangeToken: (firebaseIdToken: string) => Promise<TokenExchangeResult>;
  private readonly readFirebaseUser: () => Promise<FirebaseUserLike | null>;
  private readonly signInWithFirebase: (email: string, password: string) => Promise<FirebaseUserLike>;
  private readonly signUpWithFirebase: (email: string, password: string, displayName?: string) => Promise<FirebaseUserLike>;
  private readonly resetPasswordWithFirebase: (email: string) => Promise<void>;
  private readonly signOutFromFirebase: () => Promise<void>;
  private readonly listeners = new Set<(snapshot: AuthSnapshot) => void>();

  private snapshotState: AuthSnapshot = emptySnapshot();
  private bootstrapTask: Promise<void> | null = null;
  private renewalTask: Promise<string> | null = null;

  constructor(dependencies: AuthSessionDependencies = {}) {
    this.storage = dependencies.storage ?? browserSessionStorage();
    this.now = dependencies.now ?? (() => Date.now());
    this.exchangeToken = dependencies.exchangeFirebaseToken ?? exchangeFirebaseToken;
    this.readFirebaseUser = dependencies.getCurrentFirebaseUser ?? getCurrentFirebaseUser;
    this.signInWithFirebase = dependencies.signInFirebase ?? signInFirebase;
    this.signUpWithFirebase = dependencies.signUpFirebase ?? signUpFirebase;
    this.resetPasswordWithFirebase = dependencies.sendPasswordReset ?? sendFirebasePasswordReset;
    this.signOutFromFirebase = dependencies.signOutFirebase ?? signOutFirebase;
  }

  get snapshot(): AuthSnapshot {
    return this.snapshotState;
  }

  get accessToken(): string | null {
    return this.snapshotState.accessToken;
  }

  get isAuthenticated(): boolean {
    return this.hasUsableToken(this.snapshotState);
  }

  subscribe(listener: (snapshot: AuthSnapshot) => void): () => void {
    this.listeners.add(listener);
    listener(this.snapshotState);
    return () => {
      this.listeners.delete(listener);
    };
  }

  async restoreSession(): Promise<void> {
    if (this.bootstrapTask) {
      return this.bootstrapTask;
    }

    this.bootstrapTask = this.restoreSessionOnce().finally(() => {
      this.bootstrapTask = null;
    });
    return this.bootstrapTask;
  }

  async signIn(email: string, password: string): Promise<string> {
    this.setSnapshot({ ...this.snapshotState, status: "loading", error: null, accessDenied: null });
    try {
      await this.signInWithFirebase(email.trim(), password);
      return await this.renewSession();
    } catch (error) {
      this.clearStoredSession();
      this.setSnapshot({
        ...emptySnapshot(),
        status: "anonymous",
        error: messageForError(error),
      });
      throw error;
    }
  }

  async signUp(email: string, password: string, displayName?: string): Promise<string> {
    this.setSnapshot({ ...this.snapshotState, status: "loading", error: null, accessDenied: null });
    try {
      await this.signUpWithFirebase(email.trim(), password, displayName);
      return await this.renewSession();
    } catch (error) {
      this.clearStoredSession();
      this.setSnapshot({
        ...emptySnapshot(),
        status: "anonymous",
        error: messageForError(error),
      });
      throw error;
    }
  }

  async sendPasswordReset(email: string): Promise<void> {
    await this.resetPasswordWithFirebase(email.trim());
  }

  async getValidAccessToken(forceRefresh = false): Promise<string | null> {
    if (!forceRefresh && this.hasUsableToken(this.snapshotState)) {
      return this.snapshotState.accessToken;
    }

    const firebaseUser = await this.readFirebaseUser();
    if (!firebaseUser) {
      if (this.snapshotState.status === "authenticated") {
        await this.expireSession();
      }
      return null;
    }

    return this.renewSession();
  }

  async renewSession(): Promise<string> {
    if (this.renewalTask) return this.renewalTask;

    this.renewalTask = this.exchangeFirebaseSession().finally(() => {
      this.renewalTask = null;
    });

    return this.renewalTask;
  }

  async expireSession(message = "Your session has expired. Please sign in again."): Promise<void> {
    this.clearStoredSession();
    this.setSnapshot({
      ...emptySnapshot(),
      status: "expired",
      error: message,
    });
  }

  async logout(): Promise<void> {
    this.clearStoredSession();
    try {
      await this.signOutFromFirebase();
    } finally {
      this.setSnapshot({ ...emptySnapshot(), status: "anonymous" });
    }
  }

  markAccessDenied(message = "You do not have permission to perform this action."): void {
    this.setSnapshot({
      ...this.snapshotState,
      accessDenied: message,
    });
  }

  clearAccessDenied(): void {
    if (!this.snapshotState.accessDenied) return;
    this.setSnapshot({
      ...this.snapshotState,
      accessDenied: null,
    });
  }

  private async restoreSessionOnce(): Promise<void> {
    const storedSession = safeParseSession(this.storage);
    if (storedSession && this.hasUsableStoredSession(storedSession)) {
      this.setAuthenticated({
        accessToken: storedSession.accessToken,
        expiresAt: storedSession.expiresAt,
        user: storedSession.user,
      });
      return;
    }

    this.clearStoredSession();
    try {
      const firebaseUser = await this.readFirebaseUser();
      if (firebaseUser) {
        await this.renewSession();
        return;
      }
    } catch {
      this.clearStoredSession();
    }

    this.setSnapshot({ ...emptySnapshot(), status: "anonymous" });
  }

  private async exchangeFirebaseSession(): Promise<string> {
    const firebaseUser = await this.readFirebaseUser();
    if (!firebaseUser) {
      throw new AuthSessionError("Sign in with Firebase before starting a ValorAI session.");
    }

    const firebaseIdToken = await firebaseUser.getIdToken(true);
    if (!firebaseIdToken) {
      throw new AuthSessionError("Firebase did not return an identity token.");
    }

    const exchange = await this.exchangeToken(firebaseIdToken);
    const expiresAt = new Date(this.now() + exchange.expires_in * 1000).toISOString();
    this.storeSession(exchange.access_token, expiresAt, exchange.user);
    this.setAuthenticated({
      accessToken: exchange.access_token,
      expiresAt,
      user: exchange.user,
    });
    return exchange.access_token;
  }

  private hasUsableToken(snapshot: AuthSnapshot): snapshot is AuthSnapshot & { accessToken: string; expiresAt: string } {
    if (snapshot.status !== "authenticated" || !snapshot.accessToken || !snapshot.expiresAt) return false;
    const expiresAt = Date.parse(snapshot.expiresAt);
    return Number.isFinite(expiresAt) && expiresAt - this.now() > REFRESH_WINDOW_MS;
  }

  private hasUsableStoredSession(session: StoredSession): boolean {
    const expiresAt = Date.parse(session.expiresAt);
    return Boolean(session.accessToken) && Number.isFinite(expiresAt) && expiresAt - this.now() > REFRESH_WINDOW_MS;
  }

  private setAuthenticated(session: { accessToken: string; expiresAt: string; user: ValorUser }): void {
    this.setSnapshot({
      status: "authenticated",
      accessToken: session.accessToken,
      expiresAt: session.expiresAt,
      user: session.user,
      error: null,
      accessDenied: null,
    });
  }

  private storeSession(accessToken: string, expiresAt: string, user: ValorUser): void {
    try {
      this.storage?.setItem(ACCESS_TOKEN_KEY, accessToken);
      this.storage?.setItem(EXPIRES_AT_KEY, expiresAt);
      this.storage?.setItem(USER_METADATA_KEY, JSON.stringify(user));
    } catch {
      // Browser storage can be unavailable in private modes; keep the in-memory session.
    }
  }

  private clearStoredSession(): void {
    try {
      this.storage?.removeItem(ACCESS_TOKEN_KEY);
      this.storage?.removeItem(EXPIRES_AT_KEY);
      this.storage?.removeItem(USER_METADATA_KEY);
    } catch {
      // Ignored for environments that expose but reject storage access.
    }
  }

  private setSnapshot(snapshot: AuthSnapshot): void {
    this.snapshotState = snapshot;
    for (const listener of this.listeners) {
      listener(snapshot);
    }
  }
}

export const authSessionManager = new AuthSessionManager();
