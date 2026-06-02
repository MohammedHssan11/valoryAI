import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';

import '../../../../app/router/route_names.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_radius.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../valuation/domain/models/valuation_response.dart';
import '../../data/datasources/copilot_remote_data_source.dart';
import '../../data/repositories/copilot_repository_impl.dart';
import '../../domain/models/copilot_session.dart';
import '../../domain/repositories/copilot_repository.dart';
import '../../../workspace/presentation/state/workspace_state_manager.dart';

// Singleton/Static Session Store to persist state during the app session
class CopilotSessionStore {
  CopilotSessionStore._();

  static final List<CopilotSession> sessions = _generateInitialSessions();
  static CopilotSession? activeSession;

  static List<CopilotSession> _generateInitialSessions() {
    final now = DateTime.now();
    return [
      CopilotSession(
        id: 'session_mivida',
        title: 'Mivida Valuation Review',
        isPinned: true,
        createdAt: now.subtract(const Duration(hours: 4)),
        workspaceId: 1,
        messages: [
          CopilotMessage(
            id: 'msg_u1',
            role: 'user',
            content: 'Why is confidence only 82%?',
            timestamp: now.subtract(const Duration(hours: 4)),
          ),
          CopilotMessage(
            id: 'msg_a1',
            role: 'assistant',
            content: '### Model Confidence Analysis\nThe valuation model yielded an 82% confidence score due to local pricing dispersion among recent comps in Sheikh Zayed. The location resolution is strong, but aged listings in the cluster introduce a minor discount.',
            timestamp: now.subtract(const Duration(hours: 4, minutes: 59)),
            confidence: const ConfidenceCardData(
              valuationId: 'val_mivida',
              score: 0.82,
              label: 'High Confidence',
              factors: {
                'Location Resolution': 0.92,
                'Transaction Density': 0.84,
                'Submarket Consistency': 0.70,
              },
            ),
          ),
        ],
      ),
      CopilotSession(
        id: 'session_new_cairo',
        title: 'New Cairo Market Analysis',
        isPinned: false,
        createdAt: now.subtract(const Duration(days: 1)),
        workspaceId: 1,
        messages: [
          CopilotMessage(
            id: 'msg_u2',
            role: 'user',
            content: 'Market outlook for New Cairo.',
            timestamp: now.subtract(const Duration(days: 1)),
          ),
          CopilotMessage(
            id: 'msg_a2',
            role: 'assistant',
            content: '### Regional Market Outlook\nNew Cairo exhibits premium pricing indicators and low inventory aging. Demand is highly concentrated around major compounds.',
            timestamp: now.subtract(const Duration(days: 1, minutes: 1)),
            marketInsight: const MarketInsightCardData(
              demandTrend: 'High',
              marketStrength: 'Active',
              activeCompounds: ['Mivida', 'Eastown', 'Palm Hills'],
              activeAreas: ['Golden Square', 'Fifth Settlement'],
              statements: [
                'Master-planned compounds command a 12% pricing premium.',
                'Average premium rental yields stabilized at 6.8%.',
                'Listing velocity increased by 14% quarter-over-quarter.',
              ],
            ),
          ),
        ],
      ),
      CopilotSession(
        id: 'session_comps',
        title: 'Sheikh Zayed Apartment Comps',
        isPinned: false,
        createdAt: now.subtract(const Duration(days: 3)),
        workspaceId: 1,
        messages: [
          CopilotMessage(
            id: 'msg_u3',
            role: 'user',
            content: 'Show comparable properties.',
            timestamp: now.subtract(const Duration(days: 3)),
          ),
          CopilotMessage(
            id: 'msg_a3',
            role: 'assistant',
            content: '### Comparable Evidence Retrieval\nI have isolated the top 3 high-similarity comparable transaction controls. These represent the primary reference points used by our valuation algorithms.',
            timestamp: now.subtract(const Duration(days: 3, minutes: 1)),
            comparables: const [
              ComparableReferenceData(
                comparableId: 'COMP-729A',
                price: 8200000,
                sizeSqm: 175,
                distanceKm: 0.4,
                similarityScore: 0.94,
                propertyType: 'Apartment',
                compoundName: 'Mivida',
              ),
              ComparableReferenceData(
                comparableId: 'COMP-110C',
                price: 8600000,
                sizeSqm: 190,
                distanceKm: 0.9,
                similarityScore: 0.88,
                propertyType: 'Apartment',
                compoundName: 'Eastown',
              ),
            ],
          ),
        ],
      ),
    ];
  }
}

class CopilotScreen extends StatefulWidget {
  const CopilotScreen({super.key, this.valuationResponse});

  final ValuationResponse? valuationResponse;

  @override
  State<CopilotScreen> createState() => _CopilotScreenState();
}

class _CopilotScreenState extends State<CopilotScreen> {
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final CopilotRepository _repository = CopilotRepositoryImpl(CopilotRemoteDataSource());

  late List<CopilotSession> _sessions;
  CopilotSession? _currentSession;
  ValuationResponse? _activeValuationContext;

  bool _isLoading = false;
  String? _searchQuery;

