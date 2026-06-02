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

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _auth = FirebaseAuth.instance;

  static final _googleSignIn = GoogleSignIn.instance;
  static Future<void>? _googleInitialization;

  bool _isLoading = false;
  bool _isPasswordVisible = false;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _signInWithEmail() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    await _runAuthAction(() async {
      await _auth.signInWithEmailAndPassword(
        email: _emailController.text.trim(),
        password: _passwordController.text,
      );
    });
  }

  Future<void> _signInWithGoogle() async {
    await _runAuthAction(() async {
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
    });
  }

  Future<void> _signInWithApple() async {
    await _runAuthAction(() async {
      final provider = AppleAuthProvider()
        ..addScope('email')
        ..addScope('name');

      if (kIsWeb) {
        await _auth.signInWithPopup(provider);
        return;
      }

      await _auth.signInWithProvider(provider);
    });
  }

  Future<void> _runAuthAction(Future<void> Function() action) async {
    if (_isLoading) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      await action();
      if (!mounted) {
        return;
      }
      context.goNamed(RouteNames.home);
    } on Exception catch (exception) {
      if (!mounted) {
        return;
      }
      _showError(FirebaseExceptions.getMessage(exception));
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(
        SnackBar(
          content: Text(message),
          behavior: SnackBarBehavior.floating,
          backgroundColor: const Color(0xFF7F1D1D),
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
                top: 100,
                right: -100,
                child: _LoginAmbientGlow(),
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
                            const _LoginLogo()
                                .animate()
                                .fadeIn(duration: 620.ms)
                                .scale(
                                  begin: const Offset(0.94, 0.94),
                                  end: const Offset(1, 1),
                                  duration: 680.ms,
                                  curve: Curves.easeOutCubic,
                                ),
                            const SizedBox(height: AppSpacing.xl),
                            Text(
                                  'Welcome Back',
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
                                .animate(delay: 100.ms)
                                .fadeIn(duration: 580.ms)
                                .slideY(begin: 0.14, end: 0),
                            const SizedBox(height: AppSpacing.sm),
                            Text(
                              'Sign in to access your intelligence dashboard.',
                              textAlign: TextAlign.center,
                              style: Theme.of(context).textTheme.bodyMedium
                                  ?.copyWith(
                                    color: AppColors.textSecondary.withValues(
                                      alpha: 0.78,
                                    ),
                                  ),
                            ).animate(delay: 160.ms).fadeIn(duration: 600.ms),
                            const SizedBox(height: AppSpacing.xl),
                            _LoginPanel(
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.stretch,
                                    children: [
                                      TextFormField(
                                        controller: _emailController,
                                        enabled: !_isLoading,
                                        keyboardType:
                                            TextInputType.emailAddress,
                                        textInputAction: TextInputAction.next,
                                        autofillHints: const [
                                          AutofillHints.username,
                                          AutofillHints.email,
                                        ],
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
                                          if (!email.contains('@')) {
                                            return 'Enter a valid email address.';
                                          }
                                          return null;
                                        },
                                      ),
                                      const SizedBox(height: AppSpacing.md),
                                      TextFormField(
                                        controller: _passwordController,
                                        enabled: !_isLoading,
                                        obscureText: !_isPasswordVisible,
                                        textInputAction: TextInputAction.done,
                                        autofillHints: const [
                                          AutofillHints.password,
                                        ],
                                        onFieldSubmitted: (_) {
                                          _signInWithEmail();
                                        },
                                        decoration: InputDecoration(
                                          labelText: 'Password',
                                          hintText: 'Enter your password',
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
                                        validator: (value) {
                                          if ((value ?? '').isEmpty) {
                                            return 'Enter your password.';
                                          }
                                          return null;
                                        },
                                      ),
                                      Align(
                                        alignment: Alignment.centerRight,
                                        child: TextButton(
                                          onPressed: _isLoading
                                              ? null
                                              : () {
                                                  context.pushNamed(
                                                    RouteNames.forgotPassword,
                                                  );
                                                },
                                          child: const Text('Forgot Password?'),
                                        ),
                                      ),
                                      const SizedBox(height: AppSpacing.sm),
                                      FilledButton(
                                        onPressed: _isLoading
                                            ? null
                                            : _signInWithEmail,
                                        child: _isLoading
                                            ? const SizedBox(
                                                width: 20,
                                                height: 20,
                                                child:
                                                    CircularProgressIndicator(
                                                      strokeWidth: 2,
                                                      color: AppColors
                                                          .backgroundPrimary,
                                                    ),
                                              )
                                            : const Text('Login'),
                                      ),
                                      const SizedBox(height: AppSpacing.lg),
                                      const _DividerLabel(),
                                      const SizedBox(height: AppSpacing.lg),
                                      _ProviderButton(
                                        icon: const Text(
                                          'G',
                                          style: TextStyle(
                                            color: AppColors.textPrimary,
                                            fontWeight: FontWeight.w700,
                                            fontSize: 16,
                                          ),
                                        ),
                                        label: 'Continue with Google',
                                        onPressed: _isLoading
                                            ? null
                                            : _signInWithGoogle,
                                      ),
                                      const SizedBox(height: AppSpacing.md),
                                      _ProviderButton(
                                        icon: const Icon(
                                          Icons.apple,
                                          color: AppColors.textPrimary,
                                          size: 22,
                                        ),
                                        label: 'Continue with Apple',
                                        onPressed: _isLoading
                                            ? null
                                            : _signInWithApple,
                                      ),
                                    ],
                                  ),
                                )
                                .animate(delay: 220.ms)
                                .fadeIn(duration: 650.ms)
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
                                  'Don\'t have an account? ',
                                  style: Theme.of(context).textTheme.bodyMedium
                                      ?.copyWith(color: AppColors.textMuted),
                                ),
                                TextButton(
                                  onPressed: _isLoading
                                      ? null
                                      : () {
                                          context.pushNamed(RouteNames.signup);
                                        },
                                  child: const Text('Create Account'),
                                ),
                              ],
                            ).animate(delay: 320.ms).fadeIn(duration: 620.ms),
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
}

