import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Activity,
  BrainCircuit,
  CheckCircle2,
  Circle,
  CircleDot,
  GitBranch,
  Loader2,
  MessageSquareText,
  Play,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { ValorApiError } from "@/api/contracts";
import { confidenceFillTransition, premiumEase, revealItem, stagedReveal } from "@/animations/motion";
import { AiOrb, type OrbState } from "@/components/intelligence/AiOrb";
import { Button } from "@/components/ui/button";
import { GlassCard, GlassPanel } from "@/components/ui/glass";
import { cn } from "@/lib/utils";
import { requestBrokerReason, streamBrokerReason } from "@/services/brokerService";
import { useAiContinuityStore } from "@/store/aiContinuityStore";
import { useBrokerStore } from "@/store/brokerStore";
import { useIntelligenceSessionStore } from "@/store/intelligenceSessionStore";
import { useValuationStore } from "@/store/valuationStore";
import type {
  BrokerComparableEvidence,
  BrokerOrchestrationResponse,
  BrokerReasonRequest,
  BrokerStage,
  BrokerStageEvent,
} from "@/types/broker";
import type { ComparableItem, RentFairPriceData } from "@/types/valuation";

const DEFAULT_PROMPT = "Explain the current valuation, comparable evidence, confidence, and investor risk as an institutional broker.";

const stageOrder: BrokerStage[] = [
  "classify_intent",
  "build_reasoning_plan",
  "execute_tools",
  "assemble_context",
  "generate_narration",
  "validate_grounding",
  "finalize_response",
];

const stageCopy: Record<BrokerStage, { label: string; detail: string }> = {
  classify_intent: {
    label: "Broker Intent Classified",
    detail: "Analytical request routed",
  },
  build_reasoning_plan: {
    label: "Institutional Plan Built",
    detail: "Evidence requirements resolved",
  },
  execute_tools: {
    label: "Inspecting Comparable Clusters",
    detail: "Valuation tools executing",
  },
  assemble_context: {
    label: "District Intelligence Resolved",
    detail: "Context and evidence assembled",
  },
  generate_narration: {
    label: "Generating Institutional Explanation",
    detail: "Governed narration composing",
  },
  validate_grounding: {
    label: "Validating Confidence Metrics",
    detail: "Grounding checks active",
  },
  finalize_response: {
    label: "Broker Output Finalized",
    detail: "Governance layer completed",
  },
  intent_analysis: {
    label: "Intent Analysis",
    detail: "Broker context reviewed",
  },
  tool_selection: {
    label: "Tool Selection",
    detail: "Analytical tools selected",
  },
  evidence_gathering: {
    label: "Evidence Gathering",
    detail: "Deterministic sources queried",
  },
  context_assembly: {
    label: "Context Assembly",
    detail: "Evidence packaged",
  },
  response_generation: {
    label: "Response Generation",
    detail: "Broker response drafting",
  },
  response_validation: {
    label: "Response Validation",
    detail: "Grounding reviewed",
  },
};

const egpFormatter = new Intl.NumberFormat("en-EG", {
  maximumFractionDigits: 0,
});

function formatEgp(value?: number | null): string {
  if (value == null || !Number.isFinite(value)) return "EGP --";
  return `EGP ${egpFormatter.format(value)}`;
}

function formatPercent(value?: number | null): string {
  if (value == null || !Number.isFinite(value)) return "--";
  return `${Math.round(value * 100)}%`;
}

function formatDistance(value?: number | null): string {
  if (value == null) return "Distance n/a";
  if (value < 1000) return `${Math.round(value)}m`;
  return `${(value / 1000).toFixed(1)}km`;
}

function readAreaName(area?: Record<string, unknown> | null): string {
  if (!area) return "District pending";
  const name = area.name ?? area.area_name ?? area.active_district;
  return typeof name === "string" && name.trim().length > 0 ? name : "District pending";
}

function latestStageEvent(events: BrokerStageEvent[], stage: BrokerStage): BrokerStageEvent | undefined {
  return [...events].reverse().find((event) => event.stage === stage);
}

function stageStatus(events: BrokerStageEvent[], stage: BrokerStage, isStreaming: boolean): "pending" | "active" | "complete" | "failed" {
  const stageEvents = events.filter((event) => event.stage === stage);
  if (stageEvents.some((event) => event.event_type === "stage_failed")) return "failed";
  if (stageEvents.some((event) => event.event_type === "stage_completed")) return "complete";
  if (stageEvents.some((event) => event.event_type === "stage_started")) return "active";
  if (isStreaming && events.length === 0 && stage === "classify_intent") return "active";
  return "pending";
}