  @override
  void initState() {
    super.initState();
    _sessions = CopilotSessionStore.sessions;
    _activeValuationContext = widget.valuationResponse;

    // Load active session, or create one if store is empty
    if (CopilotSessionStore.activeSession != null) {
      _currentSession = CopilotSessionStore.activeSession;
    } else if (_sessions.isNotEmpty) {
      _currentSession = _sessions.first;
      CopilotSessionStore.activeSession = _currentSession;
    } else {
      _createNewSession(isInitial: true);
    }
  }

  @override
  void dispose() {
    _messageController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: 300.ms,
          curve: Curves.easeOutCubic,
        );
      });
    }
  }

  void _createNewSession({bool isInitial = false}) {
    final now = DateTime.now();
    final newSession = CopilotSession(
      id: 'session_${now.millisecondsSinceEpoch}',
      title: 'New Chat Session',
      messages: const [],
      createdAt: now,
      workspaceId: 1,
    );

    setState(() {
      _sessions.insert(0, newSession);
      _currentSession = newSession;
      CopilotSessionStore.activeSession = newSession;
    });

    if (!isInitial) {
      _scrollToBottom();
    }
  }

  void _renameSession(CopilotSession session, String newTitle) {
    if (newTitle.trim().isEmpty) return;
    setState(() {
      final index = _sessions.indexWhere((s) => s.id == session.id);
      if (index != -1) {
        _sessions[index] = _sessions[index].copyWith(title: newTitle.trim());
        if (_currentSession?.id == session.id) {
          _currentSession = _sessions[index];
          CopilotSessionStore.activeSession = _currentSession;
        }
      }
    });
  }

  void _deleteSession(CopilotSession session) {
    setState(() {
      _sessions.removeWhere((s) => s.id == session.id);
      if (_currentSession?.id == session.id) {
        _currentSession = _sessions.isNotEmpty ? _sessions.first : null;
        CopilotSessionStore.activeSession = _currentSession;
      }
      if (_currentSession == null) {
        _createNewSession();
      }
    });
  }

  void _togglePinSession(CopilotSession session) {
    setState(() {
      final index = _sessions.indexWhere((s) => s.id == session.id);
      if (index != -1) {
        _sessions[index] = _sessions[index].copyWith(isPinned: !_sessions[index].isPinned);
        if (_currentSession?.id == session.id) {
          _currentSession = _sessions[index];
          CopilotSessionStore.activeSession = _currentSession;
        }
      }
    });
  }

  Future<void> _sendMessage(String text) async {
    if (text.trim().isEmpty || _isLoading || _currentSession == null) return;

    final userMessageText = text.trim();
    _messageController.clear();

    final userMessage = CopilotMessage(
      id: 'msg_user_${DateTime.now().millisecondsSinceEpoch}',
      role: 'user',
      content: userMessageText,
      timestamp: DateTime.now(),
    );

    final loadingMessage = CopilotMessage(
      id: 'msg_load_${DateTime.now().millisecondsSinceEpoch}',
      role: 'assistant',
      content: '',
      timestamp: DateTime.now(),
      isLoading: true,
    );

    setState(() {
      final updatedMessages = List<CopilotMessage>.from(_currentSession!.messages)
        ..add(userMessage)
        ..add(loadingMessage);

      // Automatically rename session from the first message if it is default
      String newTitle = _currentSession!.title;
      if (_currentSession!.title == 'New Chat Session' && _currentSession!.messages.isEmpty) {
        newTitle = userMessageText.length > 25
            ? '${userMessageText.substring(0, 25)}...'
            : userMessageText;
      }

      final index = _sessions.indexWhere((s) => s.id == _currentSession!.id);
      if (index != -1) {
        _sessions[index] = _sessions[index].copyWith(
          messages: updatedMessages,
          title: newTitle,
        );
        _currentSession = _sessions[index];
        CopilotSessionStore.activeSession = _currentSession;
      }
      _isLoading = true;
    });

    _scrollToBottom();

    // Map Valuation Response context to tool_inputs if available
    Map<String, dynamic>? toolInputs;
    if (_activeValuationContext != null) {
      toolInputs = {
        'valuation': _activeValuationContext!.rawData,
      };
    }

    try {
      final activeWorkspaceId = WorkspaceStateManager.instance.activeWorkspace?.id ?? _currentSession!.workspaceId;
      final response = await _repository.respond(
        message: userMessageText,
        workspaceId: activeWorkspaceId,
        toolInputs: toolInputs,
      );

      setState(() {
        final messagesWithoutLoading = List<CopilotMessage>.from(_currentSession!.messages)
          ..removeLast() // Remove loading message
          ..add(response);

        final index = _sessions.indexWhere((s) => s.id == _currentSession!.id);
        if (index != -1) {
          _sessions[index] = _sessions[index].copyWith(messages: messagesWithoutLoading);
          _currentSession = _sessions[index];
          CopilotSessionStore.activeSession = _currentSession;
        }
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        final errorMsg = e.toString();
        final errorResponse = CopilotMessage(
          id: 'msg_err_${DateTime.now().millisecondsSinceEpoch}',
          role: 'assistant',
          content: 'I encountered an error connecting to the orchestrator. Please retry.',
          timestamp: DateTime.now(),
          error: errorMsg,
        );

        final messagesWithoutLoading = List<CopilotMessage>.from(_currentSession!.messages)
          ..removeLast()
          ..add(errorResponse);

        final index = _sessions.indexWhere((s) => s.id == _currentSession!.id);
        if (index != -1) {
          _sessions[index] = _sessions[index].copyWith(messages: messagesWithoutLoading);
          _currentSession = _sessions[index];
          CopilotSessionStore.activeSession = _currentSession;
        }
        _isLoading = false;
      });
    }

    _scrollToBottom();
  }

  void _showRenameDialog(CopilotSession session) {
    final controller = TextEditingController(text: session.title);
    showDialog<void>(
      context: context,
      builder: (context) {
        return AlertDialog(
          backgroundColor: AppColors.surface,
          title: Text(
            'Rename Session',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.bold,
                ),
          ),
          content: TextField(
            controller: controller,
            autofocus: true,
            style: const TextStyle(color: AppColors.textPrimary),
            decoration: InputDecoration(
              hintText: 'Enter session name',
              hintStyle: const TextStyle(color: AppColors.textMuted),
              enabledBorder: UnderlineInputBorder(
                borderSide: BorderSide(color: AppColors.textMuted.withValues(alpha: 0.3)),
              ),
              focusedBorder: const UnderlineInputBorder(
                borderSide: BorderSide(color: AppColors.accent),
              ),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel', style: TextStyle(color: AppColors.textMuted)),
            ),
            TextButton(
              onPressed: () {
                _renameSession(session, controller.text);
                Navigator.pop(context);
              },
              child: const Text('Rename', style: TextStyle(color: AppColors.accent)),
            ),
          ],
        );
      },
    );
  }

  void _showDeleteConfirmDialog(CopilotSession session) {
    showDialog<void>(
      context: context,
      builder: (context) {
        return AlertDialog(
          backgroundColor: AppColors.surface,
          title: Text(
            'Delete Session',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: AppColors.textPrimary,
                  fontWeight: FontWeight.bold,
                ),
          ),
          content: const Text(
            'Are you sure you want to permanently delete this advisor session?',
            style: TextStyle(color: AppColors.textSecondary),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel', style: TextStyle(color: AppColors.textMuted)),
            ),
            TextButton(
              onPressed: () {
                _deleteSession(session);
                Navigator.pop(context);
              },
              child: const Text('Delete', style: TextStyle(color: Colors.redAccent)),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final filteredSessions = _sessions.where((s) {
      if (_searchQuery == null || _searchQuery!.trim().isEmpty) return true;
      return s.title.toLowerCase().contains(_searchQuery!.toLowerCase());
    }).toList();

    final pinnedSessions = filteredSessions.where((s) => s.isPinned).toList();
    final recentSessions = filteredSessions.where((s) => !s.isPinned).toList();

    return Scaffold(
      backgroundColor: AppColors.backgroundPrimary,
      drawer: _buildSidebarDrawer(pinnedSessions, recentSessions),
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
          child: Column(
            children: [
              _buildTopBar(),
              _buildActiveContextBanner(),
              Expanded(
                child: Stack(
                  children: [
                    const Positioned(
                      top: 40,
                      right: -130,
                      child: _AmbientGlow(color: AppColors.accent, size: 280, opacity: 0.08),
                    ),
                    const Positioned(
                      bottom: 80,
                      left: -140,
                      child: _AmbientGlow(color: AppColors.secondaryAccent, size: 260, opacity: 0.04),
                    ),
                    _currentSession == null || _currentSession!.messages.isEmpty
                        ? _buildEmptyState()
                        : _buildMessageCanvas(),
                  ],
                ),
              ),
              _buildMessageComposer(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTopBar() {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.md,
        vertical: AppSpacing.sm,
      ),
      decoration: BoxDecoration(
        border: Border(
          bottom: BorderSide(color: AppColors.textPrimary.withValues(alpha: 0.06)),
        ),
      ),
      child: Row(
        children: [
          Builder(
            builder: (context) => IconButton(
              icon: const Icon(Icons.menu_rounded, color: AppColors.textPrimary),
              onPressed: () => Scaffold.of(context).openDrawer(),
            ),
          ),
          const SizedBox(width: AppSpacing.sm),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  _currentSession?.title ?? 'ValorAI Copilot',
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.w700,
                        color: AppColors.textPrimary,
                      ),
                ),
                Text(
                  'AI Real Estate Advisor',
                  style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: AppColors.accent,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 1.1,
                      ),
                ),
              ],
            ),
          ),
          IconButton(
            icon: const Icon(Icons.arrow_back_ios_new_rounded, color: AppColors.textMuted, size: 20),
            onPressed: () {
              if (context.canPop()) {
                context.pop();
              } else {
                context.goNamed(RouteNames.home);
              }
            },
          ),
        ],
      ),
    );
  }

  Widget _buildActiveContextBanner() {
    if (_activeValuationContext == null) return const SizedBox.shrink();

    final valueText = _activeValuationContext!.hasFairValue
        ? 'EGP ${(_activeValuationContext!.fairPriceEgp / 1000000).toStringAsFixed(1)}M'
        : 'No Price';
    final areaText = _activeValuationContext!.location?.latitude != null ? 'Active Valuation' : 'Egyptian Property';

    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.md,
        vertical: AppSpacing.xs,
      ),
      color: AppColors.accent.withValues(alpha: 0.08),
      child: Row(
        children: [
          const Icon(Icons.analytics_outlined, color: AppColors.accent, size: 16),
          const SizedBox(width: AppSpacing.sm),
          Expanded(
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _buildContextChip('Target: $areaText'),
                  _buildContextChip('Value: $valueText'),
                  _buildContextChip('Conf: ${(_activeValuationContext!.confidenceScore * 100).round()}%'),
                  _buildContextChip('Comps: ${_activeValuationContext!.comparablesCount} Properties'),
                ],
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.cancel_outlined, color: AppColors.textMuted, size: 16),
            onPressed: () {
              setState(() {
                _activeValuationContext = null;
              });
            },
          ),
        ],
      ),
    );
  }

  Widget _buildContextChip(String label) {
    return Container(
      margin: const EdgeInsets.only(right: AppSpacing.sm),
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm, vertical: 2),
      decoration: BoxDecoration(
        color: AppColors.surface.withValues(alpha: 0.6),
        borderRadius: BorderRadius.circular(AppRadius.sm),
        border: Border.all(color: AppColors.accent.withValues(alpha: 0.2)),
      ),
      child: Text(
        label,
        style: const TextStyle(color: AppColors.textSecondary, fontSize: 10, fontWeight: FontWeight.w600),
      ),
    );
  }

  Widget _buildEmptyState() {
    final questions = [
      'What is driving this valuation?',
      'Show comparable properties.',
      'Market outlook for New Cairo.',
      'Should I buy or rent in Sheikh Zayed?',
      'Why is confidence only 82%?',
    ];

    return Scrollbar(
      child: ListView(
        padding: const EdgeInsets.all(AppSpacing.lg),
        physics: const BouncingScrollPhysics(),
        children: [
          const SizedBox(height: 48),
          Center(
            child: Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: AppColors.accent.withValues(alpha: 0.1),
                border: Border.all(color: AppColors.accent.withValues(alpha: 0.3)),
                boxShadow: [
                  BoxShadow(
                    color: AppColors.accent.withValues(alpha: 0.14),
                    blurRadius: 28,
                  ),
                ],
              ),
              child: const Icon(Icons.auto_awesome_outlined, color: AppColors.accent, size: 40),
            ),
          ),
          const SizedBox(height: AppSpacing.lg),
          Text(
            'Ask ValorAI Copilot',
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: AppColors.textPrimary,
                  letterSpacing: -0.5,
                ),
          ),
          const SizedBox(height: AppSpacing.sm),
          const Text(
            'Your institutional-grade Real Estate Advisor powered by the Fair Price Engine and Comparable Market Trend (CMT) metrics.',
            textAlign: TextAlign.center,
            style: TextStyle(color: AppColors.textMuted, fontSize: 13, height: 1.5),
          ),
          const SizedBox(height: 40),
          Text(
            'SUGGESTED ANALYTICAL QUESTIONS',
            style: Theme.of(context).textTheme.labelMedium?.copyWith(
                  color: AppColors.accent.withValues(alpha: 0.7),
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1.3,
                  fontSize: 10,
                ),
          ),
          const SizedBox(height: AppSpacing.sm),
          ...questions.map((q) => Card(
                margin: const EdgeInsets.only(bottom: AppSpacing.sm),
                color: AppColors.surface.withValues(alpha: 0.72),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(AppRadius.lg),
                  side: BorderSide(color: AppColors.textPrimary.withValues(alpha: 0.06)),
                ),
                child: InkWell(
                  onTap: () => _sendMessage(q),
                  borderRadius: BorderRadius.circular(AppRadius.lg),
                  child: Padding(
                    padding: const EdgeInsets.all(AppSpacing.md),
                    child: Row(
                      children: [
                        const Icon(Icons.chat_bubble_outline_rounded, color: AppColors.accent, size: 16),
                        const SizedBox(width: AppSpacing.md),
                        Expanded(
                          child: Text(
                            q,
                            style: const TextStyle(
                              color: AppColors.textSecondary,
                              fontSize: 13,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ),
                        const Icon(Icons.arrow_forward_ios_rounded, color: AppColors.textMuted, size: 12),
                      ],
                    ),
                  ),
                ),
              )),
        ],
      ),
    );
  }

  Widget _buildMessageCanvas() {
    final messages = _currentSession!.messages;

    return Scrollbar(
      child: ListView.builder(
        controller: _scrollController,
        padding: const EdgeInsets.fromLTRB(AppSpacing.md, AppSpacing.lg, AppSpacing.md, 120),
        physics: const BouncingScrollPhysics(),
        itemCount: messages.length,
        itemBuilder: (context, index) {
          final msg = messages[index];
          return _MessageBubble(
            message: msg,
            onActionTap: (text) => _sendMessage(text),
          );
        },
      ),
    );
  }

  Widget _buildMessageComposer() {
    return Container(
      padding: const EdgeInsets.fromLTRB(AppSpacing.md, AppSpacing.sm, AppSpacing.md, AppSpacing.lg),
      decoration: BoxDecoration(
        color: AppColors.backgroundPrimary,
        border: Border(
          top: BorderSide(color: AppColors.textPrimary.withValues(alpha: 0.06)),
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Expanded(
            child: Container(
              decoration: BoxDecoration(
                color: AppColors.surface,
                borderRadius: BorderRadius.circular(AppRadius.xl),
                border: Border.all(color: AppColors.textPrimary.withValues(alpha: 0.08)),
              ),
              child: TextField(
                controller: _messageController,
                maxLines: 5,
                minLines: 1,
                style: const TextStyle(color: AppColors.textPrimary, fontSize: 14),
                decoration: const InputDecoration(
                  hintText: 'Ask AI Advisor...',
                  hintStyle: TextStyle(color: AppColors.textMuted),
                  border: InputBorder.none,
                  contentPadding: EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: 12),
                ),
              ),
            ),
          ),
          const SizedBox(width: AppSpacing.sm),
          Material(
            color: _isLoading ? AppColors.textMuted.withValues(alpha: 0.2) : AppColors.accent,
            borderRadius: BorderRadius.circular(AppRadius.lg),
            child: InkWell(
              onTap: _isLoading ? null : () => _sendMessage(_messageController.text),
              borderRadius: BorderRadius.circular(AppRadius.lg),
              child: Container(
                width: 44,
                height: 44,
                alignment: Alignment.center,
                child: _isLoading
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: AppColors.backgroundPrimary,
                        ),
                      )
                    : const Icon(
                        Icons.send_rounded,
                        color: AppColors.backgroundPrimary,
                        size: 20,
                      ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSidebarDrawer(List<CopilotSession> pins, List<CopilotSession> recents) {
    return Drawer(
      backgroundColor: AppColors.backgroundPrimary,
      child: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(AppSpacing.md),
              child: Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'ValorAI Sessions',
                          style: Theme.of(context).textTheme.titleLarge?.copyWith(
                                fontWeight: FontWeight.bold,
                                color: AppColors.textPrimary,
                              ),
                        ),
                        const SizedBox(height: 2),
                        const Text(
                          'Select or search past analysis',
                          style: TextStyle(color: AppColors.textMuted, fontSize: 11),
                        ),
                      ],
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.add_comment_outlined, color: AppColors.accent),
                    onPressed: () {
                      _createNewSession();
                      Navigator.pop(context); // Close drawer
                    },
                  ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm),
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(AppRadius.md),
                  border: Border.all(color: AppColors.textPrimary.withValues(alpha: 0.06)),
                ),
                child: TextField(
                  style: const TextStyle(color: AppColors.textPrimary, fontSize: 13),
                  onChanged: (val) {
                    setState(() {
                      _searchQuery = val;
                    });
                  },
                  decoration: const InputDecoration(
                    hintText: 'Search conversations...',
                    hintStyle: TextStyle(color: AppColors.textMuted),
                    border: InputBorder.none,
                    icon: Icon(Icons.search_rounded, color: AppColors.textMuted, size: 18),
                  ),
                ),
              ),
            ),
            const SizedBox(height: AppSpacing.md),
            Expanded(
              child: ListView(
                physics: const BouncingScrollPhysics(),
                children: [
                  if (pins.isNotEmpty) ...[
                    _buildDrawerHeader('PINNED CHATS'),
                    ...pins.map((s) => _buildDrawerSessionTile(s)),
                    const SizedBox(height: AppSpacing.sm),
                  ],
                  _buildDrawerHeader('RECENT SESSIONS'),
                  if (recents.isEmpty && pins.isEmpty)
                    const Padding(
                      padding: EdgeInsets.all(AppSpacing.md),
                      child: Text('No matching sessions found.', style: TextStyle(color: AppColors.textMuted, fontSize: 12)),
                    )
                  else
                    ...recents.map((s) => _buildDrawerSessionTile(s)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDrawerHeader(String title) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(AppSpacing.md, AppSpacing.md, AppSpacing.md, AppSpacing.sm),
      child: Text(
        title,
        style: const TextStyle(
          color: AppColors.textMuted,
          fontSize: 9,
          fontWeight: FontWeight.bold,
          letterSpacing: 1.2,
        ),
      ),
    );
  }

  Widget _buildDrawerSessionTile(CopilotSession session) {
    final isActive = _currentSession?.id == session.id;

    return Material(
      color: isActive ? AppColors.surface : Colors.transparent,
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: 0),
        title: Text(
          session.title,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: TextStyle(
            color: isActive ? AppColors.accent : AppColors.textSecondary,
            fontWeight: isActive ? FontWeight.bold : FontWeight.w500,
            fontSize: 13,
          ),
        ),
        subtitle: Text(
          '${session.messages.length} messages',
          style: const TextStyle(color: AppColors.textMuted, fontSize: 10),
        ),
        leading: Icon(
          session.isPinned ? Icons.push_pin_rounded : Icons.chat_bubble_outline_rounded,
          color: isActive ? AppColors.accent : AppColors.textMuted,
          size: 16,
        ),
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            IconButton(
              icon: Icon(
                session.isPinned ? Icons.push_pin_rounded : Icons.push_pin_outlined,
                color: AppColors.textMuted,
                size: 14,
              ),
              onPressed: () => _togglePinSession(session),
            ),
            PopupMenuButton<String>(
              icon: const Icon(Icons.more_vert_rounded, color: AppColors.textMuted, size: 14),
              color: AppColors.surface,
              onSelected: (action) {
                if (action == 'rename') {
                  _showRenameDialog(session);
                } else if (action == 'delete') {
                  _showDeleteConfirmDialog(session);
                }
              },
              itemBuilder: (context) => [
                const PopupMenuItem(
                  value: 'rename',
                  child: Text('Rename', style: TextStyle(color: AppColors.textPrimary, fontSize: 12)),
                ),
                const PopupMenuItem(
                  value: 'delete',
                  child: Text('Delete', style: TextStyle(color: Colors.redAccent, fontSize: 12)),
                ),
              ],
            ),
          ],
        ),
        onTap: () {
          setState(() {
            _currentSession = session;
            CopilotSessionStore.activeSession = session;
          });
          Navigator.pop(context); // Close drawer
        },
      ),
    );
  }
}

