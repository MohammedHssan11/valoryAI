import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import '../../../../app/router/route_names.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_radius.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../domain/models/valuation_response.dart';

class ValuationResultScreen extends StatefulWidget {
  const ValuationResultScreen({super.key, this.response});

  final ValuationResponse? response;

  @override
  State<ValuationResultScreen> createState() => _ValuationResultScreenState();
}

class _ValuationResultScreenState extends State<ValuationResultScreen> {
  final _whyValueKey = GlobalKey();
  final _evidenceKey = GlobalKey();

  @override
  Widget build(BuildContext context) {
    final result = widget.response;
    return Scaffold(
      extendBody: true,
      bottomNavigationBar: result == null
          ? null
          : _StickyActionBar(
              onExplainMore: _showExplanation,
              onViewComparables: () => _openComparables(result),
              onAskCopilot: () {
                context.pushNamed(RouteNames.copilot, extra: result);
              },
              onSave: _showSaveNotice,
            ),
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
          child: result == null
              ? _EmptyResult(onBack: () => context.goNamed(RouteNames.home))
              : Stack(
                  children: [
                    const Positioned(
                      top: 76,
                      right: -128,
                      child: _AmbientGlow(
                        color: AppColors.accent,
                        size: 320,
                        opacity: 0.11,
                      ),
                    ),
                    const Positioned(
                      top: 360,
                      left: -146,
                      child: _AmbientGlow(
                        color: AppColors.secondaryAccent,
                        size: 280,
                        opacity: 0.06,
                      ),
                    ),
                    _ResultContent(
                      result: result,
                      whyValueKey: _whyValueKey,
                      evidenceKey: _evidenceKey,
                      onBack: _goBack,
                      onViewComparables: () => _openComparables(result),
                    ),
                  ],
                ),
        ),
      ),
    );
  }

  void _goBack() {
    if (context.canPop()) {
      context.pop();
    } else {
      context.goNamed(RouteNames.home);
    }
  }

  void _showExplanation() {
    final target = _whyValueKey.currentContext ?? _evidenceKey.currentContext;
    if (target == null) {
      return;
    }
    Scrollable.ensureVisible(
      target,
      duration: 480.ms,
      curve: Curves.easeOutCubic,
      alignment: 0.08,
    );
  }

  void _openComparables(ValuationResponse result) {
    context.pushNamed(RouteNames.comparableExplorer, extra: result);
  }

  void _showSaveNotice() {
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(
        const SnackBar(
          content: Text(
            'Saving becomes available when workspace persistence is connected.',
          ),
          behavior: SnackBarBehavior.floating,
        ),
      );
  }
}

class _ResultContent extends StatelessWidget {
  const _ResultContent({
    required this.result,
    required this.whyValueKey,
    required this.evidenceKey,
    required this.onBack,
    required this.onViewComparables,
  });

  final ValuationResponse result;
  final GlobalKey whyValueKey;
  final GlobalKey evidenceKey;
  final VoidCallback onBack;
  final VoidCallback onViewComparables;

  @override
  Widget build(BuildContext context) {
    final summary = result.aiSummary;
    final showWhyValue = result.drivers.isNotEmpty;
    final showMap = result.location?.isAvailable ?? false;

    return CustomScrollView(
      physics: const BouncingScrollPhysics(),
      slivers: [
        SliverPadding(
          padding: const EdgeInsets.fromLTRB(
            AppSpacing.lg,
            AppSpacing.md,
            AppSpacing.lg,
            132,
          ),
          sliver: SliverList(
            delegate: SliverChildListDelegate([
              _ResultHeader(onBack: onBack),
              const SizedBox(height: AppSpacing.lg),
              _ValuationHero(result: result),
              if (result.hasFairValue) ...[
                const SizedBox(height: AppSpacing.lg),
                _FairValueRange(result: result),
              ],
              if (showWhyValue) ...[
                const SizedBox(height: AppSpacing.xl),
                KeyedSubtree(
                  key: whyValueKey,
                  child: _WhyValueSection(drivers: result.drivers),
                ),
              ],
              if (summary != null) ...[
                const SizedBox(height: AppSpacing.xl),
                _AiSummaryCard(
                  summary: summary,
                  confidenceReason:
                      result.explainability?.confidenceReason ??
                      result.explainability?.narrative?.confidenceReason,
                ),
              ],
              const SizedBox(height: AppSpacing.xl),
              KeyedSubtree(
                key: evidenceKey,
                child: _EvidenceSection(evidence: result.evidence),
              ),
              if (result.topComparables.isNotEmpty) ...[
                const SizedBox(height: AppSpacing.xl),
                _TopComparablesSection(
                  comparables: result.topComparables.take(3).toList(),
                  onViewAll: onViewComparables,
                ),
              ],
              if (result.marketSignals.isNotEmpty) ...[
                const SizedBox(height: AppSpacing.xl),
                _MarketContextSection(signals: result.marketSignals),
              ],
              if (showMap) ...[
                const SizedBox(height: AppSpacing.xl),
                _MiniMapSection(result: result),
              ],
              const SizedBox(height: AppSpacing.md),
            ]),
          ),
        ),
      ],
    );
  }
}

