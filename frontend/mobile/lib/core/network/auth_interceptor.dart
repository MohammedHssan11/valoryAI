import 'package:dio/dio.dart';

import '../../features/auth/presentation/state/auth_session_manager.dart';

class AuthInterceptor extends QueuedInterceptor {
  AuthInterceptor(this._dio);

  final Dio _dio;

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final token = AuthSessionManager.instance.accessToken;
    if (token != null && token.isNotEmpty) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    final statusCode = err.response?.statusCode;
    final alreadyRetried = err.requestOptions.extra['authRetried'] == true;

    if (statusCode == 401 && !alreadyRetried) {
      try {
        final token = await AuthSessionManager.instance.renewSession();
        final options = err.requestOptions;
        options.extra['authRetried'] = true;
        options.headers['Authorization'] = 'Bearer $token';
        handler.resolve(await _dio.fetch<dynamic>(options));
        return;
      } on Exception {
        await AuthSessionManager.instance.expireSession();
        handler.reject(err.copyWith(error: const SessionExpiredException()));
        return;
      }
    }

    if (statusCode == 401) {
      await AuthSessionManager.instance.expireSession();
      handler.reject(err.copyWith(error: const SessionExpiredException()));
      return;
    }

    if (statusCode == 403) {
      handler.reject(err.copyWith(error: const SessionForbiddenException()));
      return;
    }

    handler.next(err);
  }
}

class SessionExpiredException implements Exception {
  const SessionExpiredException();

  @override
  String toString() => 'Your session has expired. Please sign in again.';
}

class SessionForbiddenException implements Exception {
  const SessionForbiddenException();

  @override
  String toString() => 'You do not have permission to perform this action.';
}
