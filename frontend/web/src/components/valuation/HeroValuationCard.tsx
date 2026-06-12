import * as React from "react";
import { AnimatePresence, motion } from "framer-motion";
import { AlertTriangle, CheckCircle2, CircleSlash, RefreshCcw, XCircle } from "lucide-react";
import { ValorApiError } from "@/api/contracts";
import { confidenceFillTransition, valuationReveal } from "@/animations/motion";
import { Button } from "@/components/ui/button";
import { GlassCard, GlassPanel } from "@/components/ui/glass";
import { cn } from "@/lib/utils";
import type { RentFairPriceData } from "@/types/valuation";

const egpFormatter = new Intl.NumberFormat("en-EG", {
  maximumFractionDigits: 0,
});

function formatEgp(value: number): string {
  return `EGP ${egpFormatter.format(value)}`;
}

function formatPercent(value: number): string {
  return `${Math.round(value * 100)}%`;
}

function confidenceTone(score: number): string {
  if (score >= 0.75) return "text-tertiary-fixed-dim border-tertiary-fixed-dim/25 bg-tertiary-fixed-dim/5";
  if (score >= 0.5) return "text-primary-fixed-dim border-primary-fixed-dim/25 bg-primary-fixed-dim/5";
  return "text-error border-error/25 bg-error/5";
}

function flagLabel(result: RentFairPriceData): string {
  if (result.flag === "INSUFFICIENT_DATA") return "Insufficient comparable depth";
  if (result.flag === "TOO_HIGH") return "Target is above fair range";
  if (result.flag === "TOO_LOW") return "Target is below fair range";
  if (result.flag === "OK") return "Target sits inside fair range";
  return "No target price supplied";
}

