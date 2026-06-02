import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import 'package:google_sign_in/google_sign_in.dart';

import '../../../../app/router/route_names.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_radius.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../core/services/firebase/firebase_exceptions.dart';

class SignupScreen extends StatefulWidget {
  const SignupScreen({super.key});

  @override
  State<SignupScreen> createState() => _SignupScreenState();
}

class _SignupScreenState extends State<SignupScreen> {
  final _formKey = GlobalKey<FormState>();
  final _fullNameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  final _auth = FirebaseAuth.instance;

  static final _googleSignIn = GoogleSignIn.instance;
  static Future<void>? _googleInitialization;

  bool _isLoading = false;
  bool _isPasswordVisible = false;
  bool _isConfirmPasswordVisible = false;

  @override
  void dispose() {
    _fullNameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  Future<void> _signUpWithEmail() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    await _runAuthAction(
      action: () async {
        final credential = await _auth.createUserWithEmailAndPassword(
          email: _emailController.text.trim(),
          password: _passwordController.text,
        );
        await credential.user?.updateDisplayName(
          _fullNameController.text.trim(),
        );
      },
      successMessage: 'Account created successfully. Please sign in.',
    );
  }

  Future<void> _signUpWithGoogle() async {
    await _runAuthAction(
      action: () async {
        if (kIsWeb) {
          await _auth.signInWithPopup(GoogleAuthProvider());
          return;
        }

        _googleInitialization ??= _googleSignIn.initialize();
        await _googleInitialization;

        final googleAccount = await _googleSignIn.authenticate();
        final googleAuthentication = googleAccount.authentication;
        final credential = GoogleAuthProvider.credential(
          idToken: googleAuthentication.idToken,
        );
        await _auth.signInWithCredential(credential);
      },
      successMessage: 'Google account connected successfully. Please sign in.',
    );
  }

