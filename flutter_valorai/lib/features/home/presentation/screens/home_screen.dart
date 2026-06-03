import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';

import '../../../../app/router/route_names.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_radius.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../workspace/presentation/state/workspace_state_manager.dart';
import '../../data/datasources/home_remote_data_source.dart';
import '../../data/repositories/home_repository.dart';
import '../../domain/models/home_dashboard.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final HomeRepository _repository = HomeRepository(HomeRemoteDataSource());

  HomeDashboard? _dashboard;
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadDashboard();
  }

  Future<void> _loadDashboard() async {
    try {
      final dashboard = await _repository.loadDashboard(
        activeWorkspaceId: WorkspaceStateManager.instance.activeWorkspace?.id,
      );
      if (!mounted) {
        return;
      }
      if (dashboard.activeWorkspace != null) {
        WorkspaceStateManager.instance.setActiveWorkspace(
          dashboard.activeWorkspace!,
        );
      } else {
        WorkspaceStateManager.instance.clearActiveWorkspace();
      }
      setState(() {
        _dashboard = dashboard;
        _isLoading = false;
        _errorMessage = null;
      });
    } on Exception catch (exception) {
      if (!mounted) {
        return;
      }
      setState(() {
        _isLoading = false;
        _errorMessage = exception.toString();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final dashboard = _dashboard;
    final portfolioItems = dashboard == null
        ? const <_PortfolioItem>[]
        : [
            _PortfolioItem(
              label: 'Properties Tracked',
              value: '${dashboard.trackedProperties}',
              icon: Icons.home_work_outlined,
            ),
            _PortfolioItem(
              label: 'Copilot Sessions',
              value: '${dashboard.copilotSessions}',
              icon: Icons.auto_awesome_outlined,
            ),
          ];
    final recentCopilotSessions =
        dashboard?.recentCopilotSessions ?? const <HomeCopilotSession>[];

    return Scaffold(
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
          bottom: false,
          child: Stack(
            children: [
              const Positioned(top: 70, right: -110, child: _HomeAmbientGlow()),
              CustomScrollView(
                physics: const BouncingScrollPhysics(),
                slivers: [
                  SliverPadding(
                    padding: const EdgeInsets.fromLTRB(
                      AppSpacing.lg,
                      AppSpacing.lg,
                      AppSpacing.lg,
                      AppSpacing.xxl,
                    ),
                    sliver: SliverList(
                      delegate: SliverChildListDelegate([
                        _HomeHero(
                          displayName: dashboard?.displayName ?? 'ValorAI User',
                          onProfileTap: () {
                            context.goNamed(RouteNames.profile);
                          },
                        ),
                        const SizedBox(height: AppSpacing.xl),
                        _QuickActions(
                          onNewValuation: () {
                            context.goNamed(RouteNames.valuationInput);
                          },
                          onAskCopilot: () {
                            context.goNamed(RouteNames.copilot);
                          },
                        ),
                        const SizedBox(height: AppSpacing.lg),
                        if (_isLoading)
                          const Center(
                            child: Padding(
                              padding: EdgeInsets.all(AppSpacing.xl),
                              child: CircularProgressIndicator(),
                            ),
                          ),
                        if (_errorMessage != null)
                          _DashboardUnavailable(message: _errorMessage!),
                        if (portfolioItems.isNotEmpty) ...[
                          const _SectionTitle(title: 'Portfolio Overview'),
                          const SizedBox(height: AppSpacing.md),
                          SizedBox(
                            height: 146,
                            child: ListView.separated(
                              scrollDirection: Axis.horizontal,
                              physics: const BouncingScrollPhysics(),
                              itemCount: portfolioItems.length,
                              separatorBuilder: (_, _) =>
                                  const SizedBox(width: AppSpacing.md),
                              itemBuilder: (context, index) {
                                return _PortfolioCard(
                                      item: portfolioItems[index],
                                    )
                                    .animate(delay: (80 * index).ms)
                                    .fadeIn(duration: 480.ms)
                                    .slideX(begin: 0.12, end: 0);
                              },
                            ),
                          ),
                        ],
                        if (recentCopilotSessions.isNotEmpty) ...[
                          const SizedBox(height: AppSpacing.xl),
                          const _SectionTitle(title: 'Recent Copilot Sessions'),
                          const SizedBox(height: AppSpacing.md),
                          ...List.generate(recentCopilotSessions.length, (
                            index,
                          ) {
                            final session = recentCopilotSessions[index];
                            return Padding(
                              padding: EdgeInsets.only(
                                bottom:
                                    index == recentCopilotSessions.length - 1
                                    ? 0
                                    : AppSpacing.sm,
                              ),
                              child:
                                  _CopilotSessionCard(
                                        session: _CopilotSession(
                                          title: session.title,
                                          date: _formatDate(session.updatedAt),
                                        ),
                                        onTap: () {
                                          context.goNamed(RouteNames.copilot);
                                        },
                                      )
                                      .animate(delay: (70 * index).ms)
                                      .fadeIn(duration: 460.ms)
                                      .slideY(begin: 0.08, end: 0),
                            );
                          }),
                        ],
                      ]),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: _HomeBottomNavigation(
        onWorkspaceTap: () {
          context.goNamed(RouteNames.workspace);
        },
      ),
    );
  }
}

class _HomeHero extends StatelessWidget {
  const _HomeHero({required this.displayName, required this.onProfileTap});

  final String displayName;
  final VoidCallback onProfileTap;

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
          listenable: WorkspaceStateManager.instance,
          builder: (context, _) {
            final activeWorkspace =
                WorkspaceStateManager.instance.activeWorkspace;
            return Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Good Evening,',
                        style: Theme.of(context).textTheme.headlineMedium
                            ?.copyWith(
                              color: AppColors.textPrimary,
                              fontWeight: FontWeight.w700,
                              letterSpacing: -0.8,
                            ),
                      ),
                      const SizedBox(height: AppSpacing.xs),
                      Text(
                        displayName,
                        style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          color: AppColors.accent.withValues(alpha: 0.84),
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      const SizedBox(height: AppSpacing.sm),
                      InkWell(
                        onTap: () => context.goNamed(RouteNames.workspace),
                        borderRadius: BorderRadius.circular(AppRadius.sm),
                        child: Padding(
                          padding: const EdgeInsets.symmetric(vertical: 2.0),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const Icon(
                                Icons.workspaces_outline,
                                size: 13,
                                color: AppColors.accent,
                              ),
                              const SizedBox(width: 4),
                              Text(
                                activeWorkspace?.name ?? 'Select Workspace',
                                style: Theme.of(context).textTheme.labelMedium
                                    ?.copyWith(
                                      color: AppColors.textSecondary,
                                      fontWeight: FontWeight.w600,
                                      fontSize: 11,
                                    ),
                              ),
                              const SizedBox(width: 2),
                              const Icon(
                                Icons.keyboard_arrow_down_rounded,
                                size: 13,
                                color: AppColors.textMuted,
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                _ProfileAvatar(onTap: onProfileTap),
              ],
            );
          },
        )
        .animate()
        .fadeIn(duration: 520.ms)
        .slideY(begin: -0.12, end: 0, curve: Curves.easeOutCubic);
  }
}

class _ProfileAvatar extends StatelessWidget {
  const _ProfileAvatar({required this.onTap});

  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(AppRadius.pill),
      child: Container(
        width: 48,
        height: 48,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: AppColors.surface,
          border: Border.all(
            color: AppColors.textPrimary.withValues(alpha: 0.12),
          ),
          boxShadow: [
            BoxShadow(
              color: AppColors.accent.withValues(alpha: 0.18),
              blurRadius: 18,
            ),
          ],
        ),
        child: Stack(
          children: [
            const Center(
              child: Icon(
                Icons.person_outline_rounded,
                color: AppColors.textSecondary,
                size: 24,
              ),
            ),
            Positioned(
              top: 7,
              right: 7,
              child: Container(
                width: 8,
                height: 8,
                decoration: const BoxDecoration(
                  shape: BoxShape.circle,
                  color: AppColors.accent,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _QuickActions extends StatelessWidget {
  const _QuickActions({
    required this.onNewValuation,
    required this.onAskCopilot,
  });

  final VoidCallback onNewValuation;
  final VoidCallback onAskCopilot;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
              child: _QuickActionButton(
                label: 'New Valuation',
                icon: Icons.add_circle_outline_rounded,
                isPrimary: true,
                onPressed: onNewValuation,
              ),
            )
            .animate(delay: 100.ms)
            .fadeIn(duration: 480.ms)
            .slideY(begin: 0.12, end: 0),
        const SizedBox(width: AppSpacing.md),
        Expanded(
              child: _QuickActionButton(
                label: 'Ask Copilot',
                icon: Icons.auto_awesome_outlined,
                onPressed: onAskCopilot,
              ),
            )
            .animate(delay: 170.ms)
            .fadeIn(duration: 480.ms)
            .slideY(begin: 0.12, end: 0),
      ],
    );
  }
}

class _QuickActionButton extends StatelessWidget {
  const _QuickActionButton({
    required this.label,
    required this.icon,
    required this.onPressed,
    this.isPrimary = false,
  });

  final String label;
  final IconData icon;
  final VoidCallback onPressed;
  final bool isPrimary;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onPressed,
        borderRadius: BorderRadius.circular(AppRadius.lg),
        child: Ink(
          padding: const EdgeInsets.all(AppSpacing.md),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(AppRadius.lg),
            color: isPrimary
                ? AppColors.accent
                : AppColors.surface.withValues(alpha: 0.72),
            border: Border.all(
              color: isPrimary
                  ? AppColors.accent
                  : AppColors.secondaryAccent.withValues(alpha: 0.28),
            ),
            boxShadow: [
              BoxShadow(
                color:
                    (isPrimary ? AppColors.accent : AppColors.secondaryAccent)
                        .withValues(alpha: 0.14),
                blurRadius: 20,
                offset: const Offset(0, 8),
              ),
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(
                icon,
                color: isPrimary
                    ? AppColors.backgroundPrimary
                    : AppColors.secondaryAccent,
                size: 28,
              ),
              const SizedBox(height: AppSpacing.md),
              Text(
                label,
                style: Theme.of(context).textTheme.labelLarge?.copyWith(
                  color: isPrimary
                      ? AppColors.backgroundPrimary
                      : AppColors.secondaryAccent,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _SectionTitle extends StatelessWidget {
  const _SectionTitle({required this.title});

  final String title;

  @override
  Widget build(BuildContext context) {
    return Text(
      title,
      style: Theme.of(context).textTheme.titleMedium?.copyWith(
        color: AppColors.textPrimary,
        fontWeight: FontWeight.w700,
      ),
    );
  }
}

class _DashboardUnavailable extends StatelessWidget {
  const _DashboardUnavailable({required this.message});

  final String message;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: _cardDecoration(),
      child: Text(
        message,
        style: Theme.of(
          context,
        ).textTheme.bodyMedium?.copyWith(color: AppColors.textMuted),
      ),
    );
  }
}

class _PortfolioCard extends StatelessWidget {
  const _PortfolioCard({required this.item});

  final _PortfolioItem item;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 136,
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: _cardDecoration(),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Container(
            width: 36,
            height: 36,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: AppColors.backgroundSecondary,
              border: Border.all(
                color: AppColors.textPrimary.withValues(alpha: 0.06),
              ),
            ),
            child: Icon(item.icon, color: AppColors.textMuted, size: 19),
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                item.value,
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: AppSpacing.xs),
              Text(
                item.label,
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                  color: AppColors.textMuted,
                  height: 1.25,
                  fontSize: 11,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _CopilotSessionCard extends StatelessWidget {
  const _CopilotSessionCard({required this.session, required this.onTap});

  final _CopilotSession session;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppRadius.lg),
        child: Ink(
          padding: const EdgeInsets.all(AppSpacing.md),
          decoration: _cardDecoration(),
          child: Row(
            children: [
              const _ListIcon(icon: Icons.auto_awesome_outlined),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      session.title,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: AppColors.textSecondary,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: AppSpacing.xs),
                    Text(
                      session.date,
                      style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: AppColors.textMuted,
                      ),
                    ),
                  ],
                ),
              ),
              const Icon(
                Icons.chevron_right_rounded,
                color: AppColors.textMuted,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _ListIcon extends StatelessWidget {
  const _ListIcon({required this.icon});

  final IconData icon;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 42,
      height: 42,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(AppRadius.md),
        color: AppColors.backgroundSecondary,
        border: Border.all(
          color: AppColors.textPrimary.withValues(alpha: 0.06),
        ),
      ),
      child: Icon(icon, color: AppColors.accent, size: 21),
    );
  }
}

class _HomeBottomNavigation extends StatelessWidget {
  const _HomeBottomNavigation({required this.onWorkspaceTap});

  final VoidCallback onWorkspaceTap;

  @override
  Widget build(BuildContext context) {
    const items = [
      _BottomNavigationItem(label: 'Home', icon: Icons.dashboard_rounded),
      _BottomNavigationItem(label: 'Valuation', icon: Icons.analytics_outlined),
      _BottomNavigationItem(
        label: 'Copilot',
        icon: Icons.auto_awesome_outlined,
      ),
      _BottomNavigationItem(label: 'Workspace', icon: Icons.workspaces_outline),
      _BottomNavigationItem(label: 'Profile', icon: Icons.person_outline),
    ];

    return Container(
      decoration: BoxDecoration(
        color: AppColors.backgroundSecondary.withValues(alpha: 0.98),
        border: Border(
          top: BorderSide(color: AppColors.textPrimary.withValues(alpha: 0.08)),
        ),
        boxShadow: [
          BoxShadow(
            color: AppColors.accent.withValues(alpha: 0.08),
            blurRadius: 24,
            offset: const Offset(0, -8),
          ),
        ],
      ),
      child: SafeArea(
        top: false,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(
            AppSpacing.sm,
            AppSpacing.sm,
            AppSpacing.sm,
            AppSpacing.sm,
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: List.generate(items.length, (index) {
              return _BottomNavigationButton(
                item: items[index],
                isSelected: index == 0,
                onTap: () {
                  switch (index) {
                    case 0:
                      return;
                    case 1:
                      context.goNamed(RouteNames.valuationInput);
                    case 2:
                      context.goNamed(RouteNames.copilot);
                    case 3:
                      onWorkspaceTap();
                    case 4:
                      context.goNamed(RouteNames.profile);
                  }
                },
              );
            }),
          ),
        ),
      ),
    );
  }
}

class _BottomNavigationButton extends StatelessWidget {
  const _BottomNavigationButton({
    required this.item,
    required this.isSelected,
    required this.onTap,
  });

  final _BottomNavigationItem item;
  final bool isSelected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final color = isSelected ? AppColors.accent : AppColors.textMuted;

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(AppRadius.md),
      child: SizedBox(
        width: 66,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            AnimatedContainer(
              duration: 220.ms,
              width: isSelected ? 28 : 0,
              height: 3,
              decoration: BoxDecoration(
                color: AppColors.accent,
                borderRadius: BorderRadius.circular(AppRadius.pill),
                boxShadow: isSelected
                    ? [
                        BoxShadow(
                          color: AppColors.accent.withValues(alpha: 0.52),
                          blurRadius: 8,
                        ),
                      ]
                    : null,
              ),
            ),
            const SizedBox(height: AppSpacing.sm),
            Icon(item.icon, color: color, size: 23),
            const SizedBox(height: AppSpacing.xs),
            Text(
              item.label,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: Theme.of(context).textTheme.labelMedium?.copyWith(
                color: color,
                fontWeight: isSelected ? FontWeight.w700 : FontWeight.w500,
                fontSize: 10,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _HomeAmbientGlow extends StatelessWidget {
  const _HomeAmbientGlow();

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 280,
      height: 280,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        gradient: RadialGradient(
          colors: [
            AppColors.accent.withValues(alpha: 0.09),
            Colors.transparent,
          ],
        ),
      ),
    );
  }
}

BoxDecoration _cardDecoration() {
  return BoxDecoration(
    color: AppColors.surface.withValues(alpha: 0.7),
    borderRadius: BorderRadius.circular(AppRadius.lg),
    border: Border.all(color: AppColors.textPrimary.withValues(alpha: 0.07)),
  );
}

class _PortfolioItem {
  const _PortfolioItem({
    required this.label,
    required this.value,
    required this.icon,
  });

  final String label;
  final String value;
  final IconData icon;
}

class _CopilotSession {
  const _CopilotSession({required this.title, required this.date});

  final String title;
  final String date;
}

class _BottomNavigationItem {
  const _BottomNavigationItem({required this.label, required this.icon});

  final String label;
  final IconData icon;
}

String _formatDate(DateTime date) {
  final local = date.toLocal();
  return '${local.day}/${local.month}/${local.year}';
}