function factorLabel(value: string): string {
  return value.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function hasResolvedLocation(result: RentFairPriceData): boolean {
  return Boolean(result.resolved_location && Object.keys(result.resolved_location).length > 0);
}

function valueBasisLabel(result: RentFairPriceData): string {
  const basis = String(result.valuation_contract?.value_basis ?? "");
  return basis === "sale_price" ? "Estimated Sale Price" : "Estimated Monthly Rent";
}

interface HeroValuationCardProps {
  result: RentFairPriceData | null;
  targetPrice?: number | null;
  requestId?: string;
  isLoading?: boolean;
  error?: ValorApiError | null;
  onRetry?: () => void;
  onCancel?: () => void;
  className?: string;
}

export const HeroValuationCard = React.memo(function HeroValuationCard({
  result,
  targetPrice,
  requestId,
  isLoading = false,
  error,
  onRetry,
  onCancel,
  className,
}: HeroValuationCardProps) {
  const [showConfidenceDetails, setShowConfidenceDetails] = React.useState(false);
  const confidenceClass = React.useMemo(
    () => (result ? confidenceTone(result.confidence.score) : ""),
    [result],
  );
  const factorEntries = React.useMemo(
    () => Object.entries(result?.confidence.factors ?? {}).slice(0, 8),
    [result],
  );
  const targetMarker = React.useMemo(() => {
    if (!result || !targetPrice || result.range_high_egp <= result.range_low_egp) return 50;
    return Math.max(0, Math.min(100, ((targetPrice - result.range_low_egp) / (result.range_high_egp - result.range_low_egp)) * 100));
  }, [result, targetPrice]);

  if (isLoading) {
    return (
      <GlassCard className={cn("w-full p-6 md:p-8", className)} aria-live="polite">
        <div className="flex flex-col items-center gap-6 text-center">
          <div className="relative flex h-56 w-56 items-center justify-center md:h-72 md:w-72">
            <div className="absolute inset-0 rounded-full border border-primary-fixed-dim/10 animate-[pulse_3s_ease-in-out_infinite]" />
            <div className="absolute inset-5 rounded-full border border-primary-fixed-dim/5 border-dashed animate-[spin_80s_linear_infinite]" />
            <div className="flex flex-col items-center gap-3">
              <div className="h-3 w-24 rounded bg-surface-variant animate-pulse" />
              <div className="h-10 w-44 rounded-lg bg-surface-variant animate-pulse" />
              <div className="h-4 w-32 rounded bg-surface-variant animate-pulse" />
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="font-label-caps text-xs text-on-surface-variant">CMT engine is retrieving comparable evidence</span>
            {onCancel && (
              <Button type="button" variant="ghost" size="sm" onClick={onCancel}>
                Cancel
              </Button>
            )}
          </div>
        </div>
      </GlassCard>
    );
  }

  if (error) {
    return (
      <GlassCard className={cn("w-full p-6 md:p-8", className)} aria-live="assertive">
        <div className="flex flex-col gap-5">
          <div className="flex items-start gap-3">
            <XCircle className="mt-0.5 h-5 w-5 text-error" />
            <div>
              <p className="font-label-caps text-xs text-error">{error.code}</p>
              <h2 className="mt-1 font-headline-lg-mobile text-on-surface">{error.message}</h2>
              {(error.requestId || error.status) && (
                <p className="mt-2 font-data-tabular text-xs text-outline">
                  {error.status ? `HTTP ${error.status}` : "API error"}
                  {error.requestId ? ` | Request ${error.requestId}` : ""}
                </p>
              )}
              {error.correlationId && <p className="mt-1 font-data-tabular text-[10px] text-outline">Trace {error.correlationId}</p>}
            </div>
          </div>
          {error.details.length > 0 && (
            <div className="grid gap-2">
              {error.details.map((detail, index) => (
                <GlassPanel key={`${detail.code}-${index}`} className="p-3 text-sm text-on-surface-variant">
                  <span className="font-label-caps text-[10px] text-primary-fixed-dim">{detail.field ?? detail.code}</span>
                  <p>{detail.message}</p>
                </GlassPanel>
              ))}
            </div>
          )}
          {onRetry && (
            <Button type="button" variant="holo" size="sm" onClick={onRetry} className="self-start">
              <RefreshCcw className="h-4 w-4" />
              Retry
            </Button>
          )}
        </div>
      </GlassCard>
    );
  }

  if (!result) {
    return (
      <GlassCard className={cn("w-full p-6 md:p-8", className)}>
        <div className="flex min-h-72 flex-col items-center justify-center gap-4 text-center">
          <CircleSlash className="h-8 w-8 text-primary-fixed-dim/70" />
          <div>
            <p className="font-label-caps text-xs text-primary-fixed-dim">Live Valuation Awaiting Input</p>
            <h2 className="mt-2 font-headline-lg-mobile text-on-surface">Run the fair-price engine to reveal evidence-backed property intelligence.</h2>
          </div>
        </div>
      </GlassCard>
    );
  }

  const insufficient = result.flag === "INSUFFICIENT_DATA";
  const showResolvedLocation = hasResolvedLocation(result);

  return (
    <motion.div variants={valuationReveal} initial="hidden" animate="show" className={cn("w-full", className)}>
      <GlassCard className="w-full overflow-hidden p-6 md:p-8">
        <div className="grid gap-8 lg:grid-cols-[1fr_360px] lg:items-center">
          <div className="flex flex-col items-center text-center lg:items-start lg:text-left">
            <div className={cn("mb-6 inline-flex items-center gap-2 rounded-full border px-4 py-2 font-label-caps text-xs", confidenceClass)}>
              {insufficient ? <AlertTriangle className="h-3.5 w-3.5" /> : <CheckCircle2 className="h-3.5 w-3.5" />}
              {flagLabel(result)}
            </div>

            <div className="relative flex h-64 w-64 items-center justify-center md:h-80 md:w-80">
              <div className="absolute inset-0 rounded-full border border-primary-fixed-dim/15 orb-pulse mix-blend-screen" />
              <div className="absolute inset-5 rounded-full border border-primary-fixed-dim/10 border-dashed animate-[spin_120s_linear_infinite]" />
              <div className="relative z-10 flex flex-col items-center gap-3">
                <span className="font-label-caps text-xs text-on-surface-variant">{valueBasisLabel(result)}</span>
                <h1 className="font-display-lg text-4xl text-primary drop-shadow-[0_0_12px_rgba(0,219,231,0.18)] md:text-5xl">
                  {insufficient ? "N/A" : formatEgp(result.fair_price_egp)}
                </h1>
                <span className="font-data-tabular text-sm text-on-surface-variant">
                  {insufficient ? `${result.comps_count} comps found` : `${formatEgp(result.range_low_egp)} - ${formatEgp(result.range_high_egp)}`}
                </span>
              </div>
            </div>
          </div>

          <div className="flex flex-col gap-4">
            <GlassPanel className="p-5">
              <div className="mb-4 flex items-center justify-between gap-3">
                <span className="font-label-caps text-xs text-on-surface-variant">Confidence</span>
                <button
                  type="button"
                  onClick={() => setShowConfidenceDetails((value) => !value)}
                  className={cn("rounded-md border px-3 py-1 font-data-tabular text-sm transition-colors", confidenceClass)}
                >
                  {result.confidence.label} {formatPercent(result.confidence.score)}
                </button>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-surface-container-highest">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.round(result.confidence.score * 100)}%` }}
                  transition={confidenceFillTransition}
                  className="h-full rounded-full bg-primary-fixed-dim"
                />
              </div>
              <AnimatePresence>
                {showConfidenceDetails && factorEntries.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="mt-4 grid gap-3 overflow-hidden"
                  >
                    {factorEntries.map(([key, value]) => (
                      <div key={key} className="grid gap-1">
                        <div className="flex justify-between font-label-caps text-[10px] text-outline">
                          <span>{factorLabel(key)}</span>
                          <span>{formatPercent(value)}</span>
                        </div>
                        <div className="h-1.5 overflow-hidden rounded-full bg-surface-container-high">
                          <div className="h-full rounded-full bg-tertiary-fixed-dim/80" style={{ width: `${Math.round(value * 100)}%` }} />
                        </div>
                      </div>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </GlassPanel>

            <GlassPanel className="p-5">
              <div className="mb-3 flex items-center justify-between">
                <span className="font-label-caps text-xs text-on-surface-variant">Valuation Spectrum</span>
                <span className="font-data-tabular text-xs text-outline">Tier {result.tier_used}</span>
              </div>
              <div className="relative mt-6 h-2 rounded-full bg-gradient-to-r from-tertiary-fixed-dim/80 via-primary-fixed-dim/80 to-error/80">
                <motion.div
                  initial={{ left: "50%" }}
                  animate={{ left: `${targetMarker}%` }}
                  transition={confidenceFillTransition}
                  className="absolute -top-1.5 h-5 w-0.5 rounded-full bg-white shadow-[0_0_6px_rgba(255,255,255,0.8)]"
                />
              </div>
              <div className="mt-3 flex justify-between font-label-caps text-[9px] text-outline">
                <span>Low</span>
                <span>Fair</span>
                <span>High</span>
              </div>
            </GlassPanel>

            <div className={cn("grid gap-3", showResolvedLocation ? "grid-cols-3" : "grid-cols-2")}>
              <GlassPanel className="p-4">
                <span className="font-label-caps text-[10px] text-outline">Comparables</span>
                <p className="mt-1 font-data-tabular text-xl text-on-surface">{result.comps_count}</p>
              </GlassPanel>
              <GlassPanel className="p-4 overflow-hidden">
                <span className="font-label-caps text-[10px] text-outline">Area</span>
                <p className="mt-1 truncate font-data-tabular text-sm text-on-surface" title={String(result.area.name ?? "Resolved")}>{String(result.area.name ?? "Resolved")}</p>
              </GlassPanel>
              {showResolvedLocation && (
                <GlassPanel className="p-4 overflow-hidden">
                  <span className="font-label-caps text-[10px] text-outline">Resolution</span>
                  <p className="mt-1 truncate font-data-tabular text-sm text-on-surface" title={String(result.resolved_location.precision_level ?? "Unknown")}>{String(result.resolved_location.precision_level ?? "Unknown")}</p>
                </GlassPanel>
              )}
            </div>

            {requestId && <p className="font-data-tabular text-[10px] text-outline">Request {requestId}</p>}
          </div>
        </div>
      </GlassCard>
    </motion.div>
  );
});
