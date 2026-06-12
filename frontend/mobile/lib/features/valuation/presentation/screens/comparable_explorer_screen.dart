import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import '../../../../app/router/route_names.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_radius.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../domain/models/valuation_response.dart';

enum _ExplorerSort { similarity, distance, price }

enum _ExplorerView { list, map }

class ComparableExplorerScreen extends StatefulWidget {
  const ComparableExplorerScreen({super.key, this.response});

  final ValuationResponse? response;

  @override
  State<ComparableExplorerScreen> createState() =>
      _ComparableExplorerScreenState();
}

class _ComparableExplorerScreenState extends State<ComparableExplorerScreen> {
  _ExplorerSort _sort = _ExplorerSort.similarity;
  _ExplorerView _view = _ExplorerView.list;

  @override
  Widget build(BuildContext context) {
    final result = widget.response;
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
          child: result == null
              ? _EmptyExplorer(onBack: () => context.goNamed(RouteNames.home))
              : _ExplorerContent(
                  result: result,
                  comparables: _sortedComparables(result.topComparables),
                  sort: _sort,
                  view: _view,
                  onBack: _goBack,
                  onSortChanged: (value) {
                    setState(() {
                      _sort = value;
                    });
                  },
                  onViewChanged: (value) {
                    setState(() {
                      _view = value;
                    });
                  },
                  onComparableTap: _showComparableDetails,
                ),
        ),
      ),
    );
  }

  List<ValuationComparable> _sortedComparables(
    List<ValuationComparable> comparables,
  ) {
    final sorted = [...comparables];
    sorted.sort((left, right) {
      final comparison = switch (_sort) {
        _ExplorerSort.similarity => _compareNullableDescending(
          left.similarityScore,
          right.similarityScore,
        ),
        _ExplorerSort.distance => _compareNullableAscending(
          left.distanceM,
          right.distanceM,
        ),
        _ExplorerSort.price => right.priceEgp.compareTo(left.priceEgp),
      };
      if (comparison != 0) {
        return comparison;
      }
      return (left.evidenceRank ?? 999).compareTo(right.evidenceRank ?? 999);
    });
    return sorted;
  }

  void _goBack() {
    if (context.canPop()) {
      context.pop();
    } else {
      context.goNamed(RouteNames.home);
    }
  }

  void _showComparableDetails(ValuationComparable comparable) {
    showModalBottomSheet<void>(
      context: context,
      backgroundColor: Colors.transparent,
      isScrollControlled: true,
      builder: (context) {
        return _ComparableDetailsSheet(comparable: comparable);
      },
    );
  }
}

class _ExplorerContent extends StatelessWidget {
  const _ExplorerContent({
    required this.result,
    required this.comparables,
    required this.sort,
    required this.view,
    required this.onBack,
    required this.onSortChanged,
    required this.onViewChanged,
    required this.onComparableTap,
  });

  final ValuationResponse result;
  final List<ValuationComparable> comparables;
  final _ExplorerSort sort;
  final _ExplorerView view;
  final VoidCallback onBack;
  final ValueChanged<_ExplorerSort> onSortChanged;
  final ValueChanged<_ExplorerView> onViewChanged;
  final ValueChanged<ValuationComparable> onComparableTap;

  @override
  Widget build(BuildContext context) {
    return CustomScrollView(
      physics: const BouncingScrollPhysics(),
      slivers: [
        SliverPadding(
          padding: const EdgeInsets.fromLTRB(
            AppSpacing.lg,
            AppSpacing.md,
            AppSpacing.lg,
            AppSpacing.xxl,
          ),
          sliver: SliverList(
            delegate: SliverChildListDelegate([
              _ExplorerHeader(onBack: onBack),
              const SizedBox(height: AppSpacing.lg),
              _ExplorerHero(result: result),
              const SizedBox(height: AppSpacing.lg),
              _ExplorerControls(
                sort: sort,
                view: view,
                onSortChanged: onSortChanged,
                onViewChanged: onViewChanged,
              ),
              const SizedBox(height: AppSpacing.lg),
              _WhyComparablesPanel(result: result),
              const SizedBox(height: AppSpacing.xl),
              _SectionTitle(
                eyebrow: view == _ExplorerView.list
                    ? 'RETURNED VALUATION EVIDENCE'
                    : 'LOCATION CONTEXT',
                title: view == _ExplorerView.list
                    ? 'Comparable Properties'
                    : 'Evidence Map',
              ),
              const SizedBox(height: AppSpacing.md),
              if (comparables.isEmpty)
                const _NoComparables()
              else if (view == _ExplorerView.list)
                ...List.generate(comparables.length, (index) {
                  final comparable = comparables[index];
                  return Padding(
                    padding: EdgeInsets.only(
                      bottom: index == comparables.length - 1
                          ? 0
                          : AppSpacing.sm,
                    ),
                    child:
                        _ExplorerComparableCard(
                              comparable: comparable,
                              rank: comparable.evidenceRank ?? index + 1,
                              onTap: () => onComparableTap(comparable),
                            )
                            .animate(delay: (65 * index).ms)
                            .fadeIn(duration: 430.ms)
                            .slideY(begin: 0.08, end: 0),
                  );
                })
              else
                _ExplorerMap(result: result, comparables: comparables)
                    .animate()
                    .fadeIn(duration: 380.ms)
                    .slideY(begin: 0.05, end: 0),
            ]),
          ),
        ),
      ],
    );
  }
}

