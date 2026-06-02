import 'dart:convert';

class CopilotSession {
  final String id;
  final String title;
  final List<CopilotMessage> messages;
  final bool isPinned;
  final DateTime createdAt;
  final int workspaceId;

  const CopilotSession({
    required this.id,
    required this.title,
    required this.messages,
    this.isPinned = false,
    required this.createdAt,
    required this.workspaceId,
  });

  CopilotSession copyWith({
    String? id,
    String? title,
    List<CopilotMessage>? messages,
    bool? isPinned,
    DateTime? createdAt,
    int? workspaceId,
  }) {
    return CopilotSession(
      id: id ?? this.id,
      title: title ?? this.title,
      messages: messages ?? this.messages,
      isPinned: isPinned ?? this.isPinned,
      createdAt: createdAt ?? this.createdAt,
      workspaceId: workspaceId ?? this.workspaceId,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'title': title,
      'messages': messages.map((x) => x.toMap()).toList(),
      'isPinned': isPinned,
      'createdAt': createdAt.toIso8601String(),
      'workspaceId': workspaceId,
    };
  }

  factory CopilotSession.fromMap(Map<String, dynamic> map) {
    return CopilotSession(
      id: map['id'] as String,
      title: map['title'] as String,
      messages: List<CopilotMessage>.from(
        (map['messages'] as List<dynamic>).map<CopilotMessage>(
          (x) => CopilotMessage.fromMap(x as Map<String, dynamic>),
        ),
      ),
      isPinned: map['isPinned'] as bool? ?? false,
      createdAt: DateTime.parse(map['createdAt'] as String),
      workspaceId: map['workspaceId'] as int? ?? 1,
    );
  }

  String toJson() => json.encode(toMap());

  factory CopilotSession.fromJson(String source) =>
      CopilotSession.fromMap(json.decode(source) as Map<String, dynamic>);
}

class CopilotMessage {
  final String id;
  final String role; // 'user' | 'assistant'
  final String content;
  final DateTime timestamp;
  final bool isLoading;
  final String? error;

  // Rich response components
  final PropertySummaryCardData? propertySummary;
  final ConfidenceCardData? confidence;
  final List<EvidenceCardData>? evidenceDrivers;
  final List<ComparableReferenceData>? comparables;
  final MarketInsightCardData? marketInsight;

  const CopilotMessage({
    required this.id,
    required this.role,
    required this.content,
    required this.timestamp,
    this.isLoading = false,
    this.error,
    this.propertySummary,
    this.confidence,
    this.evidenceDrivers,
    this.comparables,
    this.marketInsight,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'role': role,
      'content': content,
      'timestamp': timestamp.toIso8601String(),
      'isLoading': isLoading,
      'error': error,
      'propertySummary': propertySummary?.toMap(),
      'confidence': confidence?.toMap(),
      'evidenceDrivers': evidenceDrivers?.map((x) => x.toMap()).toList(),
      'comparables': comparables?.map((x) => x.toMap()).toList(),
      'marketInsight': marketInsight?.toMap(),
    };
  }

  factory CopilotMessage.fromMap(Map<String, dynamic> map) {
    return CopilotMessage(
      id: map['id'] as String,
      role: map['role'] as String,
      content: map['content'] as String,
      timestamp: DateTime.parse(map['timestamp'] as String),
      isLoading: map['isLoading'] as bool? ?? false,
      error: map['error'] as String?,
      propertySummary: map['propertySummary'] != null
          ? PropertySummaryCardData.fromMap(map['propertySummary'] as Map<String, dynamic>)
          : null,
      confidence: map['confidence'] != null
          ? ConfidenceCardData.fromMap(map['confidence'] as Map<String, dynamic>)
          : null,
      evidenceDrivers: map['evidenceDrivers'] != null
          ? List<EvidenceCardData>.from(
              (map['evidenceDrivers'] as List<dynamic>).map<EvidenceCardData>(
                (x) => EvidenceCardData.fromMap(x as Map<String, dynamic>),
              ),
            )
          : null,
      comparables: map['comparables'] != null
          ? List<ComparableReferenceData>.from(
              (map['comparables'] as List<dynamic>).map<ComparableReferenceData>(
                (x) => ComparableReferenceData.fromMap(x as Map<String, dynamic>),
              ),
            )
          : null,
      marketInsight: map['marketInsight'] != null
          ? MarketInsightCardData.fromMap(map['marketInsight'] as Map<String, dynamic>)
          : null,
    );
  }
}

class PropertySummaryCardData {
  final String valuationId;
  final int fairPrice;
  final String? propertyType;
  final String? areaName;
  final int? bedrooms;
  final int? bathrooms;
  final double? sizeSqm;
  final String valueBasis;

