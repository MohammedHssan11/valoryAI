import * as React from "react";
import { BadgeCheck, HandCoins, ListChecks, MessageSquareQuote, Scale, ShieldAlert } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GlassPanel } from "@/components/ui/glass";
import { cn } from "@/lib/utils";
import { useNegotiationStore } from "@/store/negotiationStore";
import type {
  BrokerTalkingPoint,
  NegotiationEvidenceReference,
  NegotiationRunTarget,
  NegotiationToolRequest,
  NegotiationToolResponse,
} from "@/types/negotiation";
import type { ScenarioState } from "@/types/scenarioHistory";
import type { RentFairPriceData, RentFairPriceRequest } from "@/types/valuation";
import type { WhatIfToolRequest, WhatIfToolResponse } from "@/types/whatIf";

const egpFormatter = new Intl.NumberFormat("en-EG", {
  maximumFractionDigits: 0,
});

const inputClass =
  "h-10 w-full rounded-lg border border-white/10 bg-surface/40 px-3 font-data-tabular text-sm text-on-surface outline-none transition-colors focus:border-primary-fixed-dim/50";

interface NegotiationIntelligencePanelProps {
  baseRequest: RentFairPriceRequest;
  baseResult: RentFairPriceData;
  workspaceId: number | null;
  propertyId: number | null;
  activeScenarioRequest: WhatIfToolRequest | null;
  activeScenarioResponse: WhatIfToolResponse | null;
  selectedScenario: ScenarioState | null;
  bridgeStatus?: string;
}

interface NegotiationTargetOption {
  id: NegotiationRunTarget;
  label: string;
  eyebrow: string;
  description: string;
  scenarioId: number | null;
  modifications?: Record<string, unknown>;
  disabled?: boolean;
}

interface MetricTileProps {
  label: string;
  value: string;
  tone?: "default" | "positive" | "warning";
}

function formatEgp(value: number): string {
  return `EGP ${egpFormatter.format(value)}`;
}

function formatSignedEgp(value: number): string {
  const sign = value > 0 ? "+" : value < 0 ? "-" : "";
  return `${sign}EGP ${egpFormatter.format(Math.abs(value))}`;
}

function formatPercent(value: number): string {
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}

function positiveIntegerFromInput(value: string): number | null {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed <= 0) return null;
  return parsed;
}

function isNonEmptyRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value) && Object.keys(value).length > 0;
}

function defaultAskingPrice(request: RentFairPriceRequest, result: RentFairPriceData): number {
  return Math.max(1, Math.round(request.target_price_egp ?? result.fair_price_egp));
}

function formatOfferBand(response: NegotiationToolResponse): string {
  const { low, high } = response.recommended_offer_band;
  if (typeof low !== "number" || typeof high !== "number") return "No numeric counter-offer";
  if (low === high) return formatEgp(low);
  return `${formatEgp(low)} - ${formatEgp(high)}`;
}

function sellerPosition(response: NegotiationToolResponse): string {
  return response.risk_notes[0]?.text ?? `${response.confidence_level} confidence: ${response.confidence_reason}`;
}

function evidenceLabel(reference: NegotiationEvidenceReference): string {
  const comparable = reference.comparable_id ? ` · ${reference.comparable_id}` : "";
  const valuation = reference.valuation_id ? ` · ${reference.valuation_id}` : "";
  return `${reference.source_tool}.${reference.field}${comparable}${valuation}`;
}

function uniqueReferences(points: BrokerTalkingPoint[]): NegotiationEvidenceReference[] {
  const seen = new Set<string>();
  const references: NegotiationEvidenceReference[] = [];
  for (const point of points) {
    for (const reference of point.evidence) {
      const key = evidenceLabel(reference);
      if (!seen.has(key)) {
        seen.add(key);
        references.push(reference);
      }
    }
  }
  return references;
}