class _ExplorerHeader extends StatelessWidget {
  const _ExplorerHeader({required this.onBack});

  final VoidCallback onBack;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        _RoundIconButton(icon: Icons.arrow_back_ios_new_rounded, onTap: onBack),
        const SizedBox(width: AppSpacing.md),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Comparable Explorer',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.w800,
                  letterSpacing: -0.5,
                ),
              ),
              const SizedBox(height: 2),
              Text(
                'Evidence Behind Your Valuation',
                style: Theme.of(
                  context,
                ).textTheme.labelMedium?.copyWith(color: AppColors.textMuted),
              ),
            ],
          ),
        ),
      ],
    ).animate().fadeIn(duration: 420.ms).slideY(begin: -0.08, end: 0);
  }
}

class _ExplorerHero extends StatelessWidget {
  const _ExplorerHero({required this.result});

  final ValuationResponse result;

  @override
  Widget build(BuildContext context) {
    return Container(
          padding: const EdgeInsets.all(AppSpacing.md),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [
                AppColors.accent.withValues(alpha: 0.16),
                AppColors.surface.withValues(alpha: 0.78),
              ],
            ),
            borderRadius: BorderRadius.circular(AppRadius.lg),
            border: Border.all(color: AppColors.accent.withValues(alpha: 0.28)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    width: 42,
                    height: 42,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: AppColors.accent.withValues(alpha: 0.12),
                    ),
                    child: const Icon(
                      Icons.travel_explore_outlined,
                      color: AppColors.accent,
                      size: 22,
                    ),
                  ),
                  const SizedBox(width: AppSpacing.sm),
                  Expanded(
                    child: Text(
                      'Deterministic comparable evidence',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        color: AppColors.textPrimary,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: AppSpacing.md),
              Row(
                children: [
                  Expanded(
                    child: _HeaderMetric(
                      label: 'TOTAL COMPARABLES',
                      value: '${result.comparablesCount}',
                    ),
                  ),
                  const SizedBox(width: AppSpacing.sm),
                  Expanded(
                    child: _HeaderMetric(
                      label: 'RADIUS',
                      value: result.evidence.radiusM == null
                          ? '-'
                          : _formatDistance(result.evidence.radiusM!),
                    ),
                  ),
                  const SizedBox(width: AppSpacing.sm),
                  Expanded(
                    child: _HeaderMetric(
                      label: 'CONFIDENCE',
                      value: '${(result.confidenceScore * 100).round()}%',
                      caption: result.confidenceLabel,
                    ),
                  ),
                ],
              ),
            ],
          ),
        )
        .animate(delay: 70.ms)
        .fadeIn(duration: 460.ms)
        .slideY(begin: 0.08, end: 0);
  }
}

class _HeaderMetric extends StatelessWidget {
  const _HeaderMetric({required this.label, required this.value, this.caption});

  final String label;
  final String value;
  final String? caption;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.sm,
        vertical: 10,
      ),
      decoration: BoxDecoration(
        color: AppColors.backgroundPrimary.withValues(alpha: 0.36),
        borderRadius: BorderRadius.circular(AppRadius.md),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: Theme.of(context).textTheme.labelMedium?.copyWith(
              color: AppColors.textMuted,
              fontSize: 8,
              fontWeight: FontWeight.w700,
              letterSpacing: 0.6,
            ),
          ),
          const SizedBox(height: 5),
          Text(
            value,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
              color: AppColors.textPrimary,
              fontWeight: FontWeight.w800,
            ),
          ),
          if (caption != null) ...[
            const SizedBox(height: 2),
            Text(
              caption!,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: Theme.of(context).textTheme.labelMedium?.copyWith(
                color: AppColors.secondaryAccent,
                fontSize: 10,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ],
      ),
    );
  }
}

class _ExplorerControls extends StatelessWidget {
  const _ExplorerControls({
    required this.sort,
    required this.view,
    required this.onSortChanged,
    required this.onViewChanged,
  });

