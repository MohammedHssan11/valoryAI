class ValuationResponse {
  const ValuationResponse({
    required this.fairPriceEgp,
    required this.rangeLowEgp,
    required this.rangeHighEgp,
    required this.flag,
    required this.tierUsed,
    required this.confidence,
    required this.comparablesCount,
    required this.engineUsed,
    required this.propertyCategory,
    required this.valuationContract,
    required this.explanation,
    required this.explainability,
    required this.evidence,
    required this.location,
    required this.topComparables,
    required this.drivers,
    required this.marketSignals,
    required this.rawData,
  });

  factory ValuationResponse.fromJson(Map<String, dynamic> json) {
    final confidence = ValuationConfidence.fromJson(_asMap(json['confidence']));
    final explainability = _nullableMap(json['explainability']);
    final evidenceSummary = _asMap(json['evidence_summary']);
    final spatialDiagnostics = _asMap(json['spatial_diagnostics']);
    final resolvedLocation = _asMap(json['resolved_location']);
    final area = _asMap(json['area']);
    final valuationContract = _asMap(json['valuation_contract']);
    final amenityIntelligence = _asMap(json['amenity_intelligence']);

    return ValuationResponse(
      fairPriceEgp: _int(json['fair_price_egp']) ?? 0,
      rangeLowEgp: _int(json['range_low_egp']) ?? 0,
      rangeHighEgp: _int(json['range_high_egp']) ?? 0,
      flag: _string(json['flag']) ?? 'UNKNOWN',
      tierUsed: _int(json['tier_used']) ?? 0,
      confidence: confidence,
      comparablesCount: _int(json['comps_count']) ?? 0,
      engineUsed: _string(json['engine_used']) ?? 'UNKNOWN',
      propertyCategory: _string(json['property_category']),
      valuationContract: valuationContract,
      explanation: _stringList(json['explanation']),
      explainability: explainability == null
          ? null
          : ValuationExplainability.fromJson(explainability),
      evidence: ValuationEvidence.fromJson(
        confidenceLabel: confidence.label,
        tierUsed: _int(json['tier_used']) ?? 0,
        comparablesCount: _int(json['comps_count']) ?? 0,
        area: area,
        resolvedLocation: resolvedLocation,
        evidenceSummary: evidenceSummary,
        spatialDiagnostics: spatialDiagnostics,
      ),
      location: ValuationLocation.fromJson(
        resolvedLocation: resolvedLocation,
        spatialDiagnostics: spatialDiagnostics,
      ),
      topComparables: _mapList(
        json['top_comps'],
      ).map(ValuationComparable.fromJson).toList(),
      drivers: _parseDrivers(
        json: json,
        confidence: confidence,
        amenityIntelligence: amenityIntelligence,
      ),
      marketSignals: _parseMarketSignals(json),
      rawData: json,
    );
  }

  final int fairPriceEgp;
  final int rangeLowEgp;
  final int rangeHighEgp;
  final String flag;
  final int tierUsed;
  final ValuationConfidence confidence;
  final int comparablesCount;
  final String engineUsed;
  final String? propertyCategory;
  final Map<String, dynamic> valuationContract;
  final List<String> explanation;
  final ValuationExplainability? explainability;
  final ValuationEvidence evidence;
  final ValuationLocation? location;
  final List<ValuationComparable> topComparables;
  final List<ValuationDriver> drivers;
  final List<ValuationMarketSignal> marketSignals;
  final Map<String, dynamic> rawData;

  String get confidenceLabel => confidence.label;

  double get confidenceScore => confidence.score;

  bool get hasFairValue => flag != 'INSUFFICIENT_DATA' && fairPriceEgp > 0;

  String get valueBasisLabel {
    final basis = _string(valuationContract['value_basis']);
    return basis == 'monthly_rent'
        ? 'Estimated Monthly Rent'
        : 'Estimated Fair Value';
  }

  String? get aiSummary {
    final narrative = explainability?.narrative;
    if (narrative != null) {
      final parts = [
        narrative.whyThisPrice,
        narrative.strongestFactors,
      ].where((item) => item != null && item.isNotEmpty).toList();
      if (parts.isNotEmpty) {
        return parts.join(' ');
      }
    }
    return explanation.isEmpty ? null : explanation.join(' ');
  }
}