class _ResultHeader extends StatelessWidget {
  const _ResultHeader({required this.onBack});

  final VoidCallback onBack;

  @override
  Widget build(BuildContext context) {
    return Row(
          children: [
            _RoundIconButton(
              icon: Icons.arrow_back_ios_new_rounded,
              onTap: onBack,
            ),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Valuation Result',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w700,
                      letterSpacing: -0.5,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    'Evidence-backed property intelligence',
                    style: Theme.of(context).textTheme.labelMedium?.copyWith(
                      color: AppColors.textMuted,
                    ),
                  ),
                ],
              ),
            ),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: AppColors.accent.withValues(alpha: 0.1),
                shape: BoxShape.circle,
                border: Border.all(
                  color: AppColors.accent.withValues(alpha: 0.24),
                ),
              ),
              child: const Icon(
                Icons.auto_awesome_rounded,
                color: AppColors.accent,
                size: 19,
              ),
            ),
          ],
        )
        .animate()
        .fadeIn(duration: 420.ms)
        .slideY(begin: -0.1, end: 0, curve: Curves.easeOutCubic);
  }
}

class _ValuationHero extends StatelessWidget {
  const _ValuationHero({required this.result});

  final ValuationResponse result;

  @override
  Widget build(BuildContext context) {
    final confidence = (result.confidenceScore * 100).round();
    final confidenceColor = _confidenceColor(result.confidenceScore);

    return Container(
          padding: const EdgeInsets.fromLTRB(
            AppSpacing.lg,
            AppSpacing.xl,
            AppSpacing.lg,
            AppSpacing.lg,
          ),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                AppColors.accent.withValues(alpha: 0.2),
                AppColors.surface.withValues(alpha: 0.94),
                AppColors.backgroundSecondary.withValues(alpha: 0.9),
              ],
            ),
            borderRadius: BorderRadius.circular(AppRadius.xl),
            border: Border.all(color: AppColors.accent.withValues(alpha: 0.46)),
            boxShadow: [
              BoxShadow(
                color: AppColors.accent.withValues(alpha: 0.18),
                blurRadius: 34,
                offset: const Offset(0, 16),
              ),
            ],
          ),
          child: Column(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.sm,
                  vertical: 6,
                ),
                decoration: BoxDecoration(
                  color: AppColors.secondaryAccent.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(AppRadius.pill),
                  border: Border.all(
                    color: AppColors.secondaryAccent.withValues(alpha: 0.24),
                  ),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      width: 7,
                      height: 7,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: AppColors.secondaryAccent,
                        boxShadow: [
                          BoxShadow(
                            color: AppColors.secondaryAccent.withValues(
                              alpha: 0.72,
                            ),
                            blurRadius: 8,
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 7),
                    Text(
                      'VALORAI INTELLIGENCE',
                      style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: AppColors.secondaryAccent,
                        fontSize: 10,
                        fontWeight: FontWeight.w700,
                        letterSpacing: 1.3,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: AppSpacing.lg),
              Text(
                result.valueBasisLabel.toUpperCase(),
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                  color: AppColors.textMuted,
                  fontSize: 10,
                  fontWeight: FontWeight.w700,
                  letterSpacing: 1.7,
                ),
              ),
              const SizedBox(height: AppSpacing.sm),
              if (result.hasFairValue)
                _AnimatedPrice(value: result.fairPriceEgp)
              else
                Text(
                  'INSUFFICIENT DATA',
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                    color: AppColors.textPrimary,
                    fontWeight: FontWeight.w800,
                    letterSpacing: -1,
                  ),
                ),
              const SizedBox(height: AppSpacing.md),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.md,
                  vertical: AppSpacing.sm,
                ),
                decoration: BoxDecoration(
                  color: confidenceColor.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(AppRadius.pill),
                  border: Border.all(
                    color: confidenceColor.withValues(alpha: 0.34),
                  ),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      Icons.verified_outlined,
                      color: confidenceColor,
                      size: 17,
                    ),
                    const SizedBox(width: 7),
                    Text(
                      '$confidence% Confidence',
                      style: Theme.of(context).textTheme.labelLarge?.copyWith(
                        color: confidenceColor,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: AppSpacing.sm),
              Text(
                'Based on ${result.comparablesCount} comparable '
                '${result.comparablesCount == 1 ? 'property' : 'properties'}',
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
              const SizedBox(height: AppSpacing.lg),
              _ConfidenceRail(
                value: result.confidenceScore,
                color: confidenceColor,
              ),
              const SizedBox(height: AppSpacing.md),
              _StatusPill(flag: result.flag),
            ],
          ),
        )
        .animate(delay: 80.ms)
        .fadeIn(duration: 560.ms)
        .slideY(begin: 0.08, end: 0, curve: Curves.easeOutCubic);
  }
}

