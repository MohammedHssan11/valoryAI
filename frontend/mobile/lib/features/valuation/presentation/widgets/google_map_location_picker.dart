import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_radius.dart';
import '../../../../app/theme/app_spacing.dart';

class GoogleMapLocationPicker extends StatefulWidget {
  const GoogleMapLocationPicker({super.key, this.initialLocation});

  final LatLng? initialLocation;

  @override
  State<GoogleMapLocationPicker> createState() =>
      _GoogleMapLocationPickerState();
}

class _GoogleMapLocationPickerState extends State<GoogleMapLocationPicker> {
  static const _cairo = LatLng(30.0444, 31.2357);

  late LatLng _selectedLocation;
  final _latitudeController = TextEditingController();
  final _longitudeController = TextEditingController();
  GoogleMapController? _mapController;

  @override
  void initState() {
    super.initState();
    _selectedLocation = widget.initialLocation ?? _cairo;
    _syncCoordinateFields(_selectedLocation);
  }

  @override
  void dispose() {
    _latitudeController.dispose();
    _longitudeController.dispose();
    _mapController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      top: false,
      child: SizedBox(
        height: MediaQuery.sizeOf(context).height * 0.78,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(
                AppSpacing.lg,
                AppSpacing.md,
                AppSpacing.lg,
                AppSpacing.md,
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    width: 42,
                    height: 4,
                    margin: const EdgeInsets.only(
                      left: 132,
                      bottom: AppSpacing.md,
                    ),
                    decoration: BoxDecoration(
                      color: AppColors.textMuted.withValues(alpha: 0.38),
                      borderRadius: BorderRadius.circular(AppRadius.pill),
                    ),
                  ),
                  Text(
                    'Pick Location On Map',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  Text(
                    'Tap the exact property position or type coordinates directly.',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: AppColors.textMuted,
                    ),
                  ),
                ],
              ),
            ),
            Expanded(
              child: Stack(
                children: [
                  GoogleMap(
                    onMapCreated: (controller) {
                      _mapController = controller;
                    },
                    initialCameraPosition: CameraPosition(
                      target: _selectedLocation,
                      zoom: 12.5,
                    ),
                    myLocationButtonEnabled: false,
                    zoomControlsEnabled: false,
                    onTap: _selectFromMap,
                    markers: {
                      Marker(
                        markerId: const MarkerId('valuation-location'),
                        position: _selectedLocation,
                      ),
                    },
                  ),
                  Positioned(
                    left: AppSpacing.md,
                    right: AppSpacing.md,
                    bottom: AppSpacing.md,
                    child: Container(
                      padding: const EdgeInsets.all(AppSpacing.md),
                      decoration: BoxDecoration(
                        color: AppColors.backgroundSecondary.withValues(
                          alpha: 0.96,
                        ),
                        borderRadius: BorderRadius.circular(AppRadius.lg),
                        border: Border.all(
                          color: AppColors.accent.withValues(alpha: 0.28),
                        ),
                      ),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Expanded(
                                child: _MapCoordinateTextField(
                                  controller: _latitudeController,
                                  label: 'Latitude',
                                  errorText: _latitudeErrorText,
                                  onChanged: _onCoordinateChanged,
                                ),
                              ),
                              const SizedBox(width: AppSpacing.sm),
                              Expanded(
                                child: _MapCoordinateTextField(
                                  controller: _longitudeController,
                                  label: 'Longitude',
                                  errorText: _longitudeErrorText,
                                  onChanged: _onCoordinateChanged,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: AppSpacing.md),
                          Row(
                            children: [
                              const Icon(
                                Icons.location_on_rounded,
                                color: AppColors.accent,
                              ),
                              const SizedBox(width: AppSpacing.sm),
                              Expanded(
                                child: Text(
                                  '${_selectedLocation.latitude.toStringAsFixed(6)}, '
                                  '${_selectedLocation.longitude.toStringAsFixed(6)}',
                                  style: Theme.of(context).textTheme.bodyMedium
                                      ?.copyWith(
                                        color: AppColors.textPrimary,
                                        fontWeight: FontWeight.w700,
                                      ),
                                ),
                              ),
                              FilledButton(
                                onPressed: _hasValidCoordinates
                                    ? () {
                                        Navigator.of(
                                          context,
                                        ).pop(_selectedLocation);
                                      }
                                    : null,
                                child: const Text('Use Pin'),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  bool get _hasValidCoordinates =>
      _latitudeErrorText == null &&
      _longitudeErrorText == null &&
      _latitudeController.text.trim().isNotEmpty &&
      _longitudeController.text.trim().isNotEmpty;

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

  void _selectFromMap(LatLng location) {
    setState(() {
      _selectedLocation = location;
      _syncCoordinateFields(location);
    });
  }

  void _onCoordinateChanged(String _) {
    final latitude = double.tryParse(_latitudeController.text.trim());
    final longitude = double.tryParse(_longitudeController.text.trim());
    setState(() {
      if (latitude != null &&
          longitude != null &&
          _isCoordinateInRange(latitude, -90, 90) &&
          _isCoordinateInRange(longitude, -180, 180)) {
        final location = LatLng(latitude, longitude);
        _selectedLocation = location;
        _mapController?.animateCamera(CameraUpdate.newLatLng(location));
      }
    });
  }

  void _syncCoordinateFields(LatLng location) {
    _latitudeController.text = location.latitude.toStringAsFixed(6);
    _longitudeController.text = location.longitude.toStringAsFixed(6);
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

class _MapCoordinateTextField extends StatelessWidget {
  const _MapCoordinateTextField({
    required this.controller,
    required this.label,
    required this.errorText,
    required this.onChanged,
  });

  final TextEditingController controller;
  final String label;
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
        errorText: errorText,
        prefixIcon: const Icon(Icons.pin_drop_outlined),
      ),
    );
  }
}
