import 'package:flutter/foundation.dart';
import '../../domain/models/workspace.dart';

class WorkspaceStateManager extends ChangeNotifier {
  WorkspaceStateManager._();

  static final WorkspaceStateManager instance = WorkspaceStateManager._();

  Workspace? _activeWorkspace;
  Workspace? get activeWorkspace {
    _activeWorkspace ??= Workspace(
      id: 1,
      userId: 1,
      name: 'New Cairo Premium Portfolio',
      description: 'Focus on Eastown, Mivida, and Fifth Settlement high-yield residential purchases.',
      propertyCount: 8,
      createdAt: DateTime.now().subtract(const Duration(days: 30)),
      updatedAt: DateTime.now().subtract(const Duration(hours: 2)),
    );
    return _activeWorkspace;
  }

  void setActiveWorkspace(Workspace workspace) {
    _activeWorkspace = workspace;
    notifyListeners();
  }

  void updateActiveWorkspaceName(String name, String description) {
    if (_activeWorkspace != null) {
      _activeWorkspace = _activeWorkspace!.copyWith(
        name: name,
        description: description,
        updatedAt: DateTime.now(),
      );
      notifyListeners();
    }
  }
}