class ValuationConfidence {
  const ValuationConfidence({
    required this.score,
    required this.label,
    required this.factors,
    required this.dimensions,
  });

  factory ValuationConfidence.fromJson(Map<String, dynamic> json) {
    return ValuationConfidence(
      score: _double(json['score']) ?? 0,
      label: _string(json['label']) ?? 'Unknown',
      factors: _numberMap(json['factors']),
      dimensions: _asMap(json['dimensions']),
    );
  }

  final double score;
  final String label;
  final Map<String, double> factors;
  final Map<String, dynamic> dimensions;
}

class ValuationExplainability {
  const ValuationExplainability({
    required this.routerExplanation,
    required this.confidenceReason,
    required this.narrative,
    required this.featureDrivers,
  });

  factory ValuationExplainability.fromJson(Map<String, dynamic> json) {
    final confidence = _asMap(json['confidence_explanation']);
    final narrative = _nullableMap(json['narrative_explanation']);
    return ValuationExplainability(
      routerExplanation: _string(json['router_explanation']),
      confidenceReason: _string(confidence['confidence_reason']),
      narrative: narrative == null
          ? null
          : ValuationNarrative.fromJson(narrative),
      featureDrivers: _mapList(
        json['feature_drivers'],
      ).map(ValuationFeatureDriver.fromJson).toList(),
    );
  }

  final String? routerExplanation;
  final String? confidenceReason;
  final ValuationNarrative? narrative;
  final List<ValuationFeatureDriver> featureDrivers;
}

class ValuationNarrative {
  const ValuationNarrative({
    required this.summary,
    required this.whyThisPrice,
    required this.strongestFactors,
    required this.confidenceReason,
  });

  factory ValuationNarrative.fromJson(Map<String, dynamic> json) {
    return ValuationNarrative(
      summary: _string(json['summary']),
      whyThisPrice: _string(json['why_this_price']),
      strongestFactors: _string(json['strongest_factors']),
      confidenceReason: _string(json['confidence_reason']),
    );
  }

  final String? summary;
  final String? whyThisPrice;
  final String? strongestFactors;
  final String? confidenceReason;
}

class ValuationFeatureDriver {
  const ValuationFeatureDriver({
    required this.name,
    required this.direction,
    required this.strength,
  });

  factory ValuationFeatureDriver.fromJson(Map<String, dynamic> json) {
    return ValuationFeatureDriver(
      name: _string(json['name']) ?? 'Signal',
      direction: _string(json['direction']),
      strength: _string(json['strength']),
    );
  }

  final String name;
  final String? direction;
  final String? strength;
}

class ValuationEvidence {
  const ValuationEvidence({
    required this.comparablesCount,
    required this.resolvedArea,
    required this.district,
    required this.governorate,
    required this.radiusM,
    required this.marketTier,
    required this.confidenceTier,
    required this.resolutionPrecision,
  });

  factory ValuationEvidence.fromJson({
    required String confidenceLabel,
    required int tierUsed,
    required int comparablesCount,
    required Map<String, dynamic> area,
    required Map<String, dynamic> resolvedLocation,
    required Map<String, dynamic> evidenceSummary,
    required Map<String, dynamic> spatialDiagnostics,
  }) {
    final selectedRetrieval = _asMap(
      evidenceSummary['selected_retrieval'] ??
          spatialDiagnostics['selected_retrieval'],
    );
    final hierarchy = _entityHierarchy(resolvedLocation);
    final areaLevel = _int(area['level']);
    final resolvedArea = _string(area['name']);

    return ValuationEvidence(
      comparablesCount: comparablesCount,
      resolvedArea: resolvedArea,
      district:
          _string(area['district']) ??
          hierarchy['district'] ??
          (areaLevel == 3 ? resolvedArea : null),
      governorate: _string(area['governorate']) ?? hierarchy['governorate'],
      radiusM:
          _double(spatialDiagnostics['retrieval_radius_m']) ??
          _double(selectedRetrieval['radius_m']),
      marketTier:
          _string(selectedRetrieval['tier_label']) ??
          (tierUsed > 0 ? 'Tier $tierUsed' : null),
      confidenceTier: confidenceLabel,
      resolutionPrecision: _string(resolvedLocation['precision_level']),
    );
  }

