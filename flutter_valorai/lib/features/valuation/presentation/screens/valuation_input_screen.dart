import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:geolocator/geolocator.dart';
import 'package:go_router/go_router.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import '../../../../app/router/route_names.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_radius.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../data/datasources/valuation_remote_data_source.dart';
import '../../data/repositories/valuation_repository_impl.dart';
import '../../domain/models/valuation_request.dart';
import '../../domain/repositories/valuation_repository.dart';
import '../models/valuation_input_catalog.dart';
import '../widgets/google_map_location_picker.dart';

class ValuationInputScreen extends StatefulWidget {
  const ValuationInputScreen({super.key, this.repository});

  final ValuationRepository? repository;

  @override
  State<ValuationInputScreen> createState() => _ValuationInputScreenState();
}

class _ValuationInputScreenState extends State<ValuationInputScreen> {
  static const _stepTitles = [
    'Category',
    'Property Type',
    'Location',
    'Property Details',
    'Amenities',
    'Review',
  ];

  late final ValuationRepository _repository;
  final _cityController = TextEditingController();
  final _districtController = TextEditingController();
  final _compoundController = TextEditingController();
  final _areaController = TextEditingController();
  final _latitudeController = TextEditingController();
  final _longitudeController = TextEditingController();
  final _selectedAmenities = <String>{};

  int _stepIndex = 0;
  ValuationCategory? _category;
  String? _propertyType;
  ValuationLocationMode _locationMode = ValuationLocationMode.hierarchy;
  String? _governorate;
  double? _latitude;
  double? _longitude;
  int? _bedrooms;
  int? _bathrooms;
  bool _isLocating = false;
  bool _isSubmitting = false;

  @override
  void initState() {
    super.initState();
    _repository =
        widget.repository ??
        ValuationRepositoryImpl(ValuationRemoteDataSource());
  }

