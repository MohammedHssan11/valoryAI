import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';

import '../../../../app/router/route_names.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_radius.dart';
import '../../../../app/theme/app_spacing.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final PageController _pageController = PageController();
  int _currentPage = 0;

  static const _pages = [
    _OnboardingPageData(
      title: 'Precision Intelligence',
      description:
          'Access real-time AI-driven valuations for any property with unparalleled accuracy.',
      icon: Icons.domain_rounded,
      illustrationLabel: 'PROPERTY INTELLIGENCE',
    ),
    _OnboardingPageData(
      title: 'Your Property Copilot',
      description:
          'An AI advisor built for real estate professionals to provide evidence-based insights.',
      icon: Icons.auto_awesome_rounded,
      illustrationLabel: 'AI ADVISOR',
    ),
  ];

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  void _openLogin() {
    context.goNamed(RouteNames.login);
  }

  void _handlePrimaryAction() {
    if (_currentPage == _pages.length - 1) {
      _openLogin();
      return;
    }

    _pageController.nextPage(duration: 480.ms, curve: Curves.easeInOutCubic);
  }

  @override
  Widget build(BuildContext context) {
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
          child: Padding(
            padding: const EdgeInsets.fromLTRB(
              AppSpacing.lg,
              AppSpacing.md,
              AppSpacing.lg,
              AppSpacing.lg,
            ),
            child: Column(
              children: [
                Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'ValorAI',
                          style: Theme.of(context).textTheme.titleLarge
                              ?.copyWith(
                                color: AppColors.accent,
                                fontWeight: FontWeight.w700,
                                letterSpacing: -0.5,
                              ),
                        ),
                        TextButton(
                          onPressed: _openLogin,
                          child: const Text('Skip'),
                        ),
                      ],
                    )
                    .animate()
                    .fadeIn(duration: 550.ms)
                    .slideY(begin: -0.18, end: 0),
                Expanded(
                  child: PageView.builder(
                    controller: _pageController,
                    itemCount: _pages.length,
                    onPageChanged: (index) {
                      setState(() {
                        _currentPage = index;
                      });
                    },
                    itemBuilder: (context, index) {
                      return _OnboardingPage(
                        key: ValueKey(index),
                        data: _pages[index],
                      );
                    },
                  ),
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: List.generate(_pages.length, (index) {
                    final isActive = index == _currentPage;
                    return AnimatedContainer(
                      duration: 280.ms,
                      curve: Curves.easeOutCubic,
                      width: isActive ? 28 : 8,
                      height: 8,
                      margin: const EdgeInsets.symmetric(
                        horizontal: AppSpacing.xs,
                      ),
                      decoration: BoxDecoration(
                        color: isActive
                            ? AppColors.accent
                            : AppColors.textMuted.withValues(alpha: 0.36),
                        borderRadius: BorderRadius.circular(AppRadius.pill),
                        boxShadow: isActive
                            ? [
                                BoxShadow(
                                  color: AppColors.accent.withValues(
                                    alpha: 0.4,
                                  ),
                                  blurRadius: 12,
                                ),
                              ]
                            : null,
                      ),
                    );
                  }),
                ),
                const SizedBox(height: AppSpacing.lg),
                SizedBox(
                      width: double.infinity,
                      child: FilledButton(
                        onPressed: _handlePrimaryAction,
                        style: FilledButton.styleFrom(
                          padding: const EdgeInsets.symmetric(
                            vertical: AppSpacing.md,
                          ),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(AppRadius.lg),
                          ),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              _currentPage == _pages.length - 1
                                  ? 'Get Started'
                                  : 'Next',
                            ),
                            const SizedBox(width: AppSpacing.sm),
                            const Icon(Icons.arrow_forward_rounded, size: 18),
                          ],
                        ),
                      ),
                    )
                    .animate(delay: 240.ms)
                    .fadeIn(duration: 520.ms)
                    .slideY(begin: 0.24, end: 0),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _OnboardingPage extends StatelessWidget {
  const _OnboardingPage({super.key, required this.data});

  final _OnboardingPageData data;

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        _HeroPlaceholder(data: data)
            .animate()
            .fadeIn(duration: 650.ms)
            .scale(
              begin: const Offset(0.93, 0.93),
              end: const Offset(1, 1),
              duration: 700.ms,
              curve: Curves.easeOutCubic,
            ),
        const SizedBox(height: AppSpacing.xxl),
        Text(
              data.title,
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                color: AppColors.textPrimary,
                fontWeight: FontWeight.w700,
                letterSpacing: -0.8,
              ),
            )
            .animate(delay: 100.ms)
            .fadeIn(duration: 600.ms)
            .slideY(begin: 0.12, end: 0),
        const SizedBox(height: AppSpacing.md),
        ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 330),
              child: Text(
                data.description,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  color: AppColors.textSecondary.withValues(alpha: 0.84),
                  height: 1.55,
                ),
              ),
            )
            .animate(delay: 180.ms)
            .fadeIn(duration: 650.ms)
            .slideY(begin: 0.12, end: 0),
      ],
    );
  }
}

class _HeroPlaceholder extends StatelessWidget {
  const _HeroPlaceholder({required this.data});

  final _OnboardingPageData data;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 292,
      height: 292,
      child: Stack(
        alignment: Alignment.center,
        children: [
          Container(
                width: 264,
                height: 264,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: RadialGradient(
                    colors: [
                      AppColors.accent.withValues(alpha: 0.17),
                      AppColors.secondaryAccent.withValues(alpha: 0.04),
                      Colors.transparent,
                    ],
                  ),
                ),
              )
              .animate(onPlay: (controller) => controller.repeat(reverse: true))
              .fade(begin: 0.58, end: 0.96, duration: 1600.ms)
              .scale(
                begin: const Offset(0.94, 0.94),
                end: const Offset(1.05, 1.05),
                duration: 1600.ms,
              ),
          Container(
            width: 236,
            height: 236,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: AppColors.surface.withValues(alpha: 0.62),
              border: Border.all(
                color: AppColors.accent.withValues(alpha: 0.34),
              ),
              boxShadow: [
                BoxShadow(
                  color: AppColors.accent.withValues(alpha: 0.12),
                  blurRadius: 36,
                  spreadRadius: 2,
                ),
              ],
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  width: 92,
                  height: 92,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: AppColors.accent.withValues(alpha: 0.1),
                    border: Border.all(
                      color: AppColors.accent.withValues(alpha: 0.22),
                    ),
                  ),
                  child: Icon(data.icon, size: 46, color: AppColors.accent),
                ),
                const SizedBox(height: AppSpacing.md),
                Text(
                  data.illustrationLabel,
                  style: Theme.of(context).textTheme.labelMedium?.copyWith(
                    color: AppColors.accent.withValues(alpha: 0.78),
                    fontWeight: FontWeight.w700,
                    letterSpacing: 1.5,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _OnboardingPageData {
  const _OnboardingPageData({
    required this.title,
    required this.description,
    required this.icon,
    required this.illustrationLabel,
  });

  final String title;
  final String description;
  final IconData icon;
  final String illustrationLabel;
}
