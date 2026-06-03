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
import '../../features/valuation/domain/models/valuation_response.dart';
import '../../features/valuation/presentation/screens/comparable_explorer_screen.dart';
import '../../features/copilot/presentation/screens/copilot_screen.dart';
import '../../features/profile/presentation/screens/profile_screen.dart';
import '../../features/workspace/presentation/screens/workspace_selector_screen.dart';
import '../../features/auth/presentation/state/auth_session_manager.dart';

class AppRouter {
  AppRouter._();

  static final GoRouter router = GoRouter(
    initialLocation: RoutePaths.splash,
    refreshListenable: AuthSessionManager.instance,
    redirect: (context, state) {
      final session = AuthSessionManager.instance;
      final publicPaths = {
        RoutePaths.splash,
        RoutePaths.onboarding,
        RoutePaths.login,
        RoutePaths.signup,
        RoutePaths.forgotPassword,
      };
      if (session.status != AuthSessionStatus.uninitialized &&
          !session.isAuthenticated &&
          !publicPaths.contains(state.matchedLocation)) {
        return RoutePaths.login;
      }
      return null;
    },
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
        builder: (context, state) => ValuationResultScreen(
          response: state.extra is ValuationResponse
              ? state.extra! as ValuationResponse
              : null,
        ),
      ),
      GoRoute(
        path: RoutePaths.comparableExplorer,
        name: RouteNames.comparableExplorer,
        builder: (context, state) => ComparableExplorerScreen(
          response: state.extra is ValuationResponse
              ? state.extra! as ValuationResponse
              : null,
        ),
      ),
      GoRoute(
        path: RoutePaths.copilot,
        name: RouteNames.copilot,
        builder: (context, state) => CopilotScreen(
          valuationResponse: state.extra is ValuationResponse
              ? state.extra! as ValuationResponse
              : null,
        ),
      ),
      GoRoute(
        path: RoutePaths.workspace,
        name: RouteNames.workspace,
        builder: (context, state) => const WorkspaceSelectorScreen(),
      ),
      GoRoute(
        path: RoutePaths.profile,
        name: RouteNames.profile,
        builder: (context, state) => const ProfileScreen(),
      ),
    ],
  );
}
