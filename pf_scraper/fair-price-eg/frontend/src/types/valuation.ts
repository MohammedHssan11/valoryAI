export const PROPERTY_CATEGORIES = [
  { value: "residential_rent", label: "Residential Rent" },
  { value: "residential_sale", label: "Residential Sale" },
  { value: "villa_sale", label: "Villas" },
  { value: "office_rent", label: "Offices" },
  { value: "retail_rent", label: "Retail" },
  { value: "commercial_rent", label: "Commercial" },
  { value: "land_sale", label: "Land" },
] as const;

export type PropertyCategory = (typeof PROPERTY_CATEGORIES)[number]["value"];

export const PROPERTY_TYPES = [
  "Apartment",
  "Villa",
  "Townhouse",
  "Twin House",
  "Duplex",
  "Penthouse",
  "Chalet",
  "iVilla",
  "Hotel Apartment",
  "Office Space",
  "Co-Working Space",
  "Full Floor",
  "Half Floor",
  "Retail",
  "Shop",
  "Show Room",
  "Restaurant",
  "Cafeteria",
  "Clinic",
  "Factory",
  "Medical Facility",
  "Warehouse",
  "Whole Building",
  "Land",
  "Farm",
] as const;

export type PropertyType = (typeof PROPERTY_TYPES)[number];
export type ConfidenceLabel = "High" | "Medium" | "Low";
export type PriceFlag = "INSUFFICIENT_DATA" | "NO_TARGET" | "TOO_HIGH" | "TOO_LOW" | "OK";
export type LocationMode = "manual_coordinates" | "address_resolution" | "canonical_entity";

export interface RentFairPriceRequest {
  location_mode?: LocationMode;
  address?: string;
  canonical_entity_id?: string | null;
  lat?: number;
  lng?: number;
  property_type: PropertyType;
  property_category?: PropertyCategory;
  bedrooms?: number | null;
  bathrooms?: number | null;
  size_sqm: number;
  target_price_egp?: number | null;
  amenities: string[];
  furnishing_status?: string | null;
  floor_number?: number | null;
  compound_name?: string | null;
  view_type?: string | null;
  building_quality?: string | null;
}

export interface ConfidenceDTO {
  score: number;
  label: ConfidenceLabel;
  factors: Record<string, number>;
  dimensions?: Record<string, unknown>;
}

export interface ExplanationItem {
  reason_code: string;
  weight?: number | null;
  details: Record<string, unknown>;
}

export interface ComparableItem {
  listing_id: string;
  price_egp: number;
  size_sqm?: number | null;
  price_per_sqm?: number | null;
  property_type?: string | null;
  bedrooms?: number | null;
  bathrooms?: number | null;
  area_id?: number | null;
  area_name?: string | null;
  lat?: number | null;
  lng?: number | null;
  location_text?: string | null;
  images_count?: number | null;
  retrieval_tier?: number | null;
  tier_label?: string | null;
  reason_code?: string | null;
  radius_m?: number | null;
  dist_m?: number | null;
  age_days?: number | null;
  weight?: number | null;
  weight_components: Record<string, number>;
  weighted_contribution?: number | null;
  confidence_contribution?: number | null;
  similarity_score?: number | null;
  geographic_similarity?: number | null;
  distance_weight?: number | null;
  recency_weight?: number | null;
  evidence_rank?: number | null;
  property_category?: string | null;
  amenities: Array<Record<string, unknown>>;
  normalized_amenities: string[];
  canonical_amenity_symbols?: string[];
  unknown_amenity_codes: string[];
  furnishing_status?: string | null;
  floor_number?: number | null;
  compound_name?: string | null;
  view_type?: string | null;
  building_quality?: string | null;
  feature_similarity?: number | null;
  feature_similarity_components: Record<string, number>;
  feature_explanation: Record<string, unknown>;
  feature_overlap?: Record<string, unknown>;
  amenity_similarity?: number | null;
  amenity_explanation?: Record<string, unknown>;
  amenity_metadata?: Array<Record<string, unknown>>;
  filter_status?: Record<string, unknown>;
}

export interface RetrievalStageItem {
  tier?: number | null;
  tier_label?: string | null;
  reason_code: string;
  scope?: string | null;
  radius_m?: number | null;
  comps_found: number;
  threshold?: number | null;
  shortfall?: number | null;
  attempt_index?: number | null;
  status?: string | null;
  selected: boolean;
  radius_expansion_m?: number | null;
}