function mergeEvents(events: BrokerStageEvent[], next: BrokerStageEvent): BrokerStageEvent[] {
  if (events.some((event) => event.event_id === next.event_id)) {
    return events.map((event) => (event.event_id === next.event_id ? next : event));
  }
  return [...events, next];
}

function mergeEventList(events: BrokerStageEvent[], incoming: BrokerStageEvent[]): BrokerStageEvent[] {
  return incoming.reduce((merged, event) => mergeEvents(merged, event), events);
}

function comparableFromValuation(comparable: ComparableItem): BrokerComparableEvidence {
  return {
    evidence_id: comparable.listing_id,
    listing_id: comparable.listing_id,
    price_egp: comparable.price_egp,
    size_sqm: comparable.size_sqm,
    bedrooms: comparable.bedrooms,
    bathrooms: comparable.bathrooms,
    area_name: comparable.area_name,
    distance_m: comparable.dist_m,
    age_days: comparable.age_days,
    weight: comparable.weight,
    reason_code: comparable.reason_code,
  };
}

function resultComparables(response: BrokerOrchestrationResponse | null, valuation: RentFairPriceData | null): BrokerComparableEvidence[] {
  if (response?.context.comparable_evidence.length) return response.context.comparable_evidence;
  return valuation?.top_comps.slice(0, 4).map(comparableFromValuation) ?? [];
}

interface BrokerMetrics {
  fairPrice?: number;
  rangeLow?: number;
  rangeHigh?: number;
  flag?: string;
  tier?: number;
  compsCount?: number;
  confidenceScore?: number;
  confidenceLabel?: string;
  areaName: string;
}

function buildMetrics(response: BrokerOrchestrationResponse | null, valuation: RentFairPriceData | null): BrokerMetrics {
  const authoritative = response?.response.authoritative_values;
  const summary = response?.context.valuation_summary;

  return {
    fairPrice: authoritative?.fair_price_egp ?? summary?.fair_price_egp ?? valuation?.fair_price_egp,
    rangeLow: authoritative?.range_low_egp ?? summary?.range_low_egp ?? valuation?.range_low_egp,
    rangeHigh: authoritative?.range_high_egp ?? summary?.range_high_egp ?? valuation?.range_high_egp,
    flag: authoritative?.flag ?? summary?.flag ?? valuation?.flag,
    tier: authoritative?.tier_used ?? summary?.tier_used ?? valuation?.tier_used,
    compsCount: authoritative?.comps_count ?? summary?.comps_count ?? valuation?.comps_count,
    confidenceScore: authoritative?.confidence_score ?? summary?.confidence_score ?? valuation?.confidence.score,
    confidenceLabel: authoritative?.confidence_label ?? summary?.confidence_label ?? valuation?.confidence.label,
    areaName: readAreaName(summary?.area ?? valuation?.area),
  };
}

function spreadRatio(metrics: BrokerMetrics): number | null {
  if (!metrics.fairPrice || !metrics.rangeLow || !metrics.rangeHigh) return null;
  return (metrics.rangeHigh - metrics.rangeLow) / metrics.fairPrice;
}

function errorMessage(error: unknown): string {
  if (error instanceof ValorApiError) return error.message;
  if (error instanceof Error) return error.message;
  return "Broker reasoning could not be completed.";
}

interface PipelineProps {
  events: BrokerStageEvent[];
  isStreaming: boolean;
}