  Future<void> _runAuthAction({
    required Future<void> Function() action,
    required String successMessage,
  }) async {
    if (_isLoading) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      await action();
      await _auth.signOut();
      if (!mounted) {
        return;
      }
      _showSnackBar(successMessage, isError: false);
      context.goNamed(RouteNames.login);
    } on Exception catch (exception) {
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
          child: Stack(
            children: [
              const Positioned(
                top: 120,
                left: -110,
                child: _SignupAmbientGlow(),
              ),
              AutofillGroup(
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
                            const _SignupLogo()
                                .animate()
                                .fadeIn(duration: 560.ms)
                                .scale(
                                  begin: const Offset(0.95, 0.95),
                                  end: const Offset(1, 1),
                                  duration: 620.ms,
                                  curve: Curves.easeOutCubic,
                                ),
                            const SizedBox(height: AppSpacing.lg),
                            Text(
                                  'Join ValorAI',
                                  textAlign: TextAlign.center,
                                  style: Theme.of(context)
                                      .textTheme
                                      .headlineMedium
                                      ?.copyWith(
                                        color: AppColors.textPrimary,
                                        fontWeight: FontWeight.w700,
                                        letterSpacing: -0.7,
                                      ),
                                )
                                .animate(delay: 90.ms)
                                .fadeIn(duration: 520.ms)
                                .slideY(begin: 0.12, end: 0),
                            const SizedBox(height: AppSpacing.sm),
                            Text(
                              'Create your account for premium real estate intelligence.',
                              textAlign: TextAlign.center,
                              style: Theme.of(context).textTheme.bodyMedium
                                  ?.copyWith(
                                    color: AppColors.textSecondary.withValues(
                                      alpha: 0.78,
                                    ),
                                  ),
                            ).animate(delay: 140.ms).fadeIn(duration: 540.ms),
                            const SizedBox(height: AppSpacing.xl),
                            _SignupPanel(
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.stretch,
                                    children: [
                                      TextFormField(
                                        controller: _fullNameController,
                                        enabled: !_isLoading,
                                        textInputAction: TextInputAction.next,
                                        autofillHints: const [
                                          AutofillHints.name,
                                        ],
                                        decoration: const InputDecoration(
                                          labelText: 'Full Name',
                                          hintText: 'Your full name',
                                          prefixIcon: Icon(
                                            Icons.person_outline_rounded,
                                          ),
                                        ),
                                        validator: (value) {
                                          if ((value?.trim() ?? '').isEmpty) {
                                            return 'Enter your full name.';
                                          }
                                          return null;
                                        },
                                      ),
                                      const SizedBox(height: AppSpacing.md),
                                      TextFormField(
                                        controller: _emailController,
                                        enabled: !_isLoading,
                                        keyboardType:
                                            TextInputType.emailAddress,
                                        textInputAction: TextInputAction.next,
                                        autofillHints: const [
                                          AutofillHints.email,
                                        ],
                                        decoration: const InputDecoration(
                                          labelText: 'Email Address',
                                          hintText: 'you@example.com',
                                          prefixIcon: Icon(
                                            Icons.mail_outline_rounded,
                                          ),
                                        ),
                                        validator: _validateEmail,
                                      ),
                                      const SizedBox(height: AppSpacing.md),
                                      TextFormField(
                                        controller: _passwordController,
                                        enabled: !_isLoading,
                                        obscureText: !_isPasswordVisible,
                                        textInputAction: TextInputAction.next,
                                        autofillHints: const [
                                          AutofillHints.newPassword,
                                        ],
                                        decoration: InputDecoration(
                                          labelText: 'Password',
                                          hintText: 'Minimum 8 characters',
                                          prefixIcon: const Icon(
                                            Icons.lock_outline_rounded,
                                          ),
                                          suffixIcon: IconButton(
                                            onPressed: _isLoading
                                                ? null
                                                : () {
                                                    setState(() {
                                                      _isPasswordVisible =
                                                          !_isPasswordVisible;
                                                    });
                                                  },
                                            icon: Icon(
                                              _isPasswordVisible
                                                  ? Icons.visibility_off_rounded
                                                  : Icons.visibility_rounded,
                                            ),
                                          ),
                                        ),
                                        validator: _validatePassword,
                                      ),
                                      const SizedBox(height: AppSpacing.md),
                                      TextFormField(
                                        controller: _confirmPasswordController,
                                        enabled: !_isLoading,
                                        obscureText: !_isConfirmPasswordVisible,
                                        textInputAction: TextInputAction.done,
                                        autofillHints: const [
                                          AutofillHints.newPassword,
                                        ],
                                        onFieldSubmitted: (_) {
                                          _signUpWithEmail();
                                        },
                                        decoration: InputDecoration(
                                          labelText: 'Confirm Password',
                                          hintText: 'Repeat your password',
                                          prefixIcon: const Icon(
                                            Icons.lock_reset_rounded,
                                          ),
                                          suffixIcon: IconButton(
                                            onPressed: _isLoading
                                                ? null
                                                : () {
                                                    setState(() {
                                                      _isConfirmPasswordVisible =
                                                          !_isConfirmPasswordVisible;
                                                    });
                                                  },
                                            icon: Icon(
                                              _isConfirmPasswordVisible
                                                  ? Icons.visibility_off_rounded
                                                  : Icons.visibility_rounded,
                                            ),
                                          ),
                                        ),
                                        validator: (value) {
                                          if ((value ?? '').isEmpty) {
                                            return 'Confirm your password.';
                                          }
                                          if (value !=
                                              _passwordController.text) {
                                            return 'Passwords do not match.';
                                          }
                                          return null;
                                        },
                                      ),
                                      const SizedBox(height: AppSpacing.lg),
                                      FilledButton(
                                        onPressed: _isLoading
                                            ? null
                                            : _signUpWithEmail,
                                        child: _isLoading
                                            ? const _ButtonProgressIndicator()
                                            : const Text('Sign Up'),
                                      ),
                                      const SizedBox(height: AppSpacing.lg),
                                      const _DividerLabel(),
                                      const SizedBox(height: AppSpacing.lg),
                                      OutlinedButton(
                                        onPressed: _isLoading
                                            ? null
                                            : _signUpWithGoogle,
                                        style: OutlinedButton.styleFrom(
                                          foregroundColor:
                                              AppColors.textPrimary,
                                          side: BorderSide(
                                            color: AppColors.textPrimary
                                                .withValues(alpha: 0.14),
                                          ),
                                          padding: const EdgeInsets.symmetric(
                                            vertical: 14,
                                          ),
                                        ),
                                        child: const Row(
                                          mainAxisAlignment:
                                              MainAxisAlignment.center,
                                          children: [
                                            Text(
                                              'G',
                                              style: TextStyle(
                                                color: AppColors.textPrimary,
                                                fontWeight: FontWeight.w700,
                                                fontSize: 16,
                                              ),
                                            ),
                                            SizedBox(width: AppSpacing.md),
                                            Text('Continue with Google'),
                                          ],
                                        ),
                                      ),
                                    ],
                                  ),
                                )
                                .animate(delay: 200.ms)
                                .fadeIn(duration: 620.ms)
                                .slideY(
                                  begin: 0.1,
                                  end: 0,
                                  curve: Curves.easeOutCubic,
                                ),
                            const SizedBox(height: AppSpacing.lg),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Text(
                                  'Already have an account? ',
                                  style: Theme.of(context).textTheme.bodyMedium
                                      ?.copyWith(color: AppColors.textMuted),
                                ),
                                TextButton(
                                  onPressed: _isLoading
                                      ? null
                                      : () {
                                          context.goNamed(RouteNames.login);
                                        },
                                  child: const Text('Login'),
                                ),
                              ],
                            ).animate(delay: 280.ms).fadeIn(duration: 560.ms),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String? _validateEmail(String? value) {
    final email = value?.trim() ?? '';
    if (email.isEmpty) {
      return 'Enter your email address.';
    }
    if (!email.contains('@') || !email.contains('.')) {
      return 'Enter a valid email address.';
    }
    return null;
  }

  String? _validatePassword(String? value) {
    final password = value ?? '';
    if (password.isEmpty) {
      return 'Enter a password.';
    }
    if (password.length < 8) {
      return 'Password must be at least 8 characters.';
    }
    return null;
  }
}

class _SignupPanel extends StatelessWidget {
  const _SignupPanel({required this.child});

  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.lg),
      decoration: BoxDecoration(
        color: AppColors.surface.withValues(alpha: 0.66),
        borderRadius: BorderRadius.circular(AppRadius.xl),
        border: Border.all(
          color: AppColors.textPrimary.withValues(alpha: 0.08),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.2),
            blurRadius: 34,
            offset: const Offset(0, 18),
          ),
        ],
      ),
      child: child,
    );
  }
}