  @override
  void dispose() {
    _cityController.dispose();
    _districtController.dispose();
    _compoundController.dispose();
    _areaController.dispose();
    _latitudeController.dispose();
    _longitudeController.dispose();
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
              Color(0xFF04111D),
            ],
          ),
        ),
        child: SafeArea(
          bottom: false,
          child: Stack(
            children: [
              const Positioned(top: 96, right: -110, child: _AmbientGlow()),
              Column(
                children: [
                  _ValuationHeader(
                    step: _stepIndex + 1,
                    stepCount: _stepTitles.length,
                    title: _stepTitles[_stepIndex],
                    onBack: _goBack,
                  ),
                  _ProgressRail(
                    stepIndex: _stepIndex,
                    stepCount: _stepTitles.length,
                  ),
                  Expanded(
                    child: AnimatedSwitcher(
                      duration: 320.ms,
                      switchInCurve: Curves.easeOutCubic,
                      switchOutCurve: Curves.easeInCubic,
                      transitionBuilder: (child, animation) {
                        return FadeTransition(
                          opacity: animation,
                          child: SlideTransition(
                            position: Tween<Offset>(
                              begin: const Offset(0.04, 0),
                              end: Offset.zero,
                            ).animate(animation),
                            child: child,
                          ),
                        );
                      },
                      child: SingleChildScrollView(
                        key: ValueKey(_stepIndex),
                        physics: const BouncingScrollPhysics(),
                        padding: const EdgeInsets.fromLTRB(
                          AppSpacing.lg,
                          AppSpacing.lg,
                          AppSpacing.lg,
                          AppSpacing.xxl,
                        ),
                        child: _buildCurrentStep(),
                      ),
                    ),
                  ),
                  _BottomAction(
                    isEnabled: _canContinue && !_isSubmitting,
                    isLoading: _isSubmitting,
                    isFinalStep: _stepIndex == _stepTitles.length - 1,
                    onPressed: _continue,
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCurrentStep() {
    return switch (_stepIndex) {
      0 => _buildCategoryStep(),
      1 => _buildPropertyTypeStep(),
      2 => _buildLocationStep(),
      3 => _buildDetailsStep(),
      4 => _buildAmenitiesStep(),
      _ => _buildReviewStep(),
    };
  }

  Widget _buildCategoryStep() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const _StepIntro(
          eyebrow: 'VALUATION MODE',
          title: 'Select Category',
          description:
              'Start with the market lane. ValorAI uses this to shape the '
              'experience and select the governed valuation contract.',
        ),
        const SizedBox(height: AppSpacing.xl),
        ...List.generate(_categoryOptions.length, (index) {
          final option = _categoryOptions[index];
          return Padding(
            padding: const EdgeInsets.only(bottom: AppSpacing.md),
            child:
                _CategoryCard(
                      option: option,
                      isSelected: _category == option.category,
                      onTap: () {
                        setState(() {
                          if (_category != option.category) {
                            _category = option.category;
                            _propertyType = null;
                            _selectedAmenities.clear();
                            _bedrooms = null;
                            _bathrooms = null;
                          }
                        });
                      },
                    )
                    .animate(delay: (70 * index).ms)
                    .fadeIn(duration: 420.ms)
                    .slideY(begin: 0.08, end: 0),
          );
        }),
      ],
    );
  }

  Widget _buildPropertyTypeStep() {
    final category = _category!;
    final choices = propertyTypesFor(category);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _StepIntro(
          eyebrow: category.label.toUpperCase(),
          title: 'Choose property type',
          description:
              'The available types come from Egypt listing coverage for this '
              'category. Select the closest match.',
        ),
        const SizedBox(height: AppSpacing.xl),
        GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: choices.length,
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            childAspectRatio: 1.22,
            crossAxisSpacing: AppSpacing.md,
            mainAxisSpacing: AppSpacing.md,
          ),
          itemBuilder: (context, index) {
            final choice = choices[index];
            return _PropertyTypeCard(
                  choice: choice,
                  isSelected: _propertyType == choice.label,
                  onTap: () {
                    setState(() {
                      _propertyType = choice.label;
                      if (_propertyType == 'Land') {
                        _bedrooms = null;
                        _bathrooms = null;
                      }
                    });
                  },
                )
                .animate(delay: (35 * index).ms)
                .fadeIn(duration: 360.ms)
                .scale(
                  begin: const Offset(0.96, 0.96),
                  end: const Offset(1, 1),
                );
          },
        ),
        if (_propertyType != null && !_isCurrentSelectionSupported) ...[
          const SizedBox(height: AppSpacing.lg),
          const _BackendCoverageNotice(),
        ],
      ],
    );
  }

  Widget _buildLocationStep() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const _StepIntro(
          eyebrow: 'LOCATION INTELLIGENCE',
          title: 'Ground the property',
          description:
              'Use the Egypt hierarchy, your live GPS position, or an exact '
              'map pin. Better grounding produces stronger comparable evidence.',
        ),
        const SizedBox(height: AppSpacing.lg),
        Row(
          children: [
            Expanded(
              child: _LocationMethodButton(
                icon: Icons.account_tree_outlined,
                label: 'Hierarchy',
                isSelected: _locationMode == ValuationLocationMode.hierarchy,
                onTap: () {
                  setState(() {
                    _locationMode = ValuationLocationMode.hierarchy;
                  });
                },
              ),
            ),
            const SizedBox(width: AppSpacing.sm),
            Expanded(
              child: _LocationMethodButton(
                icon: Icons.my_location_rounded,
                label: 'GPS',
                isSelected: _locationMode == ValuationLocationMode.gps,
                onTap: _getCurrentLocation,
              ),
            ),
            const SizedBox(width: AppSpacing.sm),
            Expanded(
              child: _LocationMethodButton(
                icon: Icons.map_outlined,
                label: 'Map Pin',
                isSelected: _locationMode == ValuationLocationMode.map,
                onTap: _pickMapLocation,
              ),
            ),
          ],
        ),
        const SizedBox(height: AppSpacing.lg),
        AnimatedSwitcher(
          duration: 260.ms,
          child: _locationMode == ValuationLocationMode.hierarchy
              ? _buildHierarchyLocation()
              : _buildCoordinateLocation(),
        ),
        const SizedBox(height: AppSpacing.lg),
        _SelectedLocationSummary(
          summary: _locationSummary,
          latitude: _latitude,
          longitude: _longitude,
          usesAddressResolution:
              _locationMode == ValuationLocationMode.hierarchy,
        ),
      ],
    );
  }

  Widget _buildHierarchyLocation() {
    return Container(
      key: const ValueKey('hierarchy-location'),
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: _panelDecoration(accent: AppColors.accent),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(
                Icons.route_outlined,
                color: AppColors.accent,
                size: 20,
              ),
              const SizedBox(width: AppSpacing.sm),
              Text(
                'Egypt location hierarchy',
                style: Theme.of(
                  context,
                ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.xs),
          Text(
            'Governorate, city, and district are required. Compound is optional.',
            style: Theme.of(
              context,
            ).textTheme.bodyMedium?.copyWith(color: AppColors.textMuted),
          ),
          const SizedBox(height: AppSpacing.lg),
          _DatasetGovernorateDropdown(
            value: _governorate,
            onChanged: (value) {
              setState(() {
                _governorate = value;
              });
            },
          ),
          const _HierarchyConnector(),
          _HierarchyTextField(
            controller: _cityController,
            label: 'City',
            hint: 'e.g. New Cairo City',
            onChanged: (_) => setState(() {}),
          ),
          const _HierarchyConnector(),
          _HierarchyTextField(
            controller: _districtController,
            label: 'District',
            hint: 'e.g. The 5th Settlement',
            onChanged: (_) => setState(() {}),
          ),
          const _HierarchyConnector(),
          _HierarchyTextField(
            controller: _compoundController,
            label: 'Compound',
            hint: 'Optional compound or street',
            isOptional: true,
            onChanged: (_) => setState(() {}),
          ),
          const SizedBox(height: AppSpacing.md),
          Text(
            'Autocomplete extension point prepared for the future backend '
            'location suggestion API.',
            style: Theme.of(context).textTheme.labelMedium?.copyWith(
              color: AppColors.textMuted,
              height: 1.4,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCoordinateLocation() {
    final isGps = _locationMode == ValuationLocationMode.gps;
    return Container(
      key: ValueKey(_locationMode),
      padding: const EdgeInsets.all(AppSpacing.lg),
      decoration: _panelDecoration(
        accent: isGps ? AppColors.secondaryAccent : AppColors.accent,
      ),
      child: Column(
        children: [
          Icon(
            isGps ? Icons.gps_fixed_rounded : Icons.add_location_alt_outlined,
            color: isGps ? AppColors.secondaryAccent : AppColors.accent,
            size: 42,
          ),
          const SizedBox(height: AppSpacing.md),
          Text(
            isGps ? 'Use device location' : 'Drop an exact map pin',
            style: Theme.of(
              context,
            ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: AppSpacing.xs),
          Text(
            isGps
                ? 'ValorAI reads your current coordinates only after permission is granted.'
                : 'Choose a point in Google Maps and the coordinates will populate automatically.',
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
              color: AppColors.textMuted,
              height: 1.45,
            ),
          ),
          const SizedBox(height: AppSpacing.lg),
          OutlinedButton.icon(
            onPressed: _isLocating
                ? null
                : isGps
                ? _getCurrentLocation
                : _pickMapLocation,
            icon: _isLocating
                ? const SizedBox(
                    width: 16,
                    height: 16,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : Icon(isGps ? Icons.my_location_rounded : Icons.map_outlined),
            label: Text(
              isGps ? 'Get Current Location' : 'Pick Location On Map',
            ),
          ),
          const SizedBox(height: AppSpacing.lg),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: _CoordinateTextField(
                  controller: _latitudeController,
                  label: 'Latitude',
                  hint: '30.0444',
                  errorText: _latitudeErrorText,
                  onChanged: _onCoordinateTextChanged,
                ),
              ),
              const SizedBox(width: AppSpacing.sm),
              Expanded(
                child: _CoordinateTextField(
                  controller: _longitudeController,
                  label: 'Longitude',
                  hint: '31.2357',
                  errorText: _longitudeErrorText,
                  onChanged: _onCoordinateTextChanged,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildDetailsStep() {
    final isResidential = _category!.isResidential;
    final isLand = _propertyType == 'Land';
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _StepIntro(
          eyebrow: isResidential ? 'RESIDENTIAL DETAILS' : 'COMMERCIAL DETAILS',
          title: 'Describe the space',
          description: isResidential
              ? 'Area is the core valuation input. Add room counts where they '
                    'apply to strengthen comparable matching.'
              : 'Commercial valuation stays focused on usable area. Bedrooms '
                    'are intentionally excluded from this workflow.',
        ),
        const SizedBox(height: AppSpacing.xl),
        Container(
          padding: const EdgeInsets.all(AppSpacing.lg),
          decoration: _panelDecoration(accent: AppColors.accent),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'USABLE AREA',
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                  color: AppColors.accent,
                  fontWeight: FontWeight.w700,
                  letterSpacing: 1.4,
                ),
              ),
              const SizedBox(height: AppSpacing.sm),
              TextField(
                controller: _areaController,
                autofocus: true,
                keyboardType: const TextInputType.numberWithOptions(
                  decimal: true,
                ),
                inputFormatters: [
                  FilteringTextInputFormatter.allow(RegExp(r'^\d*\.?\d{0,2}')),
                ],
                onChanged: (_) => setState(() {}),
                style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.w700,
                ),
                decoration: InputDecoration(
                  hintText: '0',
                  suffixText: 'sqm',
                  suffixStyle: Theme.of(context).textTheme.titleMedium
                      ?.copyWith(
                        color: AppColors.textMuted,
                        fontWeight: FontWeight.w700,
                      ),
                  errorText: _areaController.text.isNotEmpty && !_hasValidArea
                      ? 'Enter an area greater than zero.'
                      : null,
                ),
              ),
              const SizedBox(height: AppSpacing.sm),
              Text(
                'Enter the usable property area in square meters.',
                style: Theme.of(
                  context,
                ).textTheme.labelMedium?.copyWith(color: AppColors.textMuted),
              ),
            ],
          ),
        ),
        if (!isLand) ...[
          const SizedBox(height: AppSpacing.lg),
          if (isResidential)
            Row(
              children: [
                Expanded(
                  child: _RoomSelector(
                    label: 'Bedrooms',
                    icon: Icons.bed_outlined,
                    value: _bedrooms,
                    onChanged: (value) {
                      setState(() {
                        _bedrooms = value;
                      });
                    },
                  ),
                ),
                const SizedBox(width: AppSpacing.md),
                Expanded(
                  child: _RoomSelector(
                    label: 'Bathrooms',
                    icon: Icons.bathtub_outlined,
                    value: _bathrooms,
                    onChanged: (value) {
                      setState(() {
                        _bathrooms = value;
                      });
                    },
                  ),
                ),
              ],
            )
          else
            _RoomSelector(
              label: 'Bathrooms',
              icon: Icons.bathtub_outlined,
              value: _bathrooms,
              isOptional: true,
              onChanged: (value) {
                setState(() {
                  _bathrooms = value;
                });
              },
            ),
        ],
        if (isLand) ...[
          const SizedBox(height: AppSpacing.lg),
          const _ContextNote(
            icon: Icons.landscape_outlined,
            text:
                'Room counts are not collected for land. ValorAI keeps this '
                'valuation focused on site area and location.',
          ),
        ],
      ],
    );
  }

  Widget _buildAmenitiesStep() {
    final groups = amenityGroupsFor(_category!);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const _StepIntro(
          eyebrow: 'PROPERTY SIGNALS',
          title: 'Add amenities',
          description:
              'Choose every feature that applies. These are governed dataset '
              'signals used to refine comparable relevance and explainability.',
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          '${_selectedAmenities.length} selected',
          style: Theme.of(context).textTheme.labelLarge?.copyWith(
            color: AppColors.secondaryAccent,
            fontWeight: FontWeight.w700,
          ),
        ),
        const SizedBox(height: AppSpacing.xl),
        ...List.generate(groups.length, (index) {
          final group = groups[index];
          return Padding(
            padding: const EdgeInsets.only(bottom: AppSpacing.lg),
            child:
                Container(
                      padding: const EdgeInsets.all(AppSpacing.md),
                      decoration: _panelDecoration(),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            group.label.toUpperCase(),
                            style: Theme.of(context).textTheme.labelMedium
                                ?.copyWith(
                                  color: AppColors.textMuted,
                                  fontWeight: FontWeight.w700,
                                  letterSpacing: 1.3,
                                ),
                          ),
                          const SizedBox(height: AppSpacing.md),
                          Wrap(
                            spacing: AppSpacing.sm,
                            runSpacing: AppSpacing.sm,
                            children: group.amenities.map((amenity) {
                              final isSelected = _selectedAmenities.contains(
                                amenity.code,
                              );
                              return _AmenityChip(
                                amenity: amenity,
                                isSelected: isSelected,
                                onTap: () {
                                  setState(() {
                                    if (isSelected) {
                                      _selectedAmenities.remove(amenity.code);
                                    } else {
                                      _selectedAmenities.add(amenity.code);
                                    }
                                  });
                                },
                              );
                            }).toList(),
                          ),
                        ],
                      ),
                    )
                    .animate(delay: (80 * index).ms)
                    .fadeIn(duration: 420.ms)
                    .slideY(begin: 0.08, end: 0),
          );
        }),
      ],
    );
  }

  Widget _buildReviewStep() {
    final isResidential = _category!.isResidential;
    final hasCoordinates = _latitude != null && _longitude != null;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const _StepIntro(
          eyebrow: 'FINAL CHECK',
          title: 'Review valuation',
          description:
              'Confirm the property profile before ValorAI sends it to the '
              'governed fair-price service.',
        ),
        const SizedBox(height: AppSpacing.xl),
        _ReviewPanel(
          title: 'Property',
          icon: Icons.home_work_outlined,
          onEdit: () => _jumpTo(0),
          lines: [
            _ReviewLine('Category', _category!.label),
            _ReviewLine('Property Type', _propertyType!),
          ],
        ),
        const SizedBox(height: AppSpacing.md),
        _ReviewPanel(
          title: 'Location',
          icon: Icons.location_on_outlined,
          onEdit: () => _jumpTo(2),
          lines: [
            _ReviewLine('Selected Location', _locationSummary),
            _ReviewLine(
              'Latitude',
              hasCoordinates
                  ? _latitude!.toStringAsFixed(6)
                  : 'Resolved by backend',
            ),
            _ReviewLine(
              'Longitude',
              hasCoordinates
                  ? _longitude!.toStringAsFixed(6)
                  : 'Resolved by backend',
            ),
          ],
        ),
        const SizedBox(height: AppSpacing.md),
        _ReviewPanel(
          title: 'Details',
          icon: Icons.straighten_outlined,
          onEdit: () => _jumpTo(3),
          lines: [
            _ReviewLine('Area', '${_areaController.text.trim()} sqm'),
            if (isResidential && _propertyType != 'Land')
              _ReviewLine('Bedrooms', _bedrooms?.toString() ?? 'Not specified'),
            if (_propertyType != 'Land')
              _ReviewLine(
                'Bathrooms',
                _bathrooms?.toString() ?? 'Not specified',
              ),
          ],
        ),
        const SizedBox(height: AppSpacing.md),
        _ReviewPanel(
          title: 'Amenities',
          icon: Icons.auto_awesome_outlined,
          onEdit: () => _jumpTo(4),
          lines: [
            _ReviewLine(
              'Selected',
              _selectedAmenityLabels.isEmpty
                  ? 'None selected'
                  : _selectedAmenityLabels.join(', '),
            ),
          ],
        ),
        if (!_isCurrentSelectionSupported) ...[
          const SizedBox(height: AppSpacing.md),
          const _BackendCoverageNotice(),
        ],
      ],
    );
  }

  bool get _canContinue {
    return switch (_stepIndex) {
      0 => _category != null,
      1 => _propertyType != null,
      2 => _hasValidLocation,
      3 => _hasValidArea,
      _ => true,
    };
  }

  bool get _hasValidArea {
    final area = double.tryParse(_areaController.text.trim());
    return area != null && area > 0;
  }

  bool get _hasValidLocation {
    if (_locationMode == ValuationLocationMode.hierarchy) {
      return _governorate != null &&
          _cityController.text.trim().isNotEmpty &&
          _districtController.text.trim().isNotEmpty;
    }
    return _hasValidCoordinates;
  }

  bool get _isCurrentSelectionSupported {
    final category = _category;
    final propertyType = _propertyType;
    if (category == null || propertyType == null) {
      return false;
    }
    return ValuationRequest(
      category: category,
      propertyType: propertyType,
      locationMode: ValuationLocationMode.hierarchy,
      address: 'Draft location',
      sizeSqm: 1,
      amenities: const [],
    ).isSupportedByBackend;
  }

  String get _locationSummary {
    if (_locationMode != ValuationLocationMode.hierarchy &&
        _hasValidCoordinates) {
      final source = _locationMode == ValuationLocationMode.gps
          ? 'Current GPS location'
          : 'Google Maps pin';
      return '$source (${_latitude!.toStringAsFixed(5)}, '
          '${_longitude!.toStringAsFixed(5)})';
    }
    final values = [
      _compoundController.text.trim(),
      _districtController.text.trim(),
      _cityController.text.trim(),
      _governorate,
    ].whereType<String>().where((value) => value.isNotEmpty).toList();
    return values.isEmpty ? 'No location selected' : values.join(', ');
  }

  List<String> get _selectedAmenityLabels {
    final groups = amenityGroupsFor(_category!);
    return [
      for (final group in groups)
        for (final amenity in group.amenities)
          if (_selectedAmenities.contains(amenity.code)) amenity.label,
    ];
  }

  void _continue() {
    FocusScope.of(context).unfocus();
    if (!_canContinue) {
      return;
    }
    if (_stepIndex < _stepTitles.length - 1) {
      setState(() {
        _stepIndex += 1;
      });
      return;
    }
    _analyzeProperty();
  }

  void _goBack() {
    FocusScope.of(context).unfocus();
    if (_stepIndex > 0) {
      setState(() {
        _stepIndex -= 1;
      });
      return;
    }
    if (context.canPop()) {
      context.pop();
    } else {
      context.goNamed(RouteNames.home);
    }
  }

  void _jumpTo(int stepIndex) {
    setState(() {
      _stepIndex = stepIndex;
    });
  }

  Future<void> _getCurrentLocation() async {
    setState(() {
      _locationMode = ValuationLocationMode.gps;
      _isLocating = true;
    });
    try {
      final servicesEnabled = await Geolocator.isLocationServiceEnabled();
      if (!servicesEnabled) {
        throw const ValuationSubmissionException(
          'Location services are turned off on this device.',
        );
      }
      var permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
      }
      if (permission == LocationPermission.denied ||
          permission == LocationPermission.deniedForever) {
        throw const ValuationSubmissionException(
          'Location permission is required to use GPS.',
        );
      }
      final position = await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(
          accuracy: LocationAccuracy.high,
        ),
      );
      if (!mounted) {
        return;
      }
      _setCoordinateLocation(position.latitude, position.longitude);
    } catch (error) {
      if (mounted) {
        _showMessage(error.toString());
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLocating = false;
        });
      }
    }
  }

  Future<void> _pickMapLocation() async {
    setState(() {
      _locationMode = ValuationLocationMode.map;
    });
    final location = await showModalBottomSheet<LatLng>(
      context: context,
      isScrollControlled: true,
      useSafeArea: true,
      backgroundColor: AppColors.backgroundSecondary,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(AppRadius.xl)),
      ),
      builder: (context) {
        return GoogleMapLocationPicker(
          initialLocation: _latitude != null && _longitude != null
              ? LatLng(_latitude!, _longitude!)
              : null,
        );
      },
    );
    if (location == null || !mounted) {
      return;
    }
    _setCoordinateLocation(location.latitude, location.longitude);
  }

  Future<void> _analyzeProperty() async {
    if (!_isCurrentSelectionSupported) {
      _showMessage(
        'This dataset category is visible for accurate property capture, but '
        'the backend valuation contract for it is not available yet.',
      );
      return;
    }
    final request = _buildRequest();
    setState(() {
      _isSubmitting = true;
    });
    try {
      final response = await _repository.analyze(request);
      if (!mounted) {
        return;
      }
      setState(() {
        _isSubmitting = false;
      });
      await context.pushNamed(RouteNames.valuationResult, extra: response);
    } catch (error) {
      if (!mounted) {
        return;
      }
      setState(() {
        _isSubmitting = false;
      });
      _showMessage(error.toString());
    }
  }

  ValuationRequest _buildRequest() {
    return ValuationRequest(
      category: _category!,
      propertyType: _propertyType!,
      locationMode: _locationMode,
      address: _locationSummary,
      governorate: _governorate,
      city: _cityController.text.trim(),
      district: _districtController.text.trim(),
      compound: _compoundController.text.trim(),
      latitude: _latitude,
      longitude: _longitude,
      sizeSqm: double.parse(_areaController.text.trim()),
      bedrooms: _category!.isResidential && _propertyType != 'Land'
          ? _bedrooms
          : null,
      bathrooms: _propertyType != 'Land' ? _bathrooms : null,
      amenities: _selectedAmenities.toList()..sort(),
    );
  }

  void _showMessage(String message) {
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(
        SnackBar(content: Text(message), behavior: SnackBarBehavior.floating),
      );
  }

  bool get _hasValidCoordinates =>
      _latitude != null &&
      _longitude != null &&
      _isCoordinateInRange(_latitude!, -90, 90) &&
      _isCoordinateInRange(_longitude!, -180, 180);

  String? get _latitudeErrorText => _coordinateError(
    value: _latitudeController.text,
    label: 'Latitude',
    minimum: -90,
    maximum: 90,
  );

  String? get _longitudeErrorText => _coordinateError(
    value: _longitudeController.text,
    label: 'Longitude',
    minimum: -180,
    maximum: 180,
  );

  void _setCoordinateLocation(double latitude, double longitude) {
    setState(() {
      _latitude = latitude;
      _longitude = longitude;
      _latitudeController.text = latitude.toStringAsFixed(6);
      _longitudeController.text = longitude.toStringAsFixed(6);
    });
  }

  void _onCoordinateTextChanged(String _) {
    final latitude = double.tryParse(_latitudeController.text.trim());
    final longitude = double.tryParse(_longitudeController.text.trim());
    setState(() {
      if (latitude != null &&
          longitude != null &&
          _isCoordinateInRange(latitude, -90, 90) &&
          _isCoordinateInRange(longitude, -180, 180)) {
        _latitude = latitude;
        _longitude = longitude;
      } else {
        _latitude = null;
        _longitude = null;
      }
    });
  }

  String? _coordinateError({
    required String value,
    required String label,
    required double minimum,
    required double maximum,
  }) {
    final trimmed = value.trim();
    if (trimmed.isEmpty) {
      return null;
    }
    final parsed = double.tryParse(trimmed);
    if (parsed == null) {
      return '$label must be a number.';
    }
    if (!_isCoordinateInRange(parsed, minimum, maximum)) {
      return '$label must be between ${minimum.toInt()} and ${maximum.toInt()}.';
    }
    return null;
  }

  bool _isCoordinateInRange(double value, double minimum, double maximum) {
    return value >= minimum && value <= maximum;
  }
}

