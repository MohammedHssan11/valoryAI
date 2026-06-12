import 'package:dio/dio.dart';

import '../../../../core/network/api_client.dart';
import '../../domain/models/auth_session.dart';

class AuthRemoteDataSource {
  AuthRemoteDataSource({Dio? dio}) : _dio = dio ?? ApiClient.createDio();

  final Dio _dio;

  Future<TokenExchangeResult> exchangeFirebaseToken(
    String firebaseIdToken,
  ) async {
    try {
      final response = await _dio.post<Map<String, dynamic>>(
        '/v1/auth/token-exchange',
        data: {'firebase_id_token': firebaseIdToken},
      );
      final body = response.data;
      if (body == null) {
        throw const AuthSessionException(
          'The authentication service returned an empty response.',
        );
      }
      return TokenExchangeResult.fromMap(body);
    } on DioException catch (error) {
      throw AuthSessionException(_messageFor(error));
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
    }
    if (error.type == DioExceptionType.connectionError ||
        error.type == DioExceptionType.connectionTimeout) {
      return 'Unable to reach the ValorAI authentication service.';
    }
    return 'ValorAI could not establish an authenticated session.';
  }
}

class AuthSessionException implements Exception {
  const AuthSessionException(this.message);

  final String message;

  @override
  String toString() => message;
}