class _SignupLogo extends StatelessWidget {
  const _SignupLogo();

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          width: 54,
          height: 54,
          decoration: BoxDecoration(
            color: AppColors.accent.withValues(alpha: 0.1),
            borderRadius: BorderRadius.circular(AppRadius.lg),
            border: Border.all(color: AppColors.accent.withValues(alpha: 0.35)),
            boxShadow: [
              BoxShadow(
                color: AppColors.accent.withValues(alpha: 0.18),
                blurRadius: 22,
              ),
            ],
          ),
          child: const Icon(
            Icons.auto_awesome_rounded,
            color: AppColors.accent,
            size: 26,
          ),
        ),
        const SizedBox(height: AppSpacing.md),
        Text(
          'ValorAI',
          style: Theme.of(context).textTheme.titleLarge?.copyWith(
            color: AppColors.accent,
            fontWeight: FontWeight.w700,
            letterSpacing: -0.6,
          ),
        ),
      ],
    );
  }
}

class _DividerLabel extends StatelessWidget {
  const _DividerLabel();

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Divider(color: AppColors.textPrimary.withValues(alpha: 0.1)),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md),
          child: Text(
            'OR CONTINUE WITH',
            style: Theme.of(context).textTheme.labelMedium?.copyWith(
              color: AppColors.textMuted,
              letterSpacing: 1.1,
              fontSize: 10,
            ),
          ),
        ),
        Expanded(
          child: Divider(color: AppColors.textPrimary.withValues(alpha: 0.1)),
        ),
      ],
    );
  }
}

class _ButtonProgressIndicator extends StatelessWidget {
  const _ButtonProgressIndicator();

  @override
  Widget build(BuildContext context) {
    return const SizedBox(
      width: 20,
      height: 20,
      child: CircularProgressIndicator(
        strokeWidth: 2,
        color: AppColors.backgroundPrimary,
      ),
    );
  }
}

class _SignupAmbientGlow extends StatelessWidget {
  const _SignupAmbientGlow();

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 270,
      height: 270,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        gradient: RadialGradient(
          colors: [
            AppColors.secondaryAccent.withValues(alpha: 0.1),
            Colors.transparent,
          ],
        ),
      ),
    );
  }
}
