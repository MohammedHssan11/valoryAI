import '../../domain/models/valuation_request.dart';
import '../../domain/models/valuation_response.dart';
import '../../domain/repositories/valuation_repository.dart';
import '../datasources/valuation_remote_data_source.dart';

class ValuationRepositoryImpl implements ValuationRepository {
  const ValuationRepositoryImpl(this._remoteDataSource);

  final ValuationRemoteDataSource _remoteDataSource;

  @override
  Future<ValuationResponse> analyze(ValuationRequest request) {
    return _remoteDataSource.analyze(request);
  }
}
