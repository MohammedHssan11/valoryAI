import { describe, expect, it } from "vitest";
import { isApiErrorEnvelope, isApiSuccessEnvelope, ValorApiError } from "./contracts";

describe("API envelope contracts", () => {
  it("recognizes success envelopes without weakening DTO shape", () => {
    const envelope = {
      success: true,
      data: { fair_price_egp: 90000 },
      meta: { request_id: "req-1" },
    };

    expect(isApiSuccessEnvelope(envelope)).toBe(true);
    expect(isApiErrorEnvelope(envelope)).toBe(false);
  });

  it("recognizes error envelopes and preserves request metadata", () => {
    const envelope = {
      success: false,
      error: {
        code: "INVALID_SIZE",
        message: "Request validation failed",
        details: [{ code: "INVALID_SIZE", message: "Input should be greater than 0", field: "size_sqm" }],
      },
      meta: { request_id: "req-2" },
    };

    expect(isApiErrorEnvelope(envelope)).toBe(true);
    const error = new ValorApiError(envelope.error, { requestId: envelope.meta.request_id, status: 422 });
    expect(error.code).toBe("INVALID_SIZE");
    expect(error.requestId).toBe("req-2");
    expect(error.status).toBe(422);
  });
});
