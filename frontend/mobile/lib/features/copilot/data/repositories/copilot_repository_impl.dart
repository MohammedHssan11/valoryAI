import 'package:flutter/foundation.dart';

import '../../domain/models/copilot_session.dart';
import '../../domain/repositories/copilot_repository.dart';
import '../datasources/copilot_remote_data_source.dart';

class CopilotRepositoryImpl implements CopilotRepository {
  const CopilotRepositoryImpl(this._remoteDataSource);

  final CopilotRemoteDataSource _remoteDataSource;

  @override
  Future<CopilotMessage> respond({
    required String message,
    required int workspaceId,
    int? scenarioId,
    String? brokerSessionId,
    Map<String, dynamic>? toolInputs,
  }) async {
    debugPrint(
      '[CopilotRepository] respond workspace=$workspaceId '
      'toolKeys=${(toolInputs ?? {}).keys.toList()}',
    );
    final rawEnvelope = await _remoteDataSource.respond(
      message: message,
      workspaceId: workspaceId,
      scenarioId: scenarioId,
      brokerSessionId: brokerSessionId,
      toolInputs: toolInputs,
    );
    return _mapEnvelopeToMessage(rawEnvelope);
  }

  CopilotMessage _mapEnvelopeToMessage(Map<String, dynamic> envelope) {
    final responseId =
        envelope['response_id'] as String? ??
        'msg_${DateTime.now().millisecondsSinceEpoch}';
    final deliveryMode =
        envelope['delivery_mode'] as String? ?? 'DETERMINISTIC_FALLBACK';
    final responseData = envelope['response'];
    final status = envelope['status'] as String?;

    String content = '';
    PropertySummaryCardData? propertySummary;
    ConfidenceCardData? confidence;
    List<EvidenceCardData>? evidenceDrivers;
    List<ComparableReferenceData>? comparables;
    MarketInsightCardData? marketInsight;

    if (deliveryMode == 'ACCESS_DENIED') {
      content =
          'I could not access the requested Copilot context. Please check the selected workspace and try again.';
    } else if (deliveryMode == 'GROUNDED_NARRATION' && responseData is String) {
      content = responseData;
    } else if (responseData is Map<String, dynamic>) {
      final compositionStatus =
          responseData['composition_status'] as String? ?? status ?? '';
      final failedTools = responseData['failed_tools'] as List<dynamic>? ?? [];
      content = _messageForComposition(compositionStatus, failedTools);
      final sections = responseData['response_sections'];
      if (sections is Map<String, dynamic>) {
        content = _messageForSections(sections, fallback: content);
        final fairValue = sections['fair_value'];
        if (fairValue is Map<String, dynamic>) {
          final fairPrice = fairValue['fair_price'];
          final valuationIds = fairValue['valuation_ids'];
          final valuationId = valuationIds is List && valuationIds.isNotEmpty
              ? valuationIds.first
              : null;
          if (fairPrice is num && valuationId is String) {
            propertySummary ??= PropertySummaryCardData(
              valuationId: valuationId,
              fairPrice: fairPrice.toInt(),
              valueBasis: 'TruthLayer',
            );
          }
        }
      }
      final toolOutputs = responseData['tool_outputs'] as List<dynamic>? ?? [];
      final fullEvidence =
          responseData['full_evidence'] as Map<String, dynamic>?;

      for (final output in toolOutputs) {
        if (output is! Map<String, dynamic>) {
          continue;
        }
        final toolName = output['tool_name'] as String?;
        final payload = output['payload'] as Map<String, dynamic>? ?? {};
        if (toolName != 'valuation') {
          continue;
        }

        final valuationId = payload['valuation_id'];
        final fairPrice = payload['fair_price'];
        if (valuationId is String && fairPrice is num) {
          propertySummary = PropertySummaryCardData(
            valuationId: valuationId,
            fairPrice: fairPrice.toInt(),
            valueBasis: payload['value_basis'] as String? ?? '',
          );
        }

        final confidenceScore = payload['confidence_level_value'];
        final confidenceLabel = payload['confidence_level'];
        if (valuationId is String &&
            confidenceScore is num &&
            confidenceLabel is String) {
          confidence = ConfidenceCardData(
            valuationId: valuationId,
            score: confidenceScore.toDouble(),
            label: confidenceLabel,
            factors: const {},
          );
        }
      }

      if (fullEvidence != null) {
        final rawComparables =
            fullEvidence['comparables'] as List<dynamic>? ?? [];
        comparables = rawComparables
            .whereType<Map<String, dynamic>>()
            .map((entry) => entry['comparable'])
            .whereType<Map<String, dynamic>>()
            .map(_mapComparable)
            .whereType<ComparableReferenceData>()
            .toList();
        if (comparables.isEmpty) {
          comparables = null;
        }

        final rawDrivers =
            fullEvidence['feature_drivers'] as List<dynamic>? ?? [];
        evidenceDrivers = rawDrivers
            .whereType<Map<String, dynamic>>()
            .map((entry) => entry['feature_driver'])
            .whereType<Map<String, dynamic>>()
            .map(_mapEvidenceDriver)
            .whereType<EvidenceCardData>()
            .toList();
        if (evidenceDrivers.isEmpty) {
          evidenceDrivers = null;
        }

        final rawInsights =
            fullEvidence['market_insights'] as List<dynamic>? ?? [];
        if (rawInsights.isNotEmpty &&
            rawInsights.first is Map<String, dynamic>) {
          final insight = rawInsights.first as Map<String, dynamic>;
          marketInsight = MarketInsightCardData(
            activeCompounds: _stringList(insight['active_compounds']),
            activeAreas: _stringList(insight['active_areas']),
            statements: _stringList(insight['statements']),
          );
        }
      }
    } else if (responseData is String) {
      content = responseData;
    }

    if (content.trim().isEmpty) {
      content =
          'Copilot finished without a narrative response. Please retry or ask a more specific question.';
    }

    return CopilotMessage(
      id: responseId,
      role: 'assistant',
      content: content,
      timestamp: DateTime.now(),
      propertySummary: propertySummary,
      confidence: confidence,
      evidenceDrivers: evidenceDrivers,
      comparables: comparables,
      marketInsight: marketInsight,
    );
  }

