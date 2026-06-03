import { create } from "zustand";

interface IntelligenceSessionState {
  sessionId: string;
  startedAt: number;
  resetSession: () => void;
}

function createSessionId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `session-${Date.now()}`;
}

export const useIntelligenceSessionStore = create<IntelligenceSessionState>((set) => ({
  sessionId: createSessionId(),
  startedAt: Date.now(),
  resetSession: () => set({ sessionId: createSessionId(), startedAt: Date.now() }),
}));