class _MessageBubble extends StatelessWidget {
  const _MessageBubble({required this.message, required this.onActionTap});

  final CopilotMessage message;
  final ValueChanged<String> onActionTap;

  @override
  Widget build(BuildContext context) {
    final isUser = message.role == 'user';

    return Padding(
      padding: const EdgeInsets.only(bottom: AppSpacing.lg),
      child: Column(
        crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
            children: [
              if (!isUser) ...[
                Container(
                  width: 24,
                  height: 24,
                  decoration: BoxDecoration(
                    color: AppColors.accent.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(AppRadius.sm),
                    border: Border.all(color: AppColors.accent.withValues(alpha: 0.3)),
                  ),
                  child: const Icon(Icons.auto_awesome_rounded, color: AppColors.accent, size: 14),
                ),
                const SizedBox(width: AppSpacing.sm),
                Text(
                  'Valor Advisor',
                  style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: AppColors.accent,
                        fontWeight: FontWeight.bold,
                      ),
                ),
              ] else ...[
                Text(
                  'You',
                  style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: AppColors.textMuted,
                        fontWeight: FontWeight.bold,
                      ),
                ),
              ],
              const SizedBox(width: AppSpacing.sm),
              Text(
                _formatTime(message.timestamp),
                style: const TextStyle(color: AppColors.textMuted, fontSize: 10),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.sm),
          if (message.isLoading)
            _buildLoadingIndicator()
          else
            Container(
              padding: const EdgeInsets.all(AppSpacing.md),
              constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.88),
              decoration: BoxDecoration(
                color: isUser ? AppColors.accent.withValues(alpha: 0.08) : AppColors.surface.withValues(alpha: 0.7),
                borderRadius: BorderRadius.only(
                  topLeft: const Radius.circular(AppRadius.lg),
                  topRight: const Radius.circular(AppRadius.lg),
                  bottomLeft: Radius.circular(isUser ? AppRadius.lg : AppRadius.sm),
                  bottomRight: Radius.circular(isUser ? AppRadius.sm : AppRadius.lg),
                ),
                border: Border.all(
                  color: isUser
                      ? AppColors.accent.withValues(alpha: 0.24)
                      : AppColors.textPrimary.withValues(alpha: 0.06),
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    message.content,
                    style: const TextStyle(color: AppColors.textSecondary, fontSize: 13, height: 1.5),
                  ),
                  // Render Custom Structured Evidence Cards if attached
                  if (message.propertySummary != null) ...[
                    const SizedBox(height: AppSpacing.md),
                    _PropertySummaryCard(data: message.propertySummary!),
                  ],
                  if (message.confidence != null) ...[
                    const SizedBox(height: AppSpacing.md),
                    _ConfidenceCard(data: message.confidence!),
                  ],
                  if (message.evidenceDrivers != null && message.evidenceDrivers!.isNotEmpty) ...[
                    const SizedBox(height: AppSpacing.md),
                    _EvidenceCard(drivers: message.evidenceDrivers!),
                  ],
                  if (message.comparables != null && message.comparables!.isNotEmpty) ...[
                    const SizedBox(height: AppSpacing.md),
                    _ComparableCard(comparables: message.comparables!, onActionTap: onActionTap),
                  ],
                  if (message.marketInsight != null) ...[
                    const SizedBox(height: AppSpacing.md),
                    _MarketInsightCard(data: message.marketInsight!),
                  ],
                ],
              ),
            ).animate().fadeIn(duration: 320.ms).slideY(begin: 0.04, end: 0),
        ],
      ),
    );
  }

  Widget _buildLoadingIndicator() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: 12),
      decoration: BoxDecoration(
        color: AppColors.surface.withValues(alpha: 0.4),
        borderRadius: BorderRadius.circular(AppRadius.lg),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const SizedBox(
            width: 12,
            height: 12,
            child: CircularProgressIndicator(strokeWidth: 1.5, color: AppColors.accent),
          ),
          const SizedBox(width: AppSpacing.sm),
          Text(
            'Advisor is evaluating telemetry...',
            style: TextStyle(color: AppColors.textMuted.withValues(alpha: 0.8), fontSize: 11),
          ),
        ],
      ),
    );
  }

  String _formatTime(DateTime dt) {
    final hour = dt.hour.toString().padLeft(2, '0');
    final min = dt.minute.toString().padLeft(2, '0');
    return '$hour:$min';
  }
}

