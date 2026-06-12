import { create } from "zustand";
import { runCopilot } from "@/services/copilotService";
import { useInvestmentStore } from "@/store/investmentStore";
import { useMarketInsightStore } from "@/store/marketInsightStore";
import { useNegotiationStore } from "@/store/negotiationStore";
import { usePropertyContextStore } from "@/store/propertyContextStore";
import { useScenarioHistoryStore } from "@/store/scenarioHistoryStore";
import { useValuationStore } from "@/store/valuationStore";
import { useWhatIfStore } from "@/store/whatIfStore";
import type {
  CopilotConversationTurn,
  CopilotHumanContext,
  CopilotOrchestratorRequest,
  CopilotOrchestratorResponse,
  CopilotPlannedToolCall,
  CopilotSendMessageInput,
  CopilotToolInput,
} from "@/types/copilot";
import type { RentFairPriceRequest } from "@/types/valuation";

const egpFormatter = new Intl.NumberFormat("en-EG", { maximumFractionDigits: 0 });

function formatEgp(value?: number | null): string {
  if (typeof value !== "number" || !Number.isFinite(value)) return "Unavailable";
  return `EGP ${egpFormatter.format(value)}`;
}

function toError(error: unknown): Error {
  if (error instanceof Error) return error;
  return new Error("Unable to run the Copilot orchestrator.");
}

