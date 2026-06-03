import 'package:dio/dio.dart';

import '../../../../core/network/api_client.dart';
import '../../domain/models/valuation_request.dart';
import '../../domain/models/valuation_response.dart';

class ValuationRemoteDataSource {
  ValuationRemoteDataSource({Dio? dio})
    : _dio = dio ?? ApiClient.instance.authenticatedDio;

  final Dio _dio;

  Future<ValuationResponse> analyze(ValuationRequest request) async {
    try {
      final response = await _dio.post<Map<String, dynamic>>(
        '/v1/valuation/fair-price',
        data: request.toJson(),
      );
      final envelope = response.data;
      final data = envelope?['data'];
      if (data is! Map<String, dynamic>) {
        throw const ValuationSubmissionException(
          'The valuation service returned an unexpected response.',
        );
      }
      return ValuationResponse.fromJson(data);
    } on DioException catch (error) {
      throw ValuationSubmissionException(_messageFor(error));
    }
  }

  String _messageFor(DioException error) {
    final body = error.response?.data;
    if (body is Map<String, dynamic>) {
      final apiError = body['error'];
      if (apiError is Map<String, dynamic>) {
        final message = apiError['message'];
        if (message is String && message.isNotEmpty) {
          return message;
        }
      }
      final detail = body['detail'];
      if (detail is String && detail.isNotEmpty) {
        return detail;
      }
    }
    if (error.type == DioExceptionType.connectionError ||
        error.type == DioExceptionType.connectionTimeout) {
      return 'Unable to reach the ValorAI valuation service.';
    }
    return 'The valuation service could not analyze this property.';
  }
}
