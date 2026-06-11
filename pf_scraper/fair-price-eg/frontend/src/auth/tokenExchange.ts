import { appConfig } from "@/core/config";

export interface ValorUser {
  id: number;
  external_subject: string;
  display_name: string;
  created_at?: string;
  updated_at?: string;
  version?: number;
  is_deleted?: boolean;
  deleted_at?: string | null;
}

export interface TokenExchangeResult {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
  user: ValorUser;
}

export class AuthSessionError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "AuthSessionError";
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function apiErrorMessage(value: unknown): string | undefined {
  if (!isRecord(value)) return undefined;
  const detail = value.detail;
  if (typeof detail === "string" && detail.trim()) return detail;

  const error = value.error;
  if (isRecord(error) && typeof error.message === "string" && error.message.trim()) {
    return error.message;
  }

  return undefined;
}

function assertTokenExchange(value: unknown): TokenExchangeResult {
  if (!isRecord(value) || !isRecord(value.user)) {
    throw new AuthSessionError("The authentication service returned an unexpected response.");
  }

  if (
    typeof value.access_token !== "string" ||
    value.access_token.length === 0 ||
    typeof value.expires_in !== "number" ||
    !Number.isFinite(value.expires_in) ||
    value.expires_in <= 0 ||
    typeof value.user.id !== "number" ||
    typeof value.user.external_subject !== "string" ||
    typeof value.user.display_name !== "string"
  ) {
    throw new AuthSessionError("The authentication service returned an invalid session.");
  }

  return {
    access_token: value.access_token,
    token_type: value.token_type === "bearer" ? "bearer" : "bearer",
    expires_in: value.expires_in,
    user: value.user as unknown as ValorUser,
  };
}

export async function exchangeFirebaseToken(firebaseIdToken: string): Promise<TokenExchangeResult> {
  let response: Response;
  try {
    response = await fetch(`${appConfig.apiBaseUrl}/v1/auth/token-exchange`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ firebase_id_token: firebaseIdToken }),
    });
  } catch (error) {
    throw new AuthSessionError(
      error instanceof Error && error.message
        ? error.message
        : "Unable to reach the ValorAI authentication service.",
    );
  }

  let payload: unknown = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    throw new AuthSessionError(
      apiErrorMessage(payload) ?? "ValorAI could not establish an authenticated session.",
    );
  }

  return assertTokenExchange(payload);
}