// ==========================================
//结构化的卡片组件
// ==========================================

class _PropertySummaryCard extends StatelessWidget {
  const _PropertySummaryCard({required this.data});

  final PropertySummaryCardData data;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.backgroundPrimary.withValues(alpha: 0.8),
        borderRadius: BorderRadius.circular(AppRadius.md),
        border: Border.all(color: AppColors.accent.withValues(alpha: 0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.home_work_outlined, color: AppColors.accent, size: 14),
              const SizedBox(width: AppSpacing.xs),
              Text(
                'PROPERTY SUMMARY',
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                      color: AppColors.accent,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.1,
                      fontSize: 9,
                    ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.sm),
          Text(
            'EGP ${_formatPrice(data.fairPrice)}',
            style: const TextStyle(
              color: AppColors.textPrimary,
              fontSize: 18,
              fontWeight: FontWeight.w800,
            ),
          ),
          Text(
            data.valueBasis,
            style: const TextStyle(color: AppColors.textMuted, fontSize: 9),
          ),
          const Divider(height: 16, color: Colors.white10),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              if (data.propertyType != null) _buildBadge(data.propertyType!, Icons.apartment_rounded),
              if (data.sizeSqm != null) _buildBadge('${data.sizeSqm!.round()} sqm', Icons.square_foot_rounded),
              if (data.bedrooms != null) _buildBadge('${data.bedrooms}B / ${data.bathrooms ?? 0}Ba', Icons.bed_outlined),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildBadge(String label, IconData icon) {
    return Row(
      children: [
        Icon(icon, color: AppColors.textMuted, size: 12),
        const SizedBox(width: 4),
        Text(
          label,
          style: const TextStyle(color: AppColors.textSecondary, fontSize: 10, fontWeight: FontWeight.w600),
        ),
      ],
    );
  }
}

class _ConfidenceCard extends StatelessWidget {
  const _ConfidenceCard({required this.data});