  final int comparablesCount;
  final String? resolvedArea;
  final String? district;
  final String? governorate;
  final double? radiusM;
  final String? marketTier;
  final String confidenceTier;
  final String? resolutionPrecision;
}

class ValuationLocation {
  const ValuationLocation({required this.latitude, required this.longitude});

  factory ValuationLocation.fromJson({
    required Map<String, dynamic> resolvedLocation,
    required Map<String, dynamic> spatialDiagnostics,
  }) {
    final subject = _asMap(spatialDiagnostics['subject']);
    final latitude =
        _double(resolvedLocation['lat']) ?? _double(subject['lat']);
    final longitude =
        _double(resolvedLocation['lng']) ?? _double(subject['lng']);
    if (latitude == null || longitude == null) {
      return const ValuationLocation(latitude: null, longitude: null);
    }
    return ValuationLocation(latitude: latitude, longitude: longitude);
  }

  final double? latitude;
  final double? longitude;

  bool get isAvailable => latitude != null && longitude != null;
}

class ValuationComparable {
  const ValuationComparable({
    required this.listingId,
    required this.priceEgp,
    required this.pricePerSqm,
    required this.distanceM,
    required this.similarityScore,
    required this.sizeSqm,
    required this.propertyType,
    required this.bedrooms,
    required this.bathrooms,
    required this.areaName,
    required this.locationText,
    required this.latitude,
    required this.longitude,
    required this.evidenceRank,
    required this.retrievalTier,
    required this.tierLabel,
    required this.reasonCode,
    required this.radiusM,
    required this.ageDays,
    required this.weightedContribution,
    required this.confidenceContribution,
    required this.geographicSimilarity,
    required this.weightComponents,
    required this.amenities,
    required this.matchedAmenities,
    required this.missingAmenities,
    required this.extraAmenities,
    required this.amenitySimilarity,
    required this.featureSimilarityComponents,
    required this.furnishingStatus,
    required this.floorNumber,
    required this.compoundName,
    required this.viewType,
    required this.buildingQuality,
  });

  factory ValuationComparable.fromJson(Map<String, dynamic> json) {
    final amenityExplanation = _asMap(
      json['amenity_explanation'] ?? json['feature_overlap'],
    );
    return ValuationComparable(
      listingId: _string(json['listing_id']) ?? 'Comparable',
      priceEgp: _int(json['price_egp']) ?? 0,
      pricePerSqm: _double(json['price_per_sqm']),
      distanceM: _double(json['dist_m']),
      similarityScore:
          _double(json['similarity_score']) ??
          _double(json['feature_similarity']),
      sizeSqm: _double(json['size_sqm']),
      propertyType: _string(json['property_type']),
      bedrooms: _int(json['bedrooms']),
      bathrooms: _int(json['bathrooms']),
      areaName: _string(json['area_name']) ?? _string(json['location_text']),
      locationText: _string(json['location_text']),
      latitude: _double(json['lat']),
      longitude: _double(json['lng']),
      evidenceRank: _int(json['evidence_rank']),
      retrievalTier: _int(json['retrieval_tier']),
      tierLabel: _string(json['tier_label']),
      reasonCode: _string(json['reason_code']),
      radiusM: _double(json['radius_m']),
      ageDays: _double(json['age_days']),
      weightedContribution: _double(json['weighted_contribution']),
      confidenceContribution: _double(json['confidence_contribution']),
      geographicSimilarity:
          _double(json['geographic_similarity']) ??
          _double(_asMap(json['weight_components'])['distance']),
      weightComponents: _numberMap(json['weight_components']),
      amenities: _amenityLabels(json),
      matchedAmenities: _stringList(amenityExplanation['matched_amenities']),
      missingAmenities: _stringList(amenityExplanation['missing_amenities']),
      extraAmenities: _stringList(amenityExplanation['extra_amenities']),
      amenitySimilarity:
          _double(json['amenity_similarity']) ??
          _double(_asMap(json['feature_similarity_components'])['amenities']),
      featureSimilarityComponents: _numberMap(
        json['feature_similarity_components'],
      ),
      furnishingStatus: _string(json['furnishing_status']),
      floorNumber: _int(json['floor_number']),
      compoundName: _string(json['compound_name']),
      viewType: _string(json['view_type']),
      buildingQuality: _string(json['building_quality']),
    );
  }

