import '../models/location_suggestion.dart';

abstract interface class LocationAutocompleteRepository {
  Future<List<LocationSuggestion>> suggest({
    required String query,
    LocationSuggestionLevel? level,
    String? parentPath,
  });
}
