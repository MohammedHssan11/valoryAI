CREATE TABLE IF NOT EXISTS property_category_contracts (
  category              TEXT PRIMARY KEY,
  label                 TEXT NOT NULL,
  listing_category      TEXT NOT NULL,
  period                TEXT NOT NULL,
  value_basis           TEXT NOT NULL,
  compatible_property_types JSONB NOT NULL DEFAULT '[]'::jsonb,
  valuation_constraints JSONB NOT NULL DEFAULT '{}'::jsonb,
  retrieval_strategy    JSONB NOT NULL DEFAULT '{}'::jsonb,
  weighting_profile     JSONB NOT NULL DEFAULT '{}'::jsonb,
  confidence_profile    JSONB NOT NULL DEFAULT '{}'::jsonb,
  governance            JSONB NOT NULL DEFAULT '{}'::jsonb,
  active                BOOLEAN NOT NULL DEFAULT TRUE,
  created_at_utc        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at_utc        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS amenity_governance_registry (
  symbol                TEXT PRIMARY KEY,
  canonical_name        TEXT NOT NULL,
  normalized_name       TEXT NOT NULL,
  arabic_name           TEXT,
  classification        TEXT NOT NULL,
  aliases               JSONB NOT NULL DEFAULT '[]'::jsonb,
  weight_profile        JSONB NOT NULL DEFAULT '{}'::jsonb,
  retrieval_metadata    JSONB NOT NULL DEFAULT '{}'::jsonb,
  active                BOOLEAN NOT NULL DEFAULT TRUE,
  created_at_utc        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at_utc        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_amenity_governance_normalized_name
  ON amenity_governance_registry(normalized_name);

CREATE INDEX IF NOT EXISTS ix_amenity_governance_active_classification
  ON amenity_governance_registry(active, classification);

CREATE INDEX IF NOT EXISTS ix_listings_amenities_gin
  ON listings USING gin(amenities);

CREATE INDEX IF NOT EXISTS ix_listings_normalized_amenities_gin
  ON listings USING gin(normalized_amenities);

INSERT INTO property_category_contracts (
  category, label, listing_category, period, value_basis,
  compatible_property_types, valuation_constraints, retrieval_strategy,
  weighting_profile, confidence_profile, governance
) VALUES
  (
    'residential_rent', 'Residential rent', 'rent', 'monthly', 'monthly_rent',
    '["Apartment","Bungalow","Cabin","Chalet","Duplex","Hotel Apartment","iVilla","Penthouse","Roof","Townhouse","Twin House","Villa"]'::jsonb,
    '{"max_price_egp":500000,"max_size_sqm":1000,"max_target_price_egp":500000}'::jsonb,
    '{"radius_multiplier":1.0,"stale_days_multiplier":1.0,"match_threshold":40}'::jsonb,
    '{"amenities":0.55,"furnishing":0.18,"compound":0.10,"floor":0.07,"view":0.05,"building_quality":0.05}'::jsonb,
    '{"base":0.84,"distance":0.05,"recency":0.05,"similarity":0.04,"amenity":0.02}'::jsonb,
    '{"deterministic_authority":true,"amenities_override_pricing":false,"llm_may_override":false}'::jsonb
  ),
  (
    'residential_sale', 'Residential sale', 'buy', 'sale', 'sale_price',
    '["Apartment","Chalet","Duplex","Hotel Apartment","Penthouse","Roof"]'::jsonb,
    '{"max_price_egp":250000000,"max_size_sqm":1500,"max_target_price_egp":250000000}'::jsonb,
    '{"radius_multiplier":1.1,"stale_days_multiplier":1.6,"match_threshold":30}'::jsonb,
    '{"amenities":0.45,"furnishing":0.08,"compound":0.16,"floor":0.08,"view":0.10,"building_quality":0.13}'::jsonb,
    '{"base":0.82,"distance":0.05,"recency":0.04,"similarity":0.05,"amenity":0.04}'::jsonb,
    '{"deterministic_authority":true,"amenities_override_pricing":false,"llm_may_override":false}'::jsonb
  ),
  (
    'villa_sale', 'Villa sale', 'buy', 'sale', 'sale_price',
    '["Villa","Townhouse","Twin House","iVilla","Palace"]'::jsonb,
    '{"max_price_egp":800000000,"max_size_sqm":5000,"max_target_price_egp":800000000}'::jsonb,
    '{"radius_multiplier":1.45,"stale_days_multiplier":2.0,"match_threshold":22}'::jsonb,
    '{"amenities":0.58,"furnishing":0.03,"compound":0.12,"floor":0.02,"view":0.10,"building_quality":0.15}'::jsonb,
    '{"base":0.80,"distance":0.05,"recency":0.04,"similarity":0.05,"amenity":0.06}'::jsonb,
    '{"deterministic_authority":true,"amenities_override_pricing":false,"llm_may_override":false}'::jsonb
  ),
  (
    'office_rent', 'Office rent', 'commercial_rent', 'monthly', 'monthly_rent',
    '["Office Space","Co-Working Space","Full Floor","Half Floor"]'::jsonb,
    '{"max_price_egp":1500000,"max_size_sqm":3000,"max_target_price_egp":1500000}'::jsonb,
    '{"radius_multiplier":1.25,"stale_days_multiplier":1.5,"match_threshold":25}'::jsonb,
    '{"amenities":0.52,"furnishing":0.02,"compound":0.18,"floor":0.14,"view":0.02,"building_quality":0.12}'::jsonb,
    '{"base":0.81,"distance":0.06,"recency":0.04,"similarity":0.04,"amenity":0.05}'::jsonb,
    '{"deterministic_authority":true,"amenities_override_pricing":false,"llm_may_override":false}'::jsonb
  ),
  (
    'retail_rent', 'Retail rent', 'commercial_rent', 'monthly', 'monthly_rent',
    '["Retail","Shop","Show Room","Restaurant","Cafeteria"]'::jsonb,
    '{"max_price_egp":2000000,"max_size_sqm":2500,"max_target_price_egp":2000000}'::jsonb,
    '{"radius_multiplier":1.15,"stale_days_multiplier":1.35,"match_threshold":25}'::jsonb,
    '{"amenities":0.68,"furnishing":0.01,"compound":0.08,"floor":0.08,"view":0.08,"building_quality":0.07}'::jsonb,
    '{"base":0.79,"distance":0.06,"recency":0.04,"similarity":0.04,"amenity":0.07}'::jsonb,
    '{"deterministic_authority":true,"amenities_override_pricing":false,"llm_may_override":false}'::jsonb
  ),
  (
    'commercial_rent', 'Commercial rent', 'commercial_rent', 'monthly', 'monthly_rent',
    '["Clinic","Factory","Medical Facility","Staff Accommodation","Warehouse","Whole Building"]'::jsonb,
    '{"max_price_egp":5000000,"max_size_sqm":10000,"max_target_price_egp":5000000}'::jsonb,
    '{"radius_multiplier":1.6,"stale_days_multiplier":2.0,"match_threshold":20}'::jsonb,
    '{"amenities":0.55,"furnishing":0.01,"compound":0.10,"floor":0.04,"view":0.02,"building_quality":0.28}'::jsonb,
    '{"base":0.80,"distance":0.05,"recency":0.04,"similarity":0.04,"amenity":0.07}'::jsonb,
    '{"deterministic_authority":true,"amenities_override_pricing":false,"llm_may_override":false}'::jsonb
  ),
  (
    'land_sale', 'Land sale', 'buy', 'sale', 'sale_price',
    '["Land","Farm"]'::jsonb,
    '{"max_price_egp":3000000000,"max_size_sqm":100000,"max_target_price_egp":3000000000}'::jsonb,
    '{"radius_multiplier":1.8,"stale_days_multiplier":2.5,"match_threshold":18}'::jsonb,
    '{"amenities":0.82,"furnishing":0.0,"compound":0.04,"floor":0.0,"view":0.02,"building_quality":0.12}'::jsonb,
    '{"base":0.77,"distance":0.05,"recency":0.03,"similarity":0.04,"amenity":0.11}'::jsonb,
    '{"deterministic_authority":true,"amenities_override_pricing":false,"llm_may_override":false}'::jsonb
  )
ON CONFLICT (category) DO UPDATE
SET
  label = EXCLUDED.label,
  listing_category = EXCLUDED.listing_category,
  period = EXCLUDED.period,
  value_basis = EXCLUDED.value_basis,
  compatible_property_types = EXCLUDED.compatible_property_types,
  valuation_constraints = EXCLUDED.valuation_constraints,
  retrieval_strategy = EXCLUDED.retrieval_strategy,
  weighting_profile = EXCLUDED.weighting_profile,
  confidence_profile = EXCLUDED.confidence_profile,
  governance = EXCLUDED.governance,
  active = TRUE,
  updated_at_utc = NOW();

INSERT INTO amenity_governance_registry (
  symbol, canonical_name, normalized_name, arabic_name, classification, aliases, weight_profile, retrieval_metadata
) VALUES
  ('BA','Balcony','balcony','بلكونة','core','["balcony","terrace"]'::jsonb,'{"residential_rent":0.04,"villa_sale":0.01}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('FU','Furnished','furnished','مفروش','fitout','["furnished","fully furnished"]'::jsonb,'{"residential_rent":0.05,"residential_sale":0.015}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('CP','Covered Parking','covered_parking','جراج مغطى','access','["parking","garage","covered parking"]'::jsonb,'{"residential_rent":0.03,"office_rent":0.065,"retail_rent":0.035}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('PP','Private Pool','private_pool','حمام سباحة خاص','leisure','["pool","private pool"]'::jsonb,'{"villa_sale":0.07,"residential_sale":0.03}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('EL','Elevator','elevator','مصعد','core','["elevator","lift"]'::jsonb,'{"residential_rent":0.045,"office_rent":0.05}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('SE','Security','security','أمن','core','["security","secured"]'::jsonb,'{"residential_rent":0.04,"villa_sale":0.03,"office_rent":0.035}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('SH','Smart Home','smart_home','منزل ذكي','technology','["smart home","home automation"]'::jsonb,'{"residential_rent":0.018,"villa_sale":0.025}'::jsonb,'{"retrieval_refinement":false}'::jsonb),
  ('CM','Compound','compound','كمبوند','location','["compound","gated community"]'::jsonb,'{"residential_rent":0.03,"residential_sale":0.045,"villa_sale":0.045}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('SY','Shared Gym','shared_gym','جيم مشترك','leisure','["gym","fitness"]'::jsonb,'{"residential_rent":0.025,"residential_sale":0.02}'::jsonb,'{"retrieval_refinement":false}'::jsonb),
  ('PG','Private Garden','private_garden','حديقة خاصة','outdoor','["garden","private garden"]'::jsonb,'{"villa_sale":0.075,"residential_sale":0.035}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('MR','Maid Room','maids_room','غرفة مربية','layout','["maid room","maids room"]'::jsonb,'{"villa_sale":0.045,"residential_rent":0.02}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('AC','Central AC','central_ac','تكييف مركزي','core','["central ac","air conditioning"]'::jsonb,'{"residential_rent":0.035,"office_rent":0.04}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('FN','Finishing','finishing','تشطيب','fitout','["finishing","super lux"]'::jsonb,'{"residential_sale":0.045,"villa_sale":0.04,"retail_rent":0.035}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('IT','Internet','internet','إنترنت','infrastructure','["internet","fiber","wifi"]'::jsonb,'{"office_rent":0.04,"residential_rent":0.015}'::jsonb,'{"retrieval_refinement":false}'::jsonb),
  ('WF','Waterfront','waterfront','واجهة مائية','view','["waterfront","lagoon front"]'::jsonb,'{"villa_sale":0.055,"residential_sale":0.045,"land_sale":0.04}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('CH','Clubhouse','clubhouse','كلوب هاوس','compound','["clubhouse","club house"]'::jsonb,'{"villa_sale":0.04,"residential_sale":0.03}'::jsonb,'{"retrieval_refinement":false}'::jsonb),
  ('RF','Retail Frontage','retail_frontage','واجهة تجارية','exposure','["retail frontage","storefront"]'::jsonb,'{"retail_rent":0.1,"land_sale":0.05}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('OI','Office Infrastructure','office_infrastructure','بنية مكتبية','infrastructure','["office infrastructure","data cabling","meeting rooms"]'::jsonb,'{"office_rent":0.075,"commercial_rent":0.035}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('FR','Frontage','frontage','واجهة','exposure','["frontage","wide frontage"]'::jsonb,'{"retail_rent":0.09,"land_sale":0.07}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('VI','Visibility','visibility','وضوح الرؤية','exposure','["visibility","high visibility"]'::jsonb,'{"retail_rent":0.085}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('TR','Traffic Exposure','traffic_exposure','تعرض مروري','exposure','["traffic exposure","footfall"]'::jsonb,'{"retail_rent":0.09}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('ZO','Zoning','zoning','تقسيم/ترخيص','land','["zoning","licensed use","building permit"]'::jsonb,'{"land_sale":0.12,"commercial_rent":0.06}'::jsonb,'{"retrieval_refinement":true}'::jsonb),
  ('GE','Land Geometry','land_geometry','هندسة الأرض','land','["geometry","regular shape","corner plot"]'::jsonb,'{"land_sale":0.085,"commercial_rent":0.03}'::jsonb,'{"retrieval_refinement":true}'::jsonb)
ON CONFLICT (symbol) DO UPDATE
SET
  canonical_name = EXCLUDED.canonical_name,
  normalized_name = EXCLUDED.normalized_name,
  arabic_name = EXCLUDED.arabic_name,
  classification = EXCLUDED.classification,
  aliases = EXCLUDED.aliases,
  weight_profile = EXCLUDED.weight_profile,
  retrieval_metadata = EXCLUDED.retrieval_metadata,
  active = TRUE,
  updated_at_utc = NOW();