  const PropertySummaryCardData({
    required this.valuationId,
    required this.fairPrice,
    this.propertyType,
    this.areaName,
    this.bedrooms,
    this.bathrooms,
    this.sizeSqm,
    required this.valueBasis,
  });

  Map<String, dynamic> toMap() {
    return {
      'valuationId': valuationId,
      'fairPrice': fairPrice,
      'propertyType': propertyType,
      'areaName': areaName,
      'bedrooms': bedrooms,
      'bathrooms': bathrooms,
      'sizeSqm': sizeSqm,
      'valueBasis': valueBasis,
    };
  }

  factory PropertySummaryCardData.fromMap(Map<String, dynamic> map) {
    return PropertySummaryCardData(
      valuationId: map['valuationId'] as String,
      fairPrice: map['fairPrice'] as int,
      propertyType: map['propertyType'] as String?,
      areaName: map['areaName'] as String?,
      bedrooms: map['bedrooms'] as int?,
      bathrooms: map['bathrooms'] as int?,
      sizeSqm: (map['sizeSqm'] as num?)?.toDouble(),
      valueBasis: map['valueBasis'] as String? ?? 'Estimated Fair Value',
    );
  }
}

class ConfidenceCardData {
  final String valuationId;
  final double score;
  final String label;
  final Map<String, double> factors;

  const ConfidenceCardData({
    required this.valuationId,
    required this.score,
    required this.label,
    required this.factors,
  });

  Map<String, dynamic> toMap() {
    return {
      'valuationId': valuationId,
      'score': score,
      'label': label,
      'factors': factors,
    };
  }

  factory ConfidenceCardData.fromMap(Map<String, dynamic> map) {
    return ConfidenceCardData(
      valuationId: map['valuationId'] as String,
      score: (map['score'] as num).toDouble(),
      label: map['label'] as String,
      factors: Map<String, double>.from(
        (map['factors'] as Map<dynamic, dynamic>).map(
          (k, v) => MapEntry(k as String, (v as num).toDouble()),
        ),
      ),
    );
  }
}

class EvidenceCardData {
  final String label;
  final double value;
  final String direction;

  const EvidenceCardData({
    required this.label,
    required this.value,
    required this.direction,
  });

  Map<String, dynamic> toMap() {
    return {
      'label': label,
      'value': value,
      'direction': direction,
    };
  }

  factory EvidenceCardData.fromMap(Map<String, dynamic> map) {
    return EvidenceCardData(
      label: map['label'] as String,
      value: (map['value'] as num).toDouble(),
      direction: map['direction'] as String,
    );
  }
}

class ComparableReferenceData {
  final String comparableId;
  final int price;
  final double sizeSqm;
  final double distanceKm;
  final double similarityScore;
  final String? propertyType;
  final String? compoundName;

  const ComparableReferenceData({
    required this.comparableId,
    required this.price,
    required this.sizeSqm,
    required this.distanceKm,
    required this.similarityScore,
    this.propertyType,
    this.compoundName,
  });

  Map<String, dynamic> toMap() {
    return {
      'comparableId': comparableId,
      'price': price,
      'sizeSqm': sizeSqm,
      'distanceKm': distanceKm,
      'similarityScore': similarityScore,
      'propertyType': propertyType,
      'compoundName': compoundName,
    };
  }

  factory ComparableReferenceData.fromMap(Map<String, dynamic> map) {
    return ComparableReferenceData(
      comparableId: map['comparableId'] as String,
      price: map['price'] as int,
      sizeSqm: (map['sizeSqm'] as num).toDouble(),
      distanceKm: (map['distanceKm'] as num).toDouble(),
      similarityScore: (map['similarityScore'] as num).toDouble(),
      propertyType: map['propertyType'] as String?,
      compoundName: map['compoundName'] as String?,
    );
  }
}

class MarketInsightCardData {
  final String demandTrend;
  final String marketStrength;
  final List<String> activeCompounds;
  final List<String> activeAreas;
  final List<String> statements;

  const MarketInsightCardData({
    required this.demandTrend,
    required this.marketStrength,
    required this.activeCompounds,
    required this.activeAreas,
    required this.statements,
  });

  Map<String, dynamic> toMap() {
    return {
      'demandTrend': demandTrend,
      'marketStrength': marketStrength,
      'activeCompounds': activeCompounds,
      'activeAreas': activeAreas,
      'statements': statements,
    };
  }

  factory MarketInsightCardData.fromMap(Map<String, dynamic> map) {
    return MarketInsightCardData(
      demandTrend: map['demandTrend'] as String,
      marketStrength: map['marketStrength'] as String,
      activeCompounds: List<String>.from(map['activeCompounds'] as List<dynamic>),
      activeAreas: List<String>.from(map['activeAreas'] as List<dynamic>),
      statements: List<String>.from(map['statements'] as List<dynamic>),
    );
  }
}
