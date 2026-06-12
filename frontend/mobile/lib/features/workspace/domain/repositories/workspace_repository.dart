import '../models/workspace.dart';

abstract interface class WorkspaceRepository {
  Future<List<Workspace>> getWorkspaces();
  Future<Workspace> createWorkspace(String name);
  Future<Workspace> updateWorkspace(int id, String name);
  Future<bool> deleteWorkspace(int id);
}