  final ConfidenceCardData data;

  @override
  Widget build(BuildContext context) {
    final percentage = (data.score * 100).round();

    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.backgroundPrimary.withValues(alpha: 0.8),
        borderRadius: BorderRadius.circular(AppRadius.md),
        border: Border.all(color: AppColors.secondaryAccent.withValues(alpha: 0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.verified_outlined, color: AppColors.secondaryAccent, size: 14),
              const SizedBox(width: AppSpacing.xs),
              Text(
                'MODEL CONFIDENCE',
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                      color: AppColors.secondaryAccent,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.1,
                      fontSize: 9,
                    ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.sm),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                '$percentage% Score',
                style: const TextStyle(color: AppColors.textPrimary, fontSize: 16, fontWeight: FontWeight.bold),
              ),
              Text(
                data.label,
                style: const TextStyle(color: AppColors.secondaryAccent, fontSize: 11, fontWeight: FontWeight.bold),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.xs),
          ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: data.score,
              minHeight: 4,
              backgroundColor: AppColors.surface,
              valueColor: const AlwaysStoppedAnimation(AppColors.secondaryAccent),
            ),
          ),
          const SizedBox(height: AppSpacing.md),
          ...data.factors.entries.map((f) => Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(f.key, style: const TextStyle(color: AppColors.textMuted, fontSize: 10)),
                    Text('${(f.value * 100).round()}%',
                        style: const TextStyle(
                          color: AppColors.textSecondary,
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                        )),
                  ],
                ),
              )),
        ],
      ),
    );
  }
}

