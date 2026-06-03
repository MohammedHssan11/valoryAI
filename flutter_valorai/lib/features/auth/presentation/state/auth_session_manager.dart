import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../../data/datasources/auth_remote_data_source.dart';
import '../../domain/models/auth_session.dart';

enum AuthSessionStatus { uninitialized, anonymous, authenticated }

class AuthSessionManager extends ChangeNotifier {
  AuthSessionManager._({
    FirebaseAuth? firebaseAuth,
    FlutterSecureStorage? storage,
    AuthRemoteDataSource? remoteDataSource,
  }) : _firebaseAuth = firebaseAuth ?? FirebaseAuth.instance,
       _storage = storage ?? const FlutterSecureStorage(),
       _remoteDataSource = remoteDataSource ?? AuthRemoteDataSource();

  static final AuthSessionManager instance = AuthSessionManager._();

  static const _accessTokenKey = 'valorai_access_token';
  static const _expiresAtKey = 'valorai_access_token_expires_at';
  static const _userMetadataKey = 'valorai_user_metadata';

  final FirebaseAuth _firebaseAuth;
  final FlutterSecureStorage _storage;
  final AuthRemoteDataSource _remoteDataSource;

  AuthSessionStatus _status = AuthSessionStatus.uninitialized;
  String? _accessToken;
  DateTime? _expiresAt;
  AuthUserMetadata? _user;
  Future<String>? _renewal;

  AuthSessionStatus get status => _status;
  String? get accessToken => _accessToken;
  AuthUserMetadata? get user => _user;
  bool get isAuthenticated =>
      _status == AuthSessionStatus.authenticated &&
      _accessToken != null &&
      _expiresAt != null &&
      _expiresAt!.isAfter(DateTime.now());

  Future<void> restoreSession() async {
    try {
      final token = await _storage.read(key: _accessTokenKey);
      final expiresAtRaw = await _storage.read(key: _expiresAtKey);
      final userRaw = await _storage.read(key: _userMetadataKey);
      final expiresAt = expiresAtRaw == null
          ? null
          : DateTime.tryParse(expiresAtRaw);

      if (token != null &&
          token.isNotEmpty &&
          expiresAt != null &&
          expiresAt.isAfter(DateTime.now()) &&
          userRaw != null) {
        _setAuthenticated(
          token: token,
          expiresAt: expiresAt,
          user: AuthUserMetadata.fromJson(userRaw),
        );
        return;
      }

      if (_firebaseAuth.currentUser != null) {
        await renewSession();
        return;
      }
    } on Exception {
      await _clearStoredSession();
    }

    _setAnonymous();
  }

  Future<String> completeFirebaseSignIn() {
    return renewSession();
  }

  Future<String> renewSession() {
    final activeRenewal = _renewal;
    if (activeRenewal != null) {
      return activeRenewal;
    }

    final renewal = _exchangeFirebaseSession();
    _renewal = renewal;
    return renewal.whenComplete(() {
      _renewal = null;
    });
  }

  Future<String> _exchangeFirebaseSession() async {
    final firebaseUser = _firebaseAuth.currentUser;
    if (firebaseUser == null) {
      throw const AuthSessionException(
        'Sign in with Firebase before starting a ValorAI session.',
      );
    }

    final firebaseIdToken = await firebaseUser.getIdToken(true);
    if (firebaseIdToken == null || firebaseIdToken.isEmpty) {
      throw const AuthSessionException(
        'Firebase did not return an identity token.',
      );
    }

    final exchange = await _remoteDataSource.exchangeFirebaseToken(
      firebaseIdToken,
    );
    final expiresAt = DateTime.now().add(Duration(seconds: exchange.expiresIn));
    await _storage.write(key: _accessTokenKey, value: exchange.accessToken);
    await _storage.write(
      key: _expiresAtKey,
      value: expiresAt.toIso8601String(),
    );
    await _storage.write(key: _userMetadataKey, value: exchange.user.toJson());
    _setAuthenticated(
      token: exchange.accessToken,
      expiresAt: expiresAt,
      user: exchange.user,
    );
    return exchange.accessToken;
  }

  Future<void> expireSession() async {
    await _clearStoredSession();
    _setAnonymous();
  }

  Future<void> logout() async {
    await expireSession();
    await _firebaseAuth.signOut();
  }

  Future<void> _clearStoredSession() async {
    await Future.wait([
      _storage.delete(key: _accessTokenKey),
      _storage.delete(key: _expiresAtKey),
      _storage.delete(key: _userMetadataKey),
    ]);
    _accessToken = null;
    _expiresAt = null;
    _user = null;
  }

  void _setAuthenticated({
    required String token,
    required DateTime expiresAt,
    required AuthUserMetadata user,
  }) {
    _accessToken = token;
    _expiresAt = expiresAt;
    _user = user;
    _status = AuthSessionStatus.authenticated;
    notifyListeners();
  }

  void _setAnonymous() {
    _accessToken = null;
    _expiresAt = null;
    _user = null;
    _status = AuthSessionStatus.anonymous;
    notifyListeners();
  }
}


