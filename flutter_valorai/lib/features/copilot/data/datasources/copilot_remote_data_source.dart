import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart';

class CopilotRemoteDataSource {
  CopilotRemoteDataSource({Dio? dio})
      : _dio = dio ??
            Dio(
              BaseOptions(
                baseUrl: const String.fromEnvironment(
                  'VALORAI_API_BASE_URL',
                  defaultValue: 'http://localhost:8000',
                ),
                connectTimeout: const Duration(seconds: 12),
                receiveTimeout: const Duration(seconds: 30),
                headers: const {'Content-Type': 'application/json'},
              ),
            );

  final Dio _dio;

  Future<Map<String, dynamic>> respond({
    required String message,
    required int workspaceId,
    int? scenarioId,
    String? brokerSessionId,
    Map<String, dynamic>? toolInputs,
  }) async {
    try {
      // Retrieve Firebase Token if signed in
      String? token;
      final currentUser = FirebaseAuth.instance.currentUser;
      if (currentUser != null) {
        token = await currentUser.getIdToken();
      }

      final headers = <String, dynamic>{};
      if (token != null) {
        headers['Authorization'] = 'Bearer $token';
      }

      final data = <String, dynamic>{
        'workspace_id': workspaceId,
        'message': message,
        'tool_inputs': toolInputs ?? {},
      };
      if (scenarioId != null) {
        data['scenario_id'] = scenarioId;
      }
      if (brokerSessionId != null) {
        data['broker_session_id'] = brokerSessionId;
      }

      final response = await _dio.post<Map<String, dynamic>>(
        '/v1/copilot/orchestrator/respond',
        data: data,
        options: Options(headers: headers),
      );

      final body = response.data;
      if (body == null) {
        throw const CopilotException('Empty response received from Copilot service.');
      }
      return body;
    } on DioException catch (error) {
      throw CopilotException(_messageFor(error));
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
      return 'Unable to reach the ValorAI Copilot service.';
    }
    if (error.response?.statusCode == 401) {
      return 'Unauthorized access. Please ensure your session is active.';
    }
    return 'The Copilot service could not process your request.';
  }
}

class CopilotException implements Exception {
  final String message;
  const CopilotException(this.message);

  @override
  String toString() => message;
}
