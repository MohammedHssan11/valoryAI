import 'package:flutter/material.dart';
import 'core/services/firebase/firebase_initializer.dart';
import 'app/router/app_router.dart';
import 'app/theme/app_theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await FirebaseInitializer.init();
  runApp(const ValorAIApp());
}

class ValorAIApp extends StatelessWidget {
  const ValorAIApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'ValorAI',
      theme: AppTheme.darkTheme,
      routerConfig: AppRouter.router,
      debugShowCheckedModeBanner: false,
    );
  }
}
