import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';
import '../../../firebase_options.dart';

class FirebaseInitializer {
  FirebaseInitializer._();

  static Future<void> init() async {
    try {
      await Firebase.initializeApp(
        options: DefaultFirebaseOptions.currentPlatform,
      );
      debugPrint('Firebase initialized successfully.');
    } catch (e) {
      debugPrint('Failed to initialize Firebase: $e');
      rethrow;
    }
  }
}

