import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';

import '../../../../app/router/route_names.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_radius.dart';
import '../../../../app/theme/app_spacing.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  Timer? _navigationTimer;

  @override
  void initState() {
    super.initState();
    _navigationTimer = Timer(2800.ms, () {
      if (mounted) {
        context.goNamed(RouteNames.onboarding);
      }
    });
  }

  @override
  void dispose() {
    _navigationTimer?.cancel();
    super.dispose();
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
              Color(0xFF03101B),
            ],
          ),
        ),
        child: SafeArea(
          child: Stack(
            fit: StackFit.expand,
            children: [
              const _AmbientGlow(),
              Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const _ValorAILogo()
                        .animate()
                        .fadeIn(duration: 700.ms, curve: Curves.easeOut)
                        .scale(
                          begin: const Offset(0.94, 0.94),
                          end: const Offset(1, 1),
                          duration: 900.ms,
                          curve: Curves.easeOutCubic,
                        ),
                    const SizedBox(height: AppSpacing.xl),
                    const _LoadingBar()
                        .animate(delay: 350.ms)
                        .fadeIn(duration: 500.ms),
                    const SizedBox(height: AppSpacing.md),
                    Text(
                          'SYNCHRONIZING CORE',
                          style: Theme.of(context).textTheme.labelMedium
                              ?.copyWith(
                                color: AppColors.accent.withValues(alpha: 0.72),
                                letterSpacing: 2.4,
                                fontWeight: FontWeight.w600,
                              ),
                        )
                        .animate(delay: 500.ms)
                        .fadeIn(duration: 700.ms)
                        .then()
                        .shimmer(
                          delay: 650.ms,
                          duration: 1200.ms,
                          color: AppColors.textPrimary.withValues(alpha: 0.45),
                        ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _AmbientGlow extends StatelessWidget {
  const _AmbientGlow();

  @override
  Widget build(BuildContext context) {
    return Center(
      child:
          Container(
                width: 260,
                height: 260,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: RadialGradient(
                    colors: [
                      AppColors.accent.withValues(alpha: 0.18),
                      AppColors.accent.withValues(alpha: 0.04),
                      Colors.transparent,
                    ],
                  ),
                ),
              )
              .animate(onPlay: (controller) => controller.repeat(reverse: true))
              .fade(begin: 0.52, end: 0.9, duration: 1400.ms)
              .scale(
                begin: const Offset(0.9, 0.9),
                end: const Offset(1.08, 1.08),
                duration: 1400.ms,
                curve: Curves.easeInOut,
              ),
    );
  }
}

class _ValorAILogo extends StatelessWidget {
  const _ValorAILogo();

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 76,
          height: 76,
          decoration: BoxDecoration(
            color: AppColors.surface.withValues(alpha: 0.76),
            borderRadius: BorderRadius.circular(AppRadius.xl),
            border: Border.all(color: AppColors.accent.withValues(alpha: 0.44)),
            boxShadow: [
              BoxShadow(
                color: AppColors.accent.withValues(alpha: 0.28),
                blurRadius: 32,
                spreadRadius: 2,
              ),
            ],
          ),
          child: const Icon(
            Icons.auto_awesome_rounded,
            color: AppColors.accent,
            size: 36,
          ),
        ),
        const SizedBox(height: AppSpacing.lg),
        Text(
          'ValorAI',
          style: Theme.of(context).textTheme.headlineLarge?.copyWith(
            color: AppColors.textPrimary,
            fontWeight: FontWeight.w700,
            letterSpacing: -0.8,
            shadows: [
              Shadow(
                color: AppColors.accent.withValues(alpha: 0.52),
                blurRadius: 22,
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _LoadingBar extends StatelessWidget {
  const _LoadingBar();

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(AppRadius.pill),
      child: Container(
        width: 144,
        height: 4,
        color: AppColors.surface,
        child: Align(
          alignment: Alignment.centerLeft,
          child:
              FractionallySizedBox(
                    widthFactor: 0.34,
                    child: Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(AppRadius.pill),
                        gradient: const LinearGradient(
                          colors: [AppColors.accent, AppColors.secondaryAccent],
                        ),
                        boxShadow: [
                          BoxShadow(
                            color: AppColors.accent.withValues(alpha: 0.72),
                            blurRadius: 10,
                          ),
                        ],
                      ),
                    ),
                  )
                  .animate(onPlay: (controller) => controller.repeat())
                  .slideX(
                    begin: -1.05,
                    end: 3.1,
                    duration: 1200.ms,
                    curve: Curves.easeInOutCubic,
                  ),
        ),
      ),
    );
  }
}
