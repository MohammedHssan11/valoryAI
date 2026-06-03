import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';

import '../../../../app/router/route_names.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_radius.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../core/services/firebase/firebase_exceptions.dart';

class ForgotPasswordScreen extends StatefulWidget {
  const ForgotPasswordScreen({super.key});

  @override
  State<ForgotPasswordScreen> createState() => _ForgotPasswordScreenState();
}

class _ForgotPasswordScreenState extends State<ForgotPasswordScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _auth = FirebaseAuth.instance;

  bool _isLoading = false;
  bool _isSuccess = false;

  @override
  void dispose() {
    _emailController.dispose();
    super.dispose();
  }

  Future<void> _sendResetLink() async {
    if (!_formKey.currentState!.validate() || _isLoading) {
      return;
    }

    setState(() {
      _isLoading = true;
      _isSuccess = false;
    });

    try {
      await _auth.sendPasswordResetEmail(email: _emailController.text.trim());
      if (!mounted) {
        return;
      }
      setState(() {
        _isSuccess = true;
      });
      _showSnackBar(
        'Password reset link sent. Check your email inbox.',
        isError: false,
      );
    } on Exception catch (exception, stackTrace) {
      debugPrint("ERROR: $exception");
      debugPrintStack(stackTrace: stackTrace);
      if (!mounted) {
        return;
      }
      _showSnackBar(FirebaseExceptions.getMessage(exception), isError: true);
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  void _showSnackBar(String message, {required bool isError}) {
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(
        SnackBar(
          content: Text(message),
          behavior: SnackBarBehavior.floating,
          backgroundColor: isError
              ? const Color(0xFF7F1D1D)
              : const Color(0xFF065F46),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadius.md),
          ),
        ),
      );
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
          child: SingleChildScrollView(
            padding: const EdgeInsets.fromLTRB(
              AppSpacing.lg,
              AppSpacing.xl,
              AppSpacing.lg,
              AppSpacing.lg,
            ),
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 430),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Align(
                            alignment: Alignment.centerLeft,
                            child: IconButton(
                              tooltip: 'Back to login',
                              onPressed: _isLoading
                                  ? null
                                  : () {
                                      context.goNamed(RouteNames.login);
                                    },
                              icon: const Icon(
                                Icons.arrow_back_rounded,
                                color: AppColors.textPrimary,
                              ),
                            ),
                          )
                          .animate()
                          .fadeIn(duration: 420.ms)
                          .slideX(begin: -0.16, end: 0),
                      const SizedBox(height: AppSpacing.xl),
                      const _ResetPasswordIcon()
                          .animate(delay: 80.ms)
                          .fadeIn(duration: 560.ms)
                          .scale(
                            begin: const Offset(0.95, 0.95),
                            end: const Offset(1, 1),
                            duration: 620.ms,
                          ),
                      const SizedBox(height: AppSpacing.lg),
                      Text(
                            'Reset Password',
                            textAlign: TextAlign.center,
                            style: Theme.of(context).textTheme.headlineMedium
                                ?.copyWith(
                                  color: AppColors.textPrimary,
                                  fontWeight: FontWeight.w700,
                                  letterSpacing: -0.7,
                                ),
                          )
                          .animate(delay: 130.ms)
                          .fadeIn(duration: 520.ms)
                          .slideY(begin: 0.12, end: 0),
                      const SizedBox(height: AppSpacing.sm),
                      Text(
                        'Enter your email address and we will send you a secure password reset link.',
                        textAlign: TextAlign.center,
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: AppColors.textSecondary.withValues(
                            alpha: 0.78,
                          ),
                          height: 1.5,
                        ),
                      ).animate(delay: 170.ms).fadeIn(duration: 540.ms),
                      const SizedBox(height: AppSpacing.xl),
                      Container(
                            padding: const EdgeInsets.all(AppSpacing.lg),
                            decoration: BoxDecoration(
                              color: AppColors.surface.withValues(alpha: 0.66),
                              borderRadius: BorderRadius.circular(AppRadius.xl),
                              border: Border.all(
                                color: AppColors.textPrimary.withValues(
                                  alpha: 0.08,
                                ),
                              ),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withValues(alpha: 0.2),
                                  blurRadius: 34,
                                  offset: const Offset(0, 18),
                                ),
                              ],
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                TextFormField(
                                  controller: _emailController,
                                  enabled: !_isLoading,
                                  keyboardType: TextInputType.emailAddress,
                                  textInputAction: TextInputAction.done,
                                  autofillHints: const [AutofillHints.email],
                                  onFieldSubmitted: (_) {
                                    _sendResetLink();
                                  },
                                  decoration: const InputDecoration(
                                    labelText: 'Email Address',
                                    hintText: 'you@example.com',
                                    prefixIcon: Icon(
                                      Icons.mail_outline_rounded,
                                    ),
                                  ),
                                  validator: (value) {
                                    final email = value?.trim() ?? '';
                                    if (email.isEmpty) {
                                      return 'Enter your email address.';
                                    }
                                    if (!email.contains('@') ||
                                        !email.contains('.')) {
                                      return 'Enter a valid email address.';
                                    }
                                    return null;
                                  },
                                ),
                                if (_isSuccess) ...[
                                  const SizedBox(height: AppSpacing.md),
                                  Container(
                                    padding: const EdgeInsets.all(
                                      AppSpacing.md,
                                    ),
                                    decoration: BoxDecoration(
                                      color: AppColors.secondaryAccent
                                          .withValues(alpha: 0.1),
                                      borderRadius: BorderRadius.circular(
                                        AppRadius.md,
                                      ),
                                      border: Border.all(
                                        color: AppColors.secondaryAccent
                                            .withValues(alpha: 0.24),
                                      ),
                                    ),
                                    child: const Row(
                                      children: [
                                        Icon(
                                          Icons.check_circle_outline_rounded,
                                          color: AppColors.secondaryAccent,
                                          size: 20,
                                        ),
                                        SizedBox(width: AppSpacing.sm),
                                        Expanded(
                                          child: Text(
                                            'Reset link sent. Check your email inbox.',
                                            style: TextStyle(
                                              color: AppColors.textSecondary,
                                              fontSize: 13,
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                                const SizedBox(height: AppSpacing.lg),
                                FilledButton(
                                  onPressed: _isLoading ? null : _sendResetLink,
                                  child: _isLoading
                                      ? const SizedBox(
                                          width: 20,
                                          height: 20,
                                          child: CircularProgressIndicator(
                                            strokeWidth: 2,
                                            color: AppColors.backgroundPrimary,
                                          ),
                                        )
                                      : const Text('Send Reset Link'),
                                ),
                              ],
                            ),
                          )
                          .animate(delay: 220.ms)
                          .fadeIn(duration: 620.ms)
                          .slideY(
                            begin: 0.1,
                            end: 0,
                            curve: Curves.easeOutCubic,
                          ),
                      const SizedBox(height: AppSpacing.lg),
                      TextButton(
                        onPressed: _isLoading
                            ? null
                            : () {
                                context.goNamed(RouteNames.login);
                              },
                        child: const Text('Back To Login'),
                      ).animate(delay: 280.ms).fadeIn(duration: 560.ms),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _ResetPasswordIcon extends StatelessWidget {
  const _ResetPasswordIcon();

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        width: 70,
        height: 70,
        decoration: BoxDecoration(
          color: AppColors.accent.withValues(alpha: 0.1),
          borderRadius: BorderRadius.circular(AppRadius.xl),
          border: Border.all(color: AppColors.accent.withValues(alpha: 0.32)),
          boxShadow: [
            BoxShadow(
              color: AppColors.accent.withValues(alpha: 0.18),
              blurRadius: 24,
            ),
          ],
        ),
        child: const Icon(
          Icons.lock_reset_rounded,
          color: AppColors.accent,
          size: 34,
        ),
      ),
    );
  }
}