function ReasoningPipeline({ events, isStreaming }: PipelineProps) {
  return (
    <GlassCard floating className="grid gap-5 p-5">
      <div className="flex items-center justify-between gap-4 border-b border-white/5 pb-3">
        <div>
          <p className="font-label-caps text-xs text-primary-fixed-dim">Live Reasoning Pipeline</p>
          <p className="mt-1 text-sm text-on-surface-variant">Broker trace telemetry</p>
        </div>
        <Activity className={cn("h-5 w-5", isStreaming ? "text-tertiary-fixed-dim" : "text-outline")} />
      </div>

      <div className="grid gap-4">
        {stageOrder.map((stage, index) => {
          const status = stageStatus(events, stage, isStreaming);
          const event = latestStageEvent(events, stage);

          return (
            <motion.div
              key={stage}
              variants={revealItem}
              className="grid grid-cols-[28px_1fr] gap-3"
            >
              <div className="flex flex-col items-center">
                <motion.span
                  layout
                  className={cn(
                    "flex h-7 w-7 items-center justify-center rounded-full border transition-all duration-700",
                    status === "complete" && "border-primary-fixed-dim/50 bg-primary-fixed-dim/10 text-primary-fixed-dim",
                    status === "active" && "border-tertiary-fixed-dim/60 bg-tertiary-fixed-dim/10 text-tertiary-fixed-dim shadow-[0_0_14px_rgba(78,222,163,0.18)]",
                    status === "failed" && "border-error/60 bg-error/10 text-error",
                    status === "pending" && "border-white/10 text-outline",
                  )}
                >
                  {status === "complete" ? (
                    <CheckCircle2 className="h-4 w-4" />
                  ) : status === "active" ? (
                    <CircleDot className="h-4 w-4" />
                  ) : (
                    <Circle className="h-4 w-4" />
                  )}
                </motion.span>
                {index < stageOrder.length - 1 && <span className="mt-2 h-8 w-px bg-white/10" />}
              </div>

              <div className="min-w-0 pb-3">
                <div className="flex items-start justify-between gap-3">
                  <motion.p
                    layout
                    className={cn(
                      "font-data-tabular text-sm transition-colors duration-700",
                      status === "pending" ? "text-on-surface-variant" : "text-on-surface",
                    )}
                  >
                    {stageCopy[stage].label}
                  </motion.p>
                  <AnimatePresence>
                    {event?.elapsed_ms != null && (
                      <motion.span
                        initial={{ opacity: 0, filter: "blur(4px)" }}
                        animate={{ opacity: 1, filter: "blur(0px)" }}
                        className="shrink-0 font-data-tabular text-[11px] text-outline"
                      >
                        {Math.round(event.elapsed_ms)}ms
                      </motion.span>
                    )}
                  </AnimatePresence>
                </div>
                <motion.p layout className="mt-1 truncate text-xs text-outline transition-colors duration-700">
                  {event?.message ?? stageCopy[stage].detail}
                </motion.p>
              </div>
            </motion.div>
          );
        })}
      </div>
    </GlassCard>
  );
}

interface ProjectionProps {
  metrics: BrokerMetrics;
  hasValuation: boolean;
}

function ValuationProjection({ metrics, hasValuation }: ProjectionProps) {
  const score = metrics.confidenceScore ?? 0;

  return (
    <GlassCard className="relative overflow-hidden p-6">
      <div className="absolute right-0 top-0 h-40 w-40 rounded-full bg-primary-fixed-dim/5 blur-3xl" />
      <div className="relative flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="font-label-caps text-xs text-primary-fixed-dim">Projected Valuation</p>
          <h2
            className={cn(
              "mt-3 break-words font-display-lg text-primary drop-shadow-[0_0_14px_rgba(0,219,231,0.16)]",
              hasValuation ? "text-4xl md:text-5xl" : "text-3xl md:text-4xl",
            )}
          >
            {hasValuation ? formatEgp(metrics.fairPrice) : "Context Pending"}
          </h2>
          <p className="mt-2 font-data-tabular text-sm text-on-surface-variant">
            {hasValuation ? `${formatEgp(metrics.rangeLow)} - ${formatEgp(metrics.rangeHigh)}` : "No deterministic valuation loaded"}
          </p>
        </div>

        <div className="flex h-24 w-24 shrink-0 items-center justify-center rounded-full border border-primary-fixed-dim/15 bg-surface-container-low/50">
          <div className="relative flex h-20 w-20 items-center justify-center rounded-full" style={{ background: `conic-gradient(rgba(0,219,231,0.82) ${Math.round(score * 100)}%, rgba(255,255,255,0.08) 0)` }}>
            <div className="absolute inset-1 rounded-full bg-surface-container-lowest" />
            <span className="relative z-10 font-data-tabular text-lg text-primary">{hasValuation ? formatPercent(score) : "--"}</span>
          </div>
        </div>
      </div>

      <div className="relative mt-6 grid gap-3 border-t border-white/5 pt-5 md:grid-cols-3">
        <div>
          <p className="font-label-caps text-[10px] text-outline">District</p>
          <p className="mt-1 truncate text-sm text-on-surface">{metrics.areaName}</p>
        </div>
        <div>
          <p className="font-label-caps text-[10px] text-outline">Confidence</p>
          <p className={cn(
            "mt-1 font-data-tabular text-sm",
            score < 0.6 ? "text-error" : score < 0.8 ? "text-secondary-fixed" : "text-tertiary-fixed-dim"
          )}>
            {metrics.confidenceLabel ?? "--"}
          </p>
        </div>
        <div>
          <p className="font-label-caps text-[10px] text-outline">Price State</p>
          <p className="mt-1 font-data-tabular text-sm text-secondary-fixed">{metrics.flag ?? "--"}</p>
        </div>
      </div>
    </GlassCard>
  );
}

