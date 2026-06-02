import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

class FirebaseInitializer {
  FirebaseInitializer._();

  static Future<void> init() async {
    try {
      await Firebase.initializeApp();
      debugPrint('Firebase initialized successfully.');
    } catch (e) {
      debugPrint('Failed to initialize Firebase: $e');
      rethrow;
    }
  }
}
