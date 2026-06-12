import '../../domain/models/workspace.dart';
import '../../domain/repositories/workspace_repository.dart';
import '../datasources/workspace_remote_data_source.dart';

class WorkspaceRepositoryImpl implements WorkspaceRepository {
  WorkspaceRepositoryImpl(this._remoteDataSource);

  final WorkspaceRemoteDataSource _remoteDataSource;

  @override
  Future<List<Workspace>> getWorkspaces() async {
    final rawList = await _remoteDataSource.getWorkspaces();
    final results = <Workspace>[];

    for (final raw in rawList) {
      final id = raw['id'] as int;
      final properties = await _remoteDataSource.getWorkspaceProperties(id);
      results.add(
        Workspace.fromMap({
          ...raw,
          'description': '',
          'property_count': properties.length,
        }),
      );
    }

    return results;
  }

  @override
  Future<Workspace> createWorkspace(String name) async {
    final raw = await _remoteDataSource.createWorkspace(name);
    return Workspace.fromMap({...raw, 'description': '', 'property_count': 0});
  }

  @override
  Future<Workspace> updateWorkspace(int id, String name) async {
    final raw = await _remoteDataSource.updateWorkspace(id, name);
    return Workspace.fromMap({...raw, 'description': ''});
  }

  @override
  Future<bool> deleteWorkspace(int id) async {
    return _remoteDataSource.deleteWorkspace(id);
  }
}