interface EvidenceProps {
  comparables: BrokerComparableEvidence[];
  hasValuation?: boolean;
}

function EvidenceCards({ comparables, hasValuation }: EvidenceProps) {
  return (
    <GlassCard floating className="grid gap-4 p-5">
      <div className="flex items-center justify-between border-b border-white/5 pb-3">
        <div>
          <p className="font-label-caps text-xs text-primary-fixed-dim">Comparable Evidence</p>
          <p className="mt-1 text-sm text-on-surface-variant">{comparables.length} deterministic references</p>
        </div>
        <GitBranch className="h-5 w-5 text-primary-fixed-dim" />
      </div>

      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        {comparables.length === 0 ? (
          <GlassPanel className="p-4 md:col-span-2 xl:col-span-4">
            <p className="text-sm text-on-surface-variant">
              {hasValuation 
                ? "No direct comparable evidence found in this district. Valuation relies on broader market signals." 
                : "Comparable evidence appears after a valuation-backed broker run."}
            </p>
          </GlassPanel>
        ) : (
          comparables.slice(0, 4).map((comparable) => (
            <GlassPanel key={comparable.evidence_id} className="h-full p-4">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="truncate font-data-tabular text-sm font-semibold text-on-surface">
                    {comparable.area_name ?? comparable.listing_id}
                  </p>
                  <p className="mt-1 truncate text-xs text-outline">{comparable.reason_code ?? "Comparable evidence"}</p>
                </div>
                <span className="shrink-0 rounded-md border border-primary-fixed-dim/20 bg-primary-fixed-dim/5 px-2 py-1 font-data-tabular text-[11px] text-primary-fixed-dim">
                  {formatPercent(comparable.weight)}
                </span>
              </div>

              <div className="mt-4 grid grid-cols-2 gap-3 border-t border-white/5 pt-3">
                <div>
                  <p className="font-label-caps text-[10px] text-outline">Rent</p>
                  <p className="mt-1 font-data-tabular text-sm text-on-surface">{formatEgp(comparable.price_egp)}</p>
                </div>
                <div>
                  <p className="font-label-caps text-[10px] text-outline">Range</p>
                  <p className="mt-1 font-data-tabular text-sm text-on-surface">{formatDistance(comparable.distance_m)}</p>
                </div>
              </div>
            </GlassPanel>
          ))
        )}
      </div>
    </GlassCard>
  );
}

interface IntelligenceWidgetsProps {
  metrics: BrokerMetrics;
  response: BrokerOrchestrationResponse | null;
}

function IntelligenceWidgets({ metrics, response }: IntelligenceWidgetsProps) {
  const spread = spreadRatio(metrics);
  const widgets = [
    {
      label: "Evidence Depth",
      value: metrics.compsCount != null ? `${metrics.compsCount}` : "--",
      meta: "retained comps",
      tone: metrics.compsCount === 0 ? "text-error" : "text-primary",
    },
    {
      label: "Tier Strength",
      value: metrics.tier != null ? `T${metrics.tier}` : "--",
      meta: "retrieval tier",
      tone: "text-secondary-fixed",
    },
    {
      label: "Range Spread",
      value: spread != null ? formatPercent(spread) : "--",
      meta: "low to high",
      tone: "text-tertiary-fixed-dim",
    },
    {
      label: "Grounding",
      value: response?.grounding.status.toUpperCase() ?? "--",
      meta: response?.degraded_mode ? "degraded mode" : "governed output",
      tone: response?.grounding.status === "failed" ? "text-error" : "text-primary-fixed-dim",
    },
  ];

  return (
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
      {widgets.map((widget) => (
        <GlassPanel key={widget.label} className="relative overflow-hidden p-4">
          <div className="absolute left-0 top-0 h-full w-px bg-primary-fixed-dim/40" />
          <p className="font-label-caps text-[10px] text-outline">{widget.label}</p>
          <p className={cn("mt-2 font-headline-lg-mobile", widget.tone)}>{widget.value}</p>
          <p className="mt-1 text-xs text-on-surface-variant">{widget.meta}</p>
        </GlassPanel>
      ))}
    </div>
  );
}

