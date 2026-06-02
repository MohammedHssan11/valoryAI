import '../models/workspace.dart';

abstract interface class WorkspaceRepository {
  Future<List<Workspace>> getWorkspaces();
  Future<Workspace> createWorkspace(String name, String description);
  Future<Workspace> updateWorkspace(int id, String name, String description);
  Future<bool> deleteWorkspace(int id);
}
