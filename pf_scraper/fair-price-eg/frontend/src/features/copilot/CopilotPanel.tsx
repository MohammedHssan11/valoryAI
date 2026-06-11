import * as React from "react";
import { AnimatePresence, motion } from "framer-motion";
import { BrainCircuit, Database, Loader2, SendHorizonal, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GlassPanel } from "@/components/ui/glass";
import { CitationViewer } from "@/features/copilot/CitationViewer";
import { ContextSummaryBar } from "@/features/copilot/ContextSummaryBar";
import { EvidenceDrawer } from "@/features/copilot/EvidenceDrawer";
import { ToolExecutionTimeline } from "@/features/copilot/ToolExecutionTimeline";
import { cn } from "@/lib/utils";
import { useCopilotStore } from "@/store/copilotStore";
import { useInvestmentStore } from "@/store/investmentStore";
import { useMarketInsightStore } from "@/store/marketInsightStore";
import { useNegotiationStore } from "@/store/negotiationStore";
import { usePropertyContextStore } from "@/store/propertyContextStore";
import { useValuationStore } from "@/store/valuationStore";
import { useWhatIfStore } from "@/store/whatIfStore";
import type {
  CopilotCitationPackage,
  CopilotFrontendPayload,
  CopilotFrontendToolOutput,
  CopilotOrchestratorResponse,
} from "@/types/copilot";

const egpFormatter = new Intl.NumberFormat("en-EG", { maximumFractionDigits: 0 });

