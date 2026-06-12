import * as React from "react";
import { motion } from "framer-motion";
import {
  ArrowDown,
  ArrowRight,
  ArrowUp,
  Bath,
  BedDouble,
  CalendarClock,
  CheckCircle2,
  ChevronRight,
  Clock3,
  FolderOpen,
  GitBranch,
  GitCompareArrows,
  History,
  ListChecks,
  PanelRightOpen,
  Play,
  RotateCcw,
  Save,
  Sparkles,
  Undo2,
  X,
} from "lucide-react";
import { revealItem, stagedReveal } from "@/animations/motion";
import { Button } from "@/components/ui/button";
import { GlassPanel } from "@/components/ui/glass";
import { InvestmentIntelligencePanel } from "@/features/investment/InvestmentIntelligencePanel";
import { cn } from "@/lib/utils";
import { useScenarioHistoryStore } from "@/store/scenarioHistoryStore";
import { useWhatIfStore } from "@/store/whatIfStore";
import { NegotiationIntelligencePanel } from "./NegotiationIntelligencePanel";
import {
  SCENARIO_HISTORY_META_KEY,
  ScenarioHistoryMeta,
  ScenarioState,
  ScenarioTreeNode,
} from "@/types/scenarioHistory";
import {
  AMENITY_OPTIONS,
  CATEGORY_PROPERTY_TYPES,
  PropertyCategory,
  PropertyType,
  RentFairPriceData,
  RentFairPriceRequest,
} from "@/types/valuation";
import type { ComparableToolItem, FeatureChange, FeatureChanges, WhatIfToolResponse } from "@/types/whatIf";

const egpFormatter = new Intl.NumberFormat("en-EG", {
  maximumFractionDigits: 0,
});

const inputClass =
  "h-10 w-full rounded-lg border border-white/10 bg-surface/40 px-3 font-data-tabular text-sm text-on-surface outline-none transition-colors focus:border-primary-fixed-dim/50";

const amenityLabels = new Map(AMENITY_OPTIONS.map((option) => [option.symbol, option.label]));
const scenarioAmenitySymbols = ["CP", "SY", "CH"];

type ScenarioDraft = Pick<
  RentFairPriceRequest,
  | "property_type"
  | "size_sqm"
  | "bedrooms"
  | "bathrooms"
  | "floor_number"
  | "building_quality"
  | "furnishing_status"
  | "view_type"
  | "compound_name"
  | "amenities"
>;

interface WhatIfScenarioPanelProps {
  baseRequest: RentFairPriceRequest;
  baseResult: RentFairPriceData;
  workspaceId: number | null;
  propertyId: number | null;
  scenarioId?: number | null;
  bridgeStatus?: string;
}

interface ScenarioModificationControlsProps {
  baseRequest: RentFairPriceRequest;
  draft: ScenarioDraft;
  hasChanges: boolean;
  isLoading: boolean;
  canRun: boolean;
  onDraftChange: <TKey extends keyof ScenarioDraft>(key: TKey, value: ScenarioDraft[TKey]) => void;
  onAmenityToggle: (symbol: string) => void;
  onRun: () => void;
  onResetDraft: () => void;
}

interface ScenarioDeltaSummaryProps {
  baseRequest: RentFairPriceRequest;
  baseResult: RentFairPriceData;
  scenarioRequest: ScenarioDraft;
  response: WhatIfToolResponse;
}

interface FeatureChangesListProps {
  changes: FeatureChanges;
}

interface ScenarioAssumptionsProps {
  assumptions: string[];
}

interface ScenarioExplainabilityProps {
  response: WhatIfToolResponse;
}

interface ScenarioComparablesProps {
  comparables: ComparableToolItem[];
}

interface ScenarioHistoryPanelProps {
  scenarios: ScenarioState[];
  tree: ScenarioTreeNode[];
  lineage: ScenarioState[];
  selectedScenario: ScenarioState | null;
  comparedScenarioIds: number[];
  saveName: string;
  canSave: boolean;
  isLoading: boolean;
  isSaving: boolean;
  isRestoring: boolean;
  onSaveNameChange: (name: string) => void;
  onSaveScenario: () => void;
  onOpenScenario: (scenario: ScenarioState) => void;
  onRestoreScenario: (scenario: ScenarioState) => void;
  onToggleCompare: (scenarioId: number) => void;
  onOpenComparison: () => void;
}

interface ScenarioTimelineProps {
  scenarios: ScenarioState[];
  selectedScenarioId: number | null;
  comparedScenarioIds: number[];
  onOpenScenario: (scenario: ScenarioState) => void;
  onRestoreScenario: (scenario: ScenarioState) => void;
  onToggleCompare: (scenarioId: number) => void;
}

interface ScenarioLineageTreeProps {
  tree: ScenarioTreeNode[];
  selectedScenarioId: number | null;
  onOpenScenario: (scenario: ScenarioState) => void;
}

interface ScenarioTreeBranchProps {
  nodes: ScenarioTreeNode[];
  selectedScenarioId: number | null;
  onOpenScenario: (scenario: ScenarioState) => void;
  depth?: number;
}

