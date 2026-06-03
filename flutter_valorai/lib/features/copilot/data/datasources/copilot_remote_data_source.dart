import 'dart:async';

import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

import '../../../../core/network/api_client.dart';

class CopilotRemoteDataSource {
  CopilotRemoteDataSource({Dio? dio})
    : _dio = dio ?? ApiClient.instance.authenticatedDio;

  static const _endpoint = '/v1/copilot/orchestrator/respond';
  static const _maxAttempts = 2;

  final Dio _dio;

  Future<Map<String, dynamic>> respond({
    required String message,
    required int workspaceId,
    int? scenarioId,
    String? brokerSessionId,
    Map<String, dynamic>? toolInputs,
  }) async {
    final requestId = 'copilot_${DateTime.now().microsecondsSinceEpoch}';
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

    for (var attempt = 1; attempt <= _maxAttempts; attempt += 1) {
      try {
        debugPrint(
          '[CopilotRemoteDataSource] request id=$requestId '
          'attempt=$attempt endpoint=$_endpoint workspace=$workspaceId '
          'toolKeys=${(toolInputs ?? {}).keys.toList()}',
        );
        final response = await _dio
            .post<Map<String, dynamic>>(
              _endpoint,
              data: data,
              options: Options(
                headers: {'X-Request-ID': requestId},
                sendTimeout: const Duration(seconds: 12),
                receiveTimeout: const Duration(seconds: 45),
                extra: {'requestId': requestId, 'feature': 'copilot'},
              ),
            )
            .timeout(
              const Duration(seconds: 50),
              onTimeout: () => throw TimeoutException(
                'Copilot response timed out.',
                const Duration(seconds: 50),
              ),
            );

        final body = response.data;
        if (body == null) {
          throw CopilotException(
            'Empty response received from Copilot service.',
            requestId: requestId,
          );
        }
        debugPrint(
          '[CopilotRemoteDataSource] response id=$requestId '
          'status=${response.statusCode} delivery=${body['delivery_mode']}',
        );
        return body;
      } on TimeoutException {
        debugPrint(
          '[CopilotRemoteDataSource] timeout id=$requestId attempt=$attempt',
        );
        if (attempt < _maxAttempts) {
          continue;
        }
        throw CopilotException(
          'The Copilot service is taking too long to respond. Please retry.',
          requestId: requestId,
          canRetry: true,
        );
      } on DioException catch (error) {
        debugPrint(
          '[CopilotRemoteDataSource] dio_error id=$requestId '
          'attempt=$attempt type=${error.type} status=${error.response?.statusCode}',
        );
        if (attempt < _maxAttempts && _shouldRetry(error)) {
          continue;
        }
        throw CopilotException(
          _messageFor(error),
          requestId: requestId,
          statusCode: error.response?.statusCode,
          canRetry: _shouldRetry(error),
        );
      }
    }
    throw CopilotException(
      'The Copilot service could not process your request.',
      requestId: requestId,
      canRetry: true,
    );
  }

  String _messageFor(DioException error) {
    final cause = error.error;
    if (cause != null) {
      final message = cause.toString();
      if (message.isNotEmpty &&
          !message.startsWith('DioException') &&
          !message.startsWith('Instance of')) {
        return message;
      }
    }
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
      if (detail is List && detail.isNotEmpty) {
        return 'The Copilot request was rejected by the API contract.';
      }
    }
    if (error.type == DioExceptionType.connectionError ||
        error.type == DioExceptionType.connectionTimeout ||
        error.type == DioExceptionType.receiveTimeout ||
        error.type == DioExceptionType.sendTimeout) {
      return 'Unable to reach the ValorAI Copilot service.';
    }
    if (error.response?.statusCode == 401) {
      return 'Unauthorized access. Please ensure your session is active.';
    }
    return 'The Copilot service could not process your request.';
  }

  bool _shouldRetry(DioException error) {
    if (error.type == DioExceptionType.connectionError ||
        error.type == DioExceptionType.connectionTimeout ||
        error.type == DioExceptionType.receiveTimeout ||
        error.type == DioExceptionType.sendTimeout) {
      return true;
    }
    final statusCode = error.response?.statusCode;
    return statusCode != null && statusCode >= 500;
  }
}

class CopilotException implements Exception {
  final String message;
  final String? requestId;
  final int? statusCode;
  final bool canRetry;

  const CopilotException(
    this.message, {
    this.requestId,
    this.statusCode,
    this.canRetry = false,
  });

  @override
  String toString() => message;
}