function formatEgp(value?: number | null): string {
  if (typeof value !== "number" || !Number.isFinite(value)) return "Unavailable";
  return `EGP ${egpFormatter.format(value)}`;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function payloadFrom(response: CopilotOrchestratorResponse | null): CopilotFrontendPayload | null {
  return response && isRecord(response.response) ? (response.response as CopilotFrontendPayload) : null;
}

function citationsFrom(response: CopilotOrchestratorResponse | null): CopilotCitationPackage | null {
  const payload = payloadFrom(response);
  return response?.citation_package ?? payload?.citations ?? null;
}

function toolOutput(payload: CopilotFrontendPayload | null, toolName: string): CopilotFrontendToolOutput | null {
  return payload?.tool_outputs.find((output) => output.tool_name === toolName) ?? null;
}

function stringField(record: Record<string, unknown>, field: string): string | null {
  return typeof record[field] === "string" ? record[field] as string : null;
}

function numberField(record: Record<string, unknown>, field: string): number | null {
  return typeof record[field] === "number" ? record[field] as number : null;
}

function responseAnswer(response: CopilotOrchestratorResponse | null): string {
  if (!response) return "No Copilot response yet.";
  if (typeof response.response === "string") return response.response;

  const payload = payloadFrom(response);
  if (!payload) return "No composed payload was returned.";

  const investment = toolOutput(payload, "investment")?.payload;
  if (isRecord(investment)) {
    return stringField(investment, "investment_summary") ?? stringField(investment, "investment_position_reason") ?? "Investment evidence returned.";
  }

  const negotiation = toolOutput(payload, "negotiation")?.payload;
  if (isRecord(negotiation)) {
    const position = stringField(negotiation, "negotiation_position") ?? "Negotiation position";
    const reason = stringField(negotiation, "negotiation_position_reason") ?? "Evidence returned.";
    return `${position}: ${reason}`;
  }

  const market = toolOutput(payload, "market_insight")?.payload;
  if (isRecord(market)) return stringField(market, "market_summary") ?? "Market intelligence returned.";

  const whatIf = toolOutput(payload, "what_if")?.payload;
  if (isRecord(whatIf)) {
    return `Scenario value ${formatEgp(numberField(whatIf, "scenario_valuation"))}, delta ${formatEgp(numberField(whatIf, "delta_value"))}.`;
  }

  const valuation = toolOutput(payload, "valuation")?.payload;
  if (isRecord(valuation)) return `Fair price ${formatEgp(numberField(valuation, "fair_price"))}.`;

  if (payload.failed_tools.length) return "The orchestrator returned failures without successful evidence.";
  return `Structured evidence returned for ${response.intent}.`;
}

function confidenceLabel(payload: CopilotFrontendPayload | null): string {
  const output = payload?.tool_outputs.find((item) => isRecord(item.payload) && typeof item.payload.confidence_level === "string");
  if (output && isRecord(output.payload)) return String(output.payload.confidence_level);
  return payload?.composition_status ?? "Pending";
}

function toolSummary(output: CopilotFrontendToolOutput): string {
  if (!isRecord(output.payload)) return output.tool_name;
  if (output.tool_name === "valuation") return `Fair price ${formatEgp(numberField(output.payload, "fair_price"))}`;
  if (output.tool_name === "what_if") {
    return `Scenario ${formatEgp(numberField(output.payload, "scenario_valuation"))}, ${String(output.payload.fairness_status ?? "fairness pending")}`;
  }
  if (output.tool_name === "negotiation") {
    return `${String(output.payload.negotiation_position ?? "Position pending")} at ${formatEgp(numberField(output.payload, "asking_price"))}`;
  }
  if (output.tool_name === "investment") {
    return `${String(output.payload.investment_position ?? "Position pending")} at ${formatEgp(numberField(output.payload, "asking_price"))}`;
  }
  if (output.tool_name === "market_insight") {
    return `${String(output.payload.valuation_volume ?? 0)} valuations observed`;
  }
  return output.tool_name;
}

function suggestedQuestions(): string[] {
  const hasProperty = typeof usePropertyContextStore.getState().activePropertyId === "number";
  const hasScenario = Boolean(useWhatIfStore.getState().lastResponse);
  const hasNegotiation = Boolean(useNegotiationStore.getState().lastResponse);
  const hasInvestment = Boolean(useInvestmentStore.getState().lastResponse);
  const hasMarket = Boolean(useMarketInsightStore.getState().lastResponse);
  const hasValuation = Boolean(useValuationStore.getState().lastResult);

  const suggestions = [];
  if (hasProperty && hasValuation) suggestions.push("Should I buy this property?");
  if (hasProperty && hasValuation) suggestions.push("Is my asking price reasonable?");
  if (hasScenario) suggestions.push("Which scenario is strongest?");
  if (hasNegotiation) suggestions.push("What negotiation strategy should I use?");
  if (hasInvestment) suggestions.push("What evidence supports investing?");
  if (hasMarket) suggestions.push("What are the biggest market risks?");
  if (hasProperty && !hasMarket) suggestions.push("What market insight is available?");
  return suggestions.slice(0, 6);
}

export function CopilotPanel() {
  const {
    conversation,
    lastResponse,
    isLoading,
    error,
    memoryContext,
    sendMessage,
    clearConversation,
  } = useCopilotStore();
  const activeWorkspaceId = usePropertyContextStore((state) => state.activeWorkspaceId);
  const [message, setMessage] = React.useState("Should I buy this property?");
  const [evidenceOpen, setEvidenceOpen] = React.useState(false);
  const abortRef = React.useRef<AbortController | null>(null);
  const payload = payloadFrom(lastResponse);
  const citations = citationsFrom(lastResponse);
  const suggestions = suggestedQuestions();

  React.useEffect(
    () => () => {
      abortRef.current?.abort();
    },
    [],
  );

  const submit = React.useCallback(
    (event?: React.FormEvent) => {
      event?.preventDefault();
      const trimmed = message.trim();
      if (!trimmed || isLoading) return;
      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;
      void sendMessage({ message: trimmed, signal: controller.signal })
        .then(() => setEvidenceOpen(false))
        .finally(() => {
          if (abortRef.current === controller) abortRef.current = null;
        });
    },
    [isLoading, message, sendMessage],
  );

  const canAsk = typeof activeWorkspaceId === "number" && message.trim().length > 0 && !isLoading;

  return (
    <div className="grid h-full grid-rows-[auto_1fr_auto] gap-4">
      <div className="grid gap-4">
        <ContextSummaryBar context={memoryContext} />
        {activeWorkspaceId == null && (
          <GlassPanel className="border-secondary-fixed/20 bg-secondary-fixed/5 p-4">
            <p className="font-label-caps text-xs text-secondary-fixed">Property Context Pending</p>
            <p className="mt-1 text-sm text-on-surface-variant">Run a valuation before asking Copilot.</p>
          </GlassPanel>
        )}
      </div>

      <div className="min-h-0 overflow-y-auto pr-1">
        <div className="grid gap-4 pb-2">
          <GlassPanel className="grid gap-4 p-4">
            <div className="flex items-center justify-between gap-3 border-b border-white/5 pb-3">
              <div>
                <p className="font-label-caps text-xs text-primary-fixed-dim">Answer</p>
                <p className="mt-1 text-xs text-on-surface-variant">{lastResponse?.delivery_mode ?? "Awaiting request"}</p>
              </div>
              <BrainCircuit className={cn("h-5 w-5", isLoading ? "animate-pulse text-tertiary-fixed-dim" : "text-primary-fixed-dim")} />
            </div>
            <p className="text-sm leading-6 text-on-surface">{responseAnswer(lastResponse)}</p>
            <div className="grid gap-2 sm:grid-cols-3">
              <div className="rounded-lg border border-white/10 bg-surface/20 p-3">
                <p className="font-label-caps text-[10px] text-outline">Intent</p>
                <p className="mt-1 truncate font-data-tabular text-xs text-on-surface">{lastResponse?.intent ?? "Pending"}</p>
              </div>
              <div className="rounded-lg border border-white/10 bg-surface/20 p-3">
                <p className="font-label-caps text-[10px] text-outline">Confidence</p>
                <p className="mt-1 truncate font-data-tabular text-xs text-on-surface">{confidenceLabel(payload)}</p>
              </div>
              <div className="rounded-lg border border-white/10 bg-surface/20 p-3">
                <p className="font-label-caps text-[10px] text-outline">Memory</p>
                <p className="mt-1 truncate font-data-tabular text-xs text-on-surface">{lastResponse?.audit.memory_status ?? "Pending"}</p>
              </div>
            </div>
          </GlassPanel>

          <GlassPanel className="grid gap-3 p-4">
            <div className="flex items-center justify-between gap-3 border-b border-white/5 pb-3">
              <p className="font-label-caps text-xs text-primary-fixed-dim">Reasoning Summary</p>
              <ShieldCheck className="h-4 w-4 text-primary-fixed-dim" />
            </div>
            {payload?.tool_outputs.length ? (
              <div className="grid gap-2">
                {payload.tool_outputs.map((output) => (
                  <div key={`${output.planned_tool}-${output.ordering_metadata.order_index}`} className="rounded-lg border border-white/10 bg-surface/20 p-3">
                    <p className="font-data-tabular text-sm text-on-surface">{toolSummary(output)}</p>
                    <p className="mt-1 text-xs text-on-surface-variant">{output.planned_tool}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-on-surface-variant">No successful tool summary returned.</p>
            )}
          </GlassPanel>

          <ToolExecutionTimeline payload={payload} />
          <CitationViewer citations={citations} />

          <div className="flex flex-wrap gap-2">
            <Button type="button" variant="ghost" size="sm" disabled={!payload} onClick={() => setEvidenceOpen(true)}>
              <Database className="h-4 w-4" />
              Evidence
            </Button>
            <Button type="button" variant="ghost" size="sm" disabled={conversation.length === 0 || isLoading} onClick={clearConversation}>
              Clear
            </Button>
          </div>

          {conversation.length > 0 && (
            <GlassPanel className="grid gap-3 p-4">
              <p className="font-label-caps text-xs text-primary-fixed-dim">Conversation</p>
              {conversation.slice(-4).map((turn) => (
                <div
                  key={turn.id}
                  className={cn(
                    "rounded-lg border p-3 text-sm leading-6",
                    turn.role === "user"
                      ? "border-primary-fixed-dim/15 bg-primary-fixed-dim/5 text-on-surface"
                      : "border-white/10 bg-surface/20 text-on-surface-variant",
                  )}
                >
                  {turn.content}
                </div>
              ))}
            </GlassPanel>
          )}

          {error && (
            <GlassPanel className="border-error/25 bg-error/5 p-4">
              <p className="font-label-caps text-xs text-error">Copilot Error</p>
              <p className="mt-1 text-sm text-on-surface-variant">{error.message}</p>
            </GlassPanel>
          )}
        </div>
      </div>

      <form className="grid gap-3 border-t border-white/5 pt-4" onSubmit={submit}>
        {suggestions.length > 0 && (
          <div className="flex gap-2 overflow-x-auto pb-1">
            {suggestions.map((suggestion) => (
              <button
                key={suggestion}
                type="button"
                onClick={() => setMessage(suggestion)}
                className="shrink-0 rounded-full border border-white/10 bg-surface/30 px-3 py-1.5 text-left text-[11px] leading-snug text-on-surface-variant transition-colors hover:border-primary-fixed-dim/30 hover:text-primary-fixed-dim"
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}
        <div className="flex items-end gap-2">
          <textarea
            value={message}
            onChange={(event) => setMessage(event.currentTarget.value)}
            rows={2}
            className="min-h-16 flex-1 resize-none rounded-lg border border-white/10 bg-surface/40 px-3 py-2 text-sm leading-5 text-on-surface outline-none transition-colors placeholder:text-outline focus:border-primary-fixed-dim/50"
            placeholder="Ask about this property"
            disabled={isLoading}
          />
          <Button type="submit" variant="holo" disabled={!canAsk} aria-label="Ask Copilot">
            <AnimatePresence mode="wait" initial={false}>
              {isLoading ? (
                <motion.span key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                  <Loader2 className="h-4 w-4 animate-spin" />
                </motion.span>
              ) : (
                <motion.span key="send" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                  <SendHorizonal className="h-4 w-4" />
                </motion.span>
              )}
            </AnimatePresence>
          </Button>
        </div>
      </form>

      <EvidenceDrawer isOpen={evidenceOpen} payload={payload} onClose={() => setEvidenceOpen(false)} />
    </div>
  );
}
