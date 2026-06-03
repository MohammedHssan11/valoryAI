import { motion } from "framer-motion";
import { CheckCircle2, Database, GitBranch, Route, ShieldCheck } from "lucide-react";
import { revealItem, stagedReveal } from "@/animations/motion";
import { GlassPanel } from "@/components/ui/glass";
import { ConfidenceVisualization } from "@/features/evidence/ConfidenceVisualization";
import { cn } from "@/lib/utils";
import type { ExplanationItem, RentFairPriceData, RetrievalStageItem } from "@/types/valuation";

function summarizeDetails(details: Record<string, unknown>): string {
  const entries = Object.entries(details).slice(0, 3);
  if (entries.length === 0) return "No extra details";
  return entries.map(([key, value]) => `${key}: ${String(value)}`).join(" | ");
}

function fallbackRetrievalTrace(trace: ExplanationItem[]): RetrievalStageItem[] {
  return trace
    .filter((item) => typeof item.details.radius_m === "number" || typeof item.details.comps_found === "number")
    .map((item, index) => ({
      tier: typeof item.details.tier === "number" ? item.details.tier : null,
      tier_label: typeof item.details.tier_label === "string" ? item.details.tier_label : null,
      reason_code: item.reason_code,
      scope: typeof item.details.scope === "string" ? item.details.scope : null,
      radius_m: typeof item.details.radius_m === "number" ? item.details.radius_m : null,
      comps_found: typeof item.details.comps_found === "number" ? item.details.comps_found : 0,
      threshold: typeof item.details.threshold === "number" ? item.details.threshold : null,
      shortfall: typeof item.details.shortfall === "number" ? item.details.shortfall : null,
      attempt_index: index + 1,
      status: typeof item.details.status === "string" ? item.details.status : "attempted",
      selected: Boolean(item.details.selected),
      radius_expansion_m: typeof item.details.radius_expansion_m === "number" ? item.details.radius_expansion_m : null,
    }));
}

function formatRadius(value?: number | null): string {
  if (value == null) return "n/a";
  if (value < 1000) return `${Math.round(value)}m`;
  return `${(value / 1000).toFixed(1)}km`;
}

function formatPercentValue(value: unknown): string {
  return typeof value === "number" && Number.isFinite(value) ? `${Math.round(value * 100)}%` : "n/a";
}

function listValue(value: unknown): string {
  return Array.isArray(value) && value.length > 0 ? value.map(String).join(", ") : "none";
}

function stageTone(stage: RetrievalStageItem): string {
  if (stage.selected) return "border-tertiary-fixed-dim/30 bg-tertiary-fixed-dim/10 text-tertiary-fixed-dim";
  if (stage.status === "blocked") return "border-error/25 bg-error/10 text-error";
  return "border-white/10 bg-surface/30 text-on-surface-variant";
}

interface ExplainabilityPanelProps {
  result: RentFairPriceData;
}