class _EvidenceCard extends StatelessWidget {
  const _EvidenceCard({required this.drivers});

  final List<EvidenceCardData> drivers;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.backgroundPrimary.withValues(alpha: 0.8),
        borderRadius: BorderRadius.circular(AppRadius.md),
        border: Border.all(color: AppColors.textPrimary.withValues(alpha: 0.08)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.analytics_outlined, color: AppColors.accent, size: 14),
              const SizedBox(width: AppSpacing.xs),
              Text(
                'EVIDENCE DRIVERS',
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                      color: AppColors.textMuted,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.1,
                      fontSize: 9,
                    ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.sm),
          ...drivers.map((d) {
            final isPositive = d.direction == 'Positive';
            final isNegative = d.direction == 'Negative';
            final color = isPositive
                ? AppColors.secondaryAccent
                : (isNegative ? Colors.redAccent : AppColors.textMuted);
            final sign = isPositive ? '+' : '';

            return Padding(
              padding: const EdgeInsets.only(bottom: AppSpacing.sm),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(d.label, style: const TextStyle(color: AppColors.textSecondary, fontSize: 11)),
                  Row(
                    children: [
                      Icon(
                        isPositive ? Icons.arrow_upward_rounded : (isNegative ? Icons.arrow_downward_rounded : Icons.remove),
                        color: color,
                        size: 11,
                      ),
                      const SizedBox(width: 2),
                      Text(
                        '$sign${d.value.toStringAsFixed(1)}%',
                        style: TextStyle(color: color, fontSize: 11, fontWeight: FontWeight.bold),
                      ),
                    ],
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

class _ComparableCard extends StatelessWidget {
  const _ComparableCard({required this.comparables, required this.onActionTap});

  final List<ComparableReferenceData> comparables;
  final ValueChanged<String> onActionTap;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.backgroundPrimary.withValues(alpha: 0.8),
        borderRadius: BorderRadius.circular(AppRadius.md),
        border: Border.all(color: AppColors.textPrimary.withValues(alpha: 0.08)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.compare_arrows_rounded, color: AppColors.accent, size: 14),
              const SizedBox(width: AppSpacing.xs),
              Text(
                'COMPARABLE CONTROLS',
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                      color: AppColors.textMuted,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.1,
                      fontSize: 9,
                    ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.sm),
          ...comparables.map((c) => Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 6.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              c.comparableId,
                              style: const TextStyle(
                                color: AppColors.textPrimary,
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            Text(
                              '${c.compoundName ?? 'Submarket'} • ${(c.similarityScore * 100).round()}% match',
                              style: const TextStyle(color: AppColors.textMuted, fontSize: 9),
                            ),
                          ],
                        ),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.end,
                          children: [
                            Text(
                              'EGP ${_formatCompact(c.price)}',
                              style: const TextStyle(
                                color: AppColors.accent,
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            Text(
                              '${c.sizeSqm.round()} sqm • ${c.distanceKm.toStringAsFixed(1)} km',
                              style: const TextStyle(color: AppColors.textMuted, fontSize: 9),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                  const Divider(height: 8, color: Colors.white10),
                ],
              )),
          const SizedBox(height: AppSpacing.sm),
          SizedBox(
            width: double.infinity,
            child: OutlinedButton(
              onPressed: () => onActionTap('Show comparable properties.'),
              style: OutlinedButton.styleFrom(
                side: BorderSide(color: AppColors.accent.withValues(alpha: 0.4)),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.md)),
                padding: const EdgeInsets.symmetric(vertical: 8),
              ),
              child: const Text(
                'Explore in Comparable Explorer',
                style: TextStyle(color: AppColors.accent, fontSize: 11, fontWeight: FontWeight.bold),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _MarketInsightCard extends StatelessWidget {
  const _MarketInsightCard({required this.data});

  final MarketInsightCardData data;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.backgroundPrimary.withValues(alpha: 0.8),
        borderRadius: BorderRadius.circular(AppRadius.md),
        border: Border.all(color: AppColors.accent.withValues(alpha: 0.2)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.trending_up_rounded, color: AppColors.accent, size: 14),
              const SizedBox(width: AppSpacing.xs),
              Text(
                'MARKET SIGNALS',
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                      color: AppColors.accent,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.1,
                      fontSize: 9,
                    ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.sm),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _buildMetric('DEMAND', data.demandTrend, AppColors.secondaryAccent),
              _buildMetric('STRENGTH', data.marketStrength, AppColors.accent),
            ],
          ),
          const Divider(height: 16, color: Colors.white10),
          const Text('Top Compounds', style: TextStyle(color: AppColors.textMuted, fontSize: 9, fontWeight: FontWeight.bold)),
          const SizedBox(height: 4),
          Wrap(
            spacing: 6,
            runSpacing: 4,
            children: data.activeCompounds.map((c) => _buildTag(c)).toList(),
          ),
          const Divider(height: 16, color: Colors.white10),
          const Text('Statements & Narration', style: TextStyle(color: AppColors.textMuted, fontSize: 9, fontWeight: FontWeight.bold)),
          const SizedBox(height: 4),
          ...data.statements.map((s) => Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('• ', style: TextStyle(color: AppColors.accent, fontSize: 11)),
                    Expanded(child: Text(s, style: const TextStyle(color: AppColors.textSecondary, fontSize: 10))),
                  ],
                ),
              )),
        ],
      ),
    );
  }

  Widget _buildMetric(String label, String value, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(color: AppColors.textMuted, fontSize: 8, fontWeight: FontWeight.bold)),
        Text(
          value,
          style: TextStyle(color: color, fontSize: 14, fontWeight: FontWeight.w800),
        ),
      ],
    );
  }

  Widget _buildTag(String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(4),
      ),
      child: Text(
        text,
        style: const TextStyle(color: AppColors.textSecondary, fontSize: 9, fontWeight: FontWeight.w600),
      ),
    );
  }
}

class _AmbientGlow extends StatelessWidget {
  const _AmbientGlow({required this.color, required this.size, required this.opacity});

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

// Helpers for formatted values
String _formatPrice(int price) {
  final reg = RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))');
  return price.toString().replaceAllMapped(reg, (Match m) => '${m[1]},');
}

String _formatCompact(int price) {
  if (price >= 1000000) {
    return '${(price / 1000000).toStringAsFixed(1)}M';
  }
  if (price >= 1000) {
    return '${(price / 1000).toStringAsFixed(0)}K';
  }
  return price.toString();
}