function turnId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) return crypto.randomUUID();
  return `copilot-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function compactUndefined(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(compactUndefined);
  if (!isRecord(value)) return value;
  return Object.fromEntries(
    Object.entries(value)
      .filter(([, entry]) => entry !== undefined)
      .map(([key, entry]) => [key, compactUndefined(entry)]),
  );
}

function stableRecord(value: unknown): Record<string, unknown> | null {
  const compacted = compactUndefined(value);
  return isRecord(compacted) && Object.keys(compacted).length > 0 ? compacted : null;
}

function latestValuationId(): string | null {
  const propertyContext = usePropertyContextStore.getState();
  const valuation = useValuationStore.getState();
  const whatIf = useWhatIfStore.getState().lastResponse;
  const negotiation = useNegotiationStore.getState().lastResponse;
  const investment = useInvestmentStore.getState().lastResponse;
  return (
    investment?.valuation_id ??
    negotiation?.valuation_id ??
    whatIf?.scenario_valuation_id ??
    whatIf?.base_valuation_id ??
    valuation.lastRequestId ??
    propertyContext.lastBridgeRequestId ??
    null
  );
}

function targetPrice(request: RentFairPriceRequest | null): number | null {
  if (typeof request?.target_price_egp === "number" && Number.isFinite(request.target_price_egp)) {
    return Math.max(1, Math.round(request.target_price_egp));
  }
  const result = useValuationStore.getState().lastResult;
  if (typeof result?.fair_price_egp === "number" && Number.isFinite(result.fair_price_egp)) {
    return Math.max(1, Math.round(result.fair_price_egp));
  }
  return null;
}

function latestScenarioModifications(): Record<string, unknown> | null {
  const request = useWhatIfStore.getState().lastRequest;
  return stableRecord(request?.modifications);
}

function currentScenarioId(): number | null {
  return useScenarioHistoryStore.getState().selectedScenario?.id ?? usePropertyContextStore.getState().activeScenarioId ?? null;
}

function buildToolInputs(): Partial<Record<CopilotPlannedToolCall, CopilotToolInput>> {
  const propertyContext = usePropertyContextStore.getState();
  const valuation = useValuationStore.getState();
  const whatIf = useWhatIfStore.getState();
  const market = useMarketInsightStore.getState();
  const workspaceId = propertyContext.activeWorkspaceId;
  const propertyId = propertyContext.activePropertyId;
  const scenarioId = currentScenarioId();
  const activeRequest = valuation.lastRequest ?? valuation.draft;

  if (typeof workspaceId !== "number") return {};

  const toolInputs: Partial<Record<CopilotPlannedToolCall, CopilotToolInput>> = {
    MARKET_INSIGHT_TOOL: {
      workspace_id: workspaceId,
      time_window: market.filters.time_window || "all",
      compound_name: market.filters.compound_name || null,
      h3_res9: market.filters.h3_res9 || null,
      property_type: market.filters.property_type || activeRequest.property_type || null,
    },
  };

  if (typeof propertyId === "number") {
    const valuationInput = {
      workspace_id: workspaceId,
      property_id: propertyId,
      scenario_id: scenarioId,
    };
    toolInputs.VALUATION_TOOL = valuationInput;
    toolInputs.COMPARABLES_TOOL = {
      ...valuationInput,
      valuation_id: latestValuationId(),
    };

    const askingPrice = targetPrice(activeRequest);
    if (askingPrice != null) {
      toolInputs.FAIRNESS_TOOL = {
        ...valuationInput,
        target_price_egp: askingPrice,
      };
      const modifications = latestScenarioModifications();
      toolInputs.NEGOTIATION_TOOL = {
        ...valuationInput,
        asking_price_egp: askingPrice,
        what_if_modifications: modifications,
      };
      toolInputs.INVESTMENT_TOOL = {
        ...valuationInput,
        asking_price_egp: askingPrice,
        what_if_modifications: modifications,
      };
    }

    if (whatIf.lastRequest?.modifications) {
      toolInputs.WHAT_IF_TOOL = {
        workspace_id: workspaceId,
        property_id: propertyId,
        scenario_id: whatIf.lastRequest.scenario_id ?? scenarioId,
        modifications: whatIf.lastRequest.modifications,
      };
    }
  }

  const valuationId = latestValuationId();
  if (valuationId) {
    toolInputs.EXPLAINABILITY_TOOL = {
      workspace_id: workspaceId,
      valuation_id: valuationId,
    };
  }

  return toolInputs;
}

function humanContext(response?: CopilotOrchestratorResponse): CopilotHumanContext {
  const propertyContext = usePropertyContextStore.getState();
  const valuation = useValuationStore.getState();
  const whatIf = useWhatIfStore.getState();
  const negotiation = useNegotiationStore.getState();
  const investment = useInvestmentStore.getState();
  const market = useMarketInsightStore.getState();
  const scenarios = useScenarioHistoryStore.getState();
  const request = valuation.lastRequest;
  const draft = valuation.draft;
  const valuationResult = valuation.lastResult;
  const location =
    request?.compound_name ||
    draft.compound_name ||
    request?.address ||
    draft.address ||
    valuationResult?.area?.name ||
    valuationResult?.area?.area_name ||
    "Active property";

  return {
    activeProperty:
      typeof propertyContext.activePropertyId === "number"
        ? `${request?.property_type ?? draft.property_type ?? "Property"} at ${location} (Property ${propertyContext.activePropertyId})`
        : "No backend property context is active",
    activeScenario:
      scenarios.selectedScenario?.name ??
      (typeof propertyContext.activeScenarioId === "number"
        ? `Scenario ${propertyContext.activeScenarioId}`
        : whatIf.lastResponse
          ? `Unsaved scenario ${formatEgp(whatIf.lastResponse.scenario_valuation)}`
          : "Base valuation"),
    latestValuation: valuationResult
      ? `${formatEgp(valuationResult.fair_price_egp)} fair price, ${valuationResult.confidence.label} confidence`
      : propertyContext.lastBridgeRequestId
        ? `Latest valuation ${propertyContext.lastBridgeRequestId}`
        : "No valuation result loaded",
    latestNegotiation: negotiation.lastResponse
      ? `${negotiation.lastResponse.negotiation_position}, offer band ${formatEgp(
          negotiation.lastResponse.recommended_offer_band.low,
        )} to ${formatEgp(negotiation.lastResponse.recommended_offer_band.high)}`
      : "No negotiation run loaded",
    latestInvestment: investment.lastResponse
      ? `${investment.lastResponse.investment_position}, gap ${formatEgp(investment.lastResponse.price_gap)}`
      : "No investment run loaded",
    latestMarketInsight: market.lastResponse
      ? `${market.lastResponse.valuation_volume} valuations, ${market.lastResponse.comparable_density.density_level} density`
      : "No market insight run loaded",
    relevantHistory: [
      ...scenarios.scenarios.slice(-3).map((scenario) => `Scenario: ${scenario.name}`),
      ...negotiation.runs.slice(-2).map((run) => `Negotiation: ${run.label}`),
      ...investment.runs.slice(-2).map((run) => `Investment: ${run.label}`),
      ...market.runs.slice(-2).map((run) => `Market: ${run.request.time_window ?? "all"}`),
    ].slice(-8),
    memoryId: response?.audit.memory_id,
    memoryStatus: response?.audit.memory_status,
  };
}

function backendMessage(message: string): string {
  const normalized = message.toLowerCase();
  const hasBuyQuestion = /\b(should\s+i\s+buy|buy\s+this\s+property|worth\s+buying)\b/.test(normalized);
  const hasInvestmentKeyword = /\b(invest|investment|opportunity|worth\s+buying|good\s+investment|buying\s+opportunity)\b/.test(
    normalized,
  );
  return hasBuyQuestion && !hasInvestmentKeyword ? `${message.trim()} Is this a good investment?` : message.trim();
}

interface CopilotState {
  conversation: CopilotConversationTurn[];
  activePropertyId: number | null;
  activeScenarioId: number | null;
  lastResponse: CopilotOrchestratorResponse | null;
  isLoading: boolean;
  error: Error | null;
  citations: CopilotOrchestratorResponse["citation_package"];
  memoryContext: CopilotHumanContext | null;
  sendMessage: (input: CopilotSendMessageInput) => Promise<CopilotOrchestratorResponse>;
  clearConversation: () => void;
  reset: () => void;
}

export const initialCopilotState = {
  conversation: [],
  activePropertyId: null,
  activeScenarioId: null,
  lastResponse: null,
  isLoading: false,
  error: null,
  citations: null,
  memoryContext: null,
};

export const useCopilotStore = create<CopilotState>((set) => ({
  ...initialCopilotState,
  sendMessage: async ({ message, brokerSessionId = null, signal }) => {
    const trimmed = message.trim();
    const propertyContext = usePropertyContextStore.getState();
    const workspaceId = propertyContext.activeWorkspaceId;
    if (typeof workspaceId !== "number") {
      const error = new Error("Open or prepare a property first so Copilot has an active workspace.");
      set({ error });
      throw error;
    }

    const now = new Date().toISOString();
    const userTurn: CopilotConversationTurn = {
      id: turnId(),
      role: "user",
      content: trimmed,
      createdAt: now,
    };
    const request: CopilotOrchestratorRequest = {
      workspace_id: workspaceId,
      scenario_id: currentScenarioId(),
      broker_session_id: brokerSessionId,
      message: backendMessage(trimmed),
      tool_inputs: buildToolInputs(),
    };

    set((state) => ({
      conversation: [...state.conversation, userTurn],
      activePropertyId: propertyContext.activePropertyId,
      activeScenarioId: currentScenarioId(),
      isLoading: true,
      error: null,
      memoryContext: humanContext(),
    }));

    try {
      const result = await runCopilot(request, signal);
      const assistantTurn: CopilotConversationTurn = {
        id: turnId(),
        role: "assistant",
        content:
          typeof result.data.response === "string"
            ? result.data.response
            : `Copilot returned ${result.data.delivery_mode.toLowerCase().replaceAll("_", " ")} for ${result.data.intent}.`,
        createdAt: new Date().toISOString(),
        response: result.data,
      };
      set((state) => ({
        conversation: [...state.conversation, assistantTurn],
        lastResponse: result.data,
        isLoading: false,
        error: null,
        citations: result.data.citation_package,
        memoryContext: humanContext(result.data),
      }));
      return result.data;
    } catch (error) {
      const mapped = toError(error);
      set({ isLoading: false, error: mapped });
      throw mapped;
    }
  },
  clearConversation: () => set({ conversation: [], lastResponse: null, citations: null, error: null }),
  reset: () => set(initialCopilotState),
}));
