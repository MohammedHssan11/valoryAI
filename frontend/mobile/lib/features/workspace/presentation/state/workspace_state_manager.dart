import 'package:flutter/foundation.dart';
import '../../domain/models/workspace.dart';

class WorkspaceStateManager extends ChangeNotifier {
  WorkspaceStateManager._();

  static final WorkspaceStateManager instance = WorkspaceStateManager._();

  Workspace? _activeWorkspace;
  Workspace? get activeWorkspace => _activeWorkspace;

  void setActiveWorkspace(Workspace workspace) {
    _activeWorkspace = workspace;
    notifyListeners();
  }

  void clearActiveWorkspace() {
    _activeWorkspace = null;
    notifyListeners();
  }

  void updateActiveWorkspaceName(String name) {
    if (_activeWorkspace != null) {
      _activeWorkspace = _activeWorkspace!.copyWith(
        name: name,
        updatedAt: DateTime.now(),
      );
      notifyListeners();
    }
  }
}
