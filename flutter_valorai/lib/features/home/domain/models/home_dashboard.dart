import '../../../workspace/domain/models/workspace.dart';

class HomeDashboard {
  const HomeDashboard({
    required this.displayName,
    required this.workspaces,
    required this.activeWorkspace,
    required this.trackedProperties,
    required this.copilotSessions,
    required this.recentCopilotSessions,
  });

  final String displayName;
  final List<Workspace> workspaces;
  final Workspace? activeWorkspace;
  final int trackedProperties;
  final int copilotSessions;
  final List<HomeCopilotSession> recentCopilotSessions;
}

class HomeCopilotSession {
  const HomeCopilotSession({required this.title, required this.updatedAt});

  final String title;
  final DateTime updatedAt;
}
