import 'dart:convert';

class AuthUserMetadata {
  const AuthUserMetadata({
    required this.id,
    required this.externalSubject,
    required this.displayName,
  });

  final int id;
  final String externalSubject;
  final String displayName;

  factory AuthUserMetadata.fromMap(Map<String, dynamic> map) {
    return AuthUserMetadata(
      id: map['id'] as int,
      externalSubject: map['external_subject'] as String,
      displayName: map['display_name'] as String,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'external_subject': externalSubject,
      'display_name': displayName,
    };
  }

  String toJson() => json.encode(toMap());

  factory AuthUserMetadata.fromJson(String source) {
    return AuthUserMetadata.fromMap(
      json.decode(source) as Map<String, dynamic>,
    );
  }
}

class TokenExchangeResult {
  const TokenExchangeResult({
    required this.accessToken,
    required this.expiresIn,
    required this.user,
  });

  final String accessToken;
  final int expiresIn;
  final AuthUserMetadata user;

  factory TokenExchangeResult.fromMap(Map<String, dynamic> map) {
    return TokenExchangeResult(
      accessToken: map['access_token'] as String,
      expiresIn: map['expires_in'] as int,
      user: AuthUserMetadata.fromMap(map['user'] as Map<String, dynamic>),
    );
  }
}
