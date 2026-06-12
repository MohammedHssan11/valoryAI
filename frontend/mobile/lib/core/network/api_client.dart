import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

import 'auth_interceptor.dart';

class ApiClient {
  ApiClient._() {
    authenticatedDio = createDio();
    authenticatedDio.interceptors.add(AuthInterceptor(authenticatedDio));
  }

  static final ApiClient instance = ApiClient._();

  late final Dio authenticatedDio;

  static const _configuredBaseUrl = String.fromEnvironment(
    'VALORAI_API_BASE_URL',
  );

  static String get _baseUrl {
    if (_configuredBaseUrl.isNotEmpty) {
      return _configuredBaseUrl;
    }
    if (!kIsWeb && defaultTargetPlatform == TargetPlatform.android) {
      return 'http://10.0.2.2:8000';
    }
    return 'http://localhost:8000';
  }

  static Dio createDio() {
    return Dio(
      BaseOptions(
        baseUrl: _baseUrl,
        connectTimeout: const Duration(seconds: 12),
        receiveTimeout: const Duration(seconds: 30),
        headers: const {'Content-Type': 'application/json'},
      ),
    );
  }
}