function targetOptions(
  activeScenarioRequest: WhatIfToolRequest | null,
  activeScenarioResponse: WhatIfToolResponse | null,
  selectedScenario: ScenarioState | null,
): NegotiationTargetOption[] {
  const activeModifications = activeScenarioRequest?.modifications as Record<string, unknown> | undefined;
  return [
    {
      id: "base",
      label: "Base valuation",
      eyebrow: "Base",
      description: "Uses the direct valuation snapshot.",
      scenarioId: null,
    },
    {
      id: "active_scenario",
      label: "Active scenario",
      eyebrow: "What-if",
      description: activeScenarioResponse
        ? `Uses current what-if sensitivity at ${formatEgp(activeScenarioResponse.scenario_valuation)}.`
        : "Run a what-if scenario first.",
      scenarioId: activeScenarioRequest?.scenario_id ?? selectedScenario?.id ?? null,
      modifications: isNonEmptyRecord(activeModifications) ? activeModifications : undefined,
      disabled: !activeScenarioResponse || !isNonEmptyRecord(activeModifications),
    },
    {
      id: "selected_scenario",
      label: selectedScenario ? selectedScenario.name : "Selected scenario",
      eyebrow: "Restored",
      description: selectedScenario
        ? `Uses persisted scenario ${selectedScenario.id}.`
        : "Open or restore a saved scenario first.",
      scenarioId: selectedScenario?.id ?? null,
      disabled: !selectedScenario,
    },
  ];
}

function preferredTarget(
  activeScenarioResponse: WhatIfToolResponse | null,
  selectedScenario: ScenarioState | null,
): NegotiationRunTarget {
  if (activeScenarioResponse) return "active_scenario";
  if (selectedScenario) return "selected_scenario";
  return "base";
}

function MetricTile({ label, value, tone = "default" }: MetricTileProps) {
  return (
    <div
      className={cn(
        "rounded-lg border p-3",
        tone === "positive" && "border-tertiary-fixed-dim/25 bg-tertiary-fixed-dim/10 text-tertiary-fixed-dim",
        tone === "warning" && "border-error/25 bg-error/10 text-error",
        tone === "default" && "border-white/10 bg-surface/20 text-on-surface",
      )}
    >
      <span className="font-label-caps text-[10px] text-outline">{label}</span>
      <p className="mt-1 font-data-tabular text-sm">{value}</p>
    </div>
  );
}

function PointList({ items, empty }: { items: BrokerTalkingPoint[]; empty: string }) {
  if (items.length === 0) {
    return <p className="text-sm text-on-surface-variant">{empty}</p>;
  }

  return (
    <div className="grid gap-2">
      {items.map((item, index) => (
        <div key={`${item.text}-${index}`} className="grid gap-2 rounded-lg border border-white/10 bg-surface/20 p-3">
          <p className="text-sm leading-6 text-on-surface">{item.text}</p>
          <EvidencePills references={item.evidence} />
        </div>
      ))}
    </div>
  );
}

function EvidencePills({ references }: { references: NegotiationEvidenceReference[] }) {
  if (references.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2">
      {references.map((reference) => (
        <span
          key={evidenceLabel(reference)}
          className="rounded-md border border-white/10 bg-surface/30 px-2.5 py-1.5 font-data-tabular text-[10px] text-on-surface-variant"
        >
          {evidenceLabel(reference)}
        </span>
      ))}
    </div>
  );
}

