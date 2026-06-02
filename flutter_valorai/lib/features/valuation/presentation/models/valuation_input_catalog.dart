import 'package:flutter/material.dart';

import '../../domain/models/valuation_request.dart';

class PropertyTypeChoice {
  const PropertyTypeChoice(this.label, this.icon);

  final String label;
  final IconData icon;
}

class AmenityChoice {
  const AmenityChoice(this.code, this.label);

  final String code;
  final String label;
}

class AmenityGroup {
  const AmenityGroup(this.label, this.amenities);

  final String label;
  final List<AmenityChoice> amenities;
}

const residentialPropertyTypes = [
  PropertyTypeChoice('Apartment', Icons.apartment_rounded),
  PropertyTypeChoice('Villa', Icons.villa_outlined),
  PropertyTypeChoice('Townhouse', Icons.holiday_village_outlined),
  PropertyTypeChoice('Twin House', Icons.other_houses_outlined),
  PropertyTypeChoice('Penthouse', Icons.domain_rounded),
  PropertyTypeChoice('Duplex', Icons.stairs_outlined),
  PropertyTypeChoice('Chalet', Icons.cottage_outlined),
  PropertyTypeChoice('Cabin', Icons.cabin_outlined),
  PropertyTypeChoice('Hotel Apartment', Icons.hotel_outlined),
  PropertyTypeChoice('iVilla', Icons.home_work_outlined),
  PropertyTypeChoice('Palace', Icons.account_balance_outlined),
  PropertyTypeChoice('Roof', Icons.roofing_outlined),
  PropertyTypeChoice('Whole Building', Icons.business_outlined),
  PropertyTypeChoice('Land', Icons.landscape_outlined),
];

const commercialPropertyTypes = [
  PropertyTypeChoice('Office Space', Icons.corporate_fare_outlined),
  PropertyTypeChoice('Clinic', Icons.medical_services_outlined),
  PropertyTypeChoice('Shop', Icons.storefront_outlined),
  PropertyTypeChoice('Retail', Icons.shopping_bag_outlined),
  PropertyTypeChoice('Show Room', Icons.window_outlined),
  PropertyTypeChoice('Restaurant', Icons.restaurant_outlined),
  PropertyTypeChoice('Cafeteria', Icons.local_cafe_outlined),
  PropertyTypeChoice('Warehouse', Icons.warehouse_outlined),
  PropertyTypeChoice('Factory', Icons.factory_outlined),
  PropertyTypeChoice('Medical Facility', Icons.local_hospital_outlined),
  PropertyTypeChoice('Whole Building', Icons.business_outlined),
  PropertyTypeChoice('Land', Icons.landscape_outlined),
];

const residentialAmenityGroups = [
  AmenityGroup('Essentials', [
    AmenityChoice('SE', 'Security'),
    AmenityChoice('BA', 'Balcony'),
    AmenityChoice('CP', 'Covered Parking'),
    AmenityChoice('EL', 'Elevator'),
    AmenityChoice('LB', 'Lobby'),
    AmenityChoice('AC', 'Central AC'),
  ]),
  AmenityGroup('Lifestyle', [
    AmenityChoice('SY', 'Shared Gym'),
    AmenityChoice('SP', 'Shared Pool'),
    AmenityChoice('SS', 'Shared Spa'),
    AmenityChoice('PP', 'Private Pool'),
    AmenityChoice('PG', 'Private Garden'),
    AmenityChoice('CH', 'Clubhouse'),
  ]),
  AmenityGroup('Interior', [
    AmenityChoice('SH', 'Smart Home'),
    AmenityChoice('BK', 'Kitchen Appliances'),
    AmenityChoice('BW', 'Built-in Wardrobes'),
    AmenityChoice('MR', 'Maid Room'),
    AmenityChoice('ST', 'Study'),
    AmenityChoice('WC', 'Walk-in Closet'),
  ]),
  AmenityGroup('Views', [
    AmenityChoice('BL', 'Landmark View'),
    AmenityChoice('VW', 'Water View'),
    AmenityChoice('WF', 'Waterfront'),
  ]),
];

const commercialAmenityGroups = [
  AmenityGroup('Access & Building', [
    AmenityChoice('CP', 'Covered Parking'),
    AmenityChoice('LB', 'Lobby'),
    AmenityChoice('EL', 'Elevator'),
    AmenityChoice('SE', 'Security'),
    AmenityChoice('AC', 'Central AC'),
    AmenityChoice('IT', 'Internet'),
  ]),
  AmenityGroup('Commercial Signals', [
    AmenityChoice('BD', 'Business District'),
    AmenityChoice('OI', 'Office Infrastructure'),
    AmenityChoice('FR', 'Frontage'),
    AmenityChoice('RF', 'Retail Frontage'),
    AmenityChoice('TR', 'Traffic Exposure'),
    AmenityChoice('VI', 'Visibility'),
  ]),
  AmenityGroup('Site & Fitout', [
    AmenityChoice('FN', 'Finishing'),
    AmenityChoice('ZO', 'Zoning'),
    AmenityChoice('GE', 'Land Geometry'),
    AmenityChoice('PG', 'Private Garden'),
    AmenityChoice('SY', 'Shared Gym'),
    AmenityChoice('SH', 'Smart Home'),
  ]),
];

const egyptDatasetGovernorates = [
  'Cairo',
  'Giza',
  'Red Sea',
  'North Coast',
  'Alexandria',
  'Suez',
  'Qalyubia',
  'Sharqia',
  'Al Daqahlya',
  'South Sainai',
  'Demyat',
  'Al Menofeya',
  'Asyut',
  'Al Fayum',
  'Matrouh',
  'Al Behera',
  'El Esmailia',
  'Kafr El Sheikh',
  'Al Gharbeya',
  'Al Menya',
];

List<PropertyTypeChoice> propertyTypesFor(ValuationCategory category) {
  return category.isResidential
      ? residentialPropertyTypes
      : commercialPropertyTypes;
}

List<AmenityGroup> amenityGroupsFor(ValuationCategory category) {
  return category.isResidential
      ? residentialAmenityGroups
      : commercialAmenityGroups;
}