  final String listingId;
  final int priceEgp;
  final double? pricePerSqm;
  final double? distanceM;
  final double? similarityScore;
  final double? sizeSqm;
  final String? propertyType;
  final int? bedrooms;
  final int? bathrooms;
  final String? areaName;
  final String? locationText;
  final double? latitude;
  final double? longitude;
  final int? evidenceRank;
  final int? retrievalTier;
  final String? tierLabel;
  final String? reasonCode;
  final double? radiusM;
  final double? ageDays;
  final double? weightedContribution;
  final double? confidenceContribution;
  final double? geographicSimilarity;
  final Map<String, double> weightComponents;
  final List<String> amenities;
  final List<String> matchedAmenities;
  final List<String> missingAmenities;
  final List<String> extraAmenities;
  final double? amenitySimilarity;
  final Map<String, double> featureSimilarityComponents;
  final String? furnishingStatus;
  final int? floorNumber;
  final String? compoundName;
  final String? viewType;
  final String? buildingQuality;

  bool get hasLocation => latitude != null && longitude != null;

  String get locationLabel => locationText ?? areaName ?? listingId;

  double? get areaSimilarity => weightComponents['same_area'];

  double? get areaSizeSimilarity => weightComponents['size_similarity'];

  double? get propertyTypeSimilarity => weightComponents['property_type'];
}

enum ValuationDriverKind { priceImpact, evidenceScore, qualitative }

class ValuationDriver {
  const ValuationDriver({
    required this.label,
    required this.value,
    required this.kind,
    this.direction,
    this.strength,
  });

  final String label;
  final double? value;
  final ValuationDriverKind kind;
  final String? direction;
  final String? strength;
}

class ValuationMarketSignal {
  const ValuationMarketSignal({required this.label, required this.value});

  final String label;
  final String value;
}

List<ValuationDriver> _parseDrivers({
  required Map<String, dynamic> json,
  required ValuationConfidence confidence,
  required Map<String, dynamic> amenityIntelligence,
}) {
  final debug = _asMap(json['debug']);
  final impactDrivers = [
    ..._impactDrivers(debug['top_positive_features']),
    ..._impactDrivers(debug['top_negative_features']),
  ];
  if (impactDrivers.isNotEmpty) {
    return impactDrivers.take(4).toList();
  }

  const priority = [
    'location_resolution',
    'similarity',
    'distance',
    'tier',
    'count',
    'recency',
    'kept_ratio',
    'dispersion',
    'valuation_evidence',
  ];
  final drivers = <ValuationDriver>[];
  for (final key in priority) {
    final value = confidence.factors[key];
    if (value == null) {
      continue;
    }
    drivers.add(
      ValuationDriver(
        label: _factorLabel(key),
        value: value,
        kind: ValuationDriverKind.evidenceScore,
      ),
    );
    if (drivers.length == 4) {
      return drivers;
    }
  }

  final amenitySimilarity = _double(
    amenityIntelligence['average_amenity_similarity'],
  );
  if (amenitySimilarity != null && drivers.length < 4) {
    drivers.add(
      ValuationDriver(
        label: 'Amenities Match',
        value: amenitySimilarity,
        kind: ValuationDriverKind.evidenceScore,
      ),
    );
  }
  return drivers;
}

List<ValuationDriver> _impactDrivers(dynamic value) {
  return _mapList(value).map((item) {
    return ValuationDriver(
      label: _displayLabel(_string(item['feature_name']) ?? 'Signal'),
      value: _double(item['impact_percentage']),
      kind: ValuationDriverKind.priceImpact,
    );
  }).toList();
}

List<ValuationMarketSignal> _parseMarketSignals(Map<String, dynamic> json) {
  final context = _asMap(json['market_context'] ?? json['market_insights']);
  if (context.isEmpty) {
    return const [];
  }
  const keys = {
    'demand_trend': 'Demand Trend',
    'demand': 'Demand Trend',
    'market_strength': 'Market Strength',
    'strength': 'Market Strength',
    'price_momentum': 'Price Momentum',
    'momentum': 'Price Momentum',
    'local_growth': 'Local Growth',
    'growth': 'Local Growth',
  };
  final signals = <ValuationMarketSignal>[];
  final usedLabels = <String>{};
  for (final entry in keys.entries) {
    final value = context[entry.key];
    if (value == null || usedLabels.contains(entry.value)) {
      continue;
    }
    final text = value is num ? value.toString() : _string(value);
    if (text == null || text.isEmpty) {
      continue;
    }
    signals.add(ValuationMarketSignal(label: entry.value, value: text));
    usedLabels.add(entry.value);
  }
  return signals;
}

