import * as React from "react";
import { Link } from "react-router-dom";
import {
  AlertTriangle,
  BarChart3,
  Database,
  FileSearch,
  Filter,
  Layers3,
  ListChecks,
  Loader2,
  MapPinned,
  RefreshCw,
  RotateCcw,
  Search,
  ShieldCheck,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { GlassPanel } from "@/components/ui/glass";
import { cn } from "@/lib/utils";
import { APP_ROUTES } from "@/navigation/routes";
import { defaultMarketInsightFilters, useMarketInsightStore } from "@/store/marketInsightStore";
import { usePropertyContextStore } from "@/store/propertyContextStore";
import type {
  MarketInsightDensityLevel,
  MarketInsightFilters,
  MarketInsightSegment,
  MarketInsightToolRequest,
  MarketInsightToolResponse,
} from "@/types/marketInsight";

const egpFormatter = new Intl.NumberFormat("en-EG", {
  maximumFractionDigits: 0,
});

const inputClass =
  "h-10 w-full rounded-lg border border-white/10 bg-surface/40 px-3 font-data-tabular text-sm text-on-surface outline-none transition-colors focus:border-primary-fixed-dim/50";

const timeWindows = [
  { value: "all", label: "All" },
  { value: "30d", label: "30d" },
  { value: "90d", label: "90d" },
];

function formatEgp(value: number | null): string {
  if (typeof value !== "number") return "No observed value";
  return `EGP ${egpFormatter.format(value)}`;
}

function formatCount(value: number | null): string {
  if (typeof value !== "number") return "No count";
  return String(value);
}

function formatDateTime(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString("en-EG", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function labelFromKey(value: string): string {
  return value
    .replace(/_/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatUnknownValue(value: unknown): string {
  if (value === null || value === undefined || value === "") return "Not supplied";
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") return String(value);
  return JSON.stringify(value);
}

function densityTone(density: MarketInsightDensityLevel): "positive" | "warning" | "default" {
  if (density === "High") return "positive";
  if (density === "Sparse" || density === "Insufficient Evidence") return "warning";
  return "default";
}

function confidenceSummary(counts: Record<string, number>): string {
  const entries = Object.entries(counts);
  if (entries.length === 0) return "No confidence counts";
  return entries.map(([label, count]) => `${label} ${count}`).join(", ");
}

function buildMarketInsightRequest(workspaceId: number, filters: MarketInsightFilters): MarketInsightToolRequest {
  const request: MarketInsightToolRequest = {
    workspace_id: workspaceId,
    time_window: filters.time_window || "all",
  };
  const compoundName = filters.compound_name?.trim();
  const propertyType = filters.property_type?.trim();
  const h3Res9 = filters.h3_res9?.trim();

  if (compoundName) request.compound_name = compoundName;
  if (propertyType) request.property_type = propertyType;
  if (h3Res9) request.h3_res9 = h3Res9;

  return request;
}

function safeTraceabilityNote(note: string): string {
  if (!/\b(forecast|future price|future-price)\b/i.test(note)) return note;
  return "Descriptive analytics only. Every statement is derived from persisted tenant-scoped TruthLayer records.";
}

interface ChipProps {
  children: React.ReactNode;
  key?: React.Key;
  tone?: "default" | "positive" | "warning";
}

function Chip({ children, tone = "default" }: ChipProps) {
  return (
    <span
      className={cn(
        "rounded-md border px-2.5 py-1.5 font-data-tabular text-[10px]",
        tone === "positive" && "border-tertiary-fixed-dim/25 bg-tertiary-fixed-dim/10 text-tertiary-fixed-dim",
        tone === "warning" && "border-error/25 bg-error/10 text-error",
        tone === "default" && "border-white/10 bg-surface/30 text-on-surface-variant",
      )}
    >
      {children}
    </span>
  );
}

function MetricTile({
  label,
  value,
  detail,
  tone = "default",
}: {
  label: string;
  value: string;
  detail?: string;
  tone?: "default" | "positive" | "warning";
}) {
  return (
    <GlassPanel
      className={cn(
        "grid min-h-28 gap-2 p-4",
        tone === "positive" && "border-tertiary-fixed-dim/20",
        tone === "warning" && "border-error/20",
      )}
    >
      <span className="font-label-caps text-[10px] text-outline">{label}</span>
      <p
        className={cn(
          "break-words font-data-tabular text-lg",
          tone === "positive" && "text-tertiary-fixed-dim",
          tone === "warning" && "text-error",
          tone === "default" && "text-on-surface",
        )}
      >
        {value}
      </p>
      {detail && <p className="text-xs leading-5 text-on-surface-variant">{detail}</p>}
    </GlassPanel>
  );
}

function DistributionList({ counts }: { counts: Record<string, number> }) {
  const entries = Object.entries(counts);
  if (entries.length === 0) {
    return <p className="text-sm text-on-surface-variant">No counts returned.</p>;
  }

  return (
    <div className="grid gap-2">
      {entries.map(([label, count]) => (
        <div key={label} className="grid grid-cols-[minmax(80px,1fr)_auto] items-center gap-3">
          <span className="truncate text-sm text-on-surface-variant">{label}</span>
          <span className="font-data-tabular text-sm text-on-surface">{count}</span>
        </div>
      ))}
    </div>
  );
}

function SegmentTable({ title, rows }: { title: string; rows: MarketInsightSegment[] }) {
  return (
    <GlassPanel className="grid gap-4 p-5">
      <div className="flex items-center gap-2">
        <Layers3 className="h-4 w-4 text-primary-fixed-dim" />
        <h3 className="font-label-caps text-xs text-primary-fixed-dim">{title}</h3>
      </div>
      {rows.length === 0 ? (
        <p className="text-sm text-on-surface-variant">No {title.toLowerCase()} returned for these filters.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full min-w-[660px] text-left">
            <thead>
              <tr className="border-b border-white/10 font-label-caps text-[10px] text-outline">
                <th className="py-2 pr-4 font-normal">Name</th>
                <th className="py-2 pr-4 font-normal">Valuations</th>
                <th className="py-2 pr-4 font-normal">Median Observed Fair Value</th>
                <th className="py-2 pr-4 font-normal">Evidence Quality</th>
                <th className="py-2 font-normal">Confidence</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.name} className="border-b border-white/5 text-sm last:border-b-0">
                  <td className="py-3 pr-4 font-data-tabular text-on-surface">{row.name}</td>
                  <td className="py-3 pr-4 font-data-tabular text-on-surface">{row.valuation_count}</td>
                  <td className="py-3 pr-4 font-data-tabular text-on-surface">{formatEgp(row.median_fair_value)}</td>
                  <td className="py-3 pr-4">
                    <div className="flex flex-wrap gap-2">
                      <Chip tone={densityTone(row.comparable_density)}>{row.comparable_density}</Chip>
                      <Chip>Median comps {formatCount(row.median_comparable_count)}</Chip>
                    </div>
                  </td>
                  <td className="py-3 text-on-surface-variant">{confidenceSummary(row.confidence_distribution)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </GlassPanel>
  );
}

function EvidenceStatements({ response }: { response: MarketInsightToolResponse }) {
  return (
    <GlassPanel className="grid gap-4 p-5">
      <div className="flex items-center gap-2">
        <FileSearch className="h-4 w-4 text-primary-fixed-dim" />
        <h3 className="font-label-caps text-xs text-primary-fixed-dim">Evidence Statements</h3>
      </div>
      {response.evidence_summary.statements.length === 0 ? (
        <p className="text-sm text-on-surface-variant">No evidence statements were returned.</p>
      ) : (
        <div className="grid gap-3">
          {response.evidence_summary.statements.map((statement, index) => (
            <div key={`${statement.text}-${index}`} className="grid gap-3 rounded-lg border border-white/10 bg-surface/20 p-3">
              <p className="text-sm leading-6 text-on-surface">{statement.text}</p>
              <div className="flex flex-wrap gap-2">
                {statement.evidence.map((evidence) => (
                  <Chip key={`${statement.text}-${evidence}`}>{evidence}</Chip>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </GlassPanel>
  );
}

function TraceabilityPanel({ response }: { response: MarketInsightToolResponse }) {
  return (
    <div className="grid gap-4 xl:grid-cols-3">
      <GlassPanel className="grid gap-3 p-5">
        <div className="flex items-center gap-2">
          <ListChecks className="h-4 w-4 text-primary-fixed-dim" />
          <h3 className="font-label-caps text-xs text-primary-fixed-dim">Filters Used</h3>
        </div>
        <div className="flex flex-wrap gap-2">
          {Object.entries(response.evidence_summary.filters_used).map(([key, value]) => (
            <Chip key={key}>
              {key} {formatUnknownValue(value)}
            </Chip>
          ))}
        </div>
      </GlassPanel>

      <GlassPanel className="grid gap-3 p-5">
        <div className="flex items-center gap-2">
          <Database className="h-4 w-4 text-primary-fixed-dim" />
          <h3 className="font-label-caps text-xs text-primary-fixed-dim">Source Counts</h3>
        </div>
        <div className="grid gap-2">
          {Object.entries(response.evidence_summary.source_record_counts).map(([key, value]) => (
            <div key={key} className="flex items-center justify-between gap-3">
              <span className="text-sm text-on-surface-variant">{labelFromKey(key)}</span>
              <span className="font-data-tabular text-sm text-on-surface">{value}</span>
            </div>
          ))}
        </div>
      </GlassPanel>

      <GlassPanel className="grid gap-3 p-5">
        <div className="flex items-center gap-2">
          <ShieldCheck className="h-4 w-4 text-primary-fixed-dim" />
          <h3 className="font-label-caps text-xs text-primary-fixed-dim">Traceability Notes</h3>
        </div>
        <p className="text-sm leading-6 text-on-surface-variant">
          {safeTraceabilityNote(response.evidence_summary.traceability_note)}
        </p>
        <div className="flex flex-wrap gap-2">
          {response.data_sources_used.map((source) => (
            <Chip key={source}>{source}</Chip>
          ))}
        </div>
      </GlassPanel>
    </div>
  );
}

function EmptyState({ response }: { response: MarketInsightToolResponse }) {
  return (
    <GlassPanel className="grid gap-4 border-primary-fixed-dim/15 p-5">
      <div className="flex items-center gap-2">
        <MapPinned className="h-5 w-5 text-primary-fixed-dim" />
        <h3 className="font-label-caps text-xs text-primary-fixed-dim">Workspace History</h3>
      </div>
      <p className="font-data-tabular text-xl text-on-surface">No persisted TruthLayer valuations match these filters.</p>
      <p className="max-w-2xl text-sm leading-6 text-on-surface-variant">
        Run valuations to build workspace market history, or widen the selected filters.
      </p>
      <div className="flex flex-wrap gap-2">
        {response.evidence_summary.statements.flatMap((statement) =>
          statement.evidence.map((evidence) => <Chip key={`${statement.text}-${evidence}`}>{evidence}</Chip>),
        )}
      </div>
      <Link
        to={APP_ROUTES.valuation}
        className="inline-flex w-fit items-center justify-center rounded-lg border border-primary text-primary-fixed-dim px-4 py-2 font-label-caps text-xs transition-colors hover:bg-primary/10"
      >
        Open Valuation
      </Link>
    </GlassPanel>
  );
}

function LoadingState() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {[0, 1, 2].map((item) => (
        <GlassPanel key={item} className="grid min-h-28 gap-3 p-4">
          <div className="h-3 w-24 animate-pulse rounded bg-white/10" />
          <div className="h-6 w-36 animate-pulse rounded bg-white/10" />
          <div className="h-3 w-full animate-pulse rounded bg-white/10" />
        </GlassPanel>
      ))}
    </div>
  );
}

function NoWorkspaceState() {
  return (
    <GlassPanel className="grid gap-4 p-5">
      <div className="flex items-center gap-2">
        <MapPinned className="h-5 w-5 text-primary-fixed-dim" />
        <h2 className="font-label-caps text-xs text-primary-fixed-dim">Workspace History</h2>
      </div>
      <p className="font-data-tabular text-xl text-on-surface">Market Intelligence needs a workspace with persisted TruthLayer valuation history.</p>
      <p className="max-w-2xl text-sm leading-6 text-on-surface-variant">
        Run a valuation first so Pulse can read the workspace history created by TruthLayer.
      </p>
      <Link
        to={APP_ROUTES.valuation}
        className="inline-flex w-fit items-center justify-center rounded-lg border border-primary text-primary-fixed-dim px-4 py-2 font-label-caps text-xs transition-colors hover:bg-primary/10"
      >
        Open Valuation
      </Link>
    </GlassPanel>
  );
}

function MarketInsightFiltersForm({
  filters,
  disabled,
  onChange,
  onReset,
  onSubmit,
}: {
  filters: MarketInsightFilters;
  disabled: boolean;
  onChange: (filters: Partial<MarketInsightFilters>) => void;
  onReset: () => void;
  onSubmit: () => void;
}) {
  return (
    <GlassPanel className="p-5">
      <form
        className="grid gap-4"
        onSubmit={(event) => {
          event.preventDefault();
          onSubmit();
        }}
      >
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-primary-fixed-dim" />
            <h2 className="font-label-caps text-xs text-primary-fixed-dim">Filters</h2>
          </div>
          <div className="flex flex-wrap gap-2">
            {timeWindows.map((option) => {
              const selected = filters.time_window === option.value;
              return (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => onChange({ time_window: option.value })}
                  className={cn(
                    "h-9 rounded-lg border px-3 font-data-tabular text-xs transition-colors",
                    selected
                      ? "border-primary-fixed-dim/50 bg-primary-fixed-dim/15 text-primary-fixed-dim"
                      : "border-white/10 bg-surface/20 text-on-surface-variant hover:border-white/20",
                  )}
                >
                  {option.label}
                </button>
              );
            })}
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <label className="grid gap-2">
            <span className="font-label-caps text-[10px] text-on-surface-variant">compound_name</span>
            <input
              aria-label="compound_name"
              className={inputClass}
              value={filters.compound_name ?? ""}
              onChange={(event) => onChange({ compound_name: event.currentTarget.value })}
              placeholder="Nile Quarter"
            />
          </label>
          <label className="grid gap-2">
            <span className="font-label-caps text-[10px] text-on-surface-variant">property_type</span>
            <input
              aria-label="property_type"
              className={inputClass}
              value={filters.property_type ?? ""}
              onChange={(event) => onChange({ property_type: event.currentTarget.value })}
              placeholder="Apartment"
            />
          </label>
          <label className="grid gap-2">
            <span className="font-label-caps text-[10px] text-on-surface-variant">h3_res9</span>
            <input
              aria-label="h3_res9"
              className={inputClass}
              value={filters.h3_res9 ?? ""}
              onChange={(event) => onChange({ h3_res9: event.currentTarget.value })}
              placeholder="89754e64993ffff"
            />
          </label>
        </div>

        <div className="flex flex-col gap-3 sm:flex-row">
          <Button type="submit" variant="holo" disabled={disabled} className="w-full sm:w-auto">
            {disabled ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
            Run Market Intelligence
          </Button>
          <Button type="button" variant="ghost" onClick={onReset} disabled={disabled}>
            <RotateCcw className="h-4 w-4" />
            Reset Filters
          </Button>
        </div>
      </form>
    </GlassPanel>
  );
}

function MarketInsightResult({ response }: { response: MarketInsightToolResponse }) {
  const isEmpty = response.valuation_volume === 0;
  const isSparse =
    response.comparable_density.density_level === "Sparse" ||
    response.comparable_density.density_level === "Insufficient Evidence";

  if (isEmpty) {
    return (
      <div className="grid gap-4">
        <EmptyState response={response} />
        <EvidenceStatements response={response} />
        <TraceabilityPanel response={response} />
      </div>
    );
  }

  return (
    <div className="grid gap-4">
      {isSparse && (
        <GlassPanel className="border-error/25 bg-error/5 p-5">
          <div className="flex items-start gap-3">
            <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-error" />
            <div>
              <p className="font-label-caps text-xs text-error">Evidence Quality</p>
              <p className="mt-1 text-sm leading-6 text-on-surface-variant">
                Evidence is sparse. Observed results are descriptive and remain tied to persisted TruthLayer records.
              </p>
            </div>
          </div>
        </GlassPanel>
      )}

      <div className="grid gap-4 lg:grid-cols-[1.3fr_0.7fr]">
        <GlassPanel className="grid gap-4 p-5">
          <div className="flex items-center gap-2">
            <BarChart3 className="h-4 w-4 text-primary-fixed-dim" />
            <h2 className="font-label-caps text-xs text-primary-fixed-dim">Market Summary</h2>
          </div>
          <p className="text-base leading-7 text-on-surface">{response.market_summary}</p>
          <div className="flex flex-wrap gap-2">
            <Chip>{response.source}</Chip>
            <Chip>{formatDateTime(response.timestamp)}</Chip>
          </div>
        </GlassPanel>

        <MetricTile
          label="Valuation Volume"
          value={String(response.valuation_volume)}
          detail={`${response.evidence_summary.valuation_ids.length} valuation ids returned`}
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricTile
          label="Observed Median"
          value={formatEgp(response.fair_value_distribution.median_fair_value)}
          detail={`${response.fair_value_distribution.valuation_count} fair-value observations`}
        />
        <MetricTile
          label="Observed Minimum"
          value={formatEgp(response.fair_value_distribution.minimum_fair_value)}
        />
        <MetricTile
          label="Observed Maximum"
          value={formatEgp(response.fair_value_distribution.maximum_fair_value)}
        />
        <MetricTile
          label="Comparable Density"
          value={response.comparable_density.density_level}
          detail={`Median comparable count ${formatCount(response.comparable_density.median_comparable_count)}`}
          tone={densityTone(response.comparable_density.density_level)}
        />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <GlassPanel className="grid gap-4 p-5">
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-primary-fixed-dim" />
            <h3 className="font-label-caps text-xs text-primary-fixed-dim">Confidence Distribution</h3>
          </div>
          <DistributionList counts={response.confidence_distribution.counts} />
          <Chip>Predominant {response.confidence_distribution.predominant_level ?? "None"}</Chip>
        </GlassPanel>

        <GlassPanel className="grid gap-4 p-5">
          <div className="flex items-center gap-2">
            <Database className="h-4 w-4 text-primary-fixed-dim" />
            <h3 className="font-label-caps text-xs text-primary-fixed-dim">Comparable Measurement Sources</h3>
          </div>
          <DistributionList counts={response.comparable_density.measurement_sources} />
          <div className="flex flex-wrap gap-2">
            <Chip>Min comps {formatCount(response.comparable_density.minimum_comparable_count)}</Chip>
            <Chip>Max comps {formatCount(response.comparable_density.maximum_comparable_count)}</Chip>
          </div>
        </GlassPanel>
      </div>

      <div className="grid gap-4">
        <SegmentTable title="Active Compounds" rows={response.active_compounds} />
        <SegmentTable title="Active Areas" rows={response.active_areas} />
      </div>

      <EvidenceStatements response={response} />
      <TraceabilityPanel response={response} />
    </div>
  );
}

export function MarketIntelligencePanel() {
  const activeWorkspaceId = usePropertyContextStore((state) => state.activeWorkspaceId);
  const {
    filters,
    lastRequest,
    lastResponse,
    isLoading,
    error,
    setFilters,
    resetFilters,
    runMarketInsight,
  } = useMarketInsightStore();
  const abortRef = React.useRef<AbortController | null>(null);

  React.useEffect(
    () => () => {
      abortRef.current?.abort();
      abortRef.current = null;
    },
    [],
  );

  const submitMarketInsight = React.useCallback(
    (nextFilters = filters) => {
      if (typeof activeWorkspaceId !== "number") return;
      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;
      const request = buildMarketInsightRequest(activeWorkspaceId, nextFilters);

      void runMarketInsight(request, controller.signal)
        .catch(() => undefined)
        .finally(() => {
          if (abortRef.current === controller) {
            abortRef.current = null;
          }
        });
    },
    [activeWorkspaceId, filters, runMarketInsight],
  );

  const resetAndRun = React.useCallback(() => {
    resetFilters();
    if (typeof activeWorkspaceId === "number") {
      submitMarketInsight(defaultMarketInsightFilters);
    }
  }, [activeWorkspaceId, resetFilters, submitMarketInsight]);

  const visibleResponse = error ? null : lastResponse;

  if (typeof activeWorkspaceId !== "number") {
    return (
      <section className="mx-auto grid w-full max-w-7xl gap-6 p-4 pb-28 pt-24 md:ml-72 md:p-8 md:pb-12 md:pt-28">
        <div className="grid gap-2">
          <p className="font-label-caps text-xs text-primary-fixed-dim">Market Intelligence</p>
          <h1 className="font-headline-lg-mobile text-on-surface md:font-headline-lg">Workspace market pulse</h1>
        </div>
        <NoWorkspaceState />
      </section>
    );
  }

  return (
    <section className="mx-auto grid w-full max-w-7xl gap-6 p-4 pb-28 pt-24 md:ml-72 md:p-8 md:pb-12 md:pt-28">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div className="grid gap-2">
          <p className="font-label-caps text-xs text-primary-fixed-dim">Market Intelligence</p>
          <h1 className="font-headline-lg-mobile text-on-surface md:font-headline-lg">Workspace market pulse</h1>
          <p className="max-w-3xl text-sm leading-6 text-on-surface-variant">
            Evidence-backed pulse from persisted TruthLayer valuation history.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Chip>Workspace {activeWorkspaceId}</Chip>
          <Chip>POST /v1/copilot/tools/market-insight</Chip>
          {lastRequest?.workspace_id === activeWorkspaceId && <Chip>Last run {lastRequest.time_window ?? "all"}</Chip>}
        </div>
      </div>

      <MarketInsightFiltersForm
        filters={filters}
        disabled={isLoading}
        onChange={setFilters}
        onReset={resetAndRun}
        onSubmit={submitMarketInsight}
      />

      {error && (
        <GlassPanel className="border-error/25 bg-error/5 p-5">
          <div className="flex items-start gap-3">
            <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-error" />
            <div>
              <p className="font-label-caps text-xs text-error">Market Intelligence Error</p>
              <p className="mt-1 text-sm leading-6 text-on-surface-variant">{error.message}</p>
            </div>
          </div>
        </GlassPanel>
      )}

      {isLoading && <LoadingState />}

      {!isLoading && visibleResponse && <MarketInsightResult response={visibleResponse} />}

      {!isLoading && !visibleResponse && !error && (
        <GlassPanel className="grid gap-3 p-5">
          <div className="flex items-center gap-2">
            <RefreshCw className="h-4 w-4 text-primary-fixed-dim" />
            <h2 className="font-label-caps text-xs text-primary-fixed-dim">Workspace History</h2>
          </div>
          <p className="text-sm leading-6 text-on-surface-variant">
            Run Market Intelligence to inspect persisted TruthLayer valuations for this workspace.
          </p>
        </GlassPanel>
      )}
    </section>
  );
}