interface ScenarioComparisonDrawerProps {
  isOpen: boolean;
  scenarios: ScenarioState[];
  comparedScenarioIds: number[];
  onClose: () => void;
  onClear: () => void;
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

function formatNullable(value: unknown): string {
  if (value === null || value === undefined || value === "") return "Unspecified";
  if (Array.isArray(value)) return value.length ? value.map((item) => amenityLabels.get(String(item)) ?? String(item)).join(", ") : "None";
  if (typeof value === "boolean") return value ? "Yes" : "No";
  return String(value);
}

function optionalNumber(value: string): number | null {
  if (value.trim() === "") return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function requiredNumber(value: string, fallback: number): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function sortedAmenities(value?: string[]): string[] {
  return [...(value ?? [])].map(String).sort();
}

function sameJson(a: unknown, b: unknown): boolean {
  return JSON.stringify(a) === JSON.stringify(b);
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function scenarioDraftFromRequest(request: RentFairPriceRequest): ScenarioDraft {
  return {
    property_type: request.property_type,
    size_sqm: request.size_sqm,
    bedrooms: request.bedrooms ?? null,
    bathrooms: request.bathrooms ?? null,
    floor_number: request.floor_number ?? null,
    building_quality: request.building_quality ?? null,
    furnishing_status: request.furnishing_status ?? null,
    view_type: request.view_type ?? null,
    compound_name: request.compound_name ?? null,
    amenities: sortedAmenities(request.amenities),
  };
}

const scenarioDraftKeys: Array<keyof ScenarioDraft> = [
  "property_type",
  "size_sqm",
  "bedrooms",
  "bathrooms",
  "floor_number",
  "building_quality",
  "furnishing_status",
  "view_type",
  "compound_name",
];

function buildDraftModifications(baseDraft: ScenarioDraft, draft: ScenarioDraft): Record<string, unknown> {
  const modifications: Record<string, unknown> = {};

  for (const key of scenarioDraftKeys) {
    const base = baseDraft[key] ?? null;
    const next = draft[key] ?? null;
    if (!sameJson(base, next)) {
      modifications[key] = next;
    }
  }

  const baseAmenities = sortedAmenities(baseDraft.amenities);
  const nextAmenities = sortedAmenities(draft.amenities);
  if (!sameJson(baseAmenities, nextAmenities)) {
    modifications.amenities = nextAmenities;
  }

  return modifications;
}

function buildScenarioModifications(baseRequest: RentFairPriceRequest, draft: ScenarioDraft): Record<string, unknown> {
  return buildDraftModifications(scenarioDraftFromRequest(baseRequest), draft);
}

function stripScenarioMetadata(modifications: Record<string, unknown>): Record<string, unknown> {
  const { [SCENARIO_HISTORY_META_KEY]: _meta, ...rest } = modifications;
  return rest;
}

function scenarioMeta(scenario: ScenarioState): ScenarioHistoryMeta | null {
  const value = scenario.modifications[SCENARIO_HISTORY_META_KEY];
  return isRecord(value) ? (value as ScenarioHistoryMeta) : null;
}

function toggleDraftAmenity(draft: ScenarioDraft, symbol: string, enabled: boolean): ScenarioDraft {
  const amenities = new Set(draft.amenities);
  if (enabled) {
    amenities.add(symbol);
  } else {
    amenities.delete(symbol);
  }
  return { ...draft, amenities: Array.from(amenities).sort() };
}

function applyModificationEntry(draft: ScenarioDraft, key: string, value: unknown): ScenarioDraft {
  if (key === "valuation_inputs" && isRecord(value)) {
    return applyScenarioModifications(draft, value);
  }
  if (key === "area" || key === "size") {
    return typeof value === "number" ? { ...draft, size_sqm: value } : draft;
  }
  if (key === "finishing") {
    return { ...draft, building_quality: typeof value === "string" ? value : null };
  }
  if (key === "furnishing") {
    return { ...draft, furnishing_status: typeof value === "string" ? value : null };
  }
  if (key === "furnished") {
    return typeof value === "boolean" ? { ...draft, furnishing_status: value ? "furnished" : "unfurnished" } : draft;
  }
  if (key === "parking") return toggleDraftAmenity(draft, "CP", value === true);
  if (key === "gym") return toggleDraftAmenity(draft, "SY", value === true);
  if (key === "clubhouse") return toggleDraftAmenity(draft, "CH", value === true);
  if (key === "amenities_added" && Array.isArray(value)) {
    return value.reduce((current, symbol) => toggleDraftAmenity(current, String(symbol), true), draft);
  }
  if (key === "amenities_removed" && Array.isArray(value)) {
    return value.reduce((current, symbol) => toggleDraftAmenity(current, String(symbol), false), draft);
  }
  if (key === "amenities" && Array.isArray(value)) {
    return { ...draft, amenities: sortedAmenities(value.map(String)) };
  }
  if (key === "property_type" && typeof value === "string") {
    return { ...draft, property_type: value as PropertyType };
  }
  if (key === "size_sqm" && typeof value === "number") {
    return { ...draft, size_sqm: value };
  }
  if (["bedrooms", "bathrooms", "floor_number"].includes(key)) {
    return { ...draft, [key]: typeof value === "number" ? value : null };
  }
  if (["building_quality", "furnishing_status", "view_type", "compound_name"].includes(key)) {
    return { ...draft, [key]: typeof value === "string" ? value : null };
  }
  return draft;
}

function applyScenarioModifications(baseDraft: ScenarioDraft, modifications: Record<string, unknown>): ScenarioDraft {
  return Object.entries(stripScenarioMetadata(modifications)).reduce(
    (draft, [key, value]) => applyModificationEntry(draft, key, value),
    baseDraft,
  );
}

function scenarioDraftFromLineage(baseRequest: RentFairPriceRequest, lineage: ScenarioState[]): ScenarioDraft {
  return lineage.reduce(
    (draft, scenario) => applyScenarioModifications(draft, scenario.modifications),
    scenarioDraftFromRequest(baseRequest),
  );
}

function scenarioCreatedLabel(scenario: ScenarioState): string {
  if (!scenario.created_at) return "Saved";
  const date = new Date(scenario.created_at);
  if (Number.isNaN(date.getTime())) return "Saved";
  return date.toLocaleString("en-EG", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function scenarioDeltaValue(scenario: ScenarioState): number | null {
  const meta = scenarioMeta(scenario);
  if (typeof meta?.signed_delta_value === "number") return meta.signed_delta_value;
  return scenario.delta_value;
}

function scenarioValuationValue(scenario: ScenarioState): number | null {
  const meta = scenarioMeta(scenario);
  return typeof meta?.scenario_valuation === "number" ? meta.scenario_valuation : null;
}

function defaultScenarioName(count: number, response?: WhatIfToolResponse | null): string {
  const suffix = response ? ` ${formatSignedEgp(response.delta_value)}` : "";
  return `Scenario ${String.fromCharCode(65 + (count % 26))}${suffix}`;
}

function rangeLabel(low?: number | null, high?: number | null): string {
  if (typeof low !== "number" || typeof high !== "number") return "Unavailable";
  return `${formatEgp(low)} - ${formatEgp(high)}`;
}

function deltaTone(value: number): string {
  if (value > 0) return "border-tertiary-fixed-dim/25 bg-tertiary-fixed-dim/10 text-tertiary-fixed-dim";
  if (value < 0) return "border-error/25 bg-error/10 text-error";
  return "border-white/10 bg-surface/30 text-on-surface-variant";
}

function DeltaIcon({ value }: { value: number }) {
  if (value > 0) return <ArrowUp className="h-4 w-4" />;
  if (value < 0) return <ArrowDown className="h-4 w-4" />;
  return <ArrowRight className="h-4 w-4" />;
}

function propertyTypesFor(category?: PropertyCategory): PropertyType[] {
  return CATEGORY_PROPERTY_TYPES[category ?? "residential_rent"] ?? CATEGORY_PROPERTY_TYPES.residential_rent;
}

function amenityOptionsFor(category?: PropertyCategory) {
  const active = category ?? "residential_rent";
  const categoryOptions = AMENITY_OPTIONS.filter((option) => option.categories.includes(active));
  const extraOptions = AMENITY_OPTIONS.filter((option) => scenarioAmenitySymbols.includes(option.symbol));
  return [...new Map([...categoryOptions, ...extraOptions].map((option) => [option.symbol, option])).values()];
}

function changeImpact(change: FeatureChange, group: keyof FeatureChanges): number {
  if (group === "added") return 1;
  if (group === "removed") return -1;
  if (typeof change.before === "number" && typeof change.after === "number") {
    const feature = change.feature.toLowerCase();
    if (["size", "bedrooms", "bathrooms"].some((key) => feature.includes(key))) {
      return change.after - change.before;
    }
  }
  return 0;
}

function changeTone(change: FeatureChange, group: keyof FeatureChanges): string {
  const impact = changeImpact(change, group);
  if (impact > 0) return "border-tertiary-fixed-dim/25 bg-tertiary-fixed-dim/10 text-tertiary-fixed-dim";
  if (impact < 0) return "border-error/25 bg-error/10 text-error";
  return "border-white/10 bg-surface/30 text-on-surface-variant";
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="grid gap-2">
      <span className="font-label-caps text-[10px] text-on-surface-variant">{label}</span>
      {children}
    </label>
  );
}

export function ScenarioModificationControls({
  baseRequest,
  draft,
  hasChanges,
  isLoading,
  canRun,
  onDraftChange,
  onAmenityToggle,
  onRun,
  onResetDraft,
}: ScenarioModificationControlsProps) {
  const propertyTypes = propertyTypesFor(baseRequest.property_category);
  const options = propertyTypes.includes(draft.property_type)
    ? propertyTypes
    : [draft.property_type, ...propertyTypes];
  const amenities = amenityOptionsFor(baseRequest.property_category);

  return (
    <GlassPanel className="grid gap-5 p-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
          <Sparkles className="h-4 w-4" />
          Scenario Modifications
        </span>
        <span className="font-data-tabular text-[10px] text-outline">{hasChanges ? "Modified" : "Baseline"}</span>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Field label="Property Type">
          <select
            aria-label="Scenario property type"
            className={inputClass}
            value={draft.property_type}
            onChange={(event) => onDraftChange("property_type", event.currentTarget.value as PropertyType)}
          >
            {options.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </Field>
        <Field label="Area sqm">
          <input
            aria-label="Scenario area"
            className={inputClass}
            type="number"
            min="1"
            value={draft.size_sqm}
            onChange={(event) => onDraftChange("size_sqm", requiredNumber(event.currentTarget.value, draft.size_sqm))}
          />
        </Field>
        <Field label="Floor">
          <input
            aria-label="Scenario floor"
            className={inputClass}
            type="number"
            value={draft.floor_number ?? ""}
            onChange={(event) => onDraftChange("floor_number", optionalNumber(event.currentTarget.value))}
          />
        </Field>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Field label="Bedrooms">
          <input
            aria-label="Scenario bedrooms"
            className={inputClass}
            type="number"
            min="0"
            value={draft.bedrooms ?? ""}
            onChange={(event) => onDraftChange("bedrooms", optionalNumber(event.currentTarget.value))}
          />
        </Field>
        <Field label="Bathrooms">
          <input
            aria-label="Scenario bathrooms"
            className={inputClass}
            type="number"
            min="0"
            value={draft.bathrooms ?? ""}
            onChange={(event) => onDraftChange("bathrooms", optionalNumber(event.currentTarget.value))}
          />
        </Field>
        <Field label="Finishing">
          <select
            aria-label="Scenario finishing"
            className={inputClass}
            value={draft.building_quality ?? ""}
            onChange={(event) => onDraftChange("building_quality", event.currentTarget.value || null)}
          >
            <option value="">Unspecified</option>
            <option value="standard">Standard</option>
            <option value="premium">Premium</option>
            <option value="luxury">Luxury</option>
            <option value="renovated">Renovated</option>
            <option value="new">New</option>
          </select>
        </Field>
        <Field label="Furnishing">
          <select
            aria-label="Scenario furnishing"
            className={inputClass}
            value={draft.furnishing_status ?? ""}
            onChange={(event) => onDraftChange("furnishing_status", event.currentTarget.value || null)}
          >
            <option value="">Unspecified</option>
            <option value="furnished">Furnished</option>
            <option value="unfurnished">Unfurnished</option>
          </select>
        </Field>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Field label="View">
          <input
            aria-label="Scenario view"
            className={inputClass}
            value={draft.view_type ?? ""}
            onChange={(event) => onDraftChange("view_type", event.currentTarget.value || null)}
          />
        </Field>
        <Field label="Compound">
          <input
            aria-label="Scenario compound"
            className={inputClass}
            value={draft.compound_name ?? ""}
            onChange={(event) => onDraftChange("compound_name", event.currentTarget.value || null)}
          />
        </Field>
      </div>

      <div className="grid gap-3">
        <span className="font-label-caps text-[10px] text-on-surface-variant">Amenities</span>
        <div className="flex flex-wrap gap-2">
          {amenities.map((amenity) => {
            const selected = draft.amenities.includes(amenity.symbol);
            return (
              <button
                key={amenity.symbol}
                type="button"
                aria-pressed={selected}
                onClick={() => onAmenityToggle(amenity.symbol)}
                className={cn(
                  "rounded-md border px-2.5 py-1.5 font-data-tabular text-xs transition-colors",
                  selected
                    ? "border-tertiary-fixed-dim/40 bg-tertiary-fixed-dim/10 text-tertiary-fixed-dim"
                    : "border-white/10 bg-surface/30 text-on-surface-variant hover:border-white/20",
                )}
              >
                {amenity.label}
              </button>
            );
          })}
        </div>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row">
        <Button type="button" variant="holo" onClick={onRun} disabled={!canRun || isLoading} className="flex-1">
          <Play className="h-4 w-4" />
          {isLoading ? "Running" : "Run Scenario"}
        </Button>
        <Button type="button" variant="ghost" onClick={onResetDraft}>
          <RotateCcw className="h-4 w-4" />
          Reset
        </Button>
      </div>
    </GlassPanel>
  );
}

export function ScenarioDeltaSummary({ baseRequest, baseResult, scenarioRequest, response }: ScenarioDeltaSummaryProps) {
  const deltaClass = deltaTone(response.delta_value);

  const propertyRows = [
    ["Fair Price", formatEgp(response.base_valuation), formatEgp(response.scenario_valuation)],
    ["Range", rangeLabel(baseResult.range_low_egp, baseResult.range_high_egp), "Unavailable"],
    ["Confidence", baseResult.confidence.label, response.confidence_level],
    ["Fairness", baseResult.flag === "OK" ? "Within Fair Value" : baseResult.flag.replace(/_/g, " "), response.fairness_status],
    ["Area", `${baseRequest.size_sqm} sqm`, `${scenarioRequest.size_sqm} sqm`],
    ["Beds / Baths", `${formatNullable(baseRequest.bedrooms)} / ${formatNullable(baseRequest.bathrooms)}`, `${formatNullable(scenarioRequest.bedrooms)} / ${formatNullable(scenarioRequest.bathrooms)}`],
    ["Floor", formatNullable(baseRequest.floor_number), formatNullable(scenarioRequest.floor_number)],
    ["Finishing", formatNullable(baseRequest.building_quality), formatNullable(scenarioRequest.building_quality)],
    ["Furnishing", formatNullable(baseRequest.furnishing_status), formatNullable(scenarioRequest.furnishing_status)],
    ["Amenities", formatNullable(baseRequest.amenities), formatNullable(scenarioRequest.amenities)],
  ];

  return (
    <div className="grid gap-4">
      <div className="grid gap-3 md:grid-cols-4">
        <div className="rounded-lg border border-white/10 bg-surface/30 p-4">
          <span className="font-label-caps text-[10px] text-outline">Base Valuation</span>
          <p className="mt-1 font-data-tabular text-lg text-on-surface">{formatEgp(response.base_valuation)}</p>
        </div>
        <div className="rounded-lg border border-white/10 bg-surface/30 p-4">
          <span className="font-label-caps text-[10px] text-outline">Scenario Valuation</span>
          <p className="mt-1 font-data-tabular text-lg text-on-surface">{formatEgp(response.scenario_valuation)}</p>
        </div>
        <div className={cn("rounded-lg border p-4", deltaClass)}>
          <span className="font-label-caps text-[10px]">Delta EGP</span>
          <p className="mt-1 inline-flex items-center gap-2 font-data-tabular text-lg">
            <DeltaIcon value={response.delta_value} />
            {formatSignedEgp(response.delta_value)}
          </p>
        </div>
        <div className={cn("rounded-lg border p-4", deltaClass)}>
          <span className="font-label-caps text-[10px]">Delta %</span>
          <p className="mt-1 font-data-tabular text-lg">{formatPercent(response.delta_percentage)}</p>
        </div>
      </div>

      <GlassPanel className="overflow-hidden p-0">
        <div className="grid grid-cols-[minmax(116px,0.75fr)_1fr_1fr] border-b border-white/10 bg-surface/30 font-label-caps text-[10px] text-outline">
          <span className="p-3">Metric</span>
          <span className="p-3">Base Property</span>
          <span className="p-3">Scenario Property</span>
        </div>
        {propertyRows.map(([label, base, scenario]) => (
          <div key={label} className="grid grid-cols-[minmax(116px,0.75fr)_1fr_1fr] border-b border-white/5 last:border-b-0">
            <span className="p-3 font-label-caps text-[10px] text-on-surface-variant">{label}</span>
            <span className="min-w-0 p-3 font-data-tabular text-xs text-on-surface">{base}</span>
            <span className="min-w-0 p-3 font-data-tabular text-xs text-on-surface">{scenario}</span>
          </div>
        ))}
      </GlassPanel>
    </div>
  );
}

export function FeatureChangesList({ changes }: FeatureChangesListProps) {
  const groups: Array<[keyof FeatureChanges, string]> = [
    ["added", "Positive Changes"],
    ["removed", "Negative Changes"],
    ["modified", "Neutral Changes"],
  ];
  const total = groups.reduce((count, [key]) => count + changes[key].length, 0);

  return (
    <GlassPanel className="grid gap-4 p-5">
      <div className="flex items-center justify-between gap-3">
        <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
          <GitCompareArrows className="h-4 w-4" />
          Feature Changes
        </span>
        <span className="font-data-tabular text-[10px] text-outline">{total} changes</span>
      </div>
      {total === 0 ? (
        <p className="text-sm text-on-surface-variant">No feature changes were returned for this scenario.</p>
      ) : (
        <div className="grid gap-3 md:grid-cols-3">
          {groups.map(([key, label]) => (
            <div key={key} className="grid content-start gap-2">
              <span className="font-label-caps text-[10px] text-outline">{label}</span>
              {changes[key].length === 0 ? (
                <span className="rounded-lg border border-white/10 bg-surface/20 p-3 text-xs text-on-surface-variant">None</span>
              ) : (
                changes[key].map((change, index) => (
                  <div key={`${change.feature}-${index}`} className={cn("rounded-lg border p-3", changeTone(change, key))}>
                    <p className="font-label-caps text-xs">{change.feature}</p>
                    <p className="mt-1 font-data-tabular text-xs">
                      {formatNullable(change.before)} <ArrowRight className="inline h-3 w-3" /> {formatNullable(change.after)}
                      {change.unit ? ` ${change.unit}` : ""}
                    </p>
                  </div>
                ))
              )}
            </div>
          ))}
        </div>
      )}
    </GlassPanel>
  );
}

export function ScenarioAssumptions({ assumptions }: ScenarioAssumptionsProps) {
  return (
    <GlassPanel className="grid gap-4 p-5">
      <div className="flex items-center justify-between gap-3">
        <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
          <ListChecks className="h-4 w-4" />
          Scenario Assumptions
        </span>
        <span className="font-data-tabular text-[10px] text-outline">{assumptions.length} unknowns</span>
      </div>
      {assumptions.length === 0 ? (
        <p className="text-sm text-on-surface-variant">No unknown scenario assumptions were flagged.</p>
      ) : (
        <div className="flex flex-wrap gap-2">
          {assumptions.map((assumption) => (
            <span key={assumption} className="rounded-md border border-white/10 bg-surface/30 px-3 py-2 font-data-tabular text-xs text-on-surface-variant">
              {assumption}
            </span>
          ))}
        </div>
      )}
    </GlassPanel>
  );
}

export function ScenarioExplainability({ response }: ScenarioExplainabilityProps) {
  const explanation = response.explainability;
  return (
    <GlassPanel className="grid gap-4 p-5">
      <div className="flex items-center justify-between gap-3">
        <span className="font-label-caps text-xs text-primary-fixed-dim">Scenario Explainability</span>
        <span className="font-data-tabular text-[10px] text-outline">{explanation.valuation_id}</span>
      </div>
      <div className="grid gap-3 text-sm leading-6 text-on-surface-variant">
        <p>{explanation.summary}</p>
        <p>{explanation.why_this_price}</p>
        <p>{explanation.strongest_factors}</p>
        <p>{explanation.confidence_reason}</p>
      </div>
      <div className="grid gap-2 border-t border-white/5 pt-4">
        <span className="font-label-caps text-[10px] text-outline">Feature Drivers</span>
        {explanation.feature_drivers.length === 0 ? (
          <span className="text-sm text-on-surface-variant">No feature drivers returned for this scenario.</span>
        ) : (
          <div className="grid gap-2 md:grid-cols-2">
            {explanation.feature_drivers.slice(0, 6).map((driver, index) => (
              <div key={index} className="rounded-lg border border-white/10 bg-surface/20 p-3">
                <p className="truncate font-data-tabular text-xs text-on-surface">{JSON.stringify(driver)}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </GlassPanel>
  );
}

export function ScenarioComparables({ comparables }: ScenarioComparablesProps) {
  return (
    <GlassPanel className="grid gap-4 p-5">
      <div className="flex items-center justify-between gap-3">
        <span className="font-label-caps text-xs text-primary-fixed-dim">Scenario Comparables</span>
        <span className="font-data-tabular text-[10px] text-outline">{comparables.length} shown</span>
      </div>
      {comparables.length === 0 ? (
        <p className="text-sm text-on-surface-variant">No scenario comparables were returned.</p>
      ) : (
        <div className="grid gap-3 md:grid-cols-2">
          {comparables.map((comparable) => (
            <div key={comparable.comparable_id} className="rounded-lg border border-white/10 bg-surface/20 p-4">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="truncate font-data-tabular text-sm font-semibold text-on-surface">{comparable.comparable_id}</p>
                  <p className="mt-1 truncate text-xs text-on-surface-variant">{comparable.compound_name ?? "Comparable evidence"}</p>
                </div>
                <span className="shrink-0 rounded-md border border-primary-fixed-dim/20 px-2 py-1 font-data-tabular text-xs text-primary-fixed-dim">
                  {formatEgp(comparable.price)}
                </span>
              </div>
              <div className="mt-4 grid grid-cols-3 gap-2 font-data-tabular text-xs text-on-surface-variant">
                <span>{comparable.size_sqm} sqm</span>
                <span className="inline-flex items-center gap-1">
                  <BedDouble className="h-3 w-3" />
                  {comparable.bedrooms}
                </span>
                <span className="inline-flex items-center gap-1">
                  <Bath className="h-3 w-3" />
                  {comparable.bathrooms}
                </span>
              </div>
              <p className="mt-3 text-xs leading-5 text-on-surface-variant">
                {(comparable.distance_km ?? 0).toFixed(2)}km away{comparable.similarity_reason ? ` | ${comparable.similarity_reason}` : ""}
              </p>
            </div>
          ))}
        </div>
      )}
    </GlassPanel>
  );
}

function ScenarioTimeline({
  scenarios,
  selectedScenarioId,
  comparedScenarioIds,
  onOpenScenario,
  onRestoreScenario,
  onToggleCompare,
}: ScenarioTimelineProps) {
  const ordered = [...scenarios].sort((a, b) => {
    const aTime = a.created_at ? new Date(a.created_at).getTime() : a.id;
    const bTime = b.created_at ? new Date(b.created_at).getTime() : b.id;
    return aTime - bTime;
  });

  return (
    <GlassPanel className="grid gap-4 p-5">
      <div className="flex items-center justify-between gap-3">
        <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
          <Clock3 className="h-4 w-4" />
          Scenario Timeline
        </span>
        <span className="font-data-tabular text-[10px] text-outline">{ordered.length} saved</span>
      </div>

      {ordered.length === 0 ? (
        <p className="text-sm text-on-surface-variant">No saved scenarios yet.</p>
      ) : (
        <div className="grid gap-3">
          {ordered.map((scenario, index) => {
            const selected = selectedScenarioId === scenario.id;
            const compared = comparedScenarioIds.includes(scenario.id);
            const delta = scenarioDeltaValue(scenario);
            const valuation = scenarioValuationValue(scenario);
            return (
              <div key={scenario.id} className="grid grid-cols-[18px_1fr] gap-3">
                <div className="grid justify-items-center">
                  <span className={cn("mt-2 h-2.5 w-2.5 rounded-full", selected ? "bg-primary-fixed-dim" : "bg-outline")} />
                  {index < ordered.length - 1 && <span className="mt-1 h-full min-h-8 w-px bg-white/10" />}
                </div>
                <div className={cn("rounded-lg border p-3", selected ? "border-primary-fixed-dim/40 bg-primary-fixed-dim/10" : "border-white/10 bg-surface/20")}>
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <button
                      type="button"
                      onClick={() => onOpenScenario(scenario)}
                      className="min-w-0 text-left"
                    >
                      <span className="block truncate font-data-tabular text-sm text-on-surface">{scenario.name}</span>
                      <span className="mt-1 inline-flex items-center gap-1.5 font-data-tabular text-[10px] text-on-surface-variant">
                        <CalendarClock className="h-3 w-3" />
                        {scenarioCreatedLabel(scenario)}
                      </span>
                    </button>
                    <div className="flex shrink-0 items-center gap-1">
                      <button
                        type="button"
                        aria-label={`Open ${scenario.name}`}
                        title="Open"
                        onClick={() => onOpenScenario(scenario)}
                        className="rounded-md border border-white/10 bg-surface/30 p-2 text-on-surface-variant transition-colors hover:border-primary-fixed-dim/30 hover:text-primary-fixed-dim"
                      >
                        <FolderOpen className="h-3.5 w-3.5" />
                      </button>
                      <button
                        type="button"
                        aria-label={`Restore ${scenario.name}`}
                        title="Restore"
                        onClick={() => onRestoreScenario(scenario)}
                        className="rounded-md border border-white/10 bg-surface/30 p-2 text-on-surface-variant transition-colors hover:border-tertiary-fixed-dim/30 hover:text-tertiary-fixed-dim"
                      >
                        <Undo2 className="h-3.5 w-3.5" />
                      </button>
                      <button
                        type="button"
                        aria-label={`${compared ? "Remove from" : "Add to"} comparison ${scenario.name}`}
                        title={compared ? "Compared" : "Compare"}
                        onClick={() => onToggleCompare(scenario.id)}
                        className={cn(
                          "rounded-md border p-2 transition-colors",
                          compared
                            ? "border-primary-fixed-dim/40 bg-primary-fixed-dim/10 text-primary-fixed-dim"
                            : "border-white/10 bg-surface/30 text-on-surface-variant hover:border-primary-fixed-dim/30 hover:text-primary-fixed-dim",
                        )}
                      >
                        <GitCompareArrows className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  </div>
                  <div className="mt-3 grid gap-2 sm:grid-cols-3">
                    <span className="rounded-md border border-white/10 bg-surface/20 px-2.5 py-2 font-data-tabular text-[10px] text-on-surface-variant">
                      {valuation === null ? "Valuation pending" : formatEgp(valuation)}
                    </span>
                    <span className={cn("rounded-md border px-2.5 py-2 font-data-tabular text-[10px]", delta === null ? "border-white/10 bg-surface/20 text-on-surface-variant" : deltaTone(delta))}>
                      {delta === null ? "Delta pending" : formatSignedEgp(delta)}
                    </span>
                    <span className="rounded-md border border-white/10 bg-surface/20 px-2.5 py-2 font-data-tabular text-[10px] text-on-surface-variant">
                      Parent {scenario.parent_scenario_id ?? "Base"}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </GlassPanel>
  );
}

function ScenarioTreeBranch({
  nodes,
  selectedScenarioId,
  onOpenScenario,
  depth = 0,
}: ScenarioTreeBranchProps) {
  return (
    <div className="grid gap-2">
      {nodes.map((node) => {
        const selected = selectedScenarioId === node.id;
        return (
          <div key={node.id} className="grid gap-2" style={{ paddingLeft: depth ? 14 : 0 }}>
            <button
              type="button"
              onClick={() => onOpenScenario(node)}
              className={cn(
                "flex min-w-0 items-center gap-2 rounded-lg border px-3 py-2 text-left transition-colors",
                selected
                  ? "border-primary-fixed-dim/40 bg-primary-fixed-dim/10 text-primary-fixed-dim"
                  : "border-white/10 bg-surface/20 text-on-surface-variant hover:border-white/20",
              )}
            >
              <GitBranch className="h-3.5 w-3.5 shrink-0" />
              <span className="min-w-0 flex-1 truncate font-data-tabular text-xs">{node.name}</span>
              {node.children.length > 0 && (
                <span className="font-data-tabular text-[10px] text-outline">{node.children.length}</span>
              )}
            </button>
            {node.children.length > 0 && (
              <ScenarioTreeBranch
                nodes={node.children}
                selectedScenarioId={selectedScenarioId}
                onOpenScenario={onOpenScenario}
                depth={depth + 1}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}

function ScenarioLineageTree({ tree, selectedScenarioId, onOpenScenario }: ScenarioLineageTreeProps) {
  return (
    <GlassPanel className="grid gap-4 p-5">
      <div className="flex items-center justify-between gap-3">
        <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
          <GitBranch className="h-4 w-4" />
          Scenario Lineage Tree
        </span>
        <span className="font-data-tabular text-[10px] text-outline">{tree.length} roots</span>
      </div>
      {tree.length === 0 ? (
        <p className="text-sm text-on-surface-variant">Lineage starts after a scenario is saved.</p>
      ) : (
        <ScenarioTreeBranch nodes={tree} selectedScenarioId={selectedScenarioId} onOpenScenario={onOpenScenario} />
      )}
    </GlassPanel>
  );
}

function ScenarioHistoryPanel({
  scenarios,
  tree,
  lineage,
  selectedScenario,
  comparedScenarioIds,
  saveName,
  canSave,
  isLoading,
  isSaving,
  isRestoring,
  onSaveNameChange,
  onSaveScenario,
  onOpenScenario,
  onRestoreScenario,
  onToggleCompare,
  onOpenComparison,
}: ScenarioHistoryPanelProps) {
  return (
    <div className="grid gap-4 xl:grid-cols-[minmax(0,1.15fr)_minmax(320px,0.85fr)]">
      <div className="grid gap-4">
        <GlassPanel className="grid gap-4 p-5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
              <History className="h-4 w-4" />
              Scenario History Panel
            </span>
            <span className="font-data-tabular text-[10px] text-outline">{isLoading ? "Syncing" : `${scenarios.length} states`}</span>
          </div>
          <div className="grid gap-3 md:grid-cols-[1fr_auto_auto]">
            <input
              aria-label="Scenario name"
              className={inputClass}
              value={saveName}
              onChange={(event) => onSaveNameChange(event.currentTarget.value)}
            />
            <Button type="button" variant="holo" onClick={onSaveScenario} disabled={!canSave || isSaving}>
              <Save className="h-4 w-4" />
              {isSaving ? "Saving" : "Save Scenario"}
            </Button>
            <Button type="button" variant="ghost" onClick={onOpenComparison} disabled={comparedScenarioIds.length < 2}>
              <PanelRightOpen className="h-4 w-4" />
              Compare
            </Button>
          </div>
          {selectedScenario && (
            <div className="flex flex-wrap items-center gap-2 rounded-lg border border-white/10 bg-surface/20 px-3 py-2">
              <span className="font-label-caps text-[10px] text-outline">Active Lineage</span>
              {lineage.map((scenario, index) => (
                <React.Fragment key={scenario.id}>
                  {index > 0 && <ChevronRight className="h-3.5 w-3.5 text-outline" />}
                  <span className="font-data-tabular text-xs text-on-surface-variant">{scenario.name}</span>
                </React.Fragment>
              ))}
            </div>
          )}
          {isRestoring && <p className="text-sm text-on-surface-variant">Restoring scenario state.</p>}
        </GlassPanel>
        <ScenarioTimeline
          scenarios={scenarios}
          selectedScenarioId={selectedScenario?.id ?? null}
          comparedScenarioIds={comparedScenarioIds}
          onOpenScenario={onOpenScenario}
          onRestoreScenario={onRestoreScenario}
          onToggleCompare={onToggleCompare}
        />
      </div>
      <ScenarioLineageTree tree={tree} selectedScenarioId={selectedScenario?.id ?? null} onOpenScenario={onOpenScenario} />
    </div>
  );
}

function ScenarioComparisonDrawer({
  isOpen,
  scenarios,
  comparedScenarioIds,
  onClose,
  onClear,
}: ScenarioComparisonDrawerProps) {
  const compared = comparedScenarioIds
    .map((id) => scenarios.find((scenario) => scenario.id === id))
    .filter((scenario): scenario is ScenarioState => Boolean(scenario));

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/45">
      <motion.aside
        initial={{ x: 420, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        exit={{ x: 420, opacity: 0 }}
        className="grid h-full w-full max-w-2xl content-start gap-5 overflow-y-auto border-l border-white/10 bg-surface-container p-5 shadow-2xl"
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="font-label-caps text-xs text-primary-fixed-dim">Scenario Comparison Drawer</p>
            <h3 className="mt-1 font-body-md text-on-surface">Compare saved scenarios</h3>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              aria-label="Clear comparison"
              title="Clear"
              onClick={onClear}
              className="rounded-md border border-white/10 bg-surface/30 p-2 text-on-surface-variant hover:text-primary-fixed-dim"
            >
              <RotateCcw className="h-4 w-4" />
            </button>
            <button
              type="button"
              aria-label="Close comparison"
              title="Close"
              onClick={onClose}
              className="rounded-md border border-white/10 bg-surface/30 p-2 text-on-surface-variant hover:text-primary-fixed-dim"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>

        {compared.length === 0 ? (
          <GlassPanel className="p-5">
            <p className="text-sm text-on-surface-variant">No scenarios selected.</p>
          </GlassPanel>
        ) : (
          <div className="grid gap-3">
            {compared.map((scenario) => {
              const meta = scenarioMeta(scenario);
              const delta = scenarioDeltaValue(scenario);
              const valuation = scenarioValuationValue(scenario);
              const cleanModifications = stripScenarioMetadata(scenario.modifications);
              return (
                <GlassPanel key={scenario.id} className="grid gap-4 p-4">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div className="min-w-0">
                      <p className="truncate font-data-tabular text-sm text-on-surface">{scenario.name}</p>
                      <p className="mt-1 font-data-tabular text-[10px] text-on-surface-variant">{scenarioCreatedLabel(scenario)}</p>
                    </div>
                    <span className="rounded-md border border-white/10 bg-surface/20 px-2.5 py-1.5 font-data-tabular text-[10px] text-outline">
                      Parent {scenario.parent_scenario_id ?? "Base"}
                    </span>
                  </div>
                  <div className="grid gap-2 sm:grid-cols-4">
                    <div className="rounded-lg border border-white/10 bg-surface/20 p-3">
                      <span className="font-label-caps text-[10px] text-outline">Valuation</span>
                      <p className="mt-1 font-data-tabular text-sm text-on-surface">{valuation === null ? "Pending" : formatEgp(valuation)}</p>
                    </div>
                    <div className={cn("rounded-lg border p-3", delta === null ? "border-white/10 bg-surface/20 text-on-surface-variant" : deltaTone(delta))}>
                      <span className="font-label-caps text-[10px]">Delta</span>
                      <p className="mt-1 font-data-tabular text-sm">{delta === null ? "Pending" : formatSignedEgp(delta)}</p>
                    </div>
                    <div className="rounded-lg border border-white/10 bg-surface/20 p-3">
                      <span className="font-label-caps text-[10px] text-outline">Fairness</span>
                      <p className="mt-1 truncate font-data-tabular text-sm text-on-surface">{meta?.fairness_status ?? "Pending"}</p>
                    </div>
                    <div className="rounded-lg border border-white/10 bg-surface/20 p-3">
                      <span className="font-label-caps text-[10px] text-outline">Confidence</span>
                      <p className="mt-1 truncate font-data-tabular text-sm text-on-surface">{meta?.confidence_level ?? "Pending"}</p>
                    </div>
                  </div>
                  <div className="grid gap-2 border-t border-white/5 pt-3">
                    <span className="font-label-caps text-[10px] text-outline">Saved Modifications</span>
                    <div className="flex flex-wrap gap-2">
                      {Object.entries(cleanModifications).length === 0 ? (
                        <span className="text-sm text-on-surface-variant">No property changes.</span>
                      ) : (
                        Object.entries(cleanModifications).map(([key, value]) => (
                          <span key={key} className="rounded-md border border-white/10 bg-surface/20 px-2.5 py-1.5 font-data-tabular text-[10px] text-on-surface-variant">
                            {key}: {formatNullable(value)}
                          </span>
                        ))
                      )}
                    </div>
                  </div>
                </GlassPanel>
              );
            })}
          </div>
        )}
      </motion.aside>
    </div>
  );
}

export function WhatIfScenarioPanel({
  baseRequest,
  baseResult,
  workspaceId,
  propertyId,
  scenarioId = null,
  bridgeStatus = "idle",
}: WhatIfScenarioPanelProps) {
  const { lastRequest, lastResponse, isLoading, error, runScenario, clearScenario } = useWhatIfStore();
  const {
    scenarios,
    tree,
    selectedScenario,
    selectedLineage,
    comparedScenarioIds,
    isComparisonOpen,
    isLoading: isHistoryLoading,
    isSaving,
    isRestoring,
    error: historyError,
    loadHistory,
    saveScenario,
    selectScenario,
    restoreScenario,
    toggleComparedScenario,
    openComparison,
    closeComparison,
    clearComparison,
  } = useScenarioHistoryStore();
  const [isOpen, setIsOpen] = React.useState(false);
  const [draft, setDraft] = React.useState<ScenarioDraft>(() => scenarioDraftFromRequest(baseRequest));
  const [saveName, setSaveName] = React.useState(() => defaultScenarioName(0));
  const abortRef = React.useRef<AbortController | null>(null);
  const historyAbortRef = React.useRef<AbortController | null>(null);
  const lastRunDraftRef = React.useRef<ScenarioDraft | null>(null);
  const lastRunEffectiveModificationsRef = React.useRef<Record<string, unknown> | null>(null);

  React.useEffect(() => {
    setDraft(scenarioDraftFromRequest(baseRequest));
    clearScenario();
    void selectScenario(null);
    lastRunDraftRef.current = null;
    lastRunEffectiveModificationsRef.current = null;
  }, [baseRequest, clearScenario, selectScenario]);

  React.useEffect(
    () => () => {
      abortRef.current?.abort();
      abortRef.current = null;
      historyAbortRef.current?.abort();
      historyAbortRef.current = null;
    },
    [],
  );

  React.useEffect(() => {
    if (!isOpen || typeof propertyId !== "number") return;
    historyAbortRef.current?.abort();
    const controller = new AbortController();
    historyAbortRef.current = controller;
    void loadHistory(propertyId, controller.signal).catch((loadError) => {
      if (controller.signal.aborted) return;
      console.error(loadError);
    });
    return () => {
      controller.abort();
      if (historyAbortRef.current === controller) {
        historyAbortRef.current = null;
      }
    };
  }, [isOpen, loadHistory, propertyId]);

  const baseDraft = React.useMemo(() => scenarioDraftFromRequest(baseRequest), [baseRequest]);
  const selectedScenarioDraft = React.useMemo(
    () => (selectedLineage.length > 0 ? scenarioDraftFromLineage(baseRequest, selectedLineage) : baseDraft),
    [baseDraft, baseRequest, selectedLineage],
  );
  const comparedScenarios = React.useMemo(
    () =>
      comparedScenarioIds
        .map((id) => scenarios.find((scenario) => scenario.id === id))
        .filter((scenario): scenario is ScenarioState => Boolean(scenario)),
    [comparedScenarioIds, scenarios],
  );
  const baseModifications = React.useMemo(() => buildDraftModifications(baseDraft, draft), [baseDraft, draft]);
  const parentModifications = React.useMemo(
    () => (selectedScenario ? buildDraftModifications(selectedScenarioDraft, draft) : baseModifications),
    [baseModifications, draft, selectedScenario, selectedScenarioDraft],
  );
  const hasParentEdits = selectedScenario ? Object.keys(parentModifications).length > 0 : false;
  const runScenarioId = selectedScenario && hasParentEdits ? selectedScenario.id : null;
  const modifications = selectedScenario && hasParentEdits ? parentModifications : baseModifications;
  const hasChanges = Object.keys(modifications).length > 0;
  const hasContext = typeof workspaceId === "number" && typeof propertyId === "number";
  const canRun = hasContext && hasChanges && !isLoading;
  const canSave = hasContext && Boolean(lastRequest && lastResponse) && saveName.trim().length > 0 && !isSaving;

  const updateDraft = React.useCallback(
    <TKey extends keyof ScenarioDraft>(key: TKey, value: ScenarioDraft[TKey]) => {
      setDraft((current) => ({ ...current, [key]: value }));
    },
    [],
  );

  const toggleAmenity = React.useCallback((symbol: string) => {
    setDraft((current) => {
      const next = new Set(current.amenities);
      if (next.has(symbol)) {
        next.delete(symbol);
      } else {
        next.add(symbol);
      }
      return { ...current, amenities: Array.from(next).sort() };
    });
  }, []);

  const resetDraft = React.useCallback(() => {
    abortRef.current?.abort();
    abortRef.current = null;
    setDraft(scenarioDraftFromRequest(baseRequest));
    clearScenario();
    void selectScenario(null);
    lastRunDraftRef.current = null;
    lastRunEffectiveModificationsRef.current = null;
  }, [baseRequest, clearScenario, selectScenario]);

  const submitScenario = React.useCallback(() => {
    if (!hasContext || !hasChanges) return;
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    lastRunDraftRef.current = draft;
    lastRunEffectiveModificationsRef.current = baseModifications;
    void runScenario(
      {
        workspace_id: workspaceId,
        property_id: propertyId,
        scenario_id: runScenarioId ?? scenarioId ?? null,
        modifications,
      },
      controller.signal,
    )
      .then((response) => {
        setSaveName(defaultScenarioName(scenarios.length, response));
      })
      .finally(() => {
        if (abortRef.current === controller) {
          abortRef.current = null;
        }
      });
  }, [baseModifications, draft, hasChanges, hasContext, modifications, propertyId, runScenario, runScenarioId, scenarioId, scenarios.length, workspaceId]);

  const openSavedScenario = React.useCallback(
    (scenario: ScenarioState) => {
      const controller = new AbortController();
      void selectScenario(scenario, controller.signal)
        .then((lineage) => {
          setDraft(scenarioDraftFromLineage(baseRequest, lineage));
          clearScenario();
          lastRunDraftRef.current = null;
          lastRunEffectiveModificationsRef.current = null;
        })
        .catch((openError) => {
          if (controller.signal.aborted) return;
          console.error(openError);
        });
    },
    [baseRequest, clearScenario, selectScenario],
  );

  const restoreSavedScenario = React.useCallback(
    (scenario: ScenarioState) => {
      const controller = new AbortController();
      void restoreScenario(scenario.id, controller.signal)
        .then((restored) => selectScenario(restored, controller.signal))
        .then((lineage) => {
          setDraft(scenarioDraftFromLineage(baseRequest, lineage));
          clearScenario();
          lastRunDraftRef.current = null;
          lastRunEffectiveModificationsRef.current = null;
        })
        .catch((restoreError) => {
          if (controller.signal.aborted) return;
          console.error(restoreError);
        });
    },
    [baseRequest, clearScenario, restoreScenario, selectScenario],
  );

  const saveCurrentScenario = React.useCallback(() => {
    if (!hasContext || typeof propertyId !== "number" || !lastRequest || !lastResponse) return;

    const cleanModifications = stripScenarioMetadata(lastRequest.modifications as Record<string, unknown>);
    const metadata: ScenarioHistoryMeta = {
      saved_at: new Date().toISOString(),
      base_valuation: lastResponse.base_valuation,
      scenario_valuation: lastResponse.scenario_valuation,
      signed_delta_value: lastResponse.delta_value,
      delta_percentage: lastResponse.delta_percentage,
      confidence_level: lastResponse.confidence_level,
      fairness_status: lastResponse.fairness_status,
      base_valuation_id: lastResponse.base_valuation_id,
      scenario_valuation_id: lastResponse.scenario_valuation_id,
      fairness_valuation_id: lastResponse.fairness_valuation_id,
      assumptions_count: lastResponse.assumptions_used.length,
      effective_modifications: lastRunEffectiveModificationsRef.current ?? cleanModifications,
    };

    const controller = new AbortController();
    void saveScenario(
      {
        property_state_id: propertyId,
        parent_scenario_id: lastRequest.scenario_id ?? null,
        name: saveName.trim() || defaultScenarioName(scenarios.length, lastResponse),
        modifications: {
          ...cleanModifications,
          [SCENARIO_HISTORY_META_KEY]: metadata,
        },
        delta_value: Math.abs(lastResponse.delta_value),
      },
      controller.signal,
    )
      .then(() => {
        setSaveName(defaultScenarioName(scenarios.length + 1));
      })
      .catch((saveError) => {
        if (controller.signal.aborted) return;
        console.error(saveError);
      });
  }, [hasContext, lastRequest, lastResponse, propertyId, saveName, saveScenario, scenarios.length]);

  return (
    <motion.section variants={stagedReveal} initial="hidden" animate="show" className="grid gap-4">
      <div className="flex flex-wrap items-end justify-between gap-4 border-b border-white/5 pb-2">
        <div>
          <p className="font-label-caps text-xs text-primary-fixed-dim">What-if Scenario Analysis</p>
          <h2 className="mt-1 font-headline-lg-mobile text-on-surface">Scenario results</h2>
        </div>
        <Button type="button" variant={isOpen ? "ghost" : "holo"} size="sm" onClick={() => setIsOpen((value) => !value)}>
          <GitCompareArrows className="h-4 w-4" />
          What if?
        </Button>
      </div>

      {isOpen && (
        <motion.div variants={revealItem} className="grid gap-4">
          {!hasContext && (
            <GlassPanel className="flex items-start gap-3 p-5">
              <CheckCircle2 className="mt-0.5 h-4 w-4 text-primary-fixed-dim" />
              <div>
                <p className="font-label-caps text-xs text-primary-fixed-dim">Property Context {bridgeStatus}</p>
                <p className="mt-1 text-sm text-on-surface-variant">The valuation is waiting for its backend property context before scenarios can run.</p>
              </div>
            </GlassPanel>
          )}

          <ScenarioModificationControls
            baseRequest={baseRequest}
            draft={draft}
            hasChanges={hasChanges}
            isLoading={isLoading}
            canRun={canRun}
            onDraftChange={updateDraft}
            onAmenityToggle={toggleAmenity}
            onRun={submitScenario}
            onResetDraft={resetDraft}
          />

          <ScenarioHistoryPanel
            scenarios={scenarios}
            tree={tree}
            lineage={selectedLineage}
            selectedScenario={selectedScenario}
            comparedScenarioIds={comparedScenarioIds}
            saveName={saveName}
            canSave={canSave}
            isLoading={isHistoryLoading}
            isSaving={isSaving}
            isRestoring={isRestoring}
            onSaveNameChange={setSaveName}
            onSaveScenario={saveCurrentScenario}
            onOpenScenario={openSavedScenario}
            onRestoreScenario={restoreSavedScenario}
            onToggleCompare={toggleComparedScenario}
            onOpenComparison={openComparison}
          />

          {error && (
            <GlassPanel className="border-error/25 bg-error/5 p-5">
              <p className="font-label-caps text-xs text-error">Scenario Error</p>
              <p className="mt-1 text-sm text-on-surface-variant">{error.message}</p>
            </GlassPanel>
          )}

          {historyError && (
            <GlassPanel className="border-error/25 bg-error/5 p-5">
              <p className="font-label-caps text-xs text-error">Scenario History Error</p>
              <p className="mt-1 text-sm text-on-surface-variant">{historyError.message}</p>
            </GlassPanel>
          )}

          {lastResponse ? (
            <div className="grid gap-4">
              <ScenarioDeltaSummary
                baseRequest={baseRequest}
                baseResult={baseResult}
                scenarioRequest={draft}
                response={lastResponse}
              />
              <FeatureChangesList changes={lastResponse.feature_changes} />
              <ScenarioAssumptions assumptions={lastResponse.assumptions_used} />
              <ScenarioExplainability response={lastResponse} />
              <ScenarioComparables comparables={lastResponse.comparables.comparables} />
            </div>
          ) : (
            <GlassPanel className="p-5">
              <p className="font-label-caps text-xs text-primary-fixed-dim">Scenario Results</p>
              <p className="mt-1 text-sm text-on-surface-variant">No scenario has been executed for this valuation.</p>
            </GlassPanel>
          )}

          <NegotiationIntelligencePanel
            baseRequest={baseRequest}
            baseResult={baseResult}
            workspaceId={workspaceId}
            propertyId={propertyId}
            activeScenarioRequest={lastRequest}
            activeScenarioResponse={lastResponse}
            selectedScenario={selectedScenario}
            bridgeStatus={bridgeStatus}
          />

          <InvestmentIntelligencePanel
            baseRequest={baseRequest}
            baseResult={baseResult}
            workspaceId={workspaceId}
            propertyId={propertyId}
            activeScenarioRequest={lastRequest}
            activeScenarioResponse={lastResponse}
            selectedScenario={selectedScenario}
            comparedScenarios={comparedScenarios}
            bridgeStatus={bridgeStatus}
          />
        </motion.div>
      )}
      <ScenarioComparisonDrawer
        isOpen={isComparisonOpen}
        scenarios={scenarios}
        comparedScenarioIds={comparedScenarioIds}
        onClose={closeComparison}
        onClear={clearComparison}
      />
    </motion.section>
  );
}