  String _messageForSections(
    Map<String, dynamic> sections, {
    required String fallback,
  }) {
    final action = sections['recommended_action'];
    final fairValue = sections['fair_value'];
    final confidence = sections['confidence'];
    final price = fairValue is Map<String, dynamic> ? fairValue['fair_price'] : null;
    final level = confidence is Map<String, dynamic> ? confidence['level'] : null;
    if (action is String && price is num) {
      final confidenceText = level is String ? ' with $level confidence' : '';
      return '$action: fair value EGP ${price.toInt()}$confidenceText.';
    }
    if (price is num) {
      final confidenceText = level is String ? ' with $level confidence' : '';
      return 'Fair value EGP ${price.toInt()}$confidenceText.';
    }
    return fallback;
  }

  String _messageForComposition(
    String compositionStatus,
    List<dynamic> failedTools,
  ) {
    if (failedTools.isEmpty) {
      return compositionStatus.isEmpty
          ? 'Copilot completed the request.'
          : compositionStatus;
    }

    final failures = failedTools.whereType<Map<String, dynamic>>().toList();
    final hasMissingToolInput = failures.any(
      (failure) => failure['failure_category'] == 'MISSING_TOOL_INPUT',
    );
    if (hasMissingToolInput) {
      return 'I need a saved workspace property before I can run that Copilot tool. Select or save a property in the active workspace, then retry.';
    }

    final toolNames = failures
        .map((failure) => failure['tool_name'])
        .whereType<String>()
        .toSet()
        .toList();
    if (toolNames.isNotEmpty) {
      return 'Copilot could not complete ${toolNames.join(', ')}. Please retry in a moment.';
    }

    return compositionStatus.isEmpty
        ? 'Copilot could not complete the requested analysis.'
        : compositionStatus;
  }

  ComparableReferenceData? _mapComparable(Map<String, dynamic> item) {
    final comparableId = item['comparable_id'];
    final price = item['price'];
    if (comparableId is! String || price is! num) {
      return null;
    }
    return ComparableReferenceData(
      comparableId: comparableId,
      price: price.toInt(),
      sizeSqm: (item['size_sqm'] as num?)?.toDouble(),
      distanceKm: (item['distance_km'] as num?)?.toDouble(),
      similarityScore: (item['similarity_score'] as num?)?.toDouble(),
      propertyType: item['property_type'] as String?,
      compoundName: item['compound_name'] as String?,
    );
  }

  EvidenceCardData? _mapEvidenceDriver(Map<String, dynamic> item) {
    final label = item['name'];
    final value = item['impact_percentage'];
    final direction = item['direction'];
    if (label is! String || value is! num || direction is! String) {
      return null;
    }
    return EvidenceCardData(
      label: label,
      value: value.toDouble(),
      direction: direction,
    );
  }

  List<String> _stringList(dynamic value) {
    return value is List<dynamic> ? value.whereType<String>().toList() : [];
  }
}