class _AnimatedPrice extends StatelessWidget {
  const _AnimatedPrice({required this.value});

  final int value;

  @override
  Widget build(BuildContext context) {
    return TweenAnimationBuilder<double>(
      duration: 760.ms,
      curve: Curves.easeOutCubic,
      tween: Tween(begin: 0, end: value.toDouble()),
      builder: (context, animatedValue, _) {
        return FittedBox(
          fit: BoxFit.scaleDown,
          child: Text(
            'EGP ${_formatNumber(animatedValue.round())}',
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.displayMedium?.copyWith(
              color: AppColors.textPrimary,
              fontSize: 42,
              fontWeight: FontWeight.w800,
              letterSpacing: -2,
              shadows: [
                Shadow(
                  color: AppColors.accent.withValues(alpha: 0.44),
                  blurRadius: 22,
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}

class _ConfidenceRail extends StatelessWidget {
  const _ConfidenceRail({required this.value, required this.color});

  final double value;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        return Container(
          height: 7,
          width: double.infinity,
          decoration: BoxDecoration(
            color: AppColors.backgroundPrimary.withValues(alpha: 0.56),
            borderRadius: BorderRadius.circular(AppRadius.pill),
          ),
          clipBehavior: Clip.antiAlias,
          child: TweenAnimationBuilder<double>(
            duration: 820.ms,
            curve: Curves.easeOutCubic,
            tween: Tween(begin: 0, end: value.clamp(0, 1)),
            builder: (context, animatedValue, _) {
              return Align(
                alignment: Alignment.centerLeft,
                child: Container(
                  width: constraints.maxWidth * animatedValue,
                  decoration: BoxDecoration(
                    gradient: LinearGradient(colors: [AppColors.accent, color]),
                    borderRadius: BorderRadius.circular(AppRadius.pill),
                    boxShadow: [
                      BoxShadow(
                        color: color.withValues(alpha: 0.54),
                        blurRadius: 10,
                      ),
                    ],
                  ),
                ),
              );
            },
          ),
        );
      },
    );
  }
}

class _StatusPill extends StatelessWidget {
  const _StatusPill({required this.flag});

  final String flag;

  @override
  Widget build(BuildContext context) {
    final label = _flagLabel(flag);
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        const Icon(Icons.shield_outlined, color: AppColors.textMuted, size: 16),
        const SizedBox(width: 6),
        Flexible(
          child: Text(
            label,
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.labelMedium?.copyWith(
              color: AppColors.textMuted,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ],
    );
  }
}

class _FairValueRange extends StatelessWidget {
  const _FairValueRange({required this.result});

  final ValuationResponse result;

  @override
  Widget build(BuildContext context) {
    return _GlassPanel(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const _SectionHeader(
                eyebrow: 'VALUATION SPECTRUM',
                title: 'Fair Value Range',
                icon: Icons.linear_scale_rounded,
              ),
              const SizedBox(height: AppSpacing.xl),
              LayoutBuilder(
                builder: (context, constraints) {
                  return SizedBox(
                    height: 44,
                    child: Stack(
                      alignment: Alignment.center,
                      children: [
                        Container(
                          height: 8,
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [
                                AppColors.secondaryAccent.withValues(
                                  alpha: 0.82,
                                ),
                                AppColors.accent,
                                const Color(0xFFFFB86B),
                              ],
                            ),
                            borderRadius: BorderRadius.circular(AppRadius.pill),
                          ),
                        ),
                        Positioned(
                          left: constraints.maxWidth / 2 - 11,
                          child: Container(
                            width: 22,
                            height: 22,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: AppColors.accent,
                              border: Border.all(
                                color: AppColors.textPrimary,
                                width: 2,
                              ),
                              boxShadow: [
                                BoxShadow(
                                  color: AppColors.accent.withValues(
                                    alpha: 0.7,
                                  ),
                                  blurRadius: 16,
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: _RangeValue(
                      label: 'LOW RANGE',
                      value: result.rangeLowEgp,
                    ),
                  ),
                  Expanded(
                    child: _RangeValue(
                      label: 'EXPECTED',
                      value: result.fairPriceEgp,
                      alignment: CrossAxisAlignment.center,
                      valueColor: AppColors.accent,
                    ),
                  ),
                  Expanded(
                    child: _RangeValue(
                      label: 'HIGH RANGE',
                      value: result.rangeHighEgp,
                      alignment: CrossAxisAlignment.end,
                    ),
                  ),
                ],
              ),
            ],
          ),
        )
        .animate(delay: 150.ms)
        .fadeIn(duration: 500.ms)
        .slideY(begin: 0.06, end: 0);
  }
}

class _RangeValue extends StatelessWidget {
  const _RangeValue({
    required this.label,
    required this.value,
    this.alignment = CrossAxisAlignment.start,
    this.valueColor = AppColors.textPrimary,
  });

  final String label;
  final int value;
  final CrossAxisAlignment alignment;
  final Color valueColor;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: alignment,
      children: [
        Text(
          label,
          style: Theme.of(context).textTheme.labelMedium?.copyWith(
            color: AppColors.textMuted,
            fontSize: 9,
            fontWeight: FontWeight.w700,
            letterSpacing: 1,
          ),
        ),
        const SizedBox(height: AppSpacing.xs),
        Text(
          _formatCompactEgp(value),
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
            color: valueColor,
            fontWeight: FontWeight.w800,
          ),
        ),
      ],
    );
  }
}

class _WhyValueSection extends StatelessWidget {
  const _WhyValueSection({required this.drivers});

  final List<ValuationDriver> drivers;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const _SectionHeader(
          eyebrow: 'EXPLAINABILITY',
          title: 'Why This Value?',
          icon: Icons.insights_outlined,
        ),
        const SizedBox(height: AppSpacing.md),
        SizedBox(
          height: 132,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            physics: const BouncingScrollPhysics(),
            itemCount: drivers.length,
            separatorBuilder: (_, _) => const SizedBox(width: AppSpacing.sm),
            itemBuilder: (context, index) {
              return _DriverCard(driver: drivers[index])
                  .animate(delay: (70 * index).ms)
                  .fadeIn(duration: 420.ms)
                  .slideX(begin: 0.1, end: 0);
            },
          ),
        ),
      ],
    );
  }
}

class _DriverCard extends StatelessWidget {
  const _DriverCard({required this.driver});