class _ValuationHeader extends StatelessWidget {
  const _ValuationHeader({
    required this.step,
    required this.stepCount,
    required this.title,
    required this.onBack,
  });

  final int step;
  final int stepCount;
  final String title;
  final VoidCallback onBack;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(
        AppSpacing.md,
        AppSpacing.md,
        AppSpacing.lg,
        AppSpacing.sm,
      ),
      child: Row(
        children: [
          IconButton(
            onPressed: onBack,
            icon: const Icon(Icons.arrow_back_ios_new_rounded, size: 19),
          ),
          const SizedBox(width: AppSpacing.xs),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'NEW VALUATION',
                  style: Theme.of(context).textTheme.labelMedium?.copyWith(
                    color: AppColors.accent,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 1.5,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  title,
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: AppColors.textPrimary,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ],
            ),
          ),
          Text(
            '$step / $stepCount',
            style: Theme.of(context).textTheme.labelLarge?.copyWith(
              color: AppColors.textMuted,
              fontWeight: FontWeight.w700,
            ),
          ),
        ],
      ),
    );
  }
}

class _ProgressRail extends StatelessWidget {
  const _ProgressRail({required this.stepIndex, required this.stepCount});

  final int stepIndex;
  final int stepCount;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
      child: Row(
        children: List.generate(stepCount, (index) {
          return Expanded(
            child: Padding(
              padding: EdgeInsets.only(
                right: index == stepCount - 1 ? 0 : AppSpacing.xs,
              ),
              child: AnimatedContainer(
                duration: 260.ms,
                height: 3,
                decoration: BoxDecoration(
                  color: index <= stepIndex
                      ? AppColors.accent
                      : AppColors.textMuted.withValues(alpha: 0.18),
                  borderRadius: BorderRadius.circular(AppRadius.pill),
                  boxShadow: index == stepIndex
                      ? [
                          BoxShadow(
                            color: AppColors.accent.withValues(alpha: 0.42),
                            blurRadius: 8,
                          ),
                        ]
                      : null,
                ),
              ),
            ),
          );
        }),
      ),
    );
  }
}

