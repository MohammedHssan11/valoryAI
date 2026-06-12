import '../models/valuation_request.dart';
import '../models/valuation_response.dart';

abstract interface class ValuationRepository {
  Future<ValuationResponse> analyze(ValuationRequest request);
}