  final ValuationDriver driver;

  @override
  Widget build(BuildContext context) {
    final isImpact = driver.kind == ValuationDriverKind.priceImpact;
    final isNegative = (driver.value ?? 0) < 0;
    final accent = isNegative ? const Color(0xFFFF8C8C) : AppColors.accent;

    return Container(
      width: 148,
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            accent.withValues(alpha: 0.14),
            AppColors.surface.withValues(alpha: 0.78),
          ],
        ),
        borderRadius: BorderRadius.circular(AppRadius.lg),
        border: Border.all(color: accent.withValues(alpha: 0.28)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Icon(_driverIcon(driver.label), color: accent, size: 21),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                driver.label,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: AppSpacing.xs),
              Row(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text(
                    _driverValue(driver),
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      color: accent,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                  const SizedBox(width: AppSpacing.xs),
                  Expanded(
                    child: Text(
                      isImpact ? 'PRICE IMPACT' : 'EVIDENCE SCORE',
                      style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: AppColors.textMuted,
                        fontSize: 8,
                        fontWeight: FontWeight.w700,
                        height: 1.15,
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _AiSummaryCard extends StatelessWidget {
  const _AiSummaryCard({required this.summary, this.confidenceReason});

  final String summary;
  final String? confidenceReason;

  @override
  Widget build(BuildContext context) {
    return _GlassPanel(
          borderColor: AppColors.accent.withValues(alpha: 0.32),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const _SectionHeader(
                eyebrow: 'TRUTH-LAYER EXPLANATION',
                title: 'AI Summary',
                icon: Icons.auto_awesome_rounded,
              ),
              const SizedBox(height: AppSpacing.md),
              Text(
                summary,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: AppColors.textSecondary,
                  height: 1.58,
                ),
              ),
              if (confidenceReason != null && confidenceReason!.isNotEmpty) ...[
                const SizedBox(height: AppSpacing.md),
                Container(
                  padding: const EdgeInsets.all(AppSpacing.sm),
                  decoration: BoxDecoration(
                    color: AppColors.secondaryAccent.withValues(alpha: 0.07),
                    borderRadius: BorderRadius.circular(AppRadius.md),
                  ),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(
                        Icons.verified_user_outlined,
                        color: AppColors.secondaryAccent,
                        size: 17,
                      ),
                      const SizedBox(width: AppSpacing.sm),
                      Expanded(
                        child: Text(
                          confidenceReason!,
                          style: Theme.of(context).textTheme.labelMedium
                              ?.copyWith(
                                color: AppColors.textSecondary,
                                height: 1.4,
                              ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ],
          ),
        )
        .animate(delay: 90.ms)
        .fadeIn(duration: 480.ms)
        .slideY(begin: 0.06, end: 0);
  }
}

class _EvidenceSection extends StatelessWidget {
  const _EvidenceSection({required this.evidence});

  final ValuationEvidence evidence;

  @override
  Widget build(BuildContext context) {
    final items = [
      _EvidenceItem(
        label: 'Comparable Count',
        value: evidence.comparablesCount.toString(),
        icon: Icons.hub_outlined,
      ),
      if (evidence.resolvedArea != null)
        _EvidenceItem(
          label: 'Resolved Area',
          value: evidence.resolvedArea!,
          icon: Icons.location_on_outlined,
        ),
      if (evidence.district != null &&
          evidence.district != evidence.resolvedArea)
        _EvidenceItem(
          label: 'District',
          value: evidence.district!,
          icon: Icons.grid_view_outlined,
        ),
      if (evidence.governorate != null)
        _EvidenceItem(
          label: 'Governorate',
          value: evidence.governorate!,
          icon: Icons.location_city_outlined,
        ),
      if (evidence.radiusM != null)
        _EvidenceItem(
          label: 'Radius',
          value: _formatDistance(evidence.radiusM),
          icon: Icons.radar_outlined,
        ),
      if (evidence.marketTier != null)
        _EvidenceItem(
          label: 'Market Tier',
          value: evidence.marketTier!,
          icon: Icons.layers_outlined,
        ),
      _EvidenceItem(
        label: 'Confidence Tier',
        value: evidence.confidenceTier,
        icon: Icons.verified_outlined,
      ),
      if (evidence.resolutionPrecision != null)
        _EvidenceItem(
          label: 'Resolution',
          value: evidence.resolutionPrecision!,
          icon: Icons.my_location_outlined,
        ),
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const _SectionHeader(
          eyebrow: 'SUPPORTING SIGNALS',
          title: 'Evidence',
          icon: Icons.shield_outlined,
        ),
        const SizedBox(height: AppSpacing.md),
        GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: items.length,
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            childAspectRatio: 1.46,
            crossAxisSpacing: AppSpacing.sm,
            mainAxisSpacing: AppSpacing.sm,
          ),
          itemBuilder: (context, index) {
            return _EvidenceTile(item: items[index])
                .animate(delay: (45 * index).ms)
                .fadeIn(duration: 390.ms)
                .slideY(begin: 0.08, end: 0);
          },
        ),
      ],
    );
  }
}

class _EvidenceTile extends StatelessWidget {
  const _EvidenceTile({required this.item});

  final _EvidenceItem item;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: _panelDecoration(),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Icon(item.icon, color: AppColors.accent, size: 20),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                item.label.toUpperCase(),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                  color: AppColors.textMuted,
                  fontSize: 8,
                  fontWeight: FontWeight.w700,
                  letterSpacing: 0.9,
                ),
              ),
              const SizedBox(height: AppSpacing.xs),
              Text(
                item.value,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.w700,
                  height: 1.15,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _TopComparablesSection extends StatelessWidget {
  const _TopComparablesSection({
    required this.comparables,
    required this.onViewAll,
  });

  final List<ValuationComparable> comparables;
  final VoidCallback onViewAll;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const _SectionHeader(
          eyebrow: 'DETERMINISTIC MATCHES',
          title: 'Top Comparables',
          icon: Icons.apartment_outlined,
        ),
        const SizedBox(height: AppSpacing.md),
        ...List.generate(comparables.length, (index) {
          return Padding(
            padding: EdgeInsets.only(
              bottom: index == comparables.length - 1
                  ? AppSpacing.md
                  : AppSpacing.sm,
            ),
            child:
                _ComparableCard(
                      comparable: comparables[index],
                      rank: comparables[index].evidenceRank ?? index + 1,
                    )
                    .animate(delay: (70 * index).ms)
                    .fadeIn(duration: 430.ms)
                    .slideY(begin: 0.08, end: 0),
          );
        }),
        SizedBox(
          width: double.infinity,
          child: OutlinedButton.icon(
            onPressed: onViewAll,
            icon: const Icon(Icons.travel_explore_outlined, size: 19),
            label: const Text('View All Comparables'),
          ),
        ),
      ],
    );
  }
}

class _ComparableCard extends StatelessWidget {
  const _ComparableCard({required this.comparable, required this.rank});

