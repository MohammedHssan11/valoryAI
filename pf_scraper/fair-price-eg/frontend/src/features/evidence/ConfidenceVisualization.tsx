import { Activity, Crosshair, DatabaseZap, Layers3, type LucideIcon } from "lucide-react";
import { GlassPanel } from "@/components/ui/glass";
import { cn } from "@/lib/utils";
import type { RentFairPriceData } from "@/types/valuation";

interface ConfidenceVisualizationProps {
  result: RentFairPriceData;
  className?: string;
}

function numeric(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

function scoreFromDimension(value: unknown): number | null {
  if (typeof value === "object" && value !== null && "score" in value) {
    return numeric((value as { score?: unknown }).score);
  }
  return null;
}

function formatPercent(value: number): string {
  return `${Math.round(value * 100)}%`;
}

function tone(score: number): string {
  if (score >= 0.75) return "text-tertiary-fixed-dim bg-tertiary-fixed-dim/10 border-tertiary-fixed-dim/20";
  if (score >= 0.5) return "text-primary-fixed-dim bg-primary-fixed-dim/10 border-primary-fixed-dim/20";
  return "text-error bg-error/10 border-error/25";
}

function Bar({ label, score, icon: Icon }: { label: string; score: number; icon: LucideIcon }) {
  return (
    <div className="grid gap-2">
      <div className="flex items-center justify-between gap-3">
        <span className="inline-flex items-center gap-2 font-label-caps text-[10px] text-on-surface-variant">
          <Icon className="h-3.5 w-3.5" />
          {label}
        </span>
        <span className={cn("rounded-md border px-2 py-1 font-data-tabular text-xs", tone(score))}>{formatPercent(score)}</span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-surface-container-highest">
        <div className={cn("h-full rounded-full", score >= 0.75 ? "bg-tertiary-fixed-dim" : score >= 0.5 ? "bg-primary-fixed-dim" : "bg-error")} style={{ width: `${Math.max(4, Math.round(score * 100))}%` }} />
      </div>
    </div>
  );
}

export function ConfidenceVisualization({ result, className }: ConfidenceVisualizationProps) {
  const valuationScore = result.confidence.score;
  const evidenceScore = scoreFromDimension(result.confidence.dimensions?.valuation_evidence) ?? result.confidence.factors.valuation_evidence ?? valuationScore;
  const locationScore = scoreFromDimension(result.confidence.dimensions?.location_resolution) ?? result.confidence.factors.location_resolution ?? valuationScore;
  const amenityScore = result.confidence.factors.amenity_similarity;
  const warnings = [
    locationScore < 0.5 ? "Weak spatial certainty" : null,
    evidenceScore < 0.5 ? "Weak comparable evidence" : null,
    (result.confidence.factors.count ?? 1) < 0.5 ? "Sparse retrieval" : null,
    (result.confidence.factors.distance ?? 1) > 0.75 && (result.confidence.factors.similarity ?? 1) > 0.75 ? "High-quality cluster" : null,
  ].filter(Boolean);

  return (
    <GlassPanel className={cn("grid gap-5 p-5", className)}>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="font-label-caps text-xs text-primary-fixed-dim">Confidence Stack</p>
          <h3 className="mt-1 font-body-md text-on-surface">Valuation, location, and evidence</h3>
        </div>
        <span className={cn("rounded-md border px-3 py-1 font-data-tabular text-sm", tone(valuationScore))}>
          {result.confidence.label} {formatPercent(valuationScore)}
        </span>
      </div>

      <div className="grid gap-4">
        <Bar label="Valuation confidence" score={valuationScore} icon={Activity} />
        <Bar label="Evidence confidence" score={evidenceScore} icon={DatabaseZap} />
        <Bar label="Location confidence" score={locationScore} icon={Crosshair} />
        {typeof amenityScore === "number" && <Bar label="Amenity confidence" score={amenityScore} icon={Layers3} />}
      </div>

      {warnings.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {warnings.map((warning) => (
            <span key={warning} className="rounded-md border border-white/10 px-2 py-1 font-data-tabular text-xs text-on-surface-variant">
              {warning}
            </span>
          ))}
        </div>
      )}
    </GlassPanel>
  );
}
