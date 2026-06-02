import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_valorai/features/workspace/domain/models/workspace.dart';
import 'package:flutter_valorai/features/workspace/presentation/state/workspace_state_manager.dart';

void main() {
  group('Workspace Model', () {
    test('supports copyWith and serialization', () {
      final now = DateTime.now();
      final workspace = Workspace(
        id: 1,
        userId: 42,
        name: 'Workspace A',
        description: 'Test workspace A',
        propertyCount: 3,
        createdAt: now,
        updatedAt: now,
      );

      final copy = workspace.copyWith(
        name: 'Workspace B',
        description: 'Updated description',
        propertyCount: 5,
      );

      expect(copy.id, 1);
      expect(copy.userId, 42);
      expect(copy.name, 'Workspace B');
      expect(copy.description, 'Updated description');
      expect(copy.propertyCount, 5);
      expect(copy.createdAt, now);
      expect(copy.updatedAt, now);

      final map = workspace.toMap();
      expect(map['id'], 1);
      expect(map['user_id'], 42);
      expect(map['name'], 'Workspace A');
      expect(map['description'], 'Test workspace A');

      final parsed = Workspace.fromMap(map);
      expect(parsed.id, 1);
      expect(parsed.userId, 42);
      expect(parsed.name, 'Workspace A');
      expect(parsed.description, 'Test workspace A');

      final serializedString = workspace.toJson();
      final parsedFromJson = Workspace.fromJson(serializedString);
      expect(parsedFromJson.id, workspace.id);
    });
  });

  group('WorkspaceStateManager', () {
    test('manages active workspace singleton state', () {
      final manager = WorkspaceStateManager.instance;
      expect(manager.activeWorkspace, isNotNull);
      expect(manager.activeWorkspace!.name, 'New Cairo Premium Portfolio');

      final now = DateTime.now();
      final customWorkspace = Workspace(
        id: 99,
        userId: 1,
        name: 'Custom W',
        description: 'Desc W',
        propertyCount: 0,
        createdAt: now,
        updatedAt: now,
      );

      bool notified = false;
      manager.addListener(() {
        notified = true;
      });

      manager.setActiveWorkspace(customWorkspace);
      expect(manager.activeWorkspace!.id, 99);
      expect(manager.activeWorkspace!.name, 'Custom W');
      expect(notified, isTrue);

      notified = false;
      manager.updateActiveWorkspaceName('Updated Custom W', 'New Desc W');
      expect(manager.activeWorkspace!.name, 'Updated Custom W');
      expect(manager.activeWorkspace!.description, 'New Desc W');
      expect(notified, isTrue);
    });
  });
}
