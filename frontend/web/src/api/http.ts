import axios, { AxiosError, AxiosResponseHeaders, RawAxiosResponseHeaders } from "axios";
import { authSessionManager } from "@/auth/authSessionManager";
import { appConfig } from "@/core/config";
import { ApiErrorPayload, isApiErrorEnvelope, ValorApiError } from "./contracts";

declare module "axios" {
  interface InternalAxiosRequestConfig {
    authRetried?: boolean;
    skipAuth?: boolean;
  }
}

function makeRequestId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `valor-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

const correlationId = makeRequestId();

function readResponseHeader(headers: AxiosResponseHeaders | RawAxiosResponseHeaders | undefined, key: string): string | undefined {
  if (!headers) return undefined;
  const getter = (headers as { get?: unknown }).get;
  const value = typeof getter === "function" ? getter.call(headers, key) : headers[key] ?? headers[key.toLowerCase()];
  return typeof value === "string" ? value : undefined;
}

function readConfigHeader(error: AxiosError, key: string): string | undefined {
  const headers = error.config?.headers;
  if (!headers) return undefined;
  const getter = (headers as { get?: unknown }).get;
  const value = typeof getter === "function" ? getter.call(headers, key) : headers[key] ?? headers[key.toLowerCase()];
  return typeof value === "string" ? value : undefined;
}

function networkErrorPayload(error: AxiosError): ApiErrorPayload {
  if (error.code === "ERR_CANCELED") {
    return {
      code: "REQUEST_CANCELLED",
      message: "The valuation request was cancelled.",
      details: [],
    };
  }

  if (typeof navigator !== "undefined" && navigator.onLine === false) {
    return {
      code: "OFFLINE",
      message: "You appear to be offline. Reconnect and try again.",
      details: [],
    };
  }

  if (error.code === "ECONNABORTED" || error.code === "ETIMEDOUT") {
    return {
      code: "REQUEST_TIMEOUT",
      message: "The ValorAI API request timed out.",
      details: [],
    };
  }

  return {
    code: "NETWORK_ERROR",
    message: error.message || "Unable to reach the ValorAI API.",
    details: [],
  };
}

export const http = axios.create({
  baseURL: appConfig.apiBaseUrl,
  timeout: appConfig.requestTimeoutMs,
  headers: {
    "Content-Type": "application/json",
  },
});

http.interceptors.request.use((config) => {
  config.headers.set("X-Request-ID", makeRequestId());
  config.headers.set("X-Correlation-ID", correlationId);
  if (config.skipAuth) {
    return config;
  }

  return authSessionManager.getValidAccessToken().then((token) => {
    if (token) {
      config.headers.set("Authorization", `Bearer ${token}`);
    }
    return config;
  });
});

http.interceptors.response.use(
  (response) => {
    if (isApiErrorEnvelope(response.data)) {
      throw new ValorApiError(response.data.error, {
        requestId: response.data.meta.request_id ?? readResponseHeader(response.headers, "x-request-id"),
        correlationId: response.data.meta.correlation_id ?? readResponseHeader(response.headers, "x-correlation-id"),
        status: response.status,
      });
    }
    return response;
  },
  async (error: AxiosError) => {
    const status = error.response?.status;
    const config = error.config;

    if (status === 401 && config && !config.authRetried && !config.skipAuth) {
      try {
        const token = await authSessionManager.renewSession();
        config.authRetried = true;
        config.headers.set("Authorization", `Bearer ${token}`);
        return http(config);
      } catch {
        await authSessionManager.expireSession();
      }
    } else if (status === 401) {
      await authSessionManager.expireSession();
    }

    if (status === 403) {
      authSessionManager.markAccessDenied();
    }

    if (isApiErrorEnvelope(error.response?.data)) {
      throw new ValorApiError(error.response.data.error, {
        requestId: error.response.data.meta.request_id ?? readResponseHeader(error.response.headers, "x-request-id"),
        correlationId: error.response.data.meta.correlation_id ?? readResponseHeader(error.response.headers, "x-correlation-id"),
        status: error.response.status,
      });
    }

    throw new ValorApiError(networkErrorPayload(error), {
      requestId: readConfigHeader(error, "X-Request-ID"),
      correlationId: readConfigHeader(error, "X-Correlation-ID"),
      status: error.response?.status,
    });
  },
);
