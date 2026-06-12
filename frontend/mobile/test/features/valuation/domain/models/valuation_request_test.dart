import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_valorai/features/valuation/domain/models/valuation_request.dart';

void main() {
  group('ValuationRequest', () {
    test('maps villa sale to the governed villa contract', () {
      const request = ValuationRequest(
        category: ValuationCategory.residentialBuy,
        propertyType: 'Villa',
        locationMode: ValuationLocationMode.hierarchy,
        address: 'Mivida, New Cairo City, Cairo',
        sizeSqm: 320,
        bedrooms: 4,
        bathrooms: 3,
        amenities: ['SE', 'PG'],
      );

      expect(request.toJson(), {
        'property_type': 'Villa',
        'property_category': 'villa_sale',
        'size_sqm': 320.0,
        'amenities': ['SE', 'PG'],
        'bedrooms': 4,
        'bathrooms': 3,
        'location_mode': 'address_resolution',
        'address': 'Mivida, New Cairo City, Cairo',
      });
    });

    test('uses coordinates and removes bedrooms for commercial rent', () {
      const request = ValuationRequest(
        category: ValuationCategory.commercialRent,
        propertyType: 'Office Space',
        locationMode: ValuationLocationMode.map,
        latitude: 30.0444,
        longitude: 31.2357,
        sizeSqm: 180,
        bedrooms: 2,
        bathrooms: 1,
        amenities: ['CP', 'OI'],
      );

      expect(request.toJson(), {
        'property_type': 'Office Space',
        'property_category': 'office_rent',
        'size_sqm': 180.0,
        'amenities': ['CP', 'OI'],
        'bathrooms': 1,
        'location_mode': 'manual_coordinates',
        'lat': 30.0444,
        'lng': 31.2357,
      });
    });

    test('rejects combinations that exist only in the dataset taxonomy', () {
      const request = ValuationRequest(
        category: ValuationCategory.commercialBuy,
        propertyType: 'Shop',
        locationMode: ValuationLocationMode.hierarchy,
        address: 'New Cairo City, Cairo',
        sizeSqm: 90,
        amenities: [],
      );

      expect(request.isSupportedByBackend, isFalse);
      expect(request.toJson, throwsA(isA<ValuationUnsupportedException>()));
    });
  });
}
