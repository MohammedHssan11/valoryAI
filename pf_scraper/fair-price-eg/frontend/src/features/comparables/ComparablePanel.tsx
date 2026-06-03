import * as React from "react";
import { motion } from "framer-motion";
import { ArrowDownUp, Bath, BedDouble, Building2, Clock3, Filter, MapPin, ShieldCheck, SlidersHorizontal } from "lucide-react";
import { revealItem, stagedReveal } from "@/animations/motion";
import { Button } from "@/components/ui/button";
import { GlassPanel } from "@/components/ui/glass";
import { EvidenceMap } from "@/features/evidence/EvidenceMap";
import { cn } from "@/lib/utils";
import { useComparableAnalysisStore } from "@/store/comparableAnalysisStore";
import type { ComparableItem, RentFairPriceData } from "@/types/valuation";

const egpFormatter = new Intl.NumberFormat("en-EG", {
  maximumFractionDigits: 0,
});

type SortKey = "weighted" | "distance" | "recency" | "similarity" | "price";

interface ComparablePanelProps {
  comparables: ComparableItem[];
  result?: RentFairPriceData | null;
  subjectPropertyType?: string | null;
}

function formatEgp(value: number): string {
  return `EGP ${egpFormatter.format(value)}`;
}

function formatDistance(value?: number | null): string {
  if (value == null) return "n/a";
  if (value < 1000) return `${Math.round(value)}m`;
  return `${(value / 1000).toFixed(1)}km`;
}

function formatPercent(value?: number | null): string {
  if (value == null) return "n/a";
  return `${Math.round(value * 100)}%`;
}

function formatAge(value?: number | null): string {
  if (value == null) return "n/a";
  if (value < 1) return "today";
  return `${Math.round(value)}d`;
}

function metricValue(comparable: ComparableItem, key: SortKey): number {
  if (key === "distance") return comparable.dist_m ?? Number.POSITIVE_INFINITY;
  if (key === "recency") return comparable.age_days ?? Number.POSITIVE_INFINITY;
  if (key === "price") return comparable.price_egp;
  if (key === "similarity") return -(comparable.similarity_score ?? comparable.feature_similarity ?? 0);
  return -(comparable.weighted_contribution ?? comparable.weight ?? 0);
}

function sortComparables(comparables: ComparableItem[], sortKey: SortKey): ComparableItem[] {
  return [...comparables].sort((a, b) => {
    const diff = metricValue(a, sortKey) - metricValue(b, sortKey);
    if (diff !== 0) return diff;
    const rankDiff = (a.evidence_rank ?? Number.MAX_SAFE_INTEGER) - (b.evidence_rank ?? Number.MAX_SAFE_INTEGER);
    if (rankDiff !== 0) return rankDiff;
    return a.listing_id.localeCompare(b.listing_id);
  });
}

function isPremiumComparable(comparable: ComparableItem): boolean {
  const quality = comparable.building_quality?.toLowerCase();
  return quality === "premium" || comparable.normalized_amenities.some((amenity) => amenity.toLowerCase().includes("premium"));
}

function overlapList(value: unknown): string[] {
  return Array.isArray(value) ? value.map(String) : [];
}

function amenityOverlap(comparable: ComparableItem, key: "matched_amenities" | "missing_amenities" | "extra_amenities"): string[] {
  return overlapList(comparable.amenity_explanation?.[key] ?? comparable.feature_overlap?.[key]);
}

