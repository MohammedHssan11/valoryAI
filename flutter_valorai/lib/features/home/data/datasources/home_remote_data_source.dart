import 'package:dio/dio.dart';

import '../../../../core/network/api_client.dart';

class HomeRemoteDataSource {
  HomeRemoteDataSource({Dio? dio})
    : _dio = dio ?? ApiClient.instance.authenticatedDio;

  final Dio _dio;

  Future<Map<String, dynamic>> getCurrentUser() async {
    return _getMap('/v1/copilot/users/me');
  }

  Future<List<Map<String, dynamic>>> getWorkspaces() async {
    return _getList('/v1/copilot/workspaces');
  }

  Future<List<Map<String, dynamic>>> getWorkspaceProperties(
    int workspaceId,
  ) async {
    return _getList('/v1/copilot/workspaces/$workspaceId/properties');
  }

  Future<List<Map<String, dynamic>>> getWorkspaceChats(int workspaceId) async {
    return _getList('/v1/copilot/workspaces/$workspaceId/chats');
  }

  Future<Map<String, dynamic>> _getMap(String path) async {
    try {
      final response = await _dio.get<Map<String, dynamic>>(path);
      final data = response.data;
      if (data == null) {
        throw const HomeDashboardException(
          'The dashboard service returned an empty response.',
        );
      }
      return data;
    } on DioException catch (error) {
      throw HomeDashboardException(_messageFor(error));
    }
  }

  Future<List<Map<String, dynamic>>> _getList(String path) async {
    try {
      final response = await _dio.get<List<dynamic>>(path);
      final data = response.data ?? [];
      return data
          .map((item) => Map<String, dynamic>.from(item as Map))
          .toList();
    } on DioException catch (error) {
      throw HomeDashboardException(_messageFor(error));
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
      return 'Unable to reach the ValorAI dashboard service.';
    }
    return 'The dashboard data could not be loaded.';
  }
}

class HomeDashboardException implements Exception {
  const HomeDashboardException(this.message);

  final String message;

  @override
  String toString() => message;
}