function NegotiationResult({ response }: { response: NegotiationToolResponse }) {
  const priceGapTone = response.price_gap > 0 ? "warning" : response.price_gap < 0 ? "positive" : "default";
  const strengths: BrokerTalkingPoint[] = [
    {
      text: response.negotiation_position_reason,
      evidence: response.negotiation_position_evidence,
    },
    {
      text: response.recommended_offer_band.derivation,
      evidence: response.recommended_offer_band.evidence,
    },
    {
      text: response.evidence_summary.strongest_factors,
      evidence: [
        {
          source_tool: "explainability",
          valuation_id: response.evidence_summary.valuation_id,
          field: "strongest_factors",
          comparable_id: null,
        },
      ],
    },
  ];
  const allReferences = uniqueReferences([
    ...strengths,
    ...response.broker_talking_points,
    ...response.risk_notes,
  ]);

  return (
    <div className="grid gap-4">
      <GlassPanel className="grid gap-4 p-5">
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <MetricTile label="Fair Price" value={formatEgp(response.fair_price)} />
          <MetricTile label="Asking Price" value={formatEgp(response.asking_price)} />
          <MetricTile label="Recommended Offer" value={formatOfferBand(response)} />
          <MetricTile label="Negotiation Range" value={formatOfferBand(response)} />
          <MetricTile
            label="Negotiation Room"
            value={`${formatSignedEgp(response.price_gap)} (${formatPercent(response.price_gap_percentage)})`}
            tone={priceGapTone}
          />
          <MetricTile label="Confidence" value={response.confidence_level} />
        </div>
      </GlassPanel>

      <div className="grid gap-4 lg:grid-cols-2">
        <GlassPanel className="grid gap-3 p-5">
          <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
            <BadgeCheck className="h-4 w-4" />
            Buyer Position
          </span>
          <p className="font-data-tabular text-lg text-on-surface">{response.negotiation_position}</p>
          <p className="text-sm leading-6 text-on-surface-variant">{response.negotiation_position_reason}</p>
          <EvidencePills references={response.negotiation_position_evidence} />
        </GlassPanel>

        <GlassPanel className="grid gap-3 p-5">
          <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
            <ShieldAlert className="h-4 w-4" />
            Seller Position
          </span>
          <p className="text-sm leading-6 text-on-surface">{sellerPosition(response)}</p>
          <p className="text-sm leading-6 text-on-surface-variant">{response.confidence_reason}</p>
        </GlassPanel>
      </div>

      {response.what_if_analysis && (
        <GlassPanel className="grid gap-3 p-5">
          <span className="font-label-caps text-xs text-primary-fixed-dim">Scenario Awareness</span>
          <div className="grid gap-3 sm:grid-cols-3">
            <MetricTile label="Base Valuation" value={formatEgp(response.what_if_analysis.base_valuation)} />
            <MetricTile label="Scenario Valuation" value={formatEgp(response.what_if_analysis.scenario_valuation)} />
            <MetricTile
              label="Sensitivity Delta"
              value={`${formatSignedEgp(response.what_if_analysis.delta_value)} (${formatPercent(
                response.what_if_analysis.delta_percentage,
              )})`}
              tone={response.what_if_analysis.delta_value > 0 ? "positive" : response.what_if_analysis.delta_value < 0 ? "warning" : "default"}
            />
          </div>
        </GlassPanel>
      )}

      <div className="grid gap-4 lg:grid-cols-2">
        <GlassPanel className="grid gap-3 p-5">
          <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
            <Scale className="h-4 w-4" />
            Strengths
          </span>
          <PointList items={strengths} empty="No buyer strengths were returned." />
        </GlassPanel>

        <GlassPanel className="grid gap-3 p-5">
          <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
            <ShieldAlert className="h-4 w-4" />
            Risks
          </span>
          <PointList items={response.risk_notes} empty="No seller risks were returned." />
        </GlassPanel>
      </div>

      <GlassPanel className="grid gap-3 p-5">
        <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
          <MessageSquareQuote className="h-4 w-4" />
          Talking Points
        </span>
        <PointList items={response.broker_talking_points} empty="No talking points were returned." />
      </GlassPanel>

      <GlassPanel className="grid gap-3 p-5">
        <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
          <ListChecks className="h-4 w-4" />
          Evidence
        </span>
        <div className="grid gap-3 md:grid-cols-2">
          <div className="grid gap-2">
            <p className="font-data-tabular text-sm text-on-surface">{response.evidence_summary.explainability_summary}</p>
            <p className="text-sm leading-6 text-on-surface-variant">{response.evidence_summary.why_this_price}</p>
            <p className="font-data-tabular text-xs text-outline">
              Range {formatEgp(response.evidence_summary.price_range.low)} - {formatEgp(response.evidence_summary.price_range.high)}
            </p>
          </div>
          <div className="grid gap-2">
            <p className="font-data-tabular text-sm text-on-surface">
              {response.comparable_summary.comparable_count} comparables
            </p>
            <p className="text-sm leading-6 text-on-surface-variant">
              Observed prices{" "}
              {typeof response.comparable_summary.lowest_observed_price === "number"
                ? `${formatEgp(response.comparable_summary.lowest_observed_price)} - ${formatEgp(
                    response.comparable_summary.highest_observed_price ?? response.comparable_summary.lowest_observed_price,
                  )}`
                : "unavailable"}
            </p>
            <EvidencePills references={allReferences} />
          </div>
        </div>
      </GlassPanel>
    </div>
  );
}

