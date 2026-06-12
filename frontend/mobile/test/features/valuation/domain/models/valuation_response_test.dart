import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_valorai/features/valuation/domain/models/valuation_response.dart';

void main() {
  group('ValuationResponse', () {
    test(
      'maps CMT explainability, evidence, comparables, and market context',
      () {
        final response = ValuationResponse.fromJson({
          'fair_price_egp': 4250000,
          'range_low_egp': 3950000,
          'range_high_egp': 4550000,
          'flag': 'NO_TARGET',
          'tier_used': 2,
          'comps_count': 18,
          'confidence': {
            'score': 0.94,
            'label': 'High',
            'factors': {
              'location_resolution': 0.95,
              'similarity': 0.82,
              'distance': 0.91,
              'tier': 0.78,
            },
            'dimensions': {},
          },
          'engine_used': 'CMT',
          'property_category': 'residential_sale',
          'valuation_contract': {'value_basis': 'sale_price'},
          'explanation': ['Fallback truth-layer explanation.'],
          'explainability': {
            'router_explanation': 'CMT selected.',
            'confidence_explanation': {
              'confidence_reason': 'High confidence from nearby evidence.',
            },
            'narrative_explanation': {
              'why_this_price': 'Nearby evidence anchors this valuation.',
              'strongest_factors': 'Location is the strongest factor.',
            },
            'feature_drivers': [],
          },
          'area': {'name': 'Fifth Settlement', 'level': 3},
          'resolved_location': {
            'lat': 30.01,
            'lng': 31.45,
            'precision_level': 'DISTRICT',
            'source_metadata': {
              'matched_entities': [
                'eg.district.fifth_settlement',
                'eg.governorate.cairo',
              ],
            },
          },
          'spatial_diagnostics': {'retrieval_radius_m': 2000},
          'evidence_summary': {
            'selected_retrieval': {'tier_label': 'same district'},
          },
          'top_comps': [
            {
              'listing_id': 'comp-1',
              'price_egp': 4200000,
              'dist_m': 450,
              'similarity_score': 0.91,
              'size_sqm': 180,
              'property_type': 'Apartment',
              'bedrooms': 3,
              'bathrooms': 2,
              'area_name': 'Fifth Settlement',
              'lat': 30.012,
              'lng': 31.452,
              'evidence_rank': 1,
              'reason_code': 'SAME_DISTRICT_MATCH',
              'weighted_contribution': 0.18,
              'confidence_contribution': 0.14,
              'weight_components': {
                'distance': 0.88,
                'same_area': 1.0,
                'size_similarity': 0.93,
                'property_type': 1.0,
              },
              'normalized_amenities': ['balcony', 'security'],
              'amenity_similarity': 0.75,
              'amenity_explanation': {
                'matched_amenities': ['security'],
                'missing_amenities': ['pool'],
              },
            },
          ],
          'market_context': {
            'demand_trend': 'Rising',
            'market_strength': 'Strong',
            'price_momentum': 'Positive',
            'local_growth': '3.4%',
          },
        });

        expect(response.hasFairValue, isTrue);
        expect(response.valueBasisLabel, 'Estimated Fair Value');
        expect(response.aiSummary, contains('Nearby evidence'));
        expect(response.evidence.district, 'Fifth Settlement');
        expect(response.evidence.governorate, 'Cairo');
        expect(response.evidence.radiusM, 2000);
        expect(response.evidence.marketTier, 'same district');
        expect(response.drivers.first.label, 'Location');
        expect(response.drivers.first.kind, ValuationDriverKind.evidenceScore);
        expect(response.topComparables.single.listingId, 'comp-1');
        expect(response.topComparables.single.bedrooms, 3);
        expect(response.topComparables.single.weightedContribution, 0.18);
        expect(response.topComparables.single.geographicSimilarity, 0.88);
        expect(response.topComparables.single.amenities, [
          'balcony',
          'security',
        ]);
        expect(response.topComparables.single.matchedAmenities, ['security']);
        expect(response.marketSignals, hasLength(4));
      },
    );

    test('uses returned ML feature percentages without inventing impacts', () {
      final response = ValuationResponse.fromJson({
        'fair_price_egp': 6000000,
        'range_low_egp': 5100000,
        'range_high_egp': 6900000,
        'flag': 'NO_TARGET',
        'tier_used': 0,
        'comps_count': 0,
        'confidence': {'score': 0.85, 'label': 'High', 'factors': {}},
        'debug': {
          'top_positive_features': [
            {'feature_name': 'area_size', 'impact_percentage': 14.5},
          ],
          'top_negative_features': [
            {'feature_name': 'listing_age', 'impact_percentage': -3.2},
          ],
        },
      });

      expect(response.drivers, hasLength(2));
      expect(response.drivers.first.label, 'Area Size');
      expect(response.drivers.first.value, 14.5);
      expect(response.drivers.first.kind, ValuationDriverKind.priceImpact);
      expect(response.drivers.last.value, -3.2);
    });
  });
}