interface NarrativeProps {
  response: BrokerOrchestrationResponse | null;
  partialNarration: string;
  latestMessage?: string;
  isStreaming: boolean;
  error?: string | null;
}

function BrokerNarrative({ response, partialNarration, latestMessage, isStreaming, error }: NarrativeProps) {
  const sections = response ? [
    ["Valuation Interpretation", response.response.valuation_interpretation, Activity],
    ["Comparable Reasoning", response.response.comparable_reasoning, GitBranch],
    ["District Insights", response.response.district_insights, BrainCircuit],
    ["Confidence Explanation", response.response.confidence_explanation, Sparkles],
  ] as const : [];

  return (
    <AnimatePresence mode="wait">
      {!response ? (
        <motion.div key="streaming" initial={{ opacity: 0, filter: "blur(8px)" }} animate={{ opacity: 1, filter: "blur(0px)" }} exit={{ opacity: 0, filter: "blur(8px)" }} transition={{ duration: 0.8, ease: premiumEase }}>
          <GlassCard className="grid min-h-[320px] content-center gap-4 p-6">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full border border-primary-fixed-dim/20 bg-primary-fixed-dim/5">
              {isStreaming ? <Loader2 className="h-6 w-6 animate-spin text-primary-fixed-dim" /> : <BrainCircuit className="h-6 w-6 text-primary-fixed-dim" />}
            </div>
            <div className="mx-auto max-w-2xl text-center">
              <p className="font-label-caps text-xs text-primary-fixed-dim">
                {isStreaming ? "Broker Intelligence Active" : "Broker Intelligence Terminal"}
              </p>
              <motion.p layout className="mt-3 text-sm leading-6 text-on-surface-variant transition-colors duration-500">
                {partialNarration || latestMessage || (error ? "Broker pipeline failed. Awaiting stable orchestration context." : "Awaiting deterministic evidence and valuation context to begin analysis.")}
              </motion.p>
            </div>
          </GlassCard>
        </motion.div>
      ) : (
        <motion.div key="final" initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, ease: premiumEase, staggerChildren: 0.1 }}>
          <GlassCard className="grid gap-6 p-6">
            <motion.div variants={revealItem} className="flex items-start justify-between gap-4 border-b border-white/5 pb-5">
              <div>
                <p className="font-label-caps text-xs text-primary-fixed-dim">Institutional Explanation</p>
                <h2 className="mt-2 font-headline-lg-mobile text-on-surface md:font-headline-lg">{response.response.executive_summary}</h2>
              </div>
              <div className="hidden rounded-full border border-tertiary-fixed-dim/20 bg-tertiary-fixed-dim/5 px-3 py-1 font-label-caps text-[10px] text-tertiary-fixed-dim sm:block">
                {response.intent.replaceAll("_", " ")}
              </div>
            </motion.div>

            <div className="grid gap-4 lg:grid-cols-2">
              {sections.map(([label, copy, Icon]) => (
                <motion.div key={label} variants={revealItem}>
                  <GlassPanel className="h-full p-4">
                    <div className="flex items-center gap-2">
                      <Icon className="h-3.5 w-3.5 text-primary-fixed-dim" />
                      <p className="font-label-caps text-[10px] text-outline">{label}</p>
                    </div>
                    <p className="mt-3 text-sm leading-6 text-on-surface-variant">{copy}</p>
                  </GlassPanel>
                </motion.div>
              ))}
            </div>

            {response.response.opportunity_risk_notes.length > 0 && (
              <motion.div variants={revealItem}>
                <GlassPanel className="p-4">
                  <div className="mb-3 flex items-center gap-2">
                    <ShieldCheck className="h-4 w-4 text-tertiary-fixed-dim" />
                    <p className="font-label-caps text-[10px] text-tertiary-fixed-dim">Opportunity And Risk Notes</p>
                  </div>
                  <div className="grid gap-2">
                    {response.response.opportunity_risk_notes.map((note, index) => (
                      <p key={`${note}-${index}`} className="text-sm leading-6 text-on-surface-variant">
                        {note}
                      </p>
                    ))}
                  </div>
                </GlassPanel>
              </motion.div>
            )}

            <motion.div variants={revealItem} className="border-t border-white/5 pt-4">
              <p className="font-label-caps text-[10px] text-outline">Analytical Conclusion</p>
              <p className="mt-2 text-sm leading-6 text-on-surface">{response.response.analytical_conclusion}</p>
            </motion.div>
          </GlassCard>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

interface CommandConsoleProps {
  message: string;
  isStreaming: boolean;
  hasValuation: boolean;
  error: string | null;
  onChange: (value: string) => void;
  onSubmit: () => void;
  onCancel: () => void;
}

function CommandConsole({ message, isStreaming, hasValuation, error, onChange, onSubmit, onCancel }: CommandConsoleProps) {
  const scenarioSeeds = [
    "Explain the confidence score, comparable variance, and pricing constraints.",
    "Assess downside risk and market signals for this asset.",
    "Provide an institutional summary of the deterministic valuation."
  ];

  return (
    <GlassCard floating className="p-4">
      <form
        className="grid gap-4"
        onSubmit={(event) => {
          event.preventDefault();
          onSubmit();
        }}
      >
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-white/5 pb-3">
          <div className="flex items-center gap-2">
            <MessageSquareText className="h-4 w-4 text-primary-fixed-dim" />
            <span className="font-label-caps text-xs text-primary-fixed-dim">Broker Command</span>
          </div>
          <span
            className={cn(
              "rounded-full border px-3 py-1 font-label-caps text-[10px]",
              hasValuation
                ? "border-tertiary-fixed-dim/20 bg-tertiary-fixed-dim/5 text-tertiary-fixed-dim"
                : "border-secondary-fixed/20 bg-secondary-fixed/5 text-secondary-fixed",
            )}
          >
            {hasValuation ? "Valuation Context Loaded" : "General Context"}
          </span>
        </div>

        <textarea
          value={message}
          onChange={(event) => onChange(event.currentTarget.value)}
          rows={3}
          className="min-h-24 w-full resize-none rounded-lg border border-white/10 bg-surface/40 px-4 py-3 text-sm leading-6 text-on-surface outline-none transition-colors placeholder:text-outline focus:border-primary-fixed-dim/50"
          placeholder="Ask for comparable logic, confidence drivers, district signals, or investor risk."
          disabled={isStreaming}
        />

        <div className="flex flex-wrap gap-2">
          {scenarioSeeds.map((seed) => (
            <button
              key={seed}
              type="button"
              disabled={isStreaming}
              onClick={() => onChange(seed)}
              className="rounded-full border border-white/5 bg-white/5 px-3 py-1.5 text-left text-[11px] leading-snug text-on-surface-variant transition-colors hover:bg-white/10 hover:text-on-surface disabled:opacity-50"
            >
              {seed}
            </button>
          ))}
        </div>

        {error && (
          <GlassPanel className="border-error/20 bg-error/5 p-3">
            <p className="text-sm text-error">{error}</p>
          </GlassPanel>
        )}

        <div className="flex flex-col gap-3 sm:flex-row sm:justify-end">
          {isStreaming && (
            <Button type="button" variant="ghost" onClick={onCancel}>
              Cancel
            </Button>
          )}
          <Button type="submit" variant="holo" disabled={isStreaming || message.trim().length === 0}>
            {isStreaming ? <Loader2 className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
            Stream Reasoning
          </Button>
        </div>
      </form>
    </GlassCard>
  );
}

export function BrokerScreen() {
  const { activeValuation, setActiveValuation, brokerContext, setBrokerContext } = useBrokerStore();
  const { draft, lastResult } = useValuationStore();
  const { sessionId } = useIntelligenceSessionStore();
  const { setOrbState, pushEvent } = useAiContinuityStore();
  const valuation = activeValuation ?? lastResult;
  const [events, setEvents] = React.useState<BrokerStageEvent[]>(brokerContext?.events ?? []);
  const [response, setResponse] = React.useState<BrokerOrchestrationResponse | null>(brokerContext?.response ?? null);
  const [partialNarration, setPartialNarration] = React.useState(brokerContext?.partialNarration ?? "");
  const [message, setMessage] = React.useState(brokerContext?.message ?? DEFAULT_PROMPT);
  const [isStreaming, setIsStreaming] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const abortRef = React.useRef<AbortController | null>(null);
  const currentStreamRunId = React.useRef<string | null>(null);
  const processedEventIds = React.useRef<Set<string>>(new Set());
  const latestStateRef = React.useRef({ events, response, partialNarration, message });
  latestStateRef.current = { events, response, partialNarration, message };

  React.useEffect(() => {
    if (!activeValuation && lastResult) {
      setActiveValuation(lastResult);
    }
  }, [activeValuation, lastResult, setActiveValuation]);

  React.useEffect(() => {
    return () => {
      abortRef.current?.abort();
      setBrokerContext(latestStateRef.current);
    };
  }, [setBrokerContext]);

  const metrics = React.useMemo(() => buildMetrics(response, valuation), [response, valuation]);
  const comparables = React.useMemo(() => resultComparables(response, valuation), [response, valuation]);
  const latestMessage = events.at(-1)?.message;
  const orbState: OrbState = isStreaming ? "analyzing" : response ? "responding" : valuation ? "thinking" : "idle";

  const buildRequest = React.useCallback((): BrokerReasonRequest => ({
    session_id: sessionId,
    message: message.trim() || DEFAULT_PROMPT,
    valuation_request: valuation ? draft : undefined,
  }), [draft, message, sessionId, valuation]);

  const cancelStream = React.useCallback(() => {
    abortRef.current?.abort();
    abortRef.current = null;
    setIsStreaming(false);
    setOrbState("idle");
    pushEvent("Broker reasoning cancelled");
    setPartialNarration((current) => current ? current + "\n\n[Broker Interruption: Pipeline Aborted]" : "");
  }, [pushEvent, setOrbState]);

  const runReasoning = React.useCallback(async () => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    const runId = typeof crypto !== "undefined" && "randomUUID" in crypto ? crypto.randomUUID() : Date.now().toString();
    currentStreamRunId.current = runId;
    processedEventIds.current.clear();

    setEvents([]);
    setResponse(null);
    setPartialNarration("");
    setError(null);
    setIsStreaming(true);
    setOrbState("analyzing");
    pushEvent("Broker reasoning stream submitted");

    const request = buildRequest();

    try {
      const streamed = await streamBrokerReason(
        request,
        {
          onEvent: (event) => {
            if (currentStreamRunId.current !== runId) return;
            if (event.event_id && processedEventIds.current.has(event.event_id)) return;
            if (event.event_id) processedEventIds.current.add(event.event_id);

            setEvents((current) => mergeEvents(current, event));
            if (event.event_type === "narration_delta" || event.event_type === "narration_chunk") {
              const delta = event.payload.delta ?? event.payload.text ?? event.message;
              if (typeof delta === "string") {
                setPartialNarration((current) => `${current}${delta}`);
              }
            }
          },
          onFinalResponse: (finalResponse) => {
            if (currentStreamRunId.current !== runId) return;
            setResponse(finalResponse);
            setEvents((current) => mergeEventList(current, finalResponse.events));
          },
        },
        controller.signal,
      );

      if (!streamed && !controller.signal.aborted && currentStreamRunId.current === runId) {
        const fallback = await requestBrokerReason(request, controller.signal);
        setResponse(fallback.data);
        setEvents((current) => mergeEventList(current, fallback.data.events));
      }

      if (!controller.signal.aborted && currentStreamRunId.current === runId) {
        setOrbState("responding");
        pushEvent("Broker reasoning completed");
      }
    } catch (reasoningError) {
      if (controller.signal.aborted) return;
      if (currentStreamRunId.current !== runId) return;
      setError(errorMessage(reasoningError));
      setOrbState("idle");
      pushEvent("Broker reasoning failed");
    } finally {
      if (abortRef.current === controller) {
        abortRef.current = null;
      }
      if (!controller.signal.aborted && currentStreamRunId.current === runId) {
        setIsStreaming(false);
      }
    }
  }, [buildRequest, pushEvent, setOrbState]);

  return (
    <motion.div variants={stagedReveal} initial="hidden" animate="show" className="mx-auto flex w-full max-w-7xl flex-col gap-6 p-4 md:p-8">
      <motion.div variants={revealItem} className="grid gap-6 xl:grid-cols-[360px_1fr]">
        <div className="grid content-start gap-6">
          <GlassCard className="relative overflow-hidden p-6 text-center">
            <div className="absolute inset-x-0 top-0 mx-auto h-40 w-40 rounded-full bg-primary-fixed-dim/10 blur-3xl" />
            <div className="relative z-10 flex flex-col items-center">
              <div className="mb-5">
                <AiOrb size="lg" state={orbState} />
              </div>
              <div className="inline-flex items-center gap-2 rounded-full border border-primary-fixed-dim/20 bg-primary-fixed-dim/5 px-4 py-2">
                <span className={cn("h-1.5 w-1.5 rounded-full", isStreaming ? "animate-pulse bg-tertiary-fixed-dim" : "bg-primary-fixed-dim")} />
                <span className="font-label-caps text-[10px] text-primary-fixed-dim">
                  {isStreaming ? "Reasoning Stream Active" : "Broker Intelligence"}
                </span>
              </div>
              <h1 className="mt-5 font-headline-lg-mobile text-on-surface md:font-headline-lg">Broker Intelligence Terminal</h1>
              <p className="mt-3 text-sm leading-6 text-on-surface-variant">
                {valuation
                  ? `${metrics.areaName} context is loaded for grounded broker analysis.`
                  : "Awaiting deterministic valuation context for full broker analysis."}
              </p>
            </div>
          </GlassCard>

          <ReasoningPipeline events={events} isStreaming={isStreaming} />
        </div>

        <div className="grid gap-6">
          <AnimatePresence mode="wait">
            <motion.div
              key={response ? "final" : "streaming"}
              initial={{ opacity: 0, filter: "blur(4px)" }}
              animate={{ opacity: 1, filter: "blur(0px)" }}
              exit={{ opacity: 0, filter: "blur(4px)", position: "absolute", zIndex: 0 }}
              transition={{ duration: 0.8, ease: premiumEase }}
              className="grid gap-6"
            >
              <div className="grid gap-6 2xl:grid-cols-[minmax(0,1fr)_320px]">
                <ValuationProjection metrics={metrics} hasValuation={Boolean(valuation)} />

                <GlassCard floating className="grid content-between gap-6 p-5">
                  <div>
                    <div className="mb-4 flex items-center justify-between gap-3">
                      <p className="font-label-caps text-xs text-primary-fixed-dim">Confidence Visualization</p>
                      <Sparkles className="h-5 w-5 text-secondary-fixed" />
                    </div>
                    <div className="h-2 overflow-hidden rounded-full bg-surface-container-highest">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${Math.round((metrics.confidenceScore ?? 0) * 100)}%` }}
                        transition={confidenceFillTransition}
                        className="h-full rounded-full bg-primary-fixed-dim shadow-[0_0_12px_rgba(0,219,231,0.28)]"
                      />
                    </div>
                    <p className="mt-4 font-data-tabular text-3xl text-primary">{formatPercent(metrics.confidenceScore)}</p>
                    <p className="mt-1 text-sm text-on-surface-variant">{metrics.confidenceLabel ?? "Confidence pending"}</p>
                  </div>

                  <div className="grid gap-2 border-t border-white/5 pt-4">
                    {(response?.governance?.checks ?? []).slice(0, 3).map((check) => (
                      <div key={check.name} className="flex items-center justify-between gap-3 text-xs">
                        <span className="truncate text-on-surface-variant">{check.name.replaceAll("_", " ")}</span>
                        <span className={cn("font-data-tabular", check.status === "passed" ? "text-tertiary-fixed-dim" : "text-outline")}>
                          {check.status}
                        </span>
                      </div>
                    ))}
                    {!response?.governance?.checks?.length && (
                      <p className="text-xs leading-5 text-outline">Governance checks populate after broker finalization.</p>
                    )}
                  </div>
                </GlassCard>
              </div>

              <IntelligenceWidgets metrics={metrics} response={response} />
              <BrokerNarrative 
                response={response} 
                partialNarration={partialNarration} 
                latestMessage={latestMessage} 
                isStreaming={isStreaming} 
                error={error}
              />
              <EvidenceCards comparables={comparables} hasValuation={Boolean(valuation)} />
            </motion.div>
          </AnimatePresence>
          <CommandConsole
            message={message}
            isStreaming={isStreaming}
            hasValuation={Boolean(valuation)}
            error={error}
            onChange={setMessage}
            onSubmit={runReasoning}
            onCancel={cancelStream}
          />
        </div>
      </motion.div>
    </motion.div>
  );
}