  final ValuationComparable comparable;
  final int rank;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: _panelDecoration(
        borderColor: AppColors.accent.withValues(alpha: 0.17),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 32,
                height: 32,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: AppColors.accent.withValues(alpha: 0.12),
                  border: Border.all(
                    color: AppColors.accent.withValues(alpha: 0.28),
                  ),
                ),
                alignment: Alignment.center,
                child: Text(
                  '#$rank',
                  style: Theme.of(context).textTheme.labelMedium?.copyWith(
                    color: AppColors.accent,
                    fontWeight: FontWeight.w800,
                  ),
                ),
              ),
              const SizedBox(width: AppSpacing.sm),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'EGP ${_formatNumber(comparable.priceEgp)}',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        color: AppColors.textPrimary,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      comparable.areaName ?? comparable.listingId,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: AppColors.textMuted,
                      ),
                    ),
                  ],
                ),
              ),
              if (comparable.similarityScore != null)
                _MetricBadge(
                  label:
                      '${(comparable.similarityScore! * 100).round()}% match',
                ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),
          Wrap(
            spacing: AppSpacing.sm,
            runSpacing: AppSpacing.sm,
            children: [
              if (comparable.distanceM != null)
                _ComparableAttribute(
                  icon: Icons.near_me_outlined,
                  value: _formatDistance(comparable.distanceM),
                ),
              if (comparable.sizeSqm != null)
                _ComparableAttribute(
                  icon: Icons.square_foot_rounded,
                  value: '${_formatDecimal(comparable.sizeSqm!)} sqm',
                ),
              if (comparable.propertyType != null)
                _ComparableAttribute(
                  icon: Icons.home_work_outlined,
                  value: comparable.propertyType!,
                ),
            ],
          ),
        ],
      ),
    );
  }
}

