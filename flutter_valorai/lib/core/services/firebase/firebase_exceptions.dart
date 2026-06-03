import 'package:firebase_auth/firebase_auth.dart';

class FirebaseExceptions {
  static String getMessage(Exception exception) {
    if (exception is FirebaseAuthException) {
      switch (exception.code) {
        case 'network-request-failed':
          return 'Network request failed. Please check your internet connection.';
        case 'user-not-found':
          return 'No user found with this email.';
        case 'wrong-password':
          return 'Incorrect password. Please try again.';
        case 'invalid-credential':
          return 'The email or password is incorrect. Please try again.';
        case 'email-already-in-use':
          return 'An account already exists for that email.';
        case 'invalid-email':
          return 'The email address is not valid.';
        case 'user-disabled':
          return 'This account has been disabled.';
        case 'operation-not-allowed':
          return 'This sign-in method is not enabled yet.';
        case 'account-exists-with-different-credential':
          return 'An account already exists with a different sign-in method.';
        case 'popup-closed-by-user':
        case 'cancelled-popup-request':
          return 'Sign-in was cancelled.';
        case 'too-many-requests':
          return 'Too many requests. Please try again later.';
        default:
          return 'An unknown authentication error occurred.';
      }
    }

    final exceptionString = exception.toString();
    if (exceptionString.isNotEmpty && !exceptionString.startsWith('Instance of ')) {
      if (exceptionString.startsWith('Exception: ')) {
        return exceptionString.substring(11);
      }
      return exceptionString;
    }

    return 'An unknown error occurred.';
  }
}