  final _ExplorerSort sort;
  final _ExplorerView view;
  final ValueChanged<_ExplorerSort> onSortChanged;
  final ValueChanged<_ExplorerView> onViewChanged;

  @override
  Widget build(BuildContext context) {
    return Container(
          padding: const EdgeInsets.all(AppSpacing.md),
          decoration: _panelDecoration(),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('SORT BY', style: _controlLabelStyle(context)),
              const SizedBox(height: AppSpacing.sm),
              _SortControl(value: sort, onChanged: onSortChanged),
              const SizedBox(height: AppSpacing.md),
              Text('VIEW', style: _controlLabelStyle(context)),
              const SizedBox(height: AppSpacing.sm),
              _ViewToggle(value: view, onChanged: onViewChanged),
            ],
          ),
        )
        .animate(delay: 120.ms)
        .fadeIn(duration: 420.ms)
        .slideY(begin: 0.06, end: 0);
  }
}

class _SortControl extends StatelessWidget {
  const _SortControl({required this.value, required this.onChanged});

  final _ExplorerSort value;
  final ValueChanged<_ExplorerSort> onChanged;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: _SegmentButton(
            label: 'Similarity',
            selected: value == _ExplorerSort.similarity,
            onTap: () => onChanged(_ExplorerSort.similarity),
          ),
        ),
        const SizedBox(width: AppSpacing.xs),
        Expanded(
          child: _SegmentButton(
            label: 'Distance',
            selected: value == _ExplorerSort.distance,
            onTap: () => onChanged(_ExplorerSort.distance),
          ),
        ),
        const SizedBox(width: AppSpacing.xs),
        Expanded(
          child: _SegmentButton(
            label: 'Price',
            selected: value == _ExplorerSort.price,
            onTap: () => onChanged(_ExplorerSort.price),
          ),
        ),
      ],
    );
  }
}

class _ViewToggle extends StatelessWidget {
  const _ViewToggle({required this.value, required this.onChanged});

  final _ExplorerView value;
  final ValueChanged<_ExplorerView> onChanged;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: _SegmentButton(
            label: 'List View',
            icon: Icons.view_agenda_outlined,
            selected: value == _ExplorerView.list,
            onTap: () => onChanged(_ExplorerView.list),
          ),
        ),
        const SizedBox(width: AppSpacing.xs),
        Expanded(
          child: _SegmentButton(
            label: 'Map View',
            icon: Icons.map_outlined,
            selected: value == _ExplorerView.map,
            onTap: () => onChanged(_ExplorerView.map),
          ),
        ),
      ],
    );
  }
}

class _SegmentButton extends StatelessWidget {
  const _SegmentButton({
    required this.label,
    required this.selected,
    required this.onTap,
    this.icon,
  });