class _ComparableAttribute extends StatelessWidget {
  const _ComparableAttribute({required this.icon, required this.value});

  final IconData icon;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 7),
      decoration: BoxDecoration(
        color: AppColors.backgroundPrimary.withValues(alpha: 0.42),
        borderRadius: BorderRadius.circular(AppRadius.pill),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: AppColors.textMuted, size: 14),
          const SizedBox(width: 5),
          Text(
            value,
            style: Theme.of(context).textTheme.labelMedium?.copyWith(
              color: AppColors.textSecondary,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }
}

class _MetricBadge extends StatelessWidget {
  const _MetricBadge({required this.label});

  final String label;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 5),
      decoration: BoxDecoration(
        color: AppColors.secondaryAccent.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(AppRadius.pill),
        border: Border.all(
          color: AppColors.secondaryAccent.withValues(alpha: 0.24),
        ),
      ),
      child: Text(
        label,
        style: Theme.of(context).textTheme.labelMedium?.copyWith(
          color: AppColors.secondaryAccent,
          fontSize: 10,
          fontWeight: FontWeight.w700,
        ),
      ),
    );
  }
}

class _MarketContextSection extends StatelessWidget {
  const _MarketContextSection({required this.signals});

  final List<ValuationMarketSignal> signals;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const _SectionHeader(
          eyebrow: 'WHEN RETURNED BY THE ENGINE',
          title: 'Market Context',
          icon: Icons.query_stats_outlined,
        ),
        const SizedBox(height: AppSpacing.md),
        _GlassPanel(
          child: Column(
            children: List.generate(signals.length, (index) {
              final signal = signals[index];
              return Column(
                children: [
                  Row(
                    children: [
                      Container(
                        width: 9,
                        height: 9,
                        decoration: BoxDecoration(
                          color: AppColors.secondaryAccent,
                          shape: BoxShape.circle,
                          boxShadow: [
                            BoxShadow(
                              color: AppColors.secondaryAccent.withValues(
                                alpha: 0.56,
                              ),
                              blurRadius: 8,
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: AppSpacing.md),
                      Expanded(
                        child: Text(
                          signal.label,
                          style: Theme.of(context).textTheme.bodyMedium
                              ?.copyWith(
                                color: AppColors.textSecondary,
                                fontWeight: FontWeight.w600,
                              ),
                        ),
                      ),
                      Text(
                        signal.value,
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: AppColors.secondaryAccent,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                    ],
                  ),
                  if (index != signals.length - 1)
                    Padding(
                      padding: const EdgeInsets.symmetric(
                        vertical: AppSpacing.md,
                      ),
                      child: Divider(
                        height: 1,
                        color: AppColors.textPrimary.withValues(alpha: 0.06),
                      ),
                    ),
                ],
              );
            }),
          ),
        ),
      ],
    );
  }
}

class _MiniMapSection extends StatelessWidget {
  const _MiniMapSection({required this.result});

  final ValuationResponse result;

