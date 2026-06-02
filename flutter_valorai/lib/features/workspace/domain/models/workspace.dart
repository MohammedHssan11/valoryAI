import 'dart:convert';

class Workspace {
  final int id;
  final int userId;
  final String name;
  final String description;
  final int propertyCount;
  final DateTime createdAt;
  final DateTime updatedAt;
  final int version;
  final bool isDeleted;
  final DateTime? deletedAt;

  const Workspace({
    required this.id,
    required this.userId,
    required this.name,
    this.description = 'Real estate workspace context',
    this.propertyCount = 0,
    required this.createdAt,
    required this.updatedAt,
    this.version = 1,
    this.isDeleted = false,
    this.deletedAt,
  });

  Workspace copyWith({
    int? id,
    int? userId,
    String? name,
    String? description,
    int? propertyCount,
    DateTime? createdAt,
    DateTime? updatedAt,
    int? version,
    bool? isDeleted,
    DateTime? deletedAt,
  }) {
    return Workspace(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      name: name ?? this.name,
      description: description ?? this.description,
      propertyCount: propertyCount ?? this.propertyCount,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      version: version ?? this.version,
      isDeleted: isDeleted ?? this.isDeleted,
      deletedAt: deletedAt ?? this.deletedAt,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'user_id': userId,
      'name': name,
      'description': description,
      'property_count': propertyCount,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'version': version,
      'is_deleted': isDeleted,
      'deleted_at': deletedAt?.toIso8601String(),
    };
  }

  factory Workspace.fromMap(Map<String, dynamic> map) {
    return Workspace(
      id: map['id'] as int,
      userId: map['user_id'] as int? ?? 1,
      name: map['name'] as String,
      description: map['description'] as String? ?? 'Real estate workspace context',
      propertyCount: map['property_count'] as int? ?? 0,
      createdAt: map['created_at'] != null ? DateTime.parse(map['created_at'] as String) : DateTime.now(),
      updatedAt: map['updated_at'] != null ? DateTime.parse(map['updated_at'] as String) : DateTime.now(),
      version: map['version'] as int? ?? 1,
      isDeleted: map['is_deleted'] as bool? ?? false,
      deletedAt: map['deleted_at'] != null ? DateTime.parse(map['deleted_at'] as String) : null,
    );
  }

  String toJson() => json.encode(toMap());

  factory Workspace.fromJson(String source) =>
      Workspace.fromMap(json.decode(source) as Map<String, dynamic>);
}
