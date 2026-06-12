class LocationSuggestion {
  const LocationSuggestion({
    required this.label,
    required this.fullPath,
    required this.level,
    this.canonicalEntityId,
  });

  final String label;
  final String fullPath;
  final LocationSuggestionLevel level;
  final String? canonicalEntityId;
}

enum LocationSuggestionLevel { governorate, city, district, compound }
