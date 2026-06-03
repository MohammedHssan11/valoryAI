import 'package:dio/dio.dart';

import '../../../../core/network/api_client.dart';

class WorkspaceRemoteDataSource {
  WorkspaceRemoteDataSource({Dio? dio})
    : _dio = dio ?? ApiClient.instance.authenticatedDio;

  final Dio _dio;

  Future<List<Map<String, dynamic>>> getWorkspaces() async {
    try {
      final response = await _dio.get<List<dynamic>>('/v1/copilot/workspaces');

      final data = response.data;
      if (data == null) return [];
      return data
          .map((item) => Map<String, dynamic>.from(item as Map))
          .toList();
    } on DioException catch (error) {
      throw WorkspaceException(_messageFor(error));
    }
  }

  Future<Map<String, dynamic>> createWorkspace(String name) async {
    try {
      final response = await _dio.post<Map<String, dynamic>>(
        '/v1/copilot/workspaces',
        data: {'name': name},
      );

      final data = response.data;
      if (data == null) {
        throw const WorkspaceException(
          'No data returned from workspace creation.',
        );
      }
      return data;
    } on DioException catch (error) {
      throw WorkspaceException(_messageFor(error));
    }
  }

  Future<Map<String, dynamic>> updateWorkspace(int id, String name) async {
    try {
      final response = await _dio.put<Map<String, dynamic>>(
        '/v1/copilot/workspaces/$id',
        data: {'name': name},
      );

      final data = response.data;
      if (data == null) {
        throw const WorkspaceException(
          'No data returned from workspace update.',
        );
      }
      return data;
    } on DioException catch (error) {
      throw WorkspaceException(_messageFor(error));
    }
  }

  Future<bool> deleteWorkspace(int id) async {
    try {
      final response = await _dio.delete<Map<String, dynamic>>(
        '/v1/copilot/workspaces/$id',
      );

      return response.statusCode == 200 ||
          response.data?['status'] == 'deleted';
    } on DioException catch (error) {
      throw WorkspaceException(_messageFor(error));
    }
  }

  Future<List<Map<String, dynamic>>> getWorkspaceProperties(int id) async {
    try {
      final response = await _dio.get<List<dynamic>>(
        '/v1/copilot/workspaces/$id/properties',
      );

      final data = response.data;
      if (data == null) return [];
      return data
          .map((item) => Map<String, dynamic>.from(item as Map))
          .toList();
    } on DioException catch (error) {
      throw WorkspaceException(_messageFor(error));
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
      return 'Unable to reach the ValorAI workspace service.';
    }
    if (error.response?.statusCode == 401) {
      return 'Unauthorized access. Please check your credentials.';
    }
    return 'An error occurred while managing workspaces.';
  }
}

class WorkspaceException implements Exception {
  final String message;
  const WorkspaceException(this.message);

  @override
  String toString() => message;
}
