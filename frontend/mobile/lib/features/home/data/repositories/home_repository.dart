import '../../domain/models/home_dashboard.dart';
import '../../../workspace/domain/models/workspace.dart';
import '../datasources/home_remote_data_source.dart';

class HomeRepository {
  const HomeRepository(this._remoteDataSource);

  final HomeRemoteDataSource _remoteDataSource;

  Future<HomeDashboard> loadDashboard({int? activeWorkspaceId}) async {
    final currentUser = await _remoteDataSource.getCurrentUser();
    final rawWorkspaces = await _remoteDataSource.getWorkspaces();
    final workspaces = rawWorkspaces
        .map(
          (item) => Workspace.fromMap({
            ...item,
            'description': '',
            'property_count': 0,
          }),
        )
        .toList();

    Workspace? activeWorkspace;
    if (workspaces.isNotEmpty) {
      activeWorkspace = workspaces.firstWhere(
        (workspace) => workspace.id == activeWorkspaceId,
        orElse: () => workspaces.first,
      );
    }

    if (activeWorkspace == null) {
      return HomeDashboard(
        displayName: currentUser['display_name'] as String? ?? '',
        workspaces: workspaces,
        activeWorkspace: null,
        trackedProperties: 0,
        copilotSessions: 0,
        recentCopilotSessions: const [],
      );
    }

    final properties = await _remoteDataSource.getWorkspaceProperties(
      activeWorkspace.id,
    );
    final chats = await _remoteDataSource.getWorkspaceChats(activeWorkspace.id);
    final activeWorkspaceWithCount = activeWorkspace.copyWith(
      propertyCount: properties.length,
    );
    final resolvedWorkspaces = workspaces
        .map(
          (workspace) => workspace.id == activeWorkspaceWithCount.id
              ? activeWorkspaceWithCount
              : workspace,
        )
        .toList();
    final recentChats =
        chats
            .map(
              (chat) => HomeCopilotSession(
                title: chat['title'] as String,
                updatedAt: DateTime.parse(chat['updated_at'] as String),
              ),
            )
            .toList()
          ..sort((a, b) => b.updatedAt.compareTo(a.updatedAt));

    return HomeDashboard(
      displayName: currentUser['display_name'] as String? ?? '',
      workspaces: resolvedWorkspaces,
      activeWorkspace: activeWorkspaceWithCount,
      trackedProperties: properties.length,
      copilotSessions: chats.length,
      recentCopilotSessions: recentChats.take(3).toList(),
    );
  }
}
