import * as React from "react";
import {
  ArrowDown,
  ArrowRight,
  ArrowUp,
  BadgeCheck,
  BarChart3,
  BriefcaseBusiness,
  CircleDollarSign,
  FileSearch,
  GitCompareArrows,
  ListChecks,
  ShieldAlert,
  TrendingDown,
  TrendingUp,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { GlassPanel } from "@/components/ui/glass";
import { cn } from "@/lib/utils";
import { useInvestmentStore } from "@/store/investmentStore";
import type {
  InvestmentFinding,
  InvestmentRunRecord,
  InvestmentRunTarget,
  InvestmentToolRequest,
  InvestmentToolResponse,
} from "@/types/investment";
import type { NegotiationEvidenceReference } from "@/types/negotiation";
import type { ScenarioState } from "@/types/scenarioHistory";
import type { RentFairPriceData, RentFairPriceRequest } from "@/types/valuation";
import type { WhatIfToolRequest, WhatIfToolResponse } from "@/types/whatIf";

const egpFormatter = new Intl.NumberFormat("en-EG", {
  maximumFractionDigits: 0,
});

const inputClass =
  "h-10 w-full rounded-lg border border-white/10 bg-surface/40 px-3 font-data-tabular text-sm text-on-surface outline-none transition-colors focus:border-primary-fixed-dim/50";

interface InvestmentIntelligencePanelProps {
  baseRequest: RentFairPriceRequest;
  baseResult: RentFairPriceData;
  workspaceId: number | null;
  propertyId: number | null;
  activeScenarioRequest: WhatIfToolRequest | null;
  activeScenarioResponse: WhatIfToolResponse | null;
  selectedScenario: ScenarioState | null;
  comparedScenarios?: ScenarioState[];
  bridgeStatus?: string;
}

interface InvestmentTargetOption {
  id: string;
  target: InvestmentRunTarget;
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

function evidenceLabel(reference: NegotiationEvidenceReference): string {
  const comparable = reference.comparable_id ? ` . ${reference.comparable_id}` : "";
  const valuation = reference.valuation_id ? ` . ${reference.valuation_id}` : "";
  return `${reference.source_tool}.${reference.field}${comparable}${valuation}`;
}

function targetOptions(
  activeScenarioRequest: WhatIfToolRequest | null,
  activeScenarioResponse: WhatIfToolResponse | null,
  selectedScenario: ScenarioState | null,
  comparedScenarios: ScenarioState[],
): InvestmentTargetOption[] {
  const activeModifications = activeScenarioRequest?.modifications as Record<string, unknown> | undefined;
  const options: InvestmentTargetOption[] = [
    {
      id: "base",
      target: "base",
      label: "Base valuation",
      eyebrow: "Base",
      description: "Uses the direct valuation snapshot.",
      scenarioId: null,
    },
    {
      id: "active_scenario",
      target: "active_scenario",
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
      target: "selected_scenario",
      label: selectedScenario ? selectedScenario.name : "Selected scenario",
      eyebrow: "Restored",
      description: selectedScenario ? `Uses persisted scenario ${selectedScenario.id}.` : "Open or restore a saved scenario first.",
      scenarioId: selectedScenario?.id ?? null,
      disabled: !selectedScenario,
    },
  ];

  for (const scenario of comparedScenarios) {
    if (scenario.id === selectedScenario?.id) continue;
    options.push({
      id: `compared_${scenario.id}`,
      target: "compared_scenario",
      label: scenario.name,
      eyebrow: "Compare",
      description: `Uses compared scenario ${scenario.id}.`,
      scenarioId: scenario.id,
    });
  }

  return options;
}

function preferredTarget(activeScenarioResponse: WhatIfToolResponse | null, selectedScenario: ScenarioState | null): string {
  if (activeScenarioResponse) return "active_scenario";
  if (selectedScenario) return "selected_scenario";
  return "base";
}

function positionTone(position: InvestmentToolResponse["investment_position"]): "positive" | "warning" | "default" {
  if (position === "Strong Opportunity" || position === "Moderate Opportunity") return "positive";
  if (position === "Caution" || position === "High Risk") return "warning";
  return "default";
}

function positionRank(position: InvestmentToolResponse["investment_position"]): number {
  if (position === "Strong Opportunity") return 5;
  if (position === "Moderate Opportunity") return 4;
  if (position === "Fairly Priced") return 3;
  if (position === "Caution") return 2;
  return 1;
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

function FindingList({ items, empty }: { items: InvestmentFinding[]; empty: string }) {
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

export function InvestmentRecommendationCard({ response }: { response: InvestmentToolResponse }) {
  const tone = positionTone(response.investment_position);
  return (
    <GlassPanel className="grid gap-4 p-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
            <BriefcaseBusiness className="h-4 w-4" />
            Investment Recommendation
          </span>
          <p
            className={cn(
              "mt-2 font-data-tabular text-xl",
              tone === "positive" && "text-tertiary-fixed-dim",
              tone === "warning" && "text-error",
              tone === "default" && "text-on-surface",
            )}
          >
            {response.investment_position}
          </p>
        </div>
        <span className="rounded-md border border-white/10 bg-surface/20 px-2.5 py-1.5 font-data-tabular text-[10px] text-outline">
          {response.source}
        </span>
      </div>
      <p className="text-sm leading-6 text-on-surface">{response.investment_position_reason}</p>
      <p className="text-sm leading-6 text-on-surface-variant">{response.investment_summary}</p>
      <EvidencePills references={response.investment_position_evidence} />
    </GlassPanel>
  );
}

export function InvestmentScoreCard({ response }: { response: InvestmentToolResponse }) {
  const gapTone = response.price_gap > 0 ? "warning" : response.price_gap < 0 ? "positive" : "default";
  return (
    <GlassPanel className="grid gap-4 p-5">
      <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
        <BarChart3 className="h-4 w-4" />
        Investment Scorecard
      </span>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <MetricTile label="Position" value={response.investment_position} tone={positionTone(response.investment_position)} />
        <MetricTile label="Confidence" value={response.confidence_level} />
        <MetricTile label="Fairness" value={response.fairness_status} />
        <MetricTile label="Fair Price" value={formatEgp(response.fair_price)} />
        <MetricTile label="Asking Price" value={formatEgp(response.asking_price)} />
        <MetricTile
          label="Price Gap"
          value={`${formatSignedEgp(response.price_gap)} (${formatPercent(response.price_gap_percentage)})`}
          tone={gapTone}
        />
      </div>
      <p className="text-sm leading-6 text-on-surface-variant">{response.confidence_reason}</p>
    </GlassPanel>
  );
}

export function InvestmentStrengthsCard({ response }: { response: InvestmentToolResponse }) {
  return (
    <GlassPanel className="grid gap-3 p-5">
      <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
        <BadgeCheck className="h-4 w-4" />
        Strengths
      </span>
      <FindingList items={response.strengths} empty="No strengths were returned." />
    </GlassPanel>
  );
}

export function InvestmentRisksCard({ response }: { response: InvestmentToolResponse }) {
  return (
    <GlassPanel className="grid gap-3 p-5">
      <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
        <ShieldAlert className="h-4 w-4" />
        Risks
      </span>
      <FindingList items={response.risks} empty="No risks were returned." />
    </GlassPanel>
  );
}

export function InvestmentUpsideCard({ response }: { response: InvestmentToolResponse }) {
  const scenario = response.what_if_summary.analysis;
  const hasPriceUpside = response.price_gap < 0;
  const hasScenarioUpside = Boolean(scenario && scenario.delta_value > 0);

  return (
    <GlassPanel className="grid gap-3 p-5">
      <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
        <TrendingUp className="h-4 w-4" />
        Upside
      </span>
      <div className="grid gap-3 sm:grid-cols-2">
        {hasPriceUpside && <MetricTile label="Value Gap" value={formatSignedEgp(response.price_gap)} tone="positive" />}
        {hasScenarioUpside && scenario && (
          <MetricTile
            label="Scenario Delta"
            value={`${formatSignedEgp(scenario.delta_value)} (${formatPercent(scenario.delta_percentage)})`}
            tone="positive"
          />
        )}
      </div>
      {!hasPriceUpside && !hasScenarioUpside && (
        <p className="text-sm text-on-surface-variant">No backend upside delta was returned for this run.</p>
      )}
      <p className="text-sm leading-6 text-on-surface-variant">{response.what_if_summary.reason}</p>
    </GlassPanel>
  );
}

export function InvestmentDownsideCard({ response }: { response: InvestmentToolResponse }) {
  const scenario = response.what_if_summary.analysis;
  const hasPriceDownside = response.price_gap > 0;
  const hasScenarioDownside = Boolean(scenario && scenario.delta_value <= 0);

  return (
    <GlassPanel className="grid gap-3 p-5">
      <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
        <TrendingDown className="h-4 w-4" />
        Downside
      </span>
      <div className="grid gap-3 sm:grid-cols-2">
        {hasPriceDownside && <MetricTile label="Premium Gap" value={formatSignedEgp(response.price_gap)} tone="warning" />}
        {hasScenarioDownside && scenario && (
          <MetricTile
            label="Scenario Delta"
            value={`${formatSignedEgp(scenario.delta_value)} (${formatPercent(scenario.delta_percentage)})`}
            tone={scenario.delta_value < 0 ? "warning" : "default"}
          />
        )}
      </div>
      {!hasPriceDownside && !hasScenarioDownside && (
        <p className="text-sm text-on-surface-variant">No backend downside delta was returned for this run.</p>
      )}
      <FindingList items={response.risks.slice(0, 2)} empty="No downside risk notes were returned." />
    </GlassPanel>
  );
}

export function InvestmentEvidenceCard({ response }: { response: InvestmentToolResponse }) {
  const observedRange =
    typeof response.comparable_summary.lowest_observed_price === "number"
      ? `${formatEgp(response.comparable_summary.lowest_observed_price)} - ${formatEgp(
          response.comparable_summary.highest_observed_price ?? response.comparable_summary.lowest_observed_price,
        )}`
      : "Unavailable";

  return (
    <GlassPanel className="grid gap-4 p-5">
      <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
        <FileSearch className="h-4 w-4" />
        Supporting Evidence
      </span>
      <div className="grid gap-4 lg:grid-cols-2">
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
          <p className="text-sm leading-6 text-on-surface-variant">Observed prices {observedRange}</p>
          <div className="flex flex-wrap gap-2">
            {response.comparable_summary.comparable_ids.length === 0 ? (
              <span className="text-sm text-on-surface-variant">No comparable ids were returned.</span>
            ) : (
              response.comparable_summary.comparable_ids.map((id) => (
                <span
                  key={id}
                  className="rounded-md border border-white/10 bg-surface/30 px-2.5 py-1.5 font-data-tabular text-[10px] text-on-surface-variant"
                >
                  {id}
                </span>
              ))
            )}
          </div>
        </div>
      </div>
      <EvidencePills references={response.investment_position_evidence} />
    </GlassPanel>
  );
}

function ComparisonMovement({ run, baseline }: { run: InvestmentRunRecord; baseline: InvestmentRunRecord }) {
  const delta = positionRank(run.response.investment_position) - positionRank(baseline.response.investment_position);
  if (delta > 0) {
    return (
      <span className="inline-flex items-center gap-1 rounded-md border border-tertiary-fixed-dim/25 bg-tertiary-fixed-dim/10 px-2 py-1 font-data-tabular text-[10px] text-tertiary-fixed-dim">
        <ArrowUp className="h-3 w-3" />
        Improved
      </span>
    );
  }
  if (delta < 0) {
    return (
      <span className="inline-flex items-center gap-1 rounded-md border border-error/25 bg-error/10 px-2 py-1 font-data-tabular text-[10px] text-error">
        <ArrowDown className="h-3 w-3" />
        Worse
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 rounded-md border border-white/10 bg-surface/20 px-2 py-1 font-data-tabular text-[10px] text-on-surface-variant">
      <ArrowRight className="h-3 w-3" />
      Neutral
    </span>
  );
}

export function InvestmentScenarioComparisonCard({ runs }: { runs: InvestmentRunRecord[] }) {
  if (runs.length <= 1) return null;
  const baseline = runs[0];

  return (
    <GlassPanel className="grid gap-3 p-5">
      <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
        <GitCompareArrows className="h-4 w-4" />
        Investment Scenario Comparison
      </span>
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {runs.map((run) => {
          const riskDelta = run.response.risks.length - baseline.response.risks.length;
          const opportunityDelta = run.response.strengths.length - baseline.response.strengths.length;
          return (
            <div key={run.key} className="grid gap-3 rounded-lg border border-white/10 bg-surface/20 p-3">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="truncate font-data-tabular text-sm text-on-surface">{run.label}</p>
                  <p className="mt-1 font-data-tabular text-[10px] text-outline">{run.target.replace("_", " ")}</p>
                </div>
                <ComparisonMovement run={run} baseline={baseline} />
              </div>
              <p className="text-sm text-on-surface-variant">{run.response.investment_position}</p>
              <div className="grid gap-2 sm:grid-cols-2">
                <MetricTile label="Gap" value={formatSignedEgp(run.response.price_gap)} tone={run.response.price_gap > 0 ? "warning" : run.response.price_gap < 0 ? "positive" : "default"} />
                <MetricTile label="Confidence" value={run.response.confidence_level} />
                <MetricTile label="Risk Change" value={riskDelta === 0 ? "0" : riskDelta > 0 ? `+${riskDelta}` : String(riskDelta)} tone={riskDelta > 0 ? "warning" : riskDelta < 0 ? "positive" : "default"} />
                <MetricTile label="Opportunity Change" value={opportunityDelta === 0 ? "0" : opportunityDelta > 0 ? `+${opportunityDelta}` : String(opportunityDelta)} tone={opportunityDelta > 0 ? "positive" : opportunityDelta < 0 ? "warning" : "default"} />
              </div>
            </div>
          );
        })}
      </div>
    </GlassPanel>
  );
}

function InvestmentResult({ response, runs }: { response: InvestmentToolResponse; runs: InvestmentRunRecord[] }) {
  return (
    <div className="grid gap-4">
      <InvestmentRecommendationCard response={response} />
      <InvestmentScoreCard response={response} />
      <div className="grid gap-4 lg:grid-cols-2">
        <InvestmentStrengthsCard response={response} />
        <InvestmentRisksCard response={response} />
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        <InvestmentUpsideCard response={response} />
        <InvestmentDownsideCard response={response} />
      </div>
      <InvestmentEvidenceCard response={response} />
      <InvestmentScenarioComparisonCard runs={runs} />
    </div>
  );
}

export function InvestmentIntelligencePanel({
  baseRequest,
  baseResult,
  workspaceId,
  propertyId,
  activeScenarioRequest,
  activeScenarioResponse,
  selectedScenario,
  comparedScenarios = [],
  bridgeStatus = "idle",
}: InvestmentIntelligencePanelProps) {
  const {
    lastResponse,
    runs,
    isLoading,
    error,
    selectedScenarioId,
    selectedScenarioName,
    runInvestmentAnalysis,
    selectScenario,
  } = useInvestmentStore();
  const [selectedTarget, setSelectedTarget] = React.useState<string>(() =>
    preferredTarget(activeScenarioResponse, selectedScenario),
  );
  const [askingPriceInput, setAskingPriceInput] = React.useState(() =>
    String(defaultAskingPrice(baseRequest, baseResult)),
  );
  const abortRef = React.useRef<AbortController | null>(null);
  const options = React.useMemo(
    () => targetOptions(activeScenarioRequest, activeScenarioResponse, selectedScenario, comparedScenarios),
    [activeScenarioRequest, activeScenarioResponse, comparedScenarios, selectedScenario],
  );
  const selectedOption = options.find((option) => option.id === selectedTarget) ?? options[0];
  const askingPrice = positiveIntegerFromInput(askingPriceInput);
  const hasContext = typeof workspaceId === "number" && typeof propertyId === "number";
  const canRun = hasContext && Boolean(selectedOption && !selectedOption.disabled) && askingPrice !== null && !isLoading;

  React.useEffect(() => {
    const preferred = preferredTarget(activeScenarioResponse, selectedScenario);
    const current = options.find((option) => option.id === selectedTarget);
    if (!current || current.disabled) {
      const next = options.find((option) => option.id === preferred && !option.disabled) ?? options[0];
      setSelectedTarget(next.id);
      selectScenario(next.scenarioId, next.label);
    }
  }, [activeScenarioResponse, options, selectScenario, selectedScenario, selectedTarget]);

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

  const changeTarget = React.useCallback(
    (option: InvestmentTargetOption) => {
      setSelectedTarget(option.id);
      selectScenario(option.scenarioId, option.label);
    },
    [selectScenario],
  );

  const submitInvestment = React.useCallback(() => {
    if (!hasContext || !selectedOption || selectedOption.disabled || askingPrice === null) return;
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    selectScenario(selectedOption.scenarioId, selectedOption.label);

    const request: InvestmentToolRequest = {
      workspace_id: workspaceId,
      property_id: propertyId,
      scenario_id: selectedOption.scenarioId,
      asking_price_egp: askingPrice,
      ...(selectedOption.modifications ? { what_if_modifications: selectedOption.modifications } : {}),
    };

    void runInvestmentAnalysis(
      request,
      {
        target: selectedOption.target,
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
  }, [askingPrice, hasContext, propertyId, runInvestmentAnalysis, selectScenario, selectedOption, workspaceId]);

  return (
    <section className="grid gap-4">
      <div className="flex flex-wrap items-end justify-between gap-4 border-b border-white/5 pb-2">
        <div>
          <p className="font-label-caps text-xs text-primary-fixed-dim">Investment Intelligence</p>
          <h3 className="mt-1 font-body-md text-on-surface">Decision support</h3>
        </div>
        <span className="font-data-tabular text-[10px] text-outline">POST /v1/copilot/tools/investment</span>
      </div>

      <GlassPanel className="grid gap-5 p-5">
        {!hasContext && (
          <div className="rounded-lg border border-white/10 bg-surface/20 p-3">
            <p className="font-label-caps text-[10px] text-outline">Property Context {bridgeStatus}</p>
            <p className="mt-1 text-sm text-on-surface-variant">Investment intelligence is waiting for the backend property context.</p>
          </div>
        )}

        <div className="grid gap-3 md:grid-cols-3 xl:grid-cols-4">
          {options.map((option) => {
            const selected = selectedTarget === option.id;
            return (
              <button
                key={option.id}
                type="button"
                disabled={option.disabled}
                onClick={() => changeTarget(option)}
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
              aria-label="Investment asking price"
              className={inputClass}
              type="number"
              min="1"
              value={askingPriceInput}
              onChange={(event) => setAskingPriceInput(event.currentTarget.value)}
            />
          </label>
          <Button type="button" variant="holo" className="w-full md:w-auto" onClick={submitInvestment} disabled={!canRun}>
            <CircleDollarSign className="h-4 w-4" />
            Run Investment
          </Button>
        </div>

        <div className="flex flex-wrap gap-2">
          <span className="rounded-md border border-white/10 bg-surface/20 px-2.5 py-1.5 font-data-tabular text-[10px] text-outline">
            Scenario {selectedScenarioId ?? "Base"}
          </span>
          {selectedScenarioName && (
            <span className="rounded-md border border-white/10 bg-surface/20 px-2.5 py-1.5 font-data-tabular text-[10px] text-on-surface-variant">
              {selectedScenarioName}
            </span>
          )}
        </div>
      </GlassPanel>

      {error && (
        <GlassPanel className="border-error/25 bg-error/5 p-5">
          <p className="font-label-caps text-xs text-error">Investment Error</p>
          <p className="mt-1 text-sm text-on-surface-variant">{error.message}</p>
        </GlassPanel>
      )}

      {lastResponse ? (
        <InvestmentResult response={lastResponse} runs={runs} />
      ) : (
        <GlassPanel className="p-5">
          <p className="font-label-caps text-xs text-primary-fixed-dim">Investment Results</p>
          <p className="mt-1 text-sm text-on-surface-variant">No investment package has been generated for this valuation.</p>
        </GlassPanel>
      )}
    </section>
  );
}