export function ComparablePanel({ comparables, result, subjectPropertyType }: ComparablePanelProps) {
  const { selectedComparable, setSelectedComparable } = useComparableAnalysisStore();
  const [sortKey, setSortKey] = React.useState<SortKey>("weighted");
  const [minSimilarity, setMinSimilarity] = React.useState(0);
  const [newerOnly, setNewerOnly] = React.useState(false);
  const [premiumOnly, setPremiumOnly] = React.useState(false);
  const [samePropertyTypeOnly, setSamePropertyTypeOnly] = React.useState(false);
  const baselineRadius = React.useMemo(
    () => Math.max(500, Math.ceil(Math.max(...comparables.map((comp) => comp.dist_m ?? 0), 500))),
    [comparables],
  );
  const [maxRadius, setMaxRadius] = React.useState(baselineRadius);

  React.useEffect(() => {
    setMaxRadius(baselineRadius);
    setMinSimilarity(0);
    setNewerOnly(false);
    setPremiumOnly(false);
    setSamePropertyTypeOnly(false);
  }, [baselineRadius]);

  const filteredComparables = React.useMemo(() => {
    const filtered = comparables.filter((comparable) => {
      if ((comparable.dist_m ?? Number.POSITIVE_INFINITY) > maxRadius) return false;
      if ((comparable.similarity_score ?? comparable.feature_similarity ?? 0) < minSimilarity) return false;
      if (newerOnly && (comparable.age_days ?? Number.POSITIVE_INFINITY) > 90) return false;
      if (premiumOnly && !isPremiumComparable(comparable)) return false;
      if (samePropertyTypeOnly && subjectPropertyType && comparable.property_type !== subjectPropertyType) return false;
      return true;
    });
    return sortComparables(filtered, sortKey);
  }, [comparables, maxRadius, minSimilarity, newerOnly, premiumOnly, samePropertyTypeOnly, sortKey, subjectPropertyType]);

  if (comparables.length === 0) {
    return (
      <GlassPanel className="p-6">
        <p className="font-label-caps text-xs text-primary-fixed-dim">Comparables</p>
        <p className="mt-2 text-sm text-on-surface-variant">No comparable listings were returned for this valuation.</p>
      </GlassPanel>
    );
  }

  const selected = selectedComparable && comparables.some((comparable) => comparable.listing_id === selectedComparable.listing_id)
    ? selectedComparable
    : filteredComparables[0] ?? null;

  return (
    <motion.section variants={stagedReveal} initial="hidden" animate="show" className="grid gap-4">
      <div className="flex flex-wrap items-end justify-between gap-4 border-b border-white/5 pb-2">
        <div>
          <p className="font-label-caps text-xs text-primary-fixed-dim">Comparable Evidence</p>
          <h2 className="mt-1 font-headline-lg-mobile text-on-surface">Top deterministic matches</h2>
        </div>
        <span className="font-data-tabular text-xs text-outline">{filteredComparables.length} / {comparables.length} shown</span>
      </div>

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1.05fr)_minmax(360px,0.95fr)]">
        <div className="grid gap-4">
          <EvidenceMap result={result} comparables={filteredComparables} />

          <GlassPanel className="grid gap-4 p-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <span className="inline-flex items-center gap-2 font-label-caps text-xs text-primary-fixed-dim">
                <SlidersHorizontal className="h-4 w-4" />
                Exploration Filters
              </span>
              <span className="font-data-tabular text-[10px] text-outline">Authoritative valuation frozen</span>
            </div>

            <div className="grid gap-4 md:grid-cols-3">
              <label className="grid gap-2">
                <span className="font-label-caps text-[10px] text-on-surface-variant">Radius {formatDistance(maxRadius)}</span>
                <input
                  aria-label="Comparable radius filter"
                  type="range"
                  min="100"
                  max={baselineRadius}
                  step="100"
                  value={maxRadius}
                  onChange={(event) => setMaxRadius(Number(event.currentTarget.value))}
                  className="accent-primary-fixed-dim"
                />
              </label>
              <label className="grid gap-2">
                <span className="font-label-caps text-[10px] text-on-surface-variant">Similarity {formatPercent(minSimilarity)}</span>
                <input
                  aria-label="Comparable similarity filter"
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={minSimilarity}
                  onChange={(event) => setMinSimilarity(Number(event.currentTarget.value))}
                  className="accent-tertiary-fixed-dim"
                />
              </label>
              <label className="grid gap-2">
                <span className="font-label-caps text-[10px] text-on-surface-variant">Sort</span>
                <select
                  aria-label="Comparable sort order"
                  value={sortKey}
                  onChange={(event) => setSortKey(event.currentTarget.value as SortKey)}
                  className="h-10 rounded-lg border border-white/10 bg-surface/50 px-3 font-data-tabular text-xs text-on-surface outline-none"
                >
                  <option value="weighted">Weighted contribution</option>
                  <option value="distance">Distance</option>
                  <option value="recency">Recency</option>
                  <option value="similarity">Similarity</option>
                  <option value="price">Price</option>
                </select>
              </label>
            </div>

            <div className="flex flex-wrap gap-2">
              <Button type="button" variant={newerOnly ? "holo" : "ghost"} size="sm" onClick={() => setNewerOnly((value) => !value)}>
                <Clock3 className="h-4 w-4" />
                Newer
              </Button>
              <Button type="button" variant={premiumOnly ? "holo" : "ghost"} size="sm" onClick={() => setPremiumOnly((value) => !value)}>
                <ShieldCheck className="h-4 w-4" />
                Premium
              </Button>
              <Button type="button" variant={samePropertyTypeOnly ? "holo" : "ghost"} size="sm" onClick={() => setSamePropertyTypeOnly((value) => !value)}>
                <Filter className="h-4 w-4" />
                Same Type
              </Button>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => {
                  setMaxRadius(baselineRadius);
                  setMinSimilarity(0);
                  setNewerOnly(false);
                  setPremiumOnly(false);
                  setSamePropertyTypeOnly(false);
                  setSortKey("weighted");
                }}
              >
                <ArrowDownUp className="h-4 w-4" />
                Reset
              </Button>
            </div>
          </GlassPanel>
        </div>

        <div className="grid content-start gap-4">
          {selected && (
            <GlassPanel className="p-5">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-label-caps text-xs text-primary-fixed-dim">Comparable Drilldown</p>
                  <h3 className="mt-1 truncate font-data-tabular text-sm text-on-surface">{selected.listing_id}</h3>
                </div>
                <span className="rounded-md border border-primary-fixed-dim/20 px-2 py-1 font-data-tabular text-xs text-primary-fixed-dim">
                  {formatPercent(selected.weighted_contribution)}
                </span>
              </div>
              <div className="mt-4 grid grid-cols-2 gap-3 text-xs">
                <div>
                  <span className="font-label-caps text-[10px] text-outline">Feature Similarity</span>
                  <p className="mt-1 font-data-tabular text-on-surface">{formatPercent(selected.feature_similarity ?? selected.similarity_score)}</p>
                </div>
                <div>
                  <span className="font-label-caps text-[10px] text-outline">Amenity Similarity</span>
                  <p className="mt-1 font-data-tabular text-on-surface">{formatPercent(selected.amenity_similarity)}</p>
                </div>
                <div>
                  <span className="font-label-caps text-[10px] text-outline">Geographic Similarity</span>
                  <p className="mt-1 font-data-tabular text-on-surface">{formatPercent(selected.geographic_similarity ?? selected.distance_weight)}</p>
                </div>
                <div>
                  <span className="font-label-caps text-[10px] text-outline">Recency Weight</span>
                  <p className="mt-1 font-data-tabular text-on-surface">{formatPercent(selected.recency_weight)}</p>
                </div>
                <div>
                  <span className="font-label-caps text-[10px] text-outline">Confidence Contribution</span>
                  <p className="mt-1 font-data-tabular text-on-surface">{formatPercent(selected.confidence_contribution)}</p>
                </div>
              </div>
              <div className="mt-4 border-t border-white/5 pt-4">
                <span className="font-label-caps text-[10px] text-outline">Feature Overlap</span>
                <p className="mt-2 text-sm leading-6 text-on-surface-variant">
                  Matched {amenityOverlap(selected, "matched_amenities").join(", ") || "none"}; missing {amenityOverlap(selected, "missing_amenities").join(", ") || "none"}.
                </p>
              </div>
            </GlassPanel>
          )}

          <div className="grid gap-3">
            {filteredComparables.map((comparable) => {
              const isSelected = selectedComparable?.listing_id === comparable.listing_id;
              return (
                <motion.button
                  key={comparable.listing_id}
                  variants={revealItem}
                  type="button"
                  data-testid={`comparable-card-${comparable.listing_id}`}
                  onClick={() => setSelectedComparable(isSelected ? null : comparable)}
                  className="text-left"
                >
                  <GlassPanel
                    className={cn(
                      "grid gap-4 border p-4 transition-transform hover:-translate-y-0.5",
                      isSelected ? "border-primary-fixed-dim/40 bg-primary-fixed-dim/5" : "border-white/5",
                    )}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="min-w-0">
                        <p className="truncate font-data-tabular text-sm font-semibold text-on-surface">{comparable.listing_id}</p>
                        <p className="mt-1 truncate text-xs text-on-surface-variant">{comparable.area_name ?? comparable.location_text ?? "Resolved area"}</p>
                      </div>
                      <span className="shrink-0 rounded-md border border-primary-fixed-dim/20 bg-primary-fixed-dim/5 px-2 py-1 font-data-tabular text-xs text-primary-fixed-dim">
                        Tier {comparable.retrieval_tier ?? comparable.tier_label ?? "-"}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
                      <div>
                        <span className="font-label-caps text-[10px] text-outline">Price</span>
                        <p className="mt-1 font-data-tabular text-sm text-on-surface">{formatEgp(comparable.price_egp)}</p>
                      </div>
                      <div>
                        <span className="font-label-caps text-[10px] text-outline">SQM</span>
                        <p className="mt-1 font-data-tabular text-sm text-on-surface">{comparable.size_sqm ?? "-"} sqm</p>
                      </div>
                      <div>
                        <span className="font-label-caps text-[10px] text-outline">Beds/Baths</span>
                        <p className="mt-1 inline-flex items-center gap-2 font-data-tabular text-sm text-on-surface">
                          <BedDouble className="h-3 w-3" /> {comparable.bedrooms ?? "-"}
                          <Bath className="h-3 w-3" /> {comparable.bathrooms ?? "-"}
                        </p>
                      </div>
                      <div>
                        <span className="font-label-caps text-[10px] text-outline">Distance</span>
                        <p className="mt-1 inline-flex items-center gap-1 font-data-tabular text-sm text-on-surface">
                          <MapPin className="h-3 w-3" />
                          {formatDistance(comparable.dist_m)}
                        </p>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-2 border-t border-white/5 pt-3 text-xs md:grid-cols-4">
                      <span className="font-data-tabular text-on-surface-variant">Recency {formatAge(comparable.age_days)}</span>
                      <span className="font-data-tabular text-on-surface-variant">Similarity {formatPercent(comparable.similarity_score)}</span>
                      <span className="font-data-tabular text-on-surface-variant">Amenity {formatPercent(comparable.amenity_similarity)}</span>
                      <span className="font-data-tabular text-on-surface-variant">Weight {formatPercent(comparable.weighted_contribution)}</span>
                      <span className="inline-flex items-center gap-1 font-data-tabular text-on-surface-variant">
                        <Building2 className="h-3 w-3" />
                        {comparable.property_type ?? "Property"}
                      </span>
                    </div>
                  </GlassPanel>
                </motion.button>
              );
            })}
          </div>
        </div>
      </div>
    </motion.section>
  );
}
