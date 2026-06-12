-- Tier 2: expand radius, size ±20%, last 180 days

SELECT
    l.listing_id,
    l.price_egp,
    l.size_sqm,
    l.bedrooms,
    l.bathrooms,
    ST_Distance(
        l.geom::geography,
        ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography
    ) AS dist_m,
    EXTRACT(EPOCH FROM (:as_of_utc - l.scraped_at_utc)) / 86400.0 AS age_days
FROM listings l
WHERE
    l.category = 'rent'
    AND l.period = 'monthly'
    AND l.property_type = :property_type
    AND l.bedrooms IS NOT DISTINCT FROM CAST(:bedrooms AS INTEGER)
    AND l.size_sqm BETWEEN (:size_sqm * :size_low) AND (:size_sqm * :size_high)
    AND l.scraped_at_utc >= (:as_of_utc - (:stale_days * INTERVAL '1 day'))
    AND ST_DWithin(
        l.geom::geography,
        ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography,
        :radius_m
    )
    AND l.price_egp BETWEEN :min_price_egp AND :max_price_egp
    AND l.size_sqm > 0
    AND l.size_sqm <= :max_size_sqm
    AND (l.price_egp / NULLIF(l.size_sqm,0)) BETWEEN :min_price_per_sqm AND :max_price_per_sqm
ORDER BY dist_m ASC, l.scraped_at_utc DESC, l.price_egp ASC, l.listing_id ASC
LIMIT :limit;