  @override
  Widget build(BuildContext context) {
    final location = result.location!;
    final subject = LatLng(location.latitude!, location.longitude!);
    final comparables = result.topComparables.where((item) {
      return item.hasLocation;
    }).toList();
    final markers = <Marker>{
      Marker(
        markerId: const MarkerId('subject-property'),
        position: subject,
        infoWindow: const InfoWindow(title: 'Subject Property'),
        icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueCyan),
      ),
      ...comparables.map((item) {
        return Marker(
          markerId: MarkerId(item.listingId),
          position: LatLng(item.latitude!, item.longitude!),
          infoWindow: InfoWindow(
            title: 'Comparable #${item.evidenceRank ?? '-'}',
            snippet: 'EGP ${_formatNumber(item.priceEgp)}',
          ),
          icon: BitmapDescriptor.defaultMarkerWithHue(
            BitmapDescriptor.hueGreen,
          ),
        );
      }),
    };
    final radius = result.evidence.radiusM;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const _SectionHeader(
          eyebrow: 'LOCATION CONTEXT',
          title: 'Evidence Map',
          icon: Icons.map_outlined,
        ),
        const SizedBox(height: AppSpacing.md),
        Container(
          height: 152,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(AppRadius.lg),
            border: Border.all(
              color: AppColors.textPrimary.withValues(alpha: 0.1),
            ),
          ),
          clipBehavior: Clip.antiAlias,
          child: Stack(
            children: [
              GoogleMap(
                initialCameraPosition: CameraPosition(
                  target: subject,
                  zoom: 13.2,
                ),
                liteModeEnabled: true,
                mapToolbarEnabled: false,
                myLocationButtonEnabled: false,
                zoomControlsEnabled: false,
                rotateGesturesEnabled: false,
                scrollGesturesEnabled: false,
                zoomGesturesEnabled: false,
                markers: markers,
                circles: radius == null
                    ? const {}
                    : {
                        Circle(
                          circleId: const CircleId('retrieval-radius'),
                          center: subject,
                          radius: radius,
                          fillColor: AppColors.accent.withValues(alpha: 0.08),
                          strokeColor: AppColors.accent.withValues(alpha: 0.38),
                          strokeWidth: 1,
                        ),
                      },
              ),
              Positioned(
                top: AppSpacing.sm,
                left: AppSpacing.sm,
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: AppSpacing.sm,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: AppColors.backgroundSecondary.withValues(
                      alpha: 0.92,
                    ),
                    borderRadius: BorderRadius.circular(AppRadius.pill),
                    border: Border.all(
                      color: AppColors.accent.withValues(alpha: 0.28),
                    ),
                  ),
                  child: Text(
                    '${comparables.length} mapped comparables',
                    style: Theme.of(context).textTheme.labelMedium?.copyWith(
                      color: AppColors.accent,
                      fontSize: 10,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _StickyActionBar extends StatelessWidget {
  const _StickyActionBar({
    required this.onExplainMore,
    required this.onViewComparables,
    required this.onAskCopilot,
    required this.onSave,
  });

  final VoidCallback onExplainMore;
  final VoidCallback onViewComparables;
  final VoidCallback onAskCopilot;
  final VoidCallback onSave;

  @override
  Widget build(BuildContext context) {
    return SafeArea(
          minimum: const EdgeInsets.fromLTRB(
            AppSpacing.md,
            0,
            AppSpacing.md,
            AppSpacing.sm,
          ),
          child: Container(
            padding: const EdgeInsets.all(AppSpacing.sm),
            decoration: BoxDecoration(
              color: AppColors.backgroundSecondary.withValues(alpha: 0.96),
              borderRadius: BorderRadius.circular(AppRadius.xl),
              border: Border.all(
                color: AppColors.accent.withValues(alpha: 0.22),
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: 0.34),
                  blurRadius: 24,
                  offset: const Offset(0, 10),
                ),
                BoxShadow(
                  color: AppColors.accent.withValues(alpha: 0.08),
                  blurRadius: 20,
                ),
              ],
            ),
            child: Row(
              children: [
                Expanded(
                  child: _StickyAction(
                    label: 'Explain',
                    icon: Icons.insights_outlined,
                    onTap: onExplainMore,
                  ),
                ),
                Expanded(
                  child: _StickyAction(
                    label: 'Comps',
                    icon: Icons.travel_explore_outlined,
                    onTap: onViewComparables,
                  ),
                ),
                Expanded(
                  child: _StickyAction(
                    label: 'Copilot',
                    icon: Icons.auto_awesome_outlined,
                    isPrimary: true,
                    onTap: onAskCopilot,
                  ),
                ),
                Expanded(
                  child: _StickyAction(
                    label: 'Save',
                    icon: Icons.bookmark_outline_rounded,
                    onTap: onSave,
                  ),
                ),
              ],
            ),
          ),
        )
        .animate(delay: 360.ms)
        .fadeIn(duration: 460.ms)
        .slideY(begin: 0.2, end: 0);
  }
}

class _StickyAction extends StatelessWidget {
  const _StickyAction({
    required this.label,
    required this.icon,
    required this.onTap,
    this.isPrimary = false,
  });

  final String label;
  final IconData icon;
  final VoidCallback onTap;
  final bool isPrimary;

  @override
  Widget build(BuildContext context) {
    final color = isPrimary ? AppColors.backgroundPrimary : AppColors.textMuted;
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(AppRadius.lg),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: AppSpacing.sm),
        decoration: BoxDecoration(
          color: isPrimary ? AppColors.accent : Colors.transparent,
          borderRadius: BorderRadius.circular(AppRadius.lg),
          boxShadow: isPrimary
              ? [
                  BoxShadow(
                    color: AppColors.accent.withValues(alpha: 0.24),
                    blurRadius: 14,
                  ),
                ]
              : null,
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, color: color, size: 20),
            const SizedBox(height: AppSpacing.xs),
            Text(
              label,
              maxLines: 1,
              style: Theme.of(context).textTheme.labelMedium?.copyWith(
                color: color,
                fontSize: 10,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  const _SectionHeader({
    required this.eyebrow,
    required this.title,
    required this.icon,
  });

  final String eyebrow;
  final String title;
  final IconData icon;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          width: 38,
          height: 38,
          decoration: BoxDecoration(
            color: AppColors.accent.withValues(alpha: 0.1),
            borderRadius: BorderRadius.circular(AppRadius.md),
            border: Border.all(color: AppColors.accent.withValues(alpha: 0.2)),
          ),
          child: Icon(icon, color: AppColors.accent, size: 20),
        ),
        const SizedBox(width: AppSpacing.sm),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                eyebrow,
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                  color: AppColors.accent,
                  fontSize: 9,
                  fontWeight: FontWeight.w700,
                  letterSpacing: 1.2,
                ),
              ),
              const SizedBox(height: 2),
              Text(
                title,
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _GlassPanel extends StatelessWidget {
  const _GlassPanel({required this.child, this.borderColor});

  final Widget child;
  final Color? borderColor;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: _panelDecoration(borderColor: borderColor),
      child: child,
    );
  }
}

class _RoundIconButton extends StatelessWidget {
  const _RoundIconButton({required this.icon, required this.onTap});

  final IconData icon;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(AppRadius.pill),
      child: Container(
        width: 42,
        height: 42,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: AppColors.surface.withValues(alpha: 0.74),
          border: Border.all(
            color: AppColors.textPrimary.withValues(alpha: 0.08),
          ),
        ),
        child: Icon(icon, color: AppColors.textSecondary, size: 18),
      ),
    );
  }
}