class _LoginPanel extends StatelessWidget {
  const _LoginPanel({required this.child});

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

class _LoginLogo extends StatelessWidget {
  const _LoginLogo();

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          width: 58,
          height: 58,
          decoration: BoxDecoration(
            color: AppColors.accent.withValues(alpha: 0.1),
            borderRadius: BorderRadius.circular(AppRadius.lg),
            border: Border.all(color: AppColors.accent.withValues(alpha: 0.35)),
            boxShadow: [
              BoxShadow(
                color: AppColors.accent.withValues(alpha: 0.2),
                blurRadius: 24,
              ),
            ],
          ),
          child: const Icon(
            Icons.auto_awesome_rounded,
            color: AppColors.accent,
            size: 28,
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

class _ProviderButton extends StatelessWidget {
  const _ProviderButton({
    required this.icon,
    required this.label,
    required this.onPressed,
  });

  final Widget icon;
  final String label;
  final VoidCallback? onPressed;

  @override
  Widget build(BuildContext context) {
    return OutlinedButton(
      onPressed: onPressed,
      style: OutlinedButton.styleFrom(
        foregroundColor: AppColors.textPrimary,
        side: BorderSide(color: AppColors.textPrimary.withValues(alpha: 0.14)),
        padding: const EdgeInsets.symmetric(vertical: 14),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          icon,
          const SizedBox(width: AppSpacing.md),
          Text(label),
        ],
      ),
    );
  }
}

class _LoginAmbientGlow extends StatelessWidget {
  const _LoginAmbientGlow();

  @override
  Widget build(BuildContext context) {
    return Container(
          width: 260,
          height: 260,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            gradient: RadialGradient(
              colors: [
                AppColors.accent.withValues(alpha: 0.12),
                Colors.transparent,
              ],
            ),
          ),
        )
        .animate(onPlay: (controller) => controller.repeat(reverse: true))
        .fade(begin: 0.46, end: 0.84, duration: 1700.ms)
        .scale(
          begin: const Offset(0.92, 0.92),
          end: const Offset(1.06, 1.06),
          duration: 1700.ms,
        );
  }
}