Map<String, String> _entityHierarchy(Map<String, dynamic> resolvedLocation) {
  final hierarchy = <String, String>{};
  final matchedEntity = _asMap(resolvedLocation['matched_entity']);
  final entityType = _string(matchedEntity['entity_type'])?.toLowerCase();
  final entityName = _string(matchedEntity['canonical_name']);
  if (entityType != null && entityName != null) {
    hierarchy[entityType] = entityName;
  }

  final sourceMetadata = _asMap(resolvedLocation['source_metadata']);
  for (final entityId in _stringList(sourceMetadata['matched_entities'])) {
    final parts = entityId.split('.');
    if (parts.length < 3) {
      continue;
    }
    final type = parts[1].toLowerCase();
    hierarchy.putIfAbsent(
      type,
      () => _displayLabel(parts.sublist(2).join('_')),
    );
  }
  return hierarchy;
}

String _factorLabel(String value) {
  const labels = {
    'location_resolution': 'Location',
    'similarity': 'Property Match',
    'distance': 'Proximity',
    'tier': 'Market Tier',
    'count': 'Comparable Depth',
    'recency': 'Listing Recency',
    'kept_ratio': 'Evidence Quality',
    'dispersion': 'Price Consistency',
    'valuation_evidence': 'Valuation Evidence',
  };
  return labels[value] ?? _displayLabel(value);
}

String _displayLabel(String value) {
  return value
      .replaceAll('_', ' ')
      .split(' ')
      .where((word) => word.isNotEmpty)
      .map((word) => '${word[0].toUpperCase()}${word.substring(1)}')
      .join(' ');
}

Map<String, dynamic> _asMap(dynamic value) {
  if (value is Map<String, dynamic>) {
    return value;
  }
  if (value is Map) {
    return value.map((key, item) => MapEntry(key.toString(), item));
  }
  return <String, dynamic>{};
}

Map<String, dynamic>? _nullableMap(dynamic value) {
  final map = _asMap(value);
  return map.isEmpty ? null : map;
}

List<Map<String, dynamic>> _mapList(dynamic value) {
  if (value is! List) {
    return const [];
  }
  return value.map(_asMap).where((item) => item.isNotEmpty).toList();
}

Map<String, double> _numberMap(dynamic value) {
  final map = _asMap(value);
  return map.map((key, item) => MapEntry(key, _double(item) ?? 0));
}

List<String> _stringList(dynamic value) {
  if (value is! List) {
    return const [];
  }
  return value
      .where((item) => item != null)
      .map((item) => item.toString())
      .where((item) => item.isNotEmpty)
      .toList();
}

List<String> _amenityLabels(Map<String, dynamic> json) {
  final normalized = _stringList(json['normalized_amenities']);
  if (normalized.isNotEmpty) {
    return normalized;
  }

  final labels = <String>[];
  for (final item in _mapList(json['amenity_metadata'])) {
    final label = _string(item['name']) ?? _string(item['normalized']);
    if (label != null && !labels.contains(label)) {
      labels.add(label);
    }
  }
  if (labels.isNotEmpty) {
    return labels;
  }

  for (final item in _mapList(json['amenities'])) {
    final label =
        _string(item['name']) ??
        _string(item['normalized']) ??
        _string(item['symbol']);
    if (label != null && !labels.contains(label)) {
      labels.add(label);
    }
  }
  return labels;
}

String? _string(dynamic value) {
  if (value is! String) {
    return null;
  }
  final normalized = value.trim();
  return normalized.isEmpty ? null : normalized;
}

int? _int(dynamic value) {
  if (value is num) {
    return value.toInt();
  }
  return int.tryParse(value?.toString() ?? '');
}

double? _double(dynamic value) {
  if (value is num) {
    return value.toDouble();
  }
  return double.tryParse(value?.toString() ?? '');
}