class _EmptyResult extends StatelessWidget {
  const _EmptyResult({required this.onBack});

  final VoidCallback onBack;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.lg),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(
              Icons.analytics_outlined,
              color: AppColors.accent,
              size: 46,
            ),
            const SizedBox(height: AppSpacing.md),
            Text(
              'No valuation result',
              style: Theme.of(
                context,
              ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: AppSpacing.sm),
            Text(
              'Start a new valuation to analyze a property.',
              textAlign: TextAlign.center,
              style: Theme.of(
                context,
              ).textTheme.bodyMedium?.copyWith(color: AppColors.textMuted),
            ),
            const SizedBox(height: AppSpacing.lg),
            FilledButton(onPressed: onBack, child: const Text('Back To Home')),
          ],
        ),
      ),
    );
  }
}

class _AmbientGlow extends StatelessWidget {
  const _AmbientGlow({
    required this.color,
    required this.size,
    required this.opacity,
  });

  final Color color;
  final double size;
  final double opacity;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        gradient: RadialGradient(
          colors: [
            color.withValues(alpha: opacity),
            Colors.transparent,
          ],
        ),
      ),
    );
  }
}

class _EvidenceItem {
  const _EvidenceItem({
    required this.label,
    required this.value,
    required this.icon,
  });

  final String label;
  final String value;
  final IconData icon;
}

BoxDecoration _panelDecoration({Color? borderColor}) {
  return BoxDecoration(
    color: AppColors.surface.withValues(alpha: 0.7),
    borderRadius: BorderRadius.circular(AppRadius.lg),
    border: Border.all(
      color: borderColor ?? AppColors.textPrimary.withValues(alpha: 0.07),
    ),
  );
}

Color _confidenceColor(double score) {
  if (score >= 0.75) {
    return AppColors.secondaryAccent;
  }
  if (score >= 0.5) {
    return AppColors.accent;
  }
  return const Color(0xFFFFB86B);
}

IconData _driverIcon(String label) {
  final normalized = label.toLowerCase();
  if (normalized.contains('location') || normalized.contains('proximity')) {
    return Icons.location_on_outlined;
  }
  if (normalized.contains('amenit')) {
    return Icons.spa_outlined;
  }
  if (normalized.contains('area') || normalized.contains('size')) {
    return Icons.square_foot_rounded;
  }
  if (normalized.contains('tier') || normalized.contains('market')) {
    return Icons.layers_outlined;
  }
  if (normalized.contains('recency')) {
    return Icons.schedule_outlined;
  }
  return Icons.auto_graph_rounded;
}

String _driverValue(ValuationDriver driver) {
  final value = driver.value;
  if (value == null) {
    return driver.strength ?? driver.direction ?? '-';
  }
  if (driver.kind == ValuationDriverKind.priceImpact) {
    final prefix = value > 0 ? '+' : '';
    return '$prefix${_formatDecimal(value)}%';
  }
  return '${(value * 100).round()}%';
}

String _flagLabel(String flag) {
  switch (flag) {
    case 'INSUFFICIENT_DATA':
      return 'Comparable depth is insufficient for a substantive valuation';
    case 'TOO_HIGH':
      return 'Target price is above the fair-value range';
    case 'TOO_LOW':
      return 'Target price is below the fair-value range';
    case 'OK':
      return 'Target price sits inside the fair-value range';
    case 'NO_TARGET':
      return 'Governed fair-value estimate';
    default:
      return flag.replaceAll('_', ' ');
  }
}

String _formatCompactEgp(int value) {
  if (value >= 1000000) {
    return 'EGP ${_formatDecimal(value / 1000000)}M';
  }
  if (value >= 1000) {
    return 'EGP ${_formatDecimal(value / 1000)}K';
  }
  return 'EGP $value';
}

String _formatDistance(double? value) {
  if (value == null) {
    return '-';
  }
  if (value < 1000) {
    return '${value.round()}m';
  }
  return '${_formatDecimal(value / 1000)}km';
}

String _formatDecimal(double value) {
  if (value == value.roundToDouble()) {
    return value.toStringAsFixed(0);
  }
  return value.toStringAsFixed(1);
}

String _formatNumber(int value) {
  return value.toString().replaceAllMapped(
    RegExp(r'(?=(\d{3})+(?!\d))'),
    (_) => ',',
  );
}