  final String label;
  final bool selected;
  final VoidCallback onTap;
  final IconData? icon;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(AppRadius.md),
      child: AnimatedContainer(
        duration: 220.ms,
        curve: Curves.easeOutCubic,
        padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 6),
        decoration: BoxDecoration(
          color: selected
              ? AppColors.accent.withValues(alpha: 0.16)
              : AppColors.backgroundPrimary.withValues(alpha: 0.3),
          borderRadius: BorderRadius.circular(AppRadius.md),
          border: Border.all(
            color: selected
                ? AppColors.accent.withValues(alpha: 0.42)
                : AppColors.textPrimary.withValues(alpha: 0.04),
          ),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (icon != null) ...[
              Icon(
                icon,
                size: 15,
                color: selected ? AppColors.accent : AppColors.textMuted,
              ),
              const SizedBox(width: 5),
            ],
            Flexible(
              child: Text(
                label,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                  color: selected ? AppColors.accent : AppColors.textMuted,
                  fontSize: 11,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _WhyComparablesPanel extends StatelessWidget {
  const _WhyComparablesPanel({required this.result});

  final ValuationResponse result;

  @override
  Widget build(BuildContext context) {
    final comparables = result.topComparables;
    final metrics = <_EvidenceMetric>[
      _EvidenceMetric(
        label: 'Location similarity',
        value: _average(comparables.map((item) => item.geographicSimilarity)),
      ),
      _EvidenceMetric(
        label: 'Area similarity',
        value: _average(comparables.map((item) => item.areaSimilarity)),
      ),
      _EvidenceMetric(
        label: 'Area size similarity',
        value: _average(comparables.map((item) => item.areaSizeSimilarity)),
      ),
      _EvidenceMetric(
        label: 'Property type similarity',
        value: _average(comparables.map((item) => item.propertyTypeSimilarity)),
      ),
      _EvidenceMetric(
        label: 'Amenities similarity',
        value: _average(comparables.map((item) => item.amenitySimilarity)),
      ),
    ].where((item) => item.value != null).toList();
    final signals = result.confidence.factors.entries
        .where((entry) => entry.value >= 0)
        .toList();

    return Container(
      decoration: _panelDecoration(
        borderColor: AppColors.accent.withValues(alpha: 0.18),
      ),
      child: Theme(
        data: Theme.of(context).copyWith(
          dividerColor: Colors.transparent,
          splashColor: AppColors.accent.withValues(alpha: 0.08),
        ),
        child: ExpansionTile(
          tilePadding: const EdgeInsets.symmetric(
            horizontal: AppSpacing.md,
            vertical: AppSpacing.xs,
          ),
          childrenPadding: const EdgeInsets.fromLTRB(
            AppSpacing.md,
            0,
            AppSpacing.md,
            AppSpacing.md,
          ),
          iconColor: AppColors.accent,
          collapsedIconColor: AppColors.textMuted,
          title: Text(
            'Why these comparables?',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
              color: AppColors.textPrimary,
              fontWeight: FontWeight.w800,
            ),
          ),
          subtitle: Text(
            'Inspect returned matching evidence',
            style: Theme.of(
              context,
            ).textTheme.labelMedium?.copyWith(color: AppColors.textMuted),
          ),
          children: [
            if (metrics.isNotEmpty) ...[
              Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'Average returned match signals',
                  style: _controlLabelStyle(context),
                ),
              ),
              const SizedBox(height: AppSpacing.sm),
              ...metrics.map(
                (metric) => Padding(
                  padding: const EdgeInsets.only(bottom: AppSpacing.sm),
                  child: _EvidenceRail(metric: metric),
                ),
              ),
            ],
            if (signals.isNotEmpty) ...[
              if (metrics.isNotEmpty) const SizedBox(height: AppSpacing.sm),
              Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'Backend confidence factors',
                  style: _controlLabelStyle(context),
                ),
              ),
              const SizedBox(height: AppSpacing.sm),
              Wrap(
                spacing: AppSpacing.sm,
                runSpacing: AppSpacing.sm,
                children: signals.map((entry) {
                  return _Attribute(
                    icon: Icons.verified_outlined,
                    label:
                        '${_humanize(entry.key)} ${(entry.value * 100).round()}%',
                  );
                }).toList(),
              ),
            ],
            if (metrics.isEmpty && signals.isEmpty)
              Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'No additional match breakdown was returned by the backend.',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: AppColors.textMuted,
                    height: 1.4,
                  ),
                ),
              ),
          ],
        ),
      ),
    ).animate(delay: 160.ms).fadeIn(duration: 420.ms).slideY(begin: 0.06, end: 0);
  }
}

class _EvidenceMetric {
  const _EvidenceMetric({required this.label, required this.value});

  final String label;
  final double? value;
}

class _EvidenceRail extends StatelessWidget {
  const _EvidenceRail({required this.metric});

  final _EvidenceMetric metric;

  @override
  Widget build(BuildContext context) {
    final value = metric.value!.clamp(0.0, 1.0).toDouble();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Expanded(
              child: Text(
                metric.label,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: AppColors.textSecondary,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
            Text(
              '${(value * 100).round()}%',
              style: Theme.of(context).textTheme.labelLarge?.copyWith(
                color: AppColors.secondaryAccent,
                fontWeight: FontWeight.w800,
              ),
            ),
          ],
        ),
        const SizedBox(height: 6),
        ClipRRect(
          borderRadius: BorderRadius.circular(AppRadius.pill),
          child: LinearProgressIndicator(
            value: value,
            minHeight: 5,
            backgroundColor: AppColors.backgroundPrimary.withValues(alpha: 0.5),
            color: AppColors.secondaryAccent,
          ),
        ),
      ],
    );
  }
}

class _SectionTitle extends StatelessWidget {
  const _SectionTitle({required this.eyebrow, required this.title});

  final String eyebrow;
  final String title;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          eyebrow,
          style: Theme.of(context).textTheme.labelMedium?.copyWith(
            color: AppColors.accent,
            fontSize: 10,
            fontWeight: FontWeight.w700,
            letterSpacing: 1.3,
          ),
        ),
        const SizedBox(height: AppSpacing.xs),
        Text(
          title,
          style: Theme.of(context).textTheme.titleLarge?.copyWith(
            color: AppColors.textPrimary,
            fontWeight: FontWeight.w800,
          ),
        ),
      ],
    );
  }
}

class _ExplorerComparableCard extends StatelessWidget {
  const _ExplorerComparableCard({
    required this.comparable,
    required this.rank,
    required this.onTap,
  });