export function NegotiationIntelligencePanel({
  baseRequest,
  baseResult,
  workspaceId,
  propertyId,
  activeScenarioRequest,
  activeScenarioResponse,
  selectedScenario,
  bridgeStatus = "idle",
}: NegotiationIntelligencePanelProps) {
  const { lastResponse, runs, isLoading, error, runNegotiation } = useNegotiationStore();
  const [selectedTarget, setSelectedTarget] = React.useState<NegotiationRunTarget>(() =>
    preferredTarget(activeScenarioResponse, selectedScenario),
  );
  const [askingPriceInput, setAskingPriceInput] = React.useState(() =>
    String(defaultAskingPrice(baseRequest, baseResult)),
  );
  const abortRef = React.useRef<AbortController | null>(null);
  const options = React.useMemo(
    () => targetOptions(activeScenarioRequest, activeScenarioResponse, selectedScenario),
    [activeScenarioRequest, activeScenarioResponse, selectedScenario],
  );
  const selectedOption = options.find((option) => option.id === selectedTarget) ?? options[0];
  const askingPrice = positiveIntegerFromInput(askingPriceInput);
  const hasContext = typeof workspaceId === "number" && typeof propertyId === "number";
  const canRun = hasContext && Boolean(selectedOption && !selectedOption.disabled) && askingPrice !== null && !isLoading;

  React.useEffect(() => {
    const preferred = preferredTarget(activeScenarioResponse, selectedScenario);
    const current = options.find((option) => option.id === selectedTarget);
    if (!current || current.disabled) {
      setSelectedTarget(preferred);
    }
  }, [activeScenarioResponse, options, selectedScenario, selectedTarget]);

  React.useEffect(() => {
    setAskingPriceInput(String(defaultAskingPrice(baseRequest, baseResult)));
  }, [baseRequest, baseResult]);

  React.useEffect(
    () => () => {
      abortRef.current?.abort();
      abortRef.current = null;
    },
    [],
  );

  const submitNegotiation = React.useCallback(() => {
    if (!hasContext || !selectedOption || selectedOption.disabled || askingPrice === null) return;
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    const request: NegotiationToolRequest = {
      workspace_id: workspaceId,
      property_id: propertyId,
      scenario_id: selectedOption.scenarioId,
      asking_price_egp: askingPrice,
      ...(selectedOption.modifications ? { what_if_modifications: selectedOption.modifications } : {}),
    };

    void runNegotiation(
      request,
      {
        target: selectedOption.id,
        label: selectedOption.label,
        scenarioId: selectedOption.scenarioId,
      },
      controller.signal,
    )
      .catch(() => undefined)
      .finally(() => {
        if (abortRef.current === controller) {
          abortRef.current = null;
        }
      });
  }, [askingPrice, hasContext, propertyId, runNegotiation, selectedOption, workspaceId]);

  return (
    <section className="grid gap-4">
      <div className="flex flex-wrap items-end justify-between gap-4 border-b border-white/5 pb-2">
        <div>
          <p className="font-label-caps text-xs text-primary-fixed-dim">Negotiation Intelligence</p>
          <h3 className="mt-1 font-body-md text-on-surface">Offer strategy</h3>
        </div>
        <span className="font-data-tabular text-[10px] text-outline">POST /v1/copilot/tools/negotiation</span>
      </div>

      <GlassPanel className="grid gap-5 p-5">
        {!hasContext && (
          <div className="rounded-lg border border-white/10 bg-surface/20 p-3">
            <p className="font-label-caps text-[10px] text-outline">Property Context {bridgeStatus}</p>
            <p className="mt-1 text-sm text-on-surface-variant">Negotiation is waiting for the backend property context.</p>
          </div>
        )}

        <div className="grid gap-3 md:grid-cols-3">
          {options.map((option) => {
            const selected = selectedTarget === option.id;
            return (
              <button
                key={option.id}
                type="button"
                disabled={option.disabled}
                onClick={() => setSelectedTarget(option.id)}
                className={cn(
                  "grid min-h-24 gap-2 rounded-lg border p-3 text-left transition-colors disabled:cursor-not-allowed disabled:opacity-45",
                  selected
                    ? "border-primary-fixed-dim/50 bg-primary-fixed-dim/10"
                    : "border-white/10 bg-surface/20 hover:border-white/20",
                )}
              >
                <span className="font-label-caps text-[10px] text-primary-fixed-dim">{option.eyebrow}</span>
                <span className="font-data-tabular text-sm text-on-surface">{option.label}</span>
                <span className="text-xs leading-5 text-on-surface-variant">{option.description}</span>
              </button>
            );
          })}
        </div>

        <div className="grid gap-4 md:grid-cols-[minmax(220px,320px)_auto] md:items-end">
          <label className="grid gap-2">
            <span className="font-label-caps text-[10px] text-on-surface-variant">Asking Price EGP</span>
            <input
              aria-label="Negotiation asking price"
              className={inputClass}
              type="number"
              min="1"
              value={askingPriceInput}
              onChange={(event) => setAskingPriceInput(event.currentTarget.value)}
            />
          </label>
          <Button type="button" variant="holo" className="w-full md:w-auto" onClick={submitNegotiation} disabled={!canRun}>
            <HandCoins className="h-4 w-4" />
            Run Negotiation
          </Button>
        </div>
      </GlassPanel>

      {error && (
        <GlassPanel className="border-error/25 bg-error/5 p-5">
          <p className="font-label-caps text-xs text-error">Negotiation Error</p>
          <p className="mt-1 text-sm text-on-surface-variant">{error.message}</p>
        </GlassPanel>
      )}

      {lastResponse ? (
        <NegotiationResult response={lastResponse} />
      ) : (
        <GlassPanel className="p-5">
          <p className="font-label-caps text-xs text-primary-fixed-dim">Negotiation Results</p>
          <p className="mt-1 text-sm text-on-surface-variant">No negotiation package has been generated for this valuation.</p>
        </GlassPanel>
      )}

      {runs.length > 1 && (
        <GlassPanel className="grid gap-3 p-5">
          <span className="font-label-caps text-xs text-primary-fixed-dim">Outcome Comparison</span>
          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
            {runs.map((run) => (
              <div key={run.key} className="grid gap-2 rounded-lg border border-white/10 bg-surface/20 p-3">
                <div className="flex items-start justify-between gap-3">
                  <p className="font-data-tabular text-sm text-on-surface">{run.label}</p>
                  <span className="font-data-tabular text-[10px] text-outline">{run.target.replace("_", " ")}</span>
                </div>
                <p className="text-sm text-on-surface-variant">{run.response.negotiation_position}</p>
                <div className="grid gap-2 sm:grid-cols-2">
                  <MetricTile label="Offer" value={formatOfferBand(run.response)} />
                  <MetricTile label="Gap" value={formatSignedEgp(run.response.price_gap)} />
                </div>
              </div>
            ))}
          </div>
        </GlassPanel>
      )}
    </section>
  );
}
