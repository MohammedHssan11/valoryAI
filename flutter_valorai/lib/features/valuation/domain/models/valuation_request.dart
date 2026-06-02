enum ValuationCategory {
  residentialBuy('Residential Buy'),
  residentialRent('Residential Rent'),
  commercialBuy('Commercial Buy'),
  commercialRent('Commercial Rent');

  const ValuationCategory(this.label);

  final String label;

  bool get isResidential =>
      this == ValuationCategory.residentialBuy ||
      this == ValuationCategory.residentialRent;
}

enum ValuationLocationMode { hierarchy, gps, map }

class ValuationRequest {
  const ValuationRequest({
    required this.category,
    required this.propertyType,
    required this.locationMode,
    required this.sizeSqm,
    required this.amenities,
    this.address,
    this.governorate,
    this.city,
    this.district,
    this.compound,
    this.latitude,
    this.longitude,
    this.bedrooms,
    this.bathrooms,
  });

  final ValuationCategory category;
  final String propertyType;
  final ValuationLocationMode locationMode;
  final String? address;
  final String? governorate;
  final String? city;
  final String? district;
  final String? compound;
  final double? latitude;
  final double? longitude;
  final double sizeSqm;
  final int? bedrooms;
  final int? bathrooms;
  final List<String> amenities;

  String? get backendPropertyCategory {
    switch (category) {
      case ValuationCategory.residentialRent:
        return _residentialRentTypes.contains(propertyType)
            ? 'residential_rent'
            : null;
      case ValuationCategory.residentialBuy:
        if (_residentialSaleTypes.contains(propertyType)) {
          return 'residential_sale';
        }
        if (_villaSaleTypes.contains(propertyType)) {
          return 'villa_sale';
        }
        if (propertyType == 'Land') {
          return 'land_sale';
        }
        return null;
      case ValuationCategory.commercialBuy:
        return propertyType == 'Land' ? 'land_sale' : null;
      case ValuationCategory.commercialRent:
        if (_officeRentTypes.contains(propertyType)) {
          return 'office_rent';
        }
        if (_retailRentTypes.contains(propertyType)) {
          return 'retail_rent';
        }
        if (_commercialRentTypes.contains(propertyType)) {
          return 'commercial_rent';
        }
        return null;
    }
  }

  bool get isSupportedByBackend => backendPropertyCategory != null;

  Map<String, dynamic> toJson() {
    final propertyCategory = backendPropertyCategory;
    if (propertyCategory == null) {
      throw const ValuationUnsupportedException(
        'This property type is present in the Egypt dataset but is not yet '
        'covered by the backend valuation contracts.',
      );
    }

    final usesCoordinates =
        latitude != null &&
        longitude != null &&
        locationMode != ValuationLocationMode.hierarchy;
    final json = <String, dynamic>{
      'property_type': propertyType,
      'property_category': propertyCategory,
      'size_sqm': sizeSqm,
      'amenities': amenities,
      if (category.isResidential && propertyType != 'Land' && bedrooms != null)
        'bedrooms': bedrooms,
      if (propertyType != 'Land' && bathrooms != null) 'bathrooms': bathrooms,
      if (compound != null && compound!.trim().isNotEmpty)
        'compound_name': compound!.trim(),
    };

    if (usesCoordinates) {
      json.addAll({
        'location_mode': 'manual_coordinates',
        'lat': latitude,
        'lng': longitude,
      });
    } else {
      final resolvedAddress = address?.trim();
      if (resolvedAddress == null || resolvedAddress.isEmpty) {
        throw const ValuationSubmissionException(
          'Choose a complete location before analyzing this property.',
        );
      }
      json.addAll({
        'location_mode': 'address_resolution',
        'address': resolvedAddress,
      });
    }
    return json;
  }
}

class ValuationUnsupportedException implements Exception {
  const ValuationUnsupportedException(this.message);

  final String message;

  @override
  String toString() => message;
}

class ValuationSubmissionException implements Exception {
  const ValuationSubmissionException(this.message);

  final String message;

  @override
  String toString() => message;
}

const _residentialRentTypes = {
  'Apartment',
  'Villa',
  'Townhouse',
  'Twin House',
  'Penthouse',
  'Duplex',
  'Chalet',
  'Cabin',
  'Hotel Apartment',
  'iVilla',
  'Roof',
};

const _residentialSaleTypes = {
  'Apartment',
  'Penthouse',
  'Duplex',
  'Chalet',
  'Hotel Apartment',
  'Roof',
};

const _villaSaleTypes = {
  'Villa',
  'Townhouse',
  'Twin House',
  'iVilla',
  'Palace',
};

const _officeRentTypes = {'Office Space'};

const _retailRentTypes = {
  'Shop',
  'Retail',
  'Show Room',
  'Restaurant',
  'Cafeteria',
};

const _commercialRentTypes = {
  'Clinic',
  'Warehouse',
  'Factory',
  'Medical Facility',
  'Whole Building',
};