  final ValuationComparable comparable;
  final int rank;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppRadius.lg),
        child: Container(
          padding: const EdgeInsets.all(AppSpacing.md),
          decoration: _panelDecoration(),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    width: 32,
                    height: 32,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: AppColors.accent.withValues(alpha: 0.12),
                      border: Border.all(
                        color: AppColors.accent.withValues(alpha: 0.28),
                      ),
                    ),
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
                    child: Text(
                      comparable.propertyType ?? 'Comparable property',
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: AppColors.textSecondary,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                  if (comparable.similarityScore != null)
                    _ScoreBadge(score: comparable.similarityScore!),
                ],
              ),
              const SizedBox(height: AppSpacing.md),
              Text(
                'EGP ${_formatNumber(comparable.priceEgp)}',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.w800,
                ),
              ),
              const SizedBox(height: AppSpacing.xs),
              Row(
                children: [
                  const Icon(
                    Icons.location_on_outlined,
                    color: AppColors.textMuted,
                    size: 15,
                  ),
                  const SizedBox(width: 4),
                  Expanded(
                    child: Text(
                      comparable.locationLabel,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: AppColors.textMuted,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: AppSpacing.md),
              Wrap(
                spacing: AppSpacing.sm,
                runSpacing: AppSpacing.sm,
                children: [
                  if (comparable.distanceM != null)
                    _Attribute(
                      icon: Icons.near_me_outlined,
                      label: _formatDistance(comparable.distanceM!),
                    ),
                  if (comparable.sizeSqm != null)
                    _Attribute(
                      icon: Icons.square_foot_rounded,
                      label: '${_formatDecimal(comparable.sizeSqm!)} sqm',
                    ),
                  if (comparable.bedrooms != null)
                    _Attribute(
                      icon: Icons.bed_outlined,
                      label: '${comparable.bedrooms} bed',
                    ),
                  if (comparable.bathrooms != null)
                    _Attribute(
                      icon: Icons.bathtub_outlined,
                      label: '${comparable.bathrooms} bath',
                    ),
                  if (comparable.weightedContribution != null)
                    _Attribute(
                      icon: Icons.insights_outlined,
                      label:
                          '${_formatPercent(comparable.weightedContribution!)} influence',
                    ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _ScoreBadge extends StatelessWidget {
  const _ScoreBadge({required this.score});

  final double score;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 6),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            AppColors.secondaryAccent.withValues(alpha: 0.2),
            AppColors.accent.withValues(alpha: 0.1),
          ],
        ),
        borderRadius: BorderRadius.circular(AppRadius.pill),
        border: Border.all(
          color: AppColors.secondaryAccent.withValues(alpha: 0.36),
        ),
      ),
      child: Text(
        '${(score * 100).round()}% Match',
        style: Theme.of(context).textTheme.labelMedium?.copyWith(
          color: AppColors.secondaryAccent,
          fontSize: 10,
          fontWeight: FontWeight.w800,
        ),
      ),
    );
  }
}

class _ExplorerMap extends StatelessWidget {
  const _ExplorerMap({required this.result, required this.comparables});

  final ValuationResponse result;
  final List<ValuationComparable> comparables;

