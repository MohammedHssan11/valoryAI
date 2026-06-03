import * as React from "react";
import { LocateFixed, MapPinned, Minus, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GlassPanel } from "@/components/ui/glass";
import { cn } from "@/lib/utils";
import { useComparableAnalysisStore } from "@/store/comparableAnalysisStore";
import type { ComparableItem, RentFairPriceData } from "@/types/valuation";

interface EvidenceMapProps {
  result?: RentFairPriceData | null;
  comparables: ComparableItem[];
  className?: string;
}

interface Point {
  lat: number;
  lng: number;
}

function numeric(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

function getSubjectPoint(result?: RentFairPriceData | null): Point | null {
  const subject = result?.spatial_diagnostics?.subject as Record<string, unknown> | undefined;
  const subjectLat = numeric(subject?.lat);
  const subjectLng = numeric(subject?.lng);
  if (subjectLat !== null && subjectLng !== null) return { lat: subjectLat, lng: subjectLng };

  const resolvedLat = numeric(result?.resolved_location?.lat);
  const resolvedLng = numeric(result?.resolved_location?.lng);
  if (resolvedLat !== null && resolvedLng !== null) return { lat: resolvedLat, lng: resolvedLng };
  return null;
}

function project(subject: Point, comparable: ComparableItem) {
  if (typeof comparable.lat !== "number" || typeof comparable.lng !== "number") return null;
  const metersPerDegreeLat = 110_540;
  const metersPerDegreeLng = 111_320 * Math.cos((subject.lat * Math.PI) / 180);
  return {
    x: (comparable.lng - subject.lng) * metersPerDegreeLng,
    y: (subject.lat - comparable.lat) * metersPerDegreeLat,
  };
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

export function EvidenceMap({ result, comparables, className }: EvidenceMapProps) {
  const { selectedComparable, setSelectedComparable } = useComparableAnalysisStore();
  const [zoom, setZoom] = React.useState(1);
  const [pan, setPan] = React.useState({ x: 0, y: 0 });
  const svgRef = React.useRef<SVGSVGElement | null>(null);
  const dragRef = React.useRef<{ x: number; y: number; panX: number; panY: number } | null>(null);
  const subject = getSubjectPoint(result);
  const retrievalRadius = numeric(result?.spatial_diagnostics?.retrieval_radius_m) ?? Math.max(...comparables.map((comp) => comp.dist_m ?? 0), 500);

  const projected = React.useMemo(() => {
    if (!subject) return [];
    return comparables
      .map((comparable) => {
        const point = project(subject, comparable);
        return point ? { comparable, ...point } : null;
      })
      .filter((item): item is { comparable: ComparableItem; x: number; y: number } => item !== null)
      .sort((a, b) => {
        const aRank = a.comparable.evidence_rank ?? Number.MAX_SAFE_INTEGER;
        const bRank = b.comparable.evidence_rank ?? Number.MAX_SAFE_INTEGER;
        return aRank - bRank || a.comparable.listing_id.localeCompare(b.comparable.listing_id);
      });
  }, [comparables, subject]);

  const extent = React.useMemo(() => {
    const maxPoint = projected.reduce((max, point) => Math.max(max, Math.abs(point.x), Math.abs(point.y)), 0);
    return Math.max(retrievalRadius || 500, maxPoint + 250, 500);
  }, [projected, retrievalRadius]);
  const half = extent / zoom;
  const viewBox = `${pan.x - half} ${pan.y - half} ${half * 2} ${half * 2}`;
  const distanceBands = (result?.spatial_diagnostics?.distance_band_counts ?? {}) as Record<string, number>;

  const startDrag = React.useCallback((event: React.PointerEvent<SVGSVGElement>) => {
    dragRef.current = { x: event.clientX, y: event.clientY, panX: pan.x, panY: pan.y };
    event.currentTarget.setPointerCapture(event.pointerId);
  }, [pan.x, pan.y]);

  const moveDrag = React.useCallback((event: React.PointerEvent<SVGSVGElement>) => {
    if (!dragRef.current || !svgRef.current) return;
    const rect = svgRef.current.getBoundingClientRect();
    const metersPerPx = (half * 2) / Math.max(rect.width, 1);
    setPan({
      x: dragRef.current.panX - (event.clientX - dragRef.current.x) * metersPerPx,
      y: dragRef.current.panY - (event.clientY - dragRef.current.y) * metersPerPx,
    });
  }, [half]);

  const endDrag = React.useCallback(() => {
    dragRef.current = null;
  }, []);

  if (!subject || projected.length === 0) {
    return (
      <GlassPanel className={cn("grid min-h-[320px] place-items-center p-6", className)}>
        <div className="text-center">
          <MapPinned className="mx-auto h-5 w-5 text-primary-fixed-dim" />
          <p className="mt-3 font-label-caps text-xs text-primary-fixed-dim">Spatial Evidence Map</p>
          <p className="mt-2 text-sm text-on-surface-variant">Coordinate-backed comparable evidence is unavailable for this valuation.</p>
        </div>
      </GlassPanel>
    );
  }

  return (
    <GlassPanel className={cn("grid gap-4 p-4 md:p-5", className)}>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="font-label-caps text-xs text-primary-fixed-dim">Spatial Evidence Map</p>
          <p className="mt-1 font-data-tabular text-xs text-outline">{projected.length} plotted comps | radius {formatDistance(retrievalRadius)}</p>
        </div>
        <div className="flex items-center gap-2">
          <Button type="button" variant="ghost" size="sm" aria-label="Zoom in" title="Zoom in" onClick={() => setZoom((value) => Math.min(value * 1.25, 4))}>
            <Plus className="h-4 w-4" />
          </Button>
          <Button type="button" variant="ghost" size="sm" aria-label="Zoom out" title="Zoom out" onClick={() => setZoom((value) => Math.max(value / 1.25, 0.5))}>
            <Minus className="h-4 w-4" />
          </Button>
          <Button type="button" variant="ghost" size="sm" aria-label="Recenter map" title="Recenter map" onClick={() => setPan({ x: 0, y: 0 })}>
            <LocateFixed className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="overflow-hidden rounded-lg border border-white/10 bg-surface-container-lowest">
        <svg
          ref={svgRef}
          role="img"
          aria-label="Deterministic comparable evidence map"
          viewBox={viewBox}
          className="h-[360px] w-full cursor-grab touch-none select-none"
          onPointerDown={startDrag}
          onPointerMove={moveDrag}
          onPointerUp={endDrag}
          onPointerCancel={endDrag}
        >
          <defs>
            <pattern id="evidence-grid" width="250" height="250" patternUnits="userSpaceOnUse">
              <path d="M 250 0 L 0 0 0 250" fill="none" stroke="rgba(132,148,149,0.18)" strokeWidth="4" />
            </pattern>
          </defs>
          <rect x={pan.x - half} y={pan.y - half} width={half * 2} height={half * 2} fill="url(#evidence-grid)" />
          <circle cx="0" cy="0" r={retrievalRadius} fill="rgba(0,219,231,0.035)" stroke="rgba(0,219,231,0.32)" strokeWidth={Math.max(8 / zoom, 2)} strokeDasharray={`${80 / zoom} ${46 / zoom}`} />
          <circle cx="0" cy="0" r={retrievalRadius / 2} fill="none" stroke="rgba(78,222,163,0.18)" strokeWidth={Math.max(5 / zoom, 1.5)} />
          {projected.map(({ comparable, x, y }) => {
            const selected = selectedComparable?.listing_id === comparable.listing_id;
            const weight = comparable.weighted_contribution ?? comparable.weight ?? 0;
            const radius = Math.max(18, 14 + weight * 60);
            return (
              <g key={comparable.listing_id}>
                <line x1="0" y1="0" x2={x} y2={y} stroke={selected ? "rgba(255,255,255,0.72)" : "rgba(132,148,149,0.26)"} strokeWidth={selected ? Math.max(8 / zoom, 2.5) : Math.max(4 / zoom, 1.2)} />
                <g
                  role="button"
                  tabIndex={0}
                  aria-label={`Select comparable ${comparable.listing_id}`}
                  onClick={() => setSelectedComparable(selected ? null : comparable)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter" || event.key === " ") {
                      event.preventDefault();
                      setSelectedComparable(selected ? null : comparable);
                    }
                  }}
                >
                  <circle
                    cx={x}
                    cy={y}
                    r={radius / zoom}
                    fill={selected ? "rgba(0,219,231,0.95)" : "rgba(78,222,163,0.82)"}
                    stroke={selected ? "white" : "rgba(225,253,255,0.72)"}
                    strokeWidth={Math.max(6 / zoom, 2)}
                  >
                    <title>{`${comparable.listing_id} | ${formatDistance(comparable.dist_m)} | similarity ${formatPercent(comparable.similarity_score)}`}</title>
                  </circle>
                </g>
              </g>
            );
          })}
          <circle cx="0" cy="0" r={24 / zoom} fill="white" stroke="#00dbe7" strokeWidth={Math.max(8 / zoom, 2)} />
          <text x={36 / zoom} y={-30 / zoom} fill="#e1fdff" fontSize={42 / zoom} fontFamily="JetBrains Mono, monospace">SUBJECT</text>
        </svg>
      </div>

      <div className="grid gap-3 text-xs text-on-surface-variant md:grid-cols-[1fr_1fr]">
        <div className="flex flex-wrap gap-2">
          <span className="rounded-md border border-primary-fixed-dim/20 px-2 py-1 font-data-tabular text-primary-fixed-dim">Subject</span>
          <span className="rounded-md border border-tertiary-fixed-dim/20 px-2 py-1 font-data-tabular text-tertiary-fixed-dim">Comparable</span>
          <span className="rounded-md border border-white/10 px-2 py-1 font-data-tabular text-outline">Radius {formatDistance(retrievalRadius)}</span>
        </div>
        <div className="flex flex-wrap gap-2 md:justify-end">
          {Object.entries(distanceBands).map(([band, count]) => (
            <span key={band} className="rounded-md border border-white/10 px-2 py-1 font-data-tabular text-outline">
              {band.replace(/_/g, "-")}: {count}
            </span>
          ))}
        </div>
      </div>
    </GlassPanel>
  );
}