class _StepIntro extends StatelessWidget {
  const _StepIntro({
    required this.eyebrow,
    required this.title,
    required this.description,
  });

  final String eyebrow;
  final String title;
  final String description;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          eyebrow,
          style: Theme.of(context).textTheme.labelMedium?.copyWith(
            color: AppColors.secondaryAccent,
            fontWeight: FontWeight.w700,
            letterSpacing: 1.6,
          ),
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          title,
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
            color: AppColors.textPrimary,
            fontWeight: FontWeight.w700,
            letterSpacing: -0.8,
          ),
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          description,
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
            color: AppColors.textMuted,
            height: 1.55,
          ),
        ),
      ],
    ).animate().fadeIn(duration: 420.ms).slideY(begin: -0.08, end: 0);
  }
}

class _CategoryCard extends StatelessWidget {
  const _CategoryCard({
    required this.option,
    required this.isSelected,
    required this.onTap,
  });

  final _CategoryOption option;
  final bool isSelected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final accent = option.accent;
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppRadius.xl),
        child: AnimatedContainer(
          duration: 240.ms,
          padding: const EdgeInsets.all(AppSpacing.lg),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: isSelected
                  ? [
                      accent.withValues(alpha: 0.28),
                      AppColors.surface.withValues(alpha: 0.94),
                    ]
                  : [
                      AppColors.surface.withValues(alpha: 0.74),
                      AppColors.backgroundSecondary.withValues(alpha: 0.78),
                    ],
            ),
            borderRadius: BorderRadius.circular(AppRadius.xl),
            border: Border.all(
              color: isSelected
                  ? accent
                  : AppColors.textPrimary.withValues(alpha: 0.07),
              width: isSelected ? 1.6 : 1,
            ),
            boxShadow: isSelected
                ? [
                    BoxShadow(
                      color: accent.withValues(alpha: 0.16),
                      blurRadius: 24,
                      offset: const Offset(0, 10),
                    ),
                  ]
                : null,
          ),
          child: Row(
            children: [
              Container(
                width: 58,
                height: 58,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: accent.withValues(alpha: isSelected ? 0.2 : 0.1),
                  border: Border.all(color: accent.withValues(alpha: 0.3)),
                ),
                child: Icon(option.icon, color: accent, size: 28),
              ),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      option.category.label,
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        color: AppColors.textPrimary,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    const SizedBox(height: AppSpacing.xs),
                    Text(
                      option.description,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: AppColors.textMuted,
                      ),
                    ),
                  ],
                ),
              ),
              AnimatedContainer(
                duration: 220.ms,
                width: 26,
                height: 26,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: isSelected ? accent : Colors.transparent,
                  border: Border.all(
                    color: isSelected ? accent : AppColors.textMuted,
                  ),
                ),
                child: isSelected
                    ? const Icon(
                        Icons.check_rounded,
                        color: AppColors.backgroundPrimary,
                        size: 17,
                      )
                    : null,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _PropertyTypeCard extends StatelessWidget {
  const _PropertyTypeCard({
    required this.choice,
    required this.isSelected,
    required this.onTap,
  });

  final PropertyTypeChoice choice;
  final bool isSelected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppRadius.lg),
        child: AnimatedContainer(
          duration: 220.ms,
          padding: const EdgeInsets.all(AppSpacing.md),
          decoration: BoxDecoration(
            color: isSelected
                ? AppColors.accent.withValues(alpha: 0.16)
                : AppColors.surface.withValues(alpha: 0.68),
            borderRadius: BorderRadius.circular(AppRadius.lg),
            border: Border.all(
              color: isSelected
                  ? AppColors.accent
                  : AppColors.textPrimary.withValues(alpha: 0.07),
              width: isSelected ? 1.5 : 1,
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Icon(
                choice.icon,
                color: isSelected ? AppColors.accent : AppColors.textMuted,
                size: 27,
              ),
              Text(
                choice.label,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: isSelected
                      ? AppColors.textPrimary
                      : AppColors.textSecondary,
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

class _LocationMethodButton extends StatelessWidget {
  const _LocationMethodButton({
    required this.icon,
    required this.label,
    required this.isSelected,
    required this.onTap,
  });

  final IconData icon;
  final String label;
  final bool isSelected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(AppRadius.lg),
      child: AnimatedContainer(
        duration: 220.ms,
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.xs,
          vertical: AppSpacing.md,
        ),
        decoration: BoxDecoration(
          color: isSelected
              ? AppColors.accent.withValues(alpha: 0.14)
              : AppColors.surface.withValues(alpha: 0.64),
          borderRadius: BorderRadius.circular(AppRadius.lg),
          border: Border.all(
            color: isSelected
                ? AppColors.accent
                : AppColors.textPrimary.withValues(alpha: 0.07),
          ),
        ),
        child: Column(
          children: [
            Icon(
              icon,
              size: 22,
              color: isSelected ? AppColors.accent : AppColors.textMuted,
            ),
            const SizedBox(height: AppSpacing.sm),
            Text(
              label,
              style: Theme.of(context).textTheme.labelMedium?.copyWith(
                color: isSelected ? AppColors.accent : AppColors.textMuted,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _DatasetGovernorateDropdown extends StatelessWidget {
  const _DatasetGovernorateDropdown({
    required this.value,
    required this.onChanged,
  });

  final String? value;
  final ValueChanged<String?> onChanged;

  @override
  Widget build(BuildContext context) {
    return InputDecorator(
      decoration: const InputDecoration(
        labelText: 'Governorate',
        prefixIcon: Icon(Icons.location_city_outlined),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: value,
          isExpanded: true,
          dropdownColor: AppColors.surface,
          hint: const Text('Select governorate'),
          items: egyptDatasetGovernorates.map((governorate) {
            return DropdownMenuItem(
              value: governorate,
              child: Text(governorate),
            );
          }).toList(),
          onChanged: onChanged,
        ),
      ),
    );
  }
}

class _HierarchyTextField extends StatelessWidget {
  const _HierarchyTextField({
    required this.controller,
    required this.label,
    required this.hint,
    required this.onChanged,
    this.isOptional = false,
  });

  final TextEditingController controller;
  final String label;
  final String hint;
  final ValueChanged<String> onChanged;
  final bool isOptional;

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      textCapitalization: TextCapitalization.words,
      onChanged: onChanged,
      decoration: InputDecoration(
        labelText: isOptional ? '$label (optional)' : label,
        hintText: hint,
        prefixIcon: const Icon(Icons.search_rounded),
      ),
    );
  }
}

class _HierarchyConnector extends StatelessWidget {
  const _HierarchyConnector();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 24),
      child: Container(
        width: 1,
        height: AppSpacing.md,
        color: AppColors.accent.withValues(alpha: 0.34),
      ),
    );
  }
}

class _CoordinateTextField extends StatelessWidget {
  const _CoordinateTextField({
    required this.controller,
    required this.label,
    required this.hint,
    required this.errorText,
    required this.onChanged,
  });

  final TextEditingController controller;
  final String label;
  final String hint;
  final String? errorText;
  final ValueChanged<String> onChanged;

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      keyboardType: const TextInputType.numberWithOptions(
        decimal: true,
        signed: true,
      ),
      inputFormatters: [
        FilteringTextInputFormatter.allow(RegExp(r'[0-9\.\-]')),
      ],
      onChanged: onChanged,
      decoration: InputDecoration(
        labelText: label,
        hintText: hint,
        prefixIcon: const Icon(Icons.my_location_outlined),
        errorText: errorText,
      ),
    );
  }
}

class _SelectedLocationSummary extends StatelessWidget {
  const _SelectedLocationSummary({
    required this.summary,
    required this.latitude,
    required this.longitude,
    required this.usesAddressResolution,
  });

  final String summary;
  final double? latitude;
  final double? longitude;
  final bool usesAddressResolution;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.secondaryAccent.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(AppRadius.lg),
        border: Border.all(
          color: AppColors.secondaryAccent.withValues(alpha: 0.28),
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(
            Icons.check_circle_outline_rounded,
            color: AppColors.secondaryAccent,
            size: 21,
          ),
          const SizedBox(width: AppSpacing.sm),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'SELECTED LOCATION',
                  style: Theme.of(context).textTheme.labelMedium?.copyWith(
                    color: AppColors.secondaryAccent,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 1.1,
                  ),
                ),
                const SizedBox(height: AppSpacing.xs),
                Text(
                  summary,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: AppColors.textSecondary,
                    height: 1.45,
                  ),
                ),
                if (usesAddressResolution) ...[
                  const SizedBox(height: AppSpacing.xs),
                  Text(
                    'Latitude and longitude will be resolved by the backend.',
                    style: Theme.of(context).textTheme.labelMedium?.copyWith(
                      color: AppColors.textMuted,
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _RoomSelector extends StatelessWidget {
  const _RoomSelector({
    required this.label,
    required this.icon,
    required this.value,
    required this.onChanged,
    this.isOptional = false,
  });

  final String label;
  final IconData icon;
  final int? value;
  final ValueChanged<int?> onChanged;
  final bool isOptional;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: _panelDecoration(),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: AppColors.secondaryAccent, size: 22),
          const SizedBox(height: AppSpacing.sm),
          Text(
            isOptional ? '$label (optional)' : label,
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
              color: AppColors.textSecondary,
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: AppSpacing.md),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _RoomActionButton(
                icon: Icons.remove_rounded,
                onTap: value == null || value == 0
                    ? null
                    : () => onChanged(value! - 1),
              ),
              Text(
                value?.toString() ?? '-',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.w700,
                ),
              ),
              _RoomActionButton(
                icon: Icons.add_rounded,
                onTap: value == 7 ? null : () => onChanged((value ?? 0) + 1),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _RoomActionButton extends StatelessWidget {
  const _RoomActionButton({required this.icon, required this.onTap});

  final IconData icon;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(AppRadius.pill),
      child: Container(
        width: 32,
        height: 32,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: AppColors.backgroundSecondary,
          border: Border.all(
            color: AppColors.textPrimary.withValues(alpha: 0.08),
          ),
        ),
        child: Icon(
          icon,
          size: 18,
          color: onTap == null ? AppColors.textMuted : AppColors.accent,
        ),
      ),
    );
  }
}

class _AmenityChip extends StatelessWidget {
  const _AmenityChip({
    required this.amenity,
    required this.isSelected,
    required this.onTap,
  });

  final AmenityChoice amenity;
  final bool isSelected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(AppRadius.pill),
      child: AnimatedContainer(
        duration: 180.ms,
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.md,
          vertical: 10,
        ),
        decoration: BoxDecoration(
          color: isSelected
              ? AppColors.secondaryAccent.withValues(alpha: 0.16)
              : AppColors.backgroundSecondary,
          borderRadius: BorderRadius.circular(AppRadius.pill),
          border: Border.all(
            color: isSelected
                ? AppColors.secondaryAccent
                : AppColors.textPrimary.withValues(alpha: 0.08),
          ),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (isSelected) ...[
              const Icon(
                Icons.check_rounded,
                color: AppColors.secondaryAccent,
                size: 16,
              ),
              const SizedBox(width: AppSpacing.xs),
            ],
            Text(
              amenity.label,
              style: Theme.of(context).textTheme.labelMedium?.copyWith(
                color: isSelected
                    ? AppColors.secondaryAccent
                    : AppColors.textSecondary,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ReviewPanel extends StatelessWidget {
  const _ReviewPanel({
    required this.title,
    required this.icon,
    required this.onEdit,
    required this.lines,
  });

  final String title;
  final IconData icon;
  final VoidCallback onEdit;
  final List<_ReviewLine> lines;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: _panelDecoration(),
      child: Column(
        children: [
          Row(
            children: [
              Icon(icon, color: AppColors.accent, size: 21),
              const SizedBox(width: AppSpacing.sm),
              Expanded(
                child: Text(
                  title,
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
              TextButton.icon(
                onPressed: onEdit,
                icon: const Icon(Icons.edit_outlined, size: 15),
                label: const Text('Edit'),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.sm),
          ...List.generate(lines.length, (index) {
            final line = lines[index];
            return Padding(
              padding: EdgeInsets.only(top: index == 0 ? 0 : AppSpacing.sm),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SizedBox(
                    width: 112,
                    child: Text(
                      line.label,
                      style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: AppColors.textMuted,
                      ),
                    ),
                  ),
                  Expanded(
                    child: Text(
                      line.value,
                      textAlign: TextAlign.right,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: AppColors.textSecondary,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }
}

class _ContextNote extends StatelessWidget {
  const _ContextNote({required this.icon, required this.text});

  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.secondaryAccent.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(AppRadius.lg),
      ),
      child: Row(
        children: [
          Icon(icon, color: AppColors.secondaryAccent),
          const SizedBox(width: AppSpacing.sm),
          Expanded(
            child: Text(
              text,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: AppColors.textSecondary,
                height: 1.45,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _BackendCoverageNotice extends StatelessWidget {
  const _BackendCoverageNotice();

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: Colors.amber.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(AppRadius.lg),
        border: Border.all(color: Colors.amber.withValues(alpha: 0.34)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.info_outline_rounded, color: Colors.amber, size: 21),
          const SizedBox(width: AppSpacing.sm),
          Expanded(
            child: Text(
              'This option exists in the Egypt dataset, but its governed '
              'backend valuation contract is still pending. You can complete '
              'the property profile; analysis will remain unavailable.',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: AppColors.textSecondary,
                height: 1.45,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _BottomAction extends StatelessWidget {
  const _BottomAction({
    required this.isEnabled,
    required this.isLoading,
    required this.isFinalStep,
    required this.onPressed,
  });

  final bool isEnabled;
  final bool isLoading;
  final bool isFinalStep;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.fromLTRB(
        AppSpacing.lg,
        AppSpacing.md,
        AppSpacing.lg,
        AppSpacing.md,
      ),
      decoration: BoxDecoration(
        color: AppColors.backgroundSecondary.withValues(alpha: 0.98),
        border: Border(
          top: BorderSide(color: AppColors.textPrimary.withValues(alpha: 0.07)),
        ),
      ),
      child: SafeArea(
        top: false,
        child: SizedBox(
          width: double.infinity,
          child: FilledButton(
            onPressed: isEnabled ? onPressed : null,
            child: isLoading
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(
                      strokeWidth: 2,
                      color: AppColors.backgroundPrimary,
                    ),
                  )
                : Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(isFinalStep ? 'Analyze Property' : 'Continue'),
                      const SizedBox(width: AppSpacing.sm),
                      Icon(
                        isFinalStep
                            ? Icons.auto_awesome_rounded
                            : Icons.arrow_forward_rounded,
                        size: 19,
                      ),
                    ],
                  ),
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
    return Container(
      width: 280,
      height: 280,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        gradient: RadialGradient(
          colors: [
            AppColors.accent.withValues(alpha: 0.08),
            Colors.transparent,
          ],
        ),
      ),
    );
  }
}

class _CategoryOption {
  const _CategoryOption({
    required this.category,
    required this.description,
    required this.icon,
    required this.accent,
  });

  final ValuationCategory category;
  final String description;
  final IconData icon;
  final Color accent;
}

class _ReviewLine {
  const _ReviewLine(this.label, this.value);

  final String label;
  final String value;
}

const _categoryOptions = [
  _CategoryOption(
    category: ValuationCategory.residentialBuy,
    description: 'Homes, villas, coastal units and land for sale',
    icon: Icons.home_work_outlined,
    accent: AppColors.accent,
  ),
  _CategoryOption(
    category: ValuationCategory.residentialRent,
    description: 'Monthly residential rental intelligence',
    icon: Icons.key_outlined,
    accent: AppColors.secondaryAccent,
  ),
  _CategoryOption(
    category: ValuationCategory.commercialBuy,
    description: 'Commercial assets and investment spaces for sale',
    icon: Icons.business_center_outlined,
    accent: Color(0xFF8DA2FF),
  ),
  _CategoryOption(
    category: ValuationCategory.commercialRent,
    description: 'Workplaces, retail and operating spaces for rent',
    icon: Icons.storefront_outlined,
    accent: Color(0xFFFFB86B),
  ),
];

BoxDecoration _panelDecoration({Color? accent}) {
  return BoxDecoration(
    color: AppColors.surface.withValues(alpha: 0.72),
    borderRadius: BorderRadius.circular(AppRadius.lg),
    border: Border.all(
      color:
          accent?.withValues(alpha: 0.3) ??
          AppColors.textPrimary.withValues(alpha: 0.07),
    ),
  );
}