export function ExplainabilityPanel({ result }: ExplainabilityPanelProps) {
  const retrievalTrace = result.retrieval_trace?.length ? result.retrieval_trace : fallbackRetrievalTrace(result.explanation_trace);
  const guardrails = (result.evidence_summary?.guardrails ?? {}) as Record<string, unknown>;
  const mad = (result.evidence_summary?.mad ?? {}) as Record<string, unknown>;
  const selectedStage = retrievalTrace.find((stage) => stage.selected);
  const valuationContract = (result.valuation_contract ?? result.evidence_summary?.valuation_contract ?? {}) as Record<string, unknown>;
  const amenityIntelligence = (result.amenity_intelligence ?? result.evidence_summary?.amenity_intelligence ?? {}) as Record<string, unknown>;

  return (
    <motion.section variants={stagedReveal} initial="hidden" animate="show" className="grid gap-4">
      <div className="flex flex-wrap items-end justify-between gap-4 border-b border-white/5 pb-2">
        <div>
          <p className="font-label-caps text-xs text-primary-fixed-dim">Explainability</p>
          <h2 className="mt-1 font-headline-lg-mobile text-on-surface">Institutional evidence trail</h2>
        </div>
        <span className="font-data-tabular text-xs text-outline">{result.explanation_trace.length} trace events</span>
      </div>

      <div className="grid gap-4 xl:grid-cols-[0.9fr_1.1fr]">
        <div className="grid gap-4">
          <ConfidenceVisualization result={result} />

          <GlassPanel className="p-5">
            <div className="mb-4 flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-tertiary-fixed-dim" />
              <span className="font-label-caps text-xs text-tertiary-fixed-dim">Valuation rationale</span>
            </div>
            <div className="grid gap-3">
              {result.explanation.map((item, index) => (
                <motion.p key={`${item}-${index}`} variants={revealItem} className="text-sm leading-6 text-on-surface-variant">
                  {item}
                </motion.p>
              ))}
            </div>
          </GlassPanel>

          <GlassPanel className="grid gap-4 p-5">
            <div className="flex items-center gap-2">
              <Database className="h-4 w-4 text-primary-fixed-dim" />
              <span className="font-label-caps text-xs text-primary-fixed-dim">Filtering Stages</span>
            </div>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div>
                <span className="font-label-caps text-[10px] text-outline">Guardrails Removed</span>
                <p className="mt-1 font-data-tabular text-on-surface">{String(guardrails.removed ?? 0)}</p>
              </div>
              <div>
                <span className="font-label-caps text-[10px] text-outline">MAD Removed</span>
                <p className="mt-1 font-data-tabular text-on-surface">{String(mad.removed ?? 0)}</p>
              </div>
              <div>
                <span className="font-label-caps text-[10px] text-outline">MAD Metric</span>
                <p className="mt-1 font-data-tabular text-on-surface">{String(mad.metric ?? "n/a")}</p>
              </div>
              <div>
                <span className="font-label-caps text-[10px] text-outline">Selected Radius</span>
                <p className="mt-1 font-data-tabular text-on-surface">{formatRadius(selectedStage?.radius_m)}</p>
              </div>
            </div>
          </GlassPanel>

          <GlassPanel className="grid gap-4 p-5">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-tertiary-fixed-dim" />
              <span className="font-label-caps text-xs text-tertiary-fixed-dim">Category & Amenity Governance</span>
            </div>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div>
                <span className="font-label-caps text-[10px] text-outline">Contract</span>
                <p className="mt-1 font-data-tabular text-on-surface">{String(valuationContract.label ?? result.property_category ?? "residential_rent")}</p>
              </div>
              <div>
                <span className="font-label-caps text-[10px] text-outline">Value Basis</span>
                <p className="mt-1 font-data-tabular text-on-surface">{String(valuationContract.value_basis ?? "monthly_rent")}</p>
              </div>
              <div>
                <span className="font-label-caps text-[10px] text-outline">Amenity Similarity</span>
                <p className="mt-1 font-data-tabular text-on-surface">{formatPercentValue(amenityIntelligence.average_amenity_similarity)}</p>
              </div>
              <div>
                <span className="font-label-caps text-[10px] text-outline">Comps Scored</span>
                <p className="mt-1 font-data-tabular text-on-surface">{String(amenityIntelligence.comps_scored ?? 0)}</p>
              </div>
            </div>
            <p className="text-sm leading-6 text-on-surface-variant">
              Matched {listValue(amenityIntelligence.matched_amenities_observed)}; missing {listValue(amenityIntelligence.missing_amenities_observed)}.
            </p>
          </GlassPanel>
        </div>

        <div className="grid content-start gap-4">
          <GlassPanel className="p-5">
            <div className="mb-4 flex items-center justify-between gap-3">
              <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
                <Route className="h-4 w-4" />
                Retrieval Timeline
              </span>
              <span className="font-data-tabular text-[10px] text-outline">{retrievalTrace.length} attempts</span>
            </div>
            <div className="grid gap-3">
              {retrievalTrace.map((stage, index) => (
                <motion.div key={`${stage.reason_code}-${stage.radius_m ?? index}-${index}`} variants={revealItem} className="grid grid-cols-[24px_1fr] gap-3">
                  <div className="flex flex-col items-center">
                    <span className={cn("grid h-6 w-6 place-items-center rounded-full border font-data-tabular text-[10px]", stageTone(stage))}>
                      {stage.selected ? <CheckCircle2 className="h-3.5 w-3.5" /> : stage.attempt_index ?? index + 1}
                    </span>
                    {index < retrievalTrace.length - 1 && <span className="h-full w-px bg-white/10" />}
                  </div>
                  <div className={cn("rounded-lg border p-3", stageTone(stage))}>
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="font-label-caps text-xs">{stage.reason_code}</span>
                      <span className="font-data-tabular text-[10px]">{stage.status ?? "attempted"}</span>
                    </div>
                    <div className="mt-2 grid grid-cols-3 gap-2 font-data-tabular text-xs">
                      <span>{formatRadius(stage.radius_m)}</span>
                      <span>{stage.comps_found} comps</span>
                      <span>{stage.shortfall ?? 0} short</span>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </GlassPanel>

          <div className="grid gap-3">
            {result.explanation_trace.map((item, index) => (
              <motion.div key={`${item.reason_code}-${index}`} variants={revealItem}>
                <GlassPanel className="p-4">
                  <div className="flex items-start gap-3">
                    <GitBranch className="mt-0.5 h-4 w-4 text-primary-fixed-dim" />
                    <div className="min-w-0">
                      <p className="font-label-caps text-xs text-primary-fixed-dim">{item.reason_code}</p>
                      <p className="mt-1 truncate text-sm text-on-surface-variant">{summarizeDetails(item.details)}</p>
                    </div>
                  </div>
                </GlassPanel>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </motion.section>
  );
}