  @override
  Widget build(BuildContext context) {
    final location = result.location;
    if (location == null || !location.isAvailable) {
      return const _MapUnavailable();
    }
    final subject = LatLng(location.latitude!, location.longitude!);
    final mapped = comparables.where((item) => item.hasLocation).toList();
    final markers = <Marker>{
      Marker(
        markerId: const MarkerId('subject-property'),
        position: subject,
        infoWindow: const InfoWindow(title: 'Subject Property'),
        icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueCyan),
      ),
      ...mapped.map((item) {
        return Marker(
          markerId: MarkerId('comparable-${item.listingId}'),
          position: LatLng(item.latitude!, item.longitude!),
          infoWindow: InfoWindow(
            title: item.propertyType ?? 'Comparable Property',
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
        Text(
          'Map view adds spatial context. Comparable evidence remains the valuation authority.',
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
            color: AppColors.textMuted,
            height: 1.4,
          ),
        ),
        const SizedBox(height: AppSpacing.sm),
        Container(
          height: 360,
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
                mapToolbarEnabled: false,
                myLocationButtonEnabled: false,
                zoomControlsEnabled: false,
                markers: markers,
                circles: radius == null
                    ? const {}
                    : {
                        Circle(
                          circleId: const CircleId('retrieval-radius'),
                          center: subject,
                          radius: radius,
                          fillColor: AppColors.accent.withValues(alpha: 0.08),
                          strokeColor: AppColors.accent.withValues(alpha: 0.42),
                          strokeWidth: 1,
                        ),
                      },
              ),
              Positioned(
                left: AppSpacing.sm,
                right: AppSpacing.sm,
                top: AppSpacing.sm,
                child: _MapLegend(mappedComparables: mapped.length),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _MapLegend extends StatelessWidget {
  const _MapLegend({required this.mappedComparables});

  final int mappedComparables;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.sm,
        vertical: 7,
      ),
      decoration: BoxDecoration(
        color: AppColors.backgroundSecondary.withValues(alpha: 0.92),
        borderRadius: BorderRadius.circular(AppRadius.md),
        border: Border.all(color: AppColors.accent.withValues(alpha: 0.26)),
      ),
      child: Row(
        children: [
          const _LegendDot(color: AppColors.accent),
          const SizedBox(width: 5),
          Text(
            'Subject',
            style: Theme.of(context).textTheme.labelMedium?.copyWith(
              color: AppColors.textSecondary,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(width: AppSpacing.md),
          const _LegendDot(color: AppColors.secondaryAccent),
          const SizedBox(width: 5),
          Expanded(
            child: Text(
              '$mappedComparables comparable markers',
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: Theme.of(context).textTheme.labelMedium?.copyWith(
                color: AppColors.textSecondary,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _LegendDot extends StatelessWidget {
  const _LegendDot({required this.color});

  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 9,
      height: 9,
      decoration: BoxDecoration(color: color, shape: BoxShape.circle),
    );
  }
}

class _MapUnavailable extends StatelessWidget {
  const _MapUnavailable();

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: _panelDecoration(),
      child: Text(
        'Map context is unavailable because the backend did not return subject coordinates.',
        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
          color: AppColors.textMuted,
          height: 1.45,
        ),
      ),
    );
  }
}

class _ComparableDetailsSheet extends StatelessWidget {
  const _ComparableDetailsSheet({required this.comparable});

  final ValuationComparable comparable;

  @override
  Widget build(BuildContext context) {
    final evidence = <_DetailValue>[
      _DetailValue('Distance', _nullableDistance(comparable.distanceM)),
      _DetailValue(
        'Similarity',
        comparable.similarityScore == null
            ? null
            : _formatPercent(comparable.similarityScore!),
      ),
      _DetailValue(
        'Area',
        comparable.sizeSqm == null
            ? null
            : '${_formatDecimal(comparable.sizeSqm!)} sqm',
      ),
      _DetailValue('Bedrooms', comparable.bedrooms?.toString()),
      _DetailValue('Bathrooms', comparable.bathrooms?.toString()),
      _DetailValue('Property Type', comparable.propertyType),
      _DetailValue('Location', comparable.locationLabel),
      _DetailValue(
        'Valuation Influence',
        comparable.weightedContribution == null
            ? null
            : _formatPercent(comparable.weightedContribution!),
      ),
      _DetailValue(
        'Confidence Contribution',
        comparable.confidenceContribution == null
            ? null
            : _formatPercent(comparable.confidenceContribution!),
      ),
      _DetailValue(
        'Price Per Sqm',
        comparable.pricePerSqm == null
            ? null
            : 'EGP ${_formatNumber(comparable.pricePerSqm!.round())}',
      ),
      _DetailValue(
        'Listing Evidence Age',
        comparable.ageDays == null
            ? null
            : '${_formatDecimal(comparable.ageDays!)} days',
      ),
      _DetailValue(
        'Retrieval Context',
        comparable.tierLabel ??
            (comparable.retrievalTier == null
                ? null
                : 'Tier ${comparable.retrievalTier}'),
      ),
      _DetailValue('Retrieval Radius', _nullableDistance(comparable.radiusM)),
    ].where((item) => item.value != null).toList();
    final matchMetrics = <_EvidenceMetric>[
      _EvidenceMetric(
        label: 'Location similarity',
        value: comparable.geographicSimilarity,
      ),
      _EvidenceMetric(
        label: 'Area similarity',
        value: comparable.areaSimilarity,
      ),
      _EvidenceMetric(
        label: 'Area size similarity',
        value: comparable.areaSizeSimilarity,
      ),
      _EvidenceMetric(
        label: 'Property type similarity',
        value: comparable.propertyTypeSimilarity,
      ),
      _EvidenceMetric(
        label: 'Amenities similarity',
        value: comparable.amenitySimilarity,
      ),
    ].where((item) => item.value != null).toList();
    final attributes = <_DetailValue>[
      _DetailValue('Compound', comparable.compoundName),
      _DetailValue('Furnishing', comparable.furnishingStatus),
      _DetailValue('Floor', comparable.floorNumber?.toString()),
      _DetailValue('View', comparable.viewType),
      _DetailValue('Building Quality', comparable.buildingQuality),
    ].where((item) => item.value != null).toList();

    return DraggableScrollableSheet(
      initialChildSize: 0.86,
      minChildSize: 0.5,
      maxChildSize: 0.94,
      expand: false,
      builder: (context, controller) {
        return Container(
          decoration: const BoxDecoration(
            color: AppColors.backgroundSecondary,
            borderRadius: BorderRadius.vertical(
              top: Radius.circular(AppRadius.xl),
            ),
          ),
          child: ListView(
            controller: controller,
            padding: const EdgeInsets.fromLTRB(
              AppSpacing.lg,
              AppSpacing.sm,
              AppSpacing.lg,
              AppSpacing.xl,
            ),
            children: [
              Center(
                child: Container(
                  width: 42,
                  height: 4,
                  decoration: BoxDecoration(
                    color: AppColors.textMuted.withValues(alpha: 0.42),
                    borderRadius: BorderRadius.circular(AppRadius.pill),
                  ),
                ),
              ),
              const SizedBox(height: AppSpacing.lg),
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          comparable.propertyType ?? 'Comparable Property',
                          style: Theme.of(context).textTheme.titleLarge
                              ?.copyWith(
                                color: AppColors.textPrimary,
                                fontWeight: FontWeight.w800,
                              ),
                        ),
                        const SizedBox(height: AppSpacing.xs),
                        Text(
                          comparable.locationLabel,
                          style: Theme.of(context).textTheme.bodyMedium
                              ?.copyWith(color: AppColors.textMuted),
                        ),
                      ],
                    ),
                  ),
                  if (comparable.similarityScore != null)
                    _ScoreBadge(score: comparable.similarityScore!),
                ],
              ),
              const SizedBox(height: AppSpacing.lg),
              Text(
                'EGP ${_formatNumber(comparable.priceEgp)}',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.w800,
                  letterSpacing: -0.8,
                ),
              ),
              const SizedBox(height: AppSpacing.xl),
              const _SheetSectionTitle('Comparable Details'),
              const SizedBox(height: AppSpacing.sm),
              ...evidence.map(_DetailRow.new),
              if (comparable.reasonCode != null) ...[
                const SizedBox(height: AppSpacing.lg),
                const _SheetSectionTitle('Reason For Match'),
                const SizedBox(height: AppSpacing.sm),
                _EvidenceText(_humanize(comparable.reasonCode!)),
              ],
              if (matchMetrics.isNotEmpty) ...[
                const SizedBox(height: AppSpacing.lg),
                const _SheetSectionTitle('Match Evidence'),
                const SizedBox(height: AppSpacing.sm),
                ...matchMetrics.map(
                  (metric) => Padding(
                    padding: const EdgeInsets.only(bottom: AppSpacing.sm),
                    child: _EvidenceRail(metric: metric),
                  ),
                ),
              ],
              if (comparable.amenities.isNotEmpty) ...[
                const SizedBox(height: AppSpacing.lg),
                const _SheetSectionTitle('Amenities'),
                const SizedBox(height: AppSpacing.sm),
                _TextChips(items: comparable.amenities),
              ],
              if (comparable.matchedAmenities.isNotEmpty) ...[
                const SizedBox(height: AppSpacing.lg),
                const _SheetSectionTitle('Matched Amenities'),
                const SizedBox(height: AppSpacing.sm),
                _TextChips(items: comparable.matchedAmenities),
              ],
              if (comparable.missingAmenities.isNotEmpty) ...[
                const SizedBox(height: AppSpacing.lg),
                const _SheetSectionTitle('Missing Amenities'),
                const SizedBox(height: AppSpacing.sm),
                _TextChips(items: comparable.missingAmenities),
              ],
              if (attributes.isNotEmpty) ...[
                const SizedBox(height: AppSpacing.lg),
                const _SheetSectionTitle('Additional Backend Evidence'),
                const SizedBox(height: AppSpacing.sm),
                ...attributes.map(_DetailRow.new),
              ],
            ],
          ),
        );
      },
    );
  }
}

class _DetailValue {
  const _DetailValue(this.label, this.value);