export interface RentFairPriceData {
  fair_price_egp: number;
  range_low_egp: number;
  range_high_egp: number;
  flag: PriceFlag;
  tier_used: number;
  comps_count: number;
  confidence: ConfidenceDTO;
  engine_used?: string;
  routing_reason?: string;
  explainability?: Record<string, unknown> | null;
  explanation: string[];
  explanation_trace: ExplanationItem[];
  retrieval_trace?: RetrievalStageItem[];
  spatial_diagnostics?: Record<string, unknown>;
  evidence_summary?: Record<string, unknown>;
  property_category?: PropertyCategory;
  valuation_contract?: Record<string, unknown>;
  amenity_intelligence?: Record<string, unknown>;
  area: Record<string, unknown>;
  resolved_location?: Record<string, unknown>;
  debug: Record<string, unknown>;
  top_comps: ComparableItem[];
}

export const CATEGORY_PROPERTY_TYPES: Record<PropertyCategory, PropertyType[]> = {
  residential_rent: ["Apartment", "Villa", "Townhouse", "Twin House", "Duplex", "Penthouse", "Chalet", "iVilla", "Hotel Apartment"],
  residential_sale: ["Apartment", "Duplex", "Penthouse", "Chalet", "Hotel Apartment"],
  villa_sale: ["Villa", "Townhouse", "Twin House", "iVilla"],
  office_rent: ["Office Space", "Co-Working Space", "Full Floor", "Half Floor"],
  retail_rent: ["Retail", "Shop", "Show Room", "Restaurant", "Cafeteria"],
  commercial_rent: ["Clinic", "Factory", "Medical Facility", "Warehouse", "Whole Building"],
  land_sale: ["Land", "Farm"],
};

export interface AmenityOption {
  symbol: string;
  label: string;
  categories: PropertyCategory[];
}

export const AMENITY_OPTIONS: AmenityOption[] = [
  { symbol: "FU", label: "Furnished", categories: ["residential_rent", "residential_sale", "villa_sale"] },
  { symbol: "CP", label: "Parking", categories: ["residential_rent", "villa_sale", "office_rent", "retail_rent", "commercial_rent"] },
  { symbol: "PP", label: "Pool", categories: ["villa_sale", "residential_sale", "residential_rent"] },
  { symbol: "EL", label: "Elevator", categories: ["residential_rent", "residential_sale", "office_rent"] },
  { symbol: "SE", label: "Security", categories: ["residential_rent", "residential_sale", "villa_sale", "office_rent"] },
  { symbol: "SH", label: "Smart Home", categories: ["residential_rent", "villa_sale"] },
  { symbol: "CM", label: "Compound", categories: ["residential_rent", "residential_sale", "villa_sale"] },
  { symbol: "SY", label: "Gym", categories: ["residential_rent", "residential_sale"] },
  { symbol: "PG", label: "Garden", categories: ["villa_sale", "residential_sale"] },
  { symbol: "MR", label: "Maid Room", categories: ["villa_sale", "residential_rent"] },
  { symbol: "AC", label: "Central AC", categories: ["residential_rent", "office_rent", "retail_rent"] },
  { symbol: "FN", label: "Finishing", categories: ["residential_sale", "villa_sale", "office_rent", "retail_rent"] },
  { symbol: "IT", label: "Internet", categories: ["office_rent", "residential_rent"] },
  { symbol: "WF", label: "Waterfront", categories: ["residential_sale", "villa_sale", "land_sale"] },
  { symbol: "CH", label: "Clubhouse", categories: ["residential_sale", "villa_sale"] },
  { symbol: "RF", label: "Retail Frontage", categories: ["retail_rent", "land_sale"] },
  { symbol: "OI", label: "Office Infrastructure", categories: ["office_rent", "commercial_rent"] },
  { symbol: "FR", label: "Frontage", categories: ["retail_rent", "land_sale"] },
  { symbol: "VI", label: "Visibility", categories: ["retail_rent"] },
  { symbol: "TR", label: "Traffic Exposure", categories: ["retail_rent"] },
  { symbol: "ZO", label: "Zoning", categories: ["land_sale", "commercial_rent"] },
  { symbol: "GE", label: "Geometry", categories: ["land_sale"] },
];
