import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';

import '../../../../app/router/route_names.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_radius.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../data/datasources/workspace_remote_data_source.dart';
import '../../data/repositories/workspace_repository_impl.dart';
import '../../domain/models/workspace.dart';
import '../../domain/repositories/workspace_repository.dart';
import '../state/workspace_state_manager.dart';

class WorkspaceSelectorScreen extends StatefulWidget {
  const WorkspaceSelectorScreen({super.key});

  @override
  State<WorkspaceSelectorScreen> createState() => _WorkspaceSelectorScreenState();
}

class _WorkspaceSelectorScreenState extends State<WorkspaceSelectorScreen> {
  final WorkspaceRepository _repository = WorkspaceRepositoryImpl(WorkspaceRemoteDataSource());
  final TextEditingController _searchController = TextEditingController();

  List<Workspace> _workspaces = [];
  bool _isLoading = false;
  String? _errorMessage;
  String _searchQuery = '';

  @override
  void initState() {
    super.initState();
    _loadWorkspaces();
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _loadWorkspaces() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final list = await _repository.getWorkspaces();
      setState(() {
        _workspaces = list;
        _isLoading = false;

        // If no active workspace is selected yet, select the first one by default
        if (WorkspaceStateManager.instance.activeWorkspace == null && list.isNotEmpty) {
          WorkspaceStateManager.instance.setActiveWorkspace(list.first);
        } else if (WorkspaceStateManager.instance.activeWorkspace != null) {
          // Sync current active workspace if it changed in repository
          final match = list.firstWhere(
            (w) => w.id == WorkspaceStateManager.instance.activeWorkspace!.id,
            orElse: () => list.first,
          );
          WorkspaceStateManager.instance.setActiveWorkspace(match);
        }
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  Future<void> _handleCreateWorkspace(String name, String description) async {
    setState(() {
      _isLoading = true;
    });

    try {
      final newWorkspace = await _repository.createWorkspace(name, description);
      setState(() {
        _workspaces.insert(0, newWorkspace);
        // Automatically make the newly created workspace active
        WorkspaceStateManager.instance.setActiveWorkspace(newWorkspace);
        _isLoading = false;
      });
      _showSnackBar('Workspace "$name" created successfully.');
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      _showSnackBar('Failed to create workspace: ${e.toString()}');
    }
  }

  Future<void> _handleUpdateWorkspace(int id, String name, String description) async {
    setState(() {
      _isLoading = true;
    });

    try {
      final updated = await _repository.updateWorkspace(id, name, description);
      setState(() {
        final index = _workspaces.indexWhere((w) => w.id == id);
        if (index != -1) {
          _workspaces[index] = updated;
        }
        if (WorkspaceStateManager.instance.activeWorkspace?.id == id) {
          WorkspaceStateManager.instance.setActiveWorkspace(updated);
        }
        _isLoading = false;
      });
      _showSnackBar('Workspace updated successfully.');
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      _showSnackBar('Failed to update workspace: ${e.toString()}');
    }
  }

  Future<void> _handleDeleteWorkspace(Workspace workspace) async {
    setState(() {
      _isLoading = true;
    });

    try {
      final success = await _repository.deleteWorkspace(workspace.id);
      if (success) {
        setState(() {
          _workspaces.removeWhere((w) => w.id == workspace.id);
          
          // Re-select active workspace if deleted
          if (WorkspaceStateManager.instance.activeWorkspace?.id == workspace.id) {
            WorkspaceStateManager.instance.setActiveWorkspace(
              _workspaces.isNotEmpty ? _workspaces.first : Workspace(
                id: -999,
                userId: 1,
                name: 'Default State',
                createdAt: DateTime.now(),
                updatedAt: DateTime.now(),
              )
            );
          }
          _isLoading = false;
        });
        _showSnackBar('Workspace deleted successfully.');
      } else {
        setState(() {
          _isLoading = false;
        });
        _showSnackBar('Could not delete this workspace.');
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      _showSnackBar('Failed to delete workspace: ${e.toString()}');
    }
  }

  void _showSnackBar(String message) {
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(
        SnackBar(
          content: Text(message),
          behavior: SnackBarBehavior.floating,
          backgroundColor: AppColors.surface,
        ),
      );
  }

  void _openCreateDialog() {
    final nameController = TextEditingController();
    final descController = TextEditingController();
    final formKey = GlobalKey<FormState>();

    showDialog<void>(
      context: context,
      builder: (context) {
        return AlertDialog(
          backgroundColor: AppColors.surface,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadius.lg),
            side: BorderSide(color: AppColors.textPrimary.withValues(alpha: 0.08)),
          ),
          title: Text(
            'Create Workspace',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.bold,
                ),
          ),
          content: Form(
            key: formKey,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextFormField(
                  controller: nameController,
                  autofocus: true,
                  style: const TextStyle(color: AppColors.textPrimary),
                  decoration: const InputDecoration(
                    labelText: 'Workspace Name',
                    labelStyle: TextStyle(color: AppColors.textMuted),
                    focusedBorder: UnderlineInputBorder(
                      borderSide: BorderSide(color: AppColors.accent),
                    ),
                  ),
                  validator: (value) {
                    if (value == null || value.trim().isEmpty) {
                      return 'Workspace Name is required';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: AppSpacing.md),
                TextFormField(
                  controller: descController,
                  style: const TextStyle(color: AppColors.textPrimary),
                  maxLines: 3,
                  decoration: const InputDecoration(
                    labelText: 'Description',
                    labelStyle: TextStyle(color: AppColors.textMuted),
                    focusedBorder: UnderlineInputBorder(
                      borderSide: BorderSide(color: AppColors.accent),
                    ),
                  ),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel', style: TextStyle(color: AppColors.textMuted)),
            ),
            TextButton(
              onPressed: () {
                if (formKey.currentState!.validate()) {
                  _handleCreateWorkspace(nameController.text, descController.text);
                  Navigator.pop(context);
                }
              },
              child: const Text('Create', style: TextStyle(color: AppColors.accent, fontWeight: FontWeight.bold)),
            ),
          ],
        );
      },
    );
  }

  void _openEditDialog(Workspace workspace) {
    final nameController = TextEditingController(text: workspace.name);
    final descController = TextEditingController(text: workspace.description);
    final formKey = GlobalKey<FormState>();

    showDialog<void>(
      context: context,
      builder: (context) {
        return AlertDialog(
          backgroundColor: AppColors.surface,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadius.lg),
            side: BorderSide(color: AppColors.textPrimary.withValues(alpha: 0.08)),
          ),
          title: Text(
            'Edit Workspace',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.bold,
                ),
          ),
          content: Form(
            key: formKey,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextFormField(
                  controller: nameController,
                  autofocus: true,
                  style: const TextStyle(color: AppColors.textPrimary),
                  decoration: const InputDecoration(
                    labelText: 'Workspace Name',
                    labelStyle: TextStyle(color: AppColors.textMuted),
                    focusedBorder: UnderlineInputBorder(
                      borderSide: BorderSide(color: AppColors.accent),
                    ),
                  ),
                  validator: (value) {
                    if (value == null || value.trim().isEmpty) {
                      return 'Workspace Name is required';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: AppSpacing.md),
                TextFormField(
                  controller: descController,
                  style: const TextStyle(color: AppColors.textPrimary),
                  maxLines: 3,
                  decoration: const InputDecoration(
                    labelText: 'Description',
                    labelStyle: TextStyle(color: AppColors.textMuted),
                    focusedBorder: UnderlineInputBorder(
                      borderSide: BorderSide(color: AppColors.accent),
                    ),
                  ),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel', style: TextStyle(color: AppColors.textMuted)),
            ),
            TextButton(
              onPressed: () {
                if (formKey.currentState!.validate()) {
                  _handleUpdateWorkspace(workspace.id, nameController.text, descController.text);
                  Navigator.pop(context);
                }
              },
              child: const Text('Save', style: TextStyle(color: AppColors.accent, fontWeight: FontWeight.bold)),
            ),
          ],
        );
      },
    );
  }

  void _openDeleteConfirmDialog(Workspace workspace) {
    showDialog<void>(
      context: context,
      builder: (context) {
        return AlertDialog(
          backgroundColor: AppColors.surface,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadius.lg),
            side: BorderSide(color: AppColors.textPrimary.withValues(alpha: 0.08)),
          ),
          title: Text(
            'Delete Workspace',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.bold,
                ),
          ),
          content: Text(
            'Are you sure you want to permanently delete workspace "${workspace.name}"? This action will also delete all associated portfolio properties and chats.',
            style: const TextStyle(color: AppColors.textSecondary),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel', style: TextStyle(color: AppColors.textMuted)),
            ),
            TextButton(
              onPressed: () {
                _handleDeleteWorkspace(workspace);
                Navigator.pop(context);
              },
              child: const Text('Delete', style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold)),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final filtered = _workspaces.where((w) {
      if (_searchQuery.trim().isEmpty) return true;
      return w.name.toLowerCase().contains(_searchQuery.toLowerCase()) ||
          w.description.toLowerCase().contains(_searchQuery.toLowerCase());
    }).toList();

    return Scaffold(
      backgroundColor: AppColors.backgroundPrimary,
      body: DecoratedBox(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              AppColors.backgroundPrimary,
              AppColors.backgroundSecondary,
              Color(0xFF04111D),
            ],
          ),
        ),
        child: SafeArea(
          child: ListenableBuilder(
            listenable: WorkspaceStateManager.instance,
            builder: (context, _) {
              final active = WorkspaceStateManager.instance.activeWorkspace;
              return Column(
                children: [
                  _buildHeader(),
                  _buildSearchBar(),
                  if (_isLoading && _workspaces.isEmpty)
                    const Expanded(
                      child: Center(
                        child: CircularProgressIndicator(color: AppColors.accent),
                      ),
                    )
                  else if (_errorMessage != null && _workspaces.isEmpty)
                    Expanded(child: _buildErrorState())
                  else if (filtered.isEmpty)
                    Expanded(child: _buildEmptyState())
                  else
                    Expanded(
                      child: ListView.builder(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        physics: const BouncingScrollPhysics(),
                        itemCount: filtered.length,
                        itemBuilder: (context, index) {
                          final item = filtered[index];
                          final isItemActive = active?.id == item.id;
                          return _buildWorkspaceCard(item, isItemActive);
                        },
                      ),
                    ),
                ],
              );
            },
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _openCreateDialog,
        backgroundColor: AppColors.accent,
        foregroundColor: AppColors.backgroundPrimary,
        child: const Icon(Icons.add_rounded),
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.md,
        vertical: AppSpacing.sm,
      ),
      child: Row(
        children: [
          IconButton(
            icon: const Icon(Icons.arrow_back_ios_new_rounded, color: AppColors.textPrimary, size: 20),
            onPressed: () {
              if (context.canPop()) {
                context.pop();
              } else {
                context.goNamed(RouteNames.home);
              }
            },
          ),
          const SizedBox(width: AppSpacing.sm),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'ValorAI Workspaces',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.w700,
                        color: AppColors.textPrimary,
                      ),
                ),
                Text(
                  'Select or manage your organization boundary',
                  style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: AppColors.textMuted,
                      ),
                ),
              ],
            ),
          ),
          IconButton(
            icon: const Icon(Icons.refresh_rounded, color: AppColors.accent),
            onPressed: _loadWorkspaces,
          ),
        ],
      ),
    );
  }

  Widget _buildSearchBar() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: AppSpacing.sm),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm),
        decoration: BoxDecoration(
          color: AppColors.surface,
          borderRadius: BorderRadius.circular(AppRadius.md),
          border: Border.all(color: AppColors.textPrimary.withValues(alpha: 0.06)),
        ),
        child: TextField(
          controller: _searchController,
          style: const TextStyle(color: AppColors.textPrimary, fontSize: 13),
          onChanged: (val) {
            setState(() {
              _searchQuery = val;
            });
          },
          decoration: const InputDecoration(
            hintText: 'Search workspaces...',
            hintStyle: TextStyle(color: AppColors.textMuted),
            border: InputBorder.none,
            icon: Icon(Icons.search_rounded, color: AppColors.textMuted, size: 18),
          ),
        ),
      ),
    );
  }

  Widget _buildWorkspaceCard(Workspace item, bool isActive) {
    return Card(
      margin: const EdgeInsets.only(bottom: AppSpacing.md),
      color: isActive ? AppColors.accent.withValues(alpha: 0.07) : AppColors.surface.withValues(alpha: 0.72),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppRadius.lg),
        side: BorderSide(
          color: isActive ? AppColors.accent.withValues(alpha: 0.48) : AppColors.textPrimary.withValues(alpha: 0.07),
        ),
      ),
      child: InkWell(
        onTap: () {
          WorkspaceStateManager.instance.setActiveWorkspace(item);
          _showSnackBar('Switched to Workspace "${item.name}"');
        },
        borderRadius: BorderRadius.circular(AppRadius.lg),
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.md),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Flexible(
                              child: Text(
                                item.name,
                                style: const TextStyle(
                                  color: AppColors.textPrimary,
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                            if (isActive) ...[
                              const SizedBox(width: AppSpacing.sm),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                decoration: BoxDecoration(
                                  color: AppColors.accent.withValues(alpha: 0.16),
                                  borderRadius: BorderRadius.circular(AppRadius.sm),
                                  border: Border.all(color: AppColors.accent.withValues(alpha: 0.3)),
                                ),
                                child: const Text(
                                  'ACTIVE',
                                  style: TextStyle(
                                    color: AppColors.accent,
                                    fontSize: 8,
                                    fontWeight: FontWeight.bold,
                                    letterSpacing: 1.1,
                                  ),
                                ),
                              ),
                            ],
                          ],
                        ),
                        const SizedBox(height: AppSpacing.xs),
                        Text(
                          item.description,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(
                            color: AppColors.textSecondary,
                            fontSize: 11,
                            height: 1.4,
                          ),
                        ),
                      ],
                    ),
                  ),
                  PopupMenuButton<String>(
                    icon: const Icon(Icons.more_vert_rounded, color: AppColors.textMuted, size: 18),
                    color: AppColors.surface,
                    onSelected: (action) {
                      if (action == 'edit') {
                        _openEditDialog(item);
                      } else if (action == 'delete') {
                        _openDeleteConfirmDialog(item);
                      }
                    },
                    itemBuilder: (context) => [
                      const PopupMenuItem(
                        value: 'edit',
                        child: Text('Edit Workspace', style: TextStyle(color: AppColors.textPrimary, fontSize: 12)),
                      ),
                      const PopupMenuItem(
                        value: 'delete',
                        child: Text('Delete Workspace', style: TextStyle(color: Colors.redAccent, fontSize: 12)),
                      ),
                    ],
                  ),
                ],
              ),
              const Divider(height: 24, color: Colors.white10),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  _buildMetaItem('Properties', '${item.propertyCount}', Icons.home_work_outlined),
                  _buildMetaItem('Created', _formatDate(item.createdAt), Icons.calendar_today_rounded),
                  _buildMetaItem('Last Activity', _formatDate(item.updatedAt), Icons.query_builder_rounded),
                ],
              ),
            ],
          ),
        ),
      ),
    ).animate().fadeIn(duration: 260.ms).slideY(begin: 0.04, end: 0);
  }

  Widget _buildMetaItem(String label, String value, IconData icon) {
    return Row(
      children: [
        Icon(icon, color: AppColors.textMuted, size: 12),
        const SizedBox(width: 4),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              label,
              style: const TextStyle(color: AppColors.textMuted, fontSize: 8),
            ),
            Text(
              value,
              style: const TextStyle(color: AppColors.textSecondary, fontSize: 10, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.workspaces_outline, size: 48, color: AppColors.textMuted.withValues(alpha: 0.5)),
          const SizedBox(height: AppSpacing.md),
          const Text('No Workspaces Found', style: TextStyle(color: AppColors.textPrimary, fontWeight: FontWeight.bold)),
          const SizedBox(height: AppSpacing.xs),
          const Text('Try adjusting your search terms or add a new workspace.', style: TextStyle(color: AppColors.textMuted, fontSize: 11)),
        ],
      ),
    );
  }

  Widget _buildErrorState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.error_outline_rounded, size: 48, color: Colors.redAccent),
          const SizedBox(height: AppSpacing.md),
          const Text('Failed to load workspaces', style: TextStyle(color: AppColors.textPrimary, fontWeight: FontWeight.bold)),
          const SizedBox(height: AppSpacing.xs),
          Text(_errorMessage ?? 'An unknown error occurred.', style: const TextStyle(color: AppColors.textMuted, fontSize: 11)),
          const SizedBox(height: AppSpacing.md),
          ElevatedButton(
            onPressed: _loadWorkspaces,
            child: const Text('Retry'),
          ),
        ],
      ),
    );
  }

  String _formatDate(DateTime dt) {
    final now = DateTime.now();
    final difference = now.difference(dt);
    if (difference.inDays == 0) {
      return 'Today';
    } else if (difference.inDays == 1) {
      return 'Yesterday';
    } else if (difference.inDays < 30) {
      return '${difference.inDays}d ago';
    } else {
      return '${dt.day}/${dt.month}/${dt.year}';
    }
  }
}
