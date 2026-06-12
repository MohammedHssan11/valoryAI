import '../models/copilot_session.dart';

abstract interface class CopilotRepository {
  Future<CopilotMessage> respond({
    required String message,
    required int workspaceId,
    int? scenarioId,
    String? brokerSessionId,
    Map<String, dynamic>? toolInputs,
  });
}
