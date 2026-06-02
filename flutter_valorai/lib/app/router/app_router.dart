import 'package:go_router/go_router.dart';

import 'route_names.dart';
import 'route_paths.dart';
import '../../features/onboarding/presentation/screens/splash_screen.dart';
import '../../features/onboarding/presentation/screens/onboarding_screen.dart';
import '../../features/auth/presentation/screens/login_screen.dart';
import '../../features/auth/presentation/screens/signup_screen.dart';
import '../../features/auth/presentation/screens/forgot_password_screen.dart';
import '../../features/home/presentation/screens/home_screen.dart';
import '../../features/valuation/presentation/screens/valuation_input_screen.dart';
import '../../features/valuation/presentation/screens/valuation_result_screen.dart';
import '../../features/valuation/presentation/screens/comparable_explorer_screen.dart';
import '../../features/copilot/presentation/screens/copilot_screen.dart';
import '../../features/profile/presentation/screens/profile_screen.dart';

class AppRouter {
  AppRouter._();

  static final GoRouter router = GoRouter(
    initialLocation: RoutePaths.splash,
    routes: [
      GoRoute(
        path: RoutePaths.splash,
        name: RouteNames.splash,
        builder: (context, state) => const SplashScreen(),
      ),
      GoRoute(
        path: RoutePaths.onboarding,
        name: RouteNames.onboarding,
        builder: (context, state) => const OnboardingScreen(),
      ),
      GoRoute(
        path: RoutePaths.login,
        name: RouteNames.login,
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: RoutePaths.signup,
        name: RouteNames.signup,
        builder: (context, state) => const SignupScreen(),
      ),
      GoRoute(
        path: RoutePaths.forgotPassword,
        name: RouteNames.forgotPassword,
        builder: (context, state) => const ForgotPasswordScreen(),
      ),
      GoRoute(
        path: RoutePaths.home,
        name: RouteNames.home,
        builder: (context, state) => const HomeScreen(),
      ),
      GoRoute(
        path: RoutePaths.valuationInput,
        name: RouteNames.valuationInput,
        builder: (context, state) => const ValuationInputScreen(),
      ),
      GoRoute(
        path: RoutePaths.valuationResult,
        name: RouteNames.valuationResult,
        builder: (context, state) => const ValuationResultScreen(),
      ),
      GoRoute(
        path: RoutePaths.comparableExplorer,
        name: RouteNames.comparableExplorer,
        builder: (context, state) => const ComparableExplorerScreen(),
      ),
      GoRoute(
        path: RoutePaths.copilot,
        name: RouteNames.copilot,
        builder: (context, state) => const CopilotScreen(),
      ),
      GoRoute(
        path: RoutePaths.profile,
        name: RouteNames.profile,
        builder: (context, state) => const ProfileScreen(),
      ),
    ],
  );
}