  final String label;
  final String? value;
}

class _DetailRow extends StatelessWidget {
  const _DetailRow(this.detail);

  final _DetailValue detail;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 7),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            child: Text(
              detail.label,
              style: Theme.of(
                context,
              ).textTheme.bodyMedium?.copyWith(color: AppColors.textMuted),
            ),
          ),
          const SizedBox(width: AppSpacing.md),
          Flexible(
            child: Text(
              detail.value!,
              textAlign: TextAlign.right,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: AppColors.textSecondary,
                fontWeight: FontWeight.w700,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _SheetSectionTitle extends StatelessWidget {
  const _SheetSectionTitle(this.title);

  final String title;

  @override
  Widget build(BuildContext context) {
    return Text(
      title.toUpperCase(),
      style: Theme.of(context).textTheme.labelMedium?.copyWith(
        color: AppColors.accent,
        fontSize: 10,
        fontWeight: FontWeight.w700,
        letterSpacing: 1.3,
      ),
    );
  }
}

class _EvidenceText extends StatelessWidget {
  const _EvidenceText(this.text);

  final String text;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: _panelDecoration(),
      child: Text(
        text,
        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
          color: AppColors.textSecondary,
          height: 1.4,
        ),
      ),
    );
  }
}

class _TextChips extends StatelessWidget {
  const _TextChips({required this.items});

