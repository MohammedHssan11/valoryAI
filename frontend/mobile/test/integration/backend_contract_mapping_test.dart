import 'dart:convert';
import 'dart:typed_data';

import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_valorai/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:flutter_valorai/features/copilot/data/datasources/copilot_remote_data_source.dart';
import 'package:flutter_valorai/features/copilot/data/repositories/copilot_repository_impl.dart';
import 'package:flutter_valorai/features/home/data/datasources/home_remote_data_source.dart';
import 'package:flutter_valorai/features/home/data/repositories/home_repository.dart';
import 'package:flutter_valorai/features/workspace/data/datasources/workspace_remote_data_source.dart';
import 'package:flutter_valorai/features/workspace/data/repositories/workspace_repository_impl.dart';

void main() {
  test(
    'exchanges Firebase ID token for ValorAI JWT and user metadata',
    () async {
      final adapter = _StubAdapter((options) {
        expect(options.path, '/v1/auth/token-exchange');
        expect(options.data, {'firebase_id_token': 'firebase-token'});
        return {
          'access_token': 'valorai-jwt',
          'token_type': 'bearer',
          'expires_in': 3600,
          'user': {
            'id': 7,
            'external_subject': 'firebase-user',
            'display_name': 'Firebase User',
          },
        };
      });

      final result = await AuthRemoteDataSource(
        dio: _dioWith(adapter),
      ).exchangeFirebaseToken('firebase-token');

      expect(result.accessToken, 'valorai-jwt');
      expect(result.expiresIn, 3600);
      expect(result.user.id, 7);
      expect(result.user.displayName, 'Firebase User');
    },
  );

  test(
    'workspace repository returns backend workspaces without mock fallback',
    () async {
      final adapter = _StubAdapter((options) {
        if (options.path == '/v1/copilot/workspaces') {
          return [
            {
              'id': 11,
              'user_id': 7,
              'name': 'Live Workspace',
              'created_at': '2026-06-02T10:00:00Z',
              'updated_at': '2026-06-02T11:00:00Z',
              'version': 1,
              'is_deleted': false,
            },
          ];
        }
        if (options.path == '/v1/copilot/workspaces/11/properties') {
          return [
            {'id': 1},
            {'id': 2},
          ];
        }
        throw StateError('Unexpected request: ${options.path}');
      });

      final repository = WorkspaceRepositoryImpl(
        WorkspaceRemoteDataSource(dio: _dioWith(adapter)),
      );
      final workspaces = await repository.getWorkspaces();

      expect(workspaces, hasLength(1));
      expect(workspaces.single.name, 'Live Workspace');
      expect(workspaces.single.propertyCount, 2);
      expect(workspaces.single.description, isEmpty);
    },
  );

  test('home repository renders only backend-owned dashboard data', () async {
    final adapter = _StubAdapter((options) {
      switch (options.path) {
        case '/v1/copilot/users/me':
          return {'display_name': 'Live User'};
        case '/v1/copilot/workspaces':
          return [
            {
              'id': 11,
              'user_id': 7,
              'name': 'Live Workspace',
              'created_at': '2026-06-02T10:00:00Z',
              'updated_at': '2026-06-02T11:00:00Z',
              'version': 1,
              'is_deleted': false,
            },
          ];
        case '/v1/copilot/workspaces/11/properties':
          return [
            {'id': 1},
          ];
        case '/v1/copilot/workspaces/11/chats':
          return [
            {
              'title': 'Live Copilot Session',
              'updated_at': '2026-06-02T12:00:00Z',
            },
          ];
      }
      throw StateError('Unexpected request: ${options.path}');
    });

    final dashboard = await HomeRepository(
      HomeRemoteDataSource(dio: _dioWith(adapter)),
    ).loadDashboard();

    expect(dashboard.displayName, 'Live User');
    expect(dashboard.activeWorkspace?.name, 'Live Workspace');
    expect(dashboard.trackedProperties, 1);
    expect(dashboard.copilotSessions, 1);
    expect(
      dashboard.recentCopilotSessions.single.title,
      'Live Copilot Session',
    );
  });

  test(
    'copilot sends workspace context and maps live response without fallback',
    () async {
      final adapter = _StubAdapter((options) {
        expect(options.path, '/v1/copilot/orchestrator/respond');
        expect(options.data, {
          'workspace_id': 11,
          'message': 'Explain the value',
          'tool_inputs': {
            'valuation': {'valuation_id': 'valuation-live'},
          },
        });
        return {
          'response_id': 'response-live',
          'delivery_mode': 'DETERMINISTIC_FALLBACK',
          'response': {
            'composition_status': 'SUCCESS',
            'tool_outputs': [
              {
                'tool_name': 'valuation',
                'payload': {
                  'valuation_id': 'valuation-live',
                  'fair_price': 4200000,
                  'confidence_level': 'High',
                },
              },
            ],
            'full_evidence': {
              'comparables': [],
              'feature_drivers': [],
              'market_insights': [],
            },
          },
        };
      });
      final repository = CopilotRepositoryImpl(
        CopilotRemoteDataSource(dio: _dioWith(adapter)),
      );

      final response = await repository.respond(
        message: 'Explain the value',
        workspaceId: 11,
        toolInputs: {
          'valuation': {'valuation_id': 'valuation-live'},
        },
      );

      expect(response.id, 'response-live');
      expect(response.content, 'SUCCESS');
      expect(response.propertySummary?.fairPrice, 4200000);
      expect(response.confidence, isNull);
    },
  );
}

Dio _dioWith(HttpClientAdapter adapter) {
  final dio = Dio();
  dio.httpClientAdapter = adapter;
  return dio;
}

class _StubAdapter implements HttpClientAdapter {
  _StubAdapter(this._handler);

  final dynamic Function(RequestOptions options) _handler;

  @override
  Future<ResponseBody> fetch(
    RequestOptions options,
    Stream<Uint8List>? requestStream,
    Future<void>? cancelFuture,
  ) async {
    return ResponseBody.fromString(
      json.encode(_handler(options)),
      200,
      headers: {
        Headers.contentTypeHeader: [Headers.jsonContentType],
      },
    );
  }

  @override
  void close({bool force = false}) {}
}
