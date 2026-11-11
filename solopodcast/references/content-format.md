# Content format

- App ID: `solopodcast`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Share show metadata and scripted segments only. Local recordings and generated audio are not included. The default web URL is unconfigured; a verified deployment URL is required to generate a link.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `episodeId` | string |
| `episodeNumber` | string |
| `partner` | object |
| `segments` | array |
| `showName` | string |
| `showNotes` | string |
| `type` | string |
| `version` | integer |

Types use JSON terminology. Check nullability, nested elements, and defaults against the conversion definitions below. Image fields are out of scope even where they appear in the app's serializer.

## Nested elements, identifiers, and date conversions

The excerpts below preserve serialization statements from the app implementation checked on 2026-11-11; source comments are omitted. You do not need to execute Dart. `fromJson` specifies accepted types and defaults; `toJson` specifies output keys. Follow the actual date conversion units rather than assuming ISO timestamps. The excerpts are reference fragments, not standalone Dart programs.

### `data/entity/content.dart`

```dart
  static Content? tryFromJson(String json) {
    try {
      return fromJson(json);
    } catch (e) {
      logger.e("error tryFromJson: $e");
      return null;
    }
  }

  static Content? tryFromSharedJson(String json) {
    try {
      final dynamic decoded = jsonDecode(json);
      if (decoded is! Map || decoded.isEmpty) {
        return null;
      }
      final Content content = fromJson(json);
      if (jsonEncode(content.toJson()) == jsonEncode(Content().toJson())) {
        return null;
      }
      return content;
    } catch (e) {
      logger.e("error tryFromSharedJson: $e");
      return null;
    }
  }

  static Content fromJson(String json) {
    final dynamic decoded = jsonDecode(json);
    if (decoded is! Map) throw const FormatException('Invalid podcast file');
    final Map<String, dynamic> data = _migrate(Map<String, dynamic>.from(decoded));
    final dynamic episodeId = data['episodeId'];
    final dynamic showName = data['showName'];
    final dynamic episodeNumber = data['episodeNumber'];
    final dynamic showNotes = data['showNotes'];
    final dynamic segments = data['segments'];
    if ((episodeId != null && episodeId is! String) || (showName != null && showName is! String) || (episodeNumber != null && episodeNumber is! String) || (showNotes != null && showNotes is! String) || (segments != null && segments is! List)) {
      throw const FormatException('Invalid podcast file');
    }
    final String? safeEpisodeId = episodeId is String && RegExp(r'^[A-Za-z0-9-]+$').hasMatch(episodeId) ? episodeId : null;
    return Content(
      episodeId: safeEpisodeId,
      showName: showName as String? ?? '',
      episodeNumber: episodeNumber as String? ?? '',
      showNotes: showNotes as String? ?? '',
      partner: PartnerCharacter.fromJson(data['partner']),
      segments: (segments as List<dynamic>? ?? const <dynamic>[]).map(Segment.fromJson).toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'version': currentVersion,
      'type': fileType,
      'createType': 'Flutter',
      'episodeId': episodeId,
      'showName': showName,
      'episodeNumber': episodeNumber,
      'showNotes': showNotes,
      'partner': partner.toJson(),
      'segments': segments.map((Segment segment) => segment.toJson()).toList(),
    };
  }
```

### `data/entity/partner_character.dart`

```dart
  static PartnerCharacter fromJson(dynamic json) {
    if (json == null) return PartnerCharacter.initial();
    if (json is! Map) throw const FormatException('Invalid partner');
    final dynamic name = json['name'];
    final dynamic personality = json['personality'];
    if ((name != null && name is! String) || (personality != null && personality is! String)) throw const FormatException('Invalid partner');
    return PartnerCharacter(
      name: name as String? ?? '',
      preset: PartnerPreset.fromId(json['preset'] as String?),
      personality: personality as String? ?? '',
      pitch: _clamp(json['pitch'], 0.5, 2.0, 1.0),
      speechRate: _clamp(json['speechRate'], 0.0, 1.0, 0.5),
    );
  }

  static PartnerCharacter? tryFromJsonString(String json) {
    if (json.isEmpty) return null;
    try {
      return fromJson(jsonDecode(json));
    } catch (_) {
      return null;
    }
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'name': name,
      if (preset != null) 'preset': preset!.id,
      'personality': personality,
      'pitch': pitch,
      'speechRate': speechRate,
    };
  }
```