  final List<String> items;

  @override
  Widget build(BuildContext context) {
    return Wrap(
      spacing: AppSpacing.sm,
      runSpacing: AppSpacing.sm,
      children: items.map((item) {
        return Container(
          padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 7),
          decoration: BoxDecoration(
            color: AppColors.accent.withValues(alpha: 0.08),
            borderRadius: BorderRadius.circular(AppRadius.pill),
            border: Border.all(color: AppColors.accent.withValues(alpha: 0.18)),
          ),
          child: Text(
            item,
            style: Theme.of(context).textTheme.labelMedium?.copyWith(
              color: AppColors.textSecondary,
              fontWeight: FontWeight.w600,
            ),
          ),
        );
      }).toList(),
    );
  }
}

class _Attribute extends StatelessWidget {
  const _Attribute({required this.icon, required this.label});

  final IconData icon;
  final String label;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 7),
      decoration: BoxDecoration(
        color: AppColors.backgroundPrimary.withValues(alpha: 0.44),
        borderRadius: BorderRadius.circular(AppRadius.pill),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 14, color: AppColors.textMuted),
          const SizedBox(width: 5),
          Text(
            label,
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

class _NoComparables extends StatelessWidget {
  const _NoComparables();

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: _panelDecoration(),
      child: Text(
        'The backend did not return comparable cards for this valuation.',
        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
          color: AppColors.textMuted,
          height: 1.45,
        ),
      ),
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

class _EmptyExplorer extends StatelessWidget {
  const _EmptyExplorer({required this.onBack});

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
              Icons.travel_explore_outlined,
              color: AppColors.accent,
              size: 46,
            ),
            const SizedBox(height: AppSpacing.md),
            Text(
              'No comparable evidence',
              style: Theme.of(
                context,
              ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: AppSpacing.sm),
            Text(
              'Run a valuation to inspect its returned comparable properties.',
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

TextStyle? _controlLabelStyle(BuildContext context) {
  return Theme.of(context).textTheme.labelMedium?.copyWith(
    color: AppColors.textMuted,
    fontSize: 9,
    fontWeight: FontWeight.w700,
    letterSpacing: 1.1,
  );
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

int _compareNullableDescending(double? left, double? right) {
  if (left == null && right == null) {
    return 0;
  }
  if (left == null) {
    return 1;
  }
  if (right == null) {
    return -1;
  }
  return right.compareTo(left);
}

int _compareNullableAscending(double? left, double? right) {
  if (left == null && right == null) {
    return 0;
  }
  if (left == null) {
    return 1;
  }
  if (right == null) {
    return -1;
  }
  return left.compareTo(right);
}

double? _average(Iterable<double?> values) {
  final present = values.whereType<double>().toList();
  if (present.isEmpty) {
    return null;
  }
  return present.reduce((left, right) => left + right) / present.length;
}

String? _nullableDistance(double? value) {
  return value == null ? null : _formatDistance(value);
}

String _formatDistance(double value) {
  if (value < 1000) {
    return '${value.round()}m';
  }
  return '${_formatDecimal(value / 1000)}km';
}

String _formatPercent(double value) {
  return '${(value * 100).round()}%';
}

String _formatDecimal(double value) {
  return value == value.roundToDouble()
      ? value.toStringAsFixed(0)
      : value.toStringAsFixed(1);
}

String _formatNumber(int value) {
  return value.toString().replaceAllMapped(
    RegExp(r'(?=(\d{3})+(?!\d))'),
    (_) => ',',
  );
}

String _humanize(String value) {
  return value
      .replaceAll('_', ' ')
      .split(' ')
      .where((word) => word.isNotEmpty)
      .map(
        (word) => '${word[0].toUpperCase()}${word.substring(1).toLowerCase()}',
      )
      .join(' ');
}
