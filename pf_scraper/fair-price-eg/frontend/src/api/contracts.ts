export interface ApiMeta {
  request_id?: string;
  correlation_id?: string;
  [key: string]: unknown;
}

export interface ApiErrorDetail {
  code: string;
  message: string;
  field?: string | null;
}

export interface ApiErrorPayload {
  code: string;
  message: string;
  details: ApiErrorDetail[];
}

export interface ApiSuccessEnvelope<TData> {
  success: true;
  data: TData;
  meta: ApiMeta;
}

export interface ApiErrorEnvelope {
  success: false;
  error: ApiErrorPayload;
  meta: ApiMeta;
}

export type ApiEnvelope<TData> = ApiSuccessEnvelope<TData> | ApiErrorEnvelope;

export class ValorApiError extends Error {
  readonly code: string;
  readonly details: ApiErrorDetail[];
  readonly requestId?: string;
  readonly correlationId?: string;
  readonly status?: number;

  constructor(payload: ApiErrorPayload, options: { requestId?: string; correlationId?: string; status?: number } = {}) {
    super(payload.message);
    this.name = "ValorApiError";
    this.code = payload.code;
    this.details = payload.details;
    this.requestId = options.requestId;
    this.correlationId = options.correlationId;
    this.status = options.status;
  }
}

export function isApiErrorEnvelope(value: unknown): value is ApiErrorEnvelope {
  return (
    typeof value === "object" &&
    value !== null &&
    "success" in value &&
    (value as { success?: unknown }).success === false &&
    "error" in value &&
    typeof (value as { error?: { code?: unknown } }).error?.code === "string"
  );
}

export function isApiSuccessEnvelope<TData>(value: unknown): value is ApiSuccessEnvelope<TData> {
  return (
    typeof value === "object" &&
    value !== null &&
    "success" in value &&
    (value as { success?: unknown }).success === true &&
    "data" in value &&
    "meta" in value
  );
}
