import * as React from "react";
import { motion } from "framer-motion";
import { Calculator, Layers3, RotateCcw, SendHorizonal } from "lucide-react";
import { ValorApiError } from "@/api/contracts";
import { revealItem, stagedReveal } from "@/animations/motion";
import { HeroValuationCard } from "@/components/valuation/HeroValuationCard";
import { Button } from "@/components/ui/button";
import { GlassCard, GlassPanel } from "@/components/ui/glass";
import { ComparablePanel } from "@/features/comparables/ComparablePanel";
import { ExplainabilityPanel } from "@/features/explainability/ExplainabilityPanel";
import { useFairRentValuation } from "@/hooks/useFairRentValuation";
import { useAiContinuityStore } from "@/store/aiContinuityStore";
import { useBrokerStore } from "@/store/brokerStore";
import { useValuationStore } from "@/store/valuationStore";
import {
  AMENITY_OPTIONS,
  CATEGORY_PROPERTY_TYPES,
  PROPERTY_CATEGORIES,
  PropertyCategory,
  PropertyType,
  RentFairPriceRequest,
} from "@/types/valuation";

function numericValue(value: string, fallback: number): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function optionalNumber(value: string): number | null {
  if (value.trim() === "") return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

interface FieldProps {
  label: string;
  children: React.ReactNode;
}

function Field({ label, children }: FieldProps) {
  return (
    <label className="grid gap-2">
      <span className="font-label-caps text-[10px] text-on-surface-variant">{label}</span>
      {children}
    </label>
  );
}

const inputClass =
  "h-11 w-full rounded-lg border border-white/10 bg-surface/40 px-3 font-data-tabular text-sm text-on-surface outline-none transition-colors focus:border-primary-fixed-dim/50";

function categoryPropertyTypes(category?: PropertyCategory): PropertyType[] {
  return CATEGORY_PROPERTY_TYPES[category ?? "residential_rent"] ?? CATEGORY_PROPERTY_TYPES.residential_rent;
}

function categoryAmenityOptions(category?: PropertyCategory) {
  const active = category ?? "residential_rent";
  return AMENITY_OPTIONS.filter((option) => option.categories.includes(active));
}

function categoryUsesRooms(category?: PropertyCategory): boolean {
  return category === "residential_rent" || category === "residential_sale" || category === "villa_sale" || category == null;
}

function categoryUsesFloor(category?: PropertyCategory): boolean {
  return category !== "land_sale" && category !== "villa_sale";
}

export function ValuationScreen() {
  const { draft, setDraft, updateDraft, resetDraft, lastResult, lastRequest, setLastResult, lastRequestId } = useValuationStore();
  const { setActiveValuation } = useBrokerStore();
  const { setOrbState, pushEvent } = useAiContinuityStore();
  const valuation = useFairRentValuation();
  const { mutate, reset, cancel, isPending } = valuation;
  const error = valuation.error instanceof ValorApiError ? valuation.error : null;
  const [showAdvancedLocation, setShowAdvancedLocation] = React.useState(false);

  const submitValuation = React.useCallback(
    (event?: React.FormEvent<HTMLFormElement>) => {
      event?.preventDefault();
      setOrbState("analyzing");
      pushEvent("Rent fair-price valuation submitted");

      const payload: RentFairPriceRequest = {
        ...draft,
        property_category: draft.property_category ?? "residential_rent",
        address: draft.location_mode === "address_resolution" ? draft.address?.trim() : undefined,
        canonical_entity_id: draft.location_mode === "canonical_entity" ? draft.canonical_entity_id : null,
        lat: draft.location_mode === "manual_coordinates" ? draft.lat : undefined,
        lng: draft.location_mode === "manual_coordinates" ? draft.lng : undefined,
        amenities: draft.amenities ?? [],
      };

      mutate(payload, {
        onSuccess: ({ data, meta }) => {
          setLastResult(data, meta.request_id, payload);
          setActiveValuation(data);
          setOrbState("responding");
          pushEvent(`Valuation completed with ${data.confidence.label.toLowerCase()} confidence`);
        },
        onError: () => {
          setOrbState("idle");
          pushEvent("Valuation request failed");
        },
      });
    },
    [draft, mutate, pushEvent, setActiveValuation, setLastResult, setOrbState],
  );

  const cancelValuation = React.useCallback(() => {
    cancel();
    reset();
    setOrbState("idle");
    pushEvent("Valuation request cancelled");
  }, [cancel, pushEvent, reset, setOrbState]);

  const retryValuation = React.useCallback(() => submitValuation(), [submitValuation]);
  const activeCategory = draft.property_category ?? "residential_rent";
  const allowedPropertyTypes = React.useMemo(() => categoryPropertyTypes(activeCategory), [activeCategory]);
  const amenityOptions = React.useMemo(() => categoryAmenityOptions(activeCategory), [activeCategory]);
  const showRooms = categoryUsesRooms(activeCategory);
  const showFloor = categoryUsesFloor(activeCategory);

  const updateCategory = React.useCallback(
    (category: PropertyCategory) => {
      const allowed = categoryPropertyTypes(category);
      const nextAmenities = (draft.amenities ?? []).filter((code) =>
        categoryAmenityOptions(category).some((option) => option.symbol === code),
      );
      setDraft({
        ...draft,
        property_category: category,
        property_type: allowed.includes(draft.property_type) ? draft.property_type : allowed[0],
        bedrooms: categoryUsesRooms(category) ? draft.bedrooms : null,
        bathrooms: categoryUsesRooms(category) ? draft.bathrooms : null,
        floor_number: categoryUsesFloor(category) ? draft.floor_number : null,
        amenities: nextAmenities,
      });
    },
    [draft, setDraft],
  );

  const toggleAmenity = React.useCallback(
    (symbol: string) => {
      const current = new Set(draft.amenities ?? []);
      if (current.has(symbol)) {
        current.delete(symbol);
      } else {
        current.add(symbol);
      }
      updateDraft("amenities", Array.from(current).sort());
    },
    [draft.amenities, updateDraft],
  );

  React.useEffect(() => {
    if (!isPending) {
      const timer = window.setTimeout(() => setOrbState("idle"), 1600);
      return () => window.clearTimeout(timer);
    }
  }, [isPending, setOrbState]);

  return (
    <motion.div variants={stagedReveal} initial="hidden" animate="show" className="mx-auto flex w-full max-w-7xl flex-col gap-8 p-4 md:p-8">
      <motion.div variants={revealItem} className="grid gap-2">
        <p className="font-label-caps text-xs text-primary-fixed-dim">Governed Valuation Engine</p>
        <h1 className="font-headline-lg-mobile text-on-surface md:font-headline-lg">Evidence-backed property intelligence</h1>
        <p className="max-w-3xl text-sm leading-6 text-on-surface-variant">
          Submit a real property profile to the FastAPI valuation engine. Results are derived from deterministic comparable retrieval, category contracts, confidence scoring, and explainability traces.
        </p>
      </motion.div>

      <div className="grid gap-6 xl:grid-cols-[420px_1fr]">
        <motion.form variants={revealItem} onSubmit={submitValuation}>
          <GlassCard className="grid gap-5 p-5 md:p-6">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="font-label-caps text-xs text-primary-fixed-dim">Request</p>
                <h2 className="mt-1 font-body-md text-on-surface">Category valuation profile</h2>
              </div>
              <Calculator className="h-5 w-5 text-primary-fixed-dim" />
            </div>

            <div className="grid gap-3">
              <span className="font-label-caps text-[10px] text-on-surface-variant">Property Category</span>
              <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
                {PROPERTY_CATEGORIES.map((category) => {
                  const selected = activeCategory === category.value;
                  return (
                    <button
                      key={category.value}
                      type="button"
                      onClick={() => updateCategory(category.value)}
                      className={[
                        "flex min-h-10 items-center justify-center rounded-lg border px-3 text-center font-label-caps text-[10px] transition-colors",
                        selected
                          ? "border-primary-fixed-dim/50 bg-primary-fixed-dim/15 text-primary-fixed-dim"
                          : "border-white/10 bg-surface/30 text-on-surface-variant hover:border-white/20",
                      ].join(" ")}
                    >
                      {category.label}
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="grid gap-2">
              <div className="flex items-center justify-between">
                <span className="font-label-caps text-[10px] text-on-surface-variant">Location (Address or District)</span>
                <button
                  type="button"
                  className="text-[10px] font-label-caps text-primary-fixed-dim hover:underline"
                  onClick={() => {
                    setShowAdvancedLocation((shown) => {
                      const next = !shown;
                      setDraft({
                        ...draft,
                        location_mode: next ? "manual_coordinates" : "address_resolution",
                        address: next ? "" : draft.address,
                        canonical_entity_id: null,
                        lat: next ? draft.lat : undefined,
                        lng: next ? draft.lng : undefined,
                      });
                      return next;
                    });
                  }}
                >
                  {showAdvancedLocation ? "Hide Advanced" : "Advanced (Lat/Lng)"}
                </button>
              </div>
              <input
                className={inputClass}
                type="text"
                placeholder="e.g. Madinaty, Cairo"
                value={draft.address ?? ""}
                onChange={(event) => {
                  updateDraft("location_mode", "address_resolution");
                  updateDraft("address", event.currentTarget.value);
                }}
                required={!showAdvancedLocation}
              />
            </div>

            {showAdvancedLocation && (
              <div className="grid grid-cols-2 gap-4">
                <Field label="Latitude">
                  <input
                    className={inputClass}
                    type="number"
                    step="0.000001"
                    value={draft.lat ?? ""}
                    onChange={(event) => {
                      updateDraft("location_mode", "manual_coordinates");
                      updateDraft("lat", optionalNumber(event.currentTarget.value));
                    }}
                    required={showAdvancedLocation}
                  />
                </Field>
                <Field label="Longitude">
                  <input
                    className={inputClass}
                    type="number"
                    step="0.000001"
                    value={draft.lng ?? ""}
                    onChange={(event) => {
                      updateDraft("location_mode", "manual_coordinates");
                      updateDraft("lng", optionalNumber(event.currentTarget.value));
                    }}
                    required={showAdvancedLocation}
                  />
                </Field>
              </div>
            )}

            <Field label="Property Type">
              <select
                className={inputClass}
                value={draft.property_type}
                onChange={(event) => updateDraft("property_type", event.currentTarget.value as PropertyType)}
              >
                {allowedPropertyTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </Field>

            <div className={showRooms ? "grid grid-cols-3 gap-4" : "grid grid-cols-1 gap-4"}>
              {showRooms && (
                <>
                  <Field label="Bedrooms">
                    <input
                      className={inputClass}
                      type="number"
                      min="0"
                      value={draft.bedrooms ?? ""}
                      onChange={(event) => updateDraft("bedrooms", optionalNumber(event.currentTarget.value))}
                    />
                  </Field>
                  <Field label="Bathrooms">
                    <input
                      className={inputClass}
                      type="number"
                      min="0"
                      value={draft.bathrooms ?? ""}
                      onChange={(event) => updateDraft("bathrooms", optionalNumber(event.currentTarget.value))}
                    />
                  </Field>
                </>
              )}
              <Field label="Size sqm">
                <input
                  className={inputClass}
                  type="number"
                  min="1"
                  value={draft.size_sqm}
                  onChange={(event) => updateDraft("size_sqm", numericValue(event.currentTarget.value, draft.size_sqm))}
                  required
                />
              </Field>
            </div>

            <div className={showFloor ? "grid grid-cols-2 gap-4" : "grid gap-4"}>
              {showFloor && (
                <Field label="Floor Level">
                  <input
                    className={inputClass}
                    type="number"
                    value={draft.floor_number ?? ""}
                    onChange={(event) => updateDraft("floor_number", optionalNumber(event.currentTarget.value))}
                  />
                </Field>
              )}
              <Field label="Finishing / Quality">
                <select
                  className={inputClass}
                  value={draft.building_quality ?? ""}
                  onChange={(event) => updateDraft("building_quality", event.currentTarget.value || null)}
                >
                  <option value="">Unspecified</option>
                  <option value="standard">Standard</option>
                  <option value="premium">Premium</option>
                  <option value="luxury">Luxury</option>
                  <option value="renovated">Renovated</option>
                  <option value="new">New</option>
                </select>
              </Field>
            </div>

            <div className="grid gap-3">
              <span className="inline-flex items-center gap-2 font-label-caps text-[10px] text-on-surface-variant">
                <Layers3 className="h-3.5 w-3.5" />
                Governed Amenities
              </span>
              <div className="flex flex-wrap gap-2">
                {amenityOptions.map((amenity) => {
                  const selected = draft.amenities?.includes(amenity.symbol);
                  return (
                    <button
                      key={amenity.symbol}
                      type="button"
                      onClick={() => toggleAmenity(amenity.symbol)}
                      className={[
                        "rounded-md border px-2.5 py-1.5 font-data-tabular text-xs transition-colors",
                        selected
                          ? "border-tertiary-fixed-dim/40 bg-tertiary-fixed-dim/10 text-tertiary-fixed-dim"
                          : "border-white/10 bg-surface/30 text-on-surface-variant hover:border-white/20",
                      ].join(" ")}
                    >
                      {amenity.label}
                    </button>
                  );
                })}
              </div>
            </div>

            <Field label="Target Price EGP">
              <input
                className={inputClass}
                type="number"
                min="1"
                value={draft.target_price_egp ?? ""}
                onChange={(event) => updateDraft("target_price_egp", optionalNumber(event.currentTarget.value))}
              />
            </Field>

            <div className="flex flex-col gap-3 sm:flex-row">
              <Button type="submit" variant="holo" className="flex-1" disabled={isPending}>
                <SendHorizonal className="h-4 w-4" />
                Estimate
              </Button>
              <Button
                type="button"
                variant="ghost"
                onClick={() => {
                  resetDraft();
                  reset();
                }}
              >
                <RotateCcw className="h-4 w-4" />
                Reset
              </Button>
            </div>

            <GlassPanel className="p-4">
              <p className="font-label-caps text-[10px] text-outline">Contract</p>
              <p className="mt-1 text-sm text-on-surface-variant">POST /v1/valuation/fair-price</p>
            </GlassPanel>
          </GlassCard>
        </motion.form>

        <motion.div variants={revealItem}>
          <HeroValuationCard
            result={lastResult}
            targetPrice={draft.target_price_egp}
            requestId={lastRequestId}
            isLoading={isPending}
            error={error}
            onRetry={retryValuation}
            onCancel={cancelValuation}
          />
        </motion.div>
      </div>

      {lastResult && (
        <div className="grid gap-8">
          <ComparablePanel comparables={lastResult.top_comps} result={lastResult} subjectPropertyType={lastRequest?.property_type} />
          <ExplainabilityPanel result={lastResult} />
        </div>
      )}
    </motion.div>
  );
}