### `data/entity/segment.dart`

```dart
  static Segment fromJson(dynamic json) {
    if (json is! Map) throw const FormatException('Invalid segment');
    final dynamic id = json['id'];
    final dynamic title = json['title'];
    final dynamic script = json['script'];
    final dynamic targetSeconds = json['targetSeconds'];
    final dynamic color = json['color'];
    final dynamic turns = json['turns'];
    if ((title != null && title is! String) || (script != null && script is! String) || (targetSeconds != null && targetSeconds is! int) || (color != null && color is! int) || (turns != null && turns is! List)) {
      throw const FormatException('Invalid segment');
    }
    final int seconds = targetSeconds as int? ?? 0;
    return Segment(
      id: id is String && id.isNotEmpty ? id : Uuid.v4().toString(),
      title: title as String? ?? '',
      script: script as String? ?? '',
      targetSeconds: seconds < 0 ? 0 : seconds,
      color: color == null ? null : Color(color as int),
      turns: (turns as List<dynamic>? ?? const <dynamic>[]).map(Turn.fromJson).toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'id': id,
      'title': title,
      if (script.isNotEmpty) 'script': script,
      if (targetSeconds > 0) 'targetSeconds': targetSeconds,
      if (color != null) 'color': color!.toARGB32(),
      if (turns.isNotEmpty) 'turns': turns.map((Turn turn) => turn.toJson()).toList(),
    };
  }
```

### `define/partner_preset.dart` identifiers

```dart
enum PartnerPreset {
  listener('listener', Icons.hearing, 1.1, 0.5),
  tsukkomi('tsukkomi', Icons.sentiment_very_satisfied, 1.25, 0.55),
  interviewer('interviewer', Icons.question_answer_outlined, 1.0, 0.5),
  expert('expert', Icons.school_outlined, 0.9, 0.47);
```

### `data/entity/turn.dart`

```dart
  static Turn fromJson(dynamic json) {
    if (json is! Map) throw const FormatException('Invalid turn');
    final dynamic id = json['id'];
    final Speaker? speaker = Speaker.fromId(json['speaker'] as String?);
    final dynamic text = json['text'];
    final dynamic fileName = json['fileName'];
    final dynamic durationMs = json['durationMs'];
    final dynamic createdAt = json['createdAt'];
    if (id is! String || id.isEmpty || speaker == null) throw const FormatException('Invalid turn');
    if ((text != null && text is! String) || (fileName != null && fileName is! String) || (durationMs != null && durationMs is! int) || (createdAt != null && createdAt is! String)) {
      throw const FormatException('Invalid turn');
    }
    final String name = fileName as String? ?? '';
    if (name.contains('/') || name.contains('\\') || name.startsWith('.')) throw const FormatException('Invalid turn');
    final int milliseconds = durationMs as int? ?? 0;
    return Turn(
      id: id,
      speaker: speaker,
      text: text as String? ?? '',
      fileName: name,
      durationMs: milliseconds < 0 ? 0 : milliseconds,
      createdAt: DateTime.tryParse(createdAt as String? ?? '') ?? DateTime.fromMillisecondsSinceEpoch(0),
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'id': id,
      'speaker': speaker.id,
      'text': text,
      if (fileName.isNotEmpty) 'fileName': fileName,
      if (durationMs > 0) 'durationMs': durationMs,
      'createdAt': createdAt.toIso8601String(),
    };
  }
```
