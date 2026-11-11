# Content format

- App ID: `tournament`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `matchList` | array |
| `matchNodeList` | array |
| `matchTree` | array |
| `rootMatchId` | string |
| `teamList` | array |
| `version` | string |

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
    try {
      logger.d("fromJson $json");
      final Map<String, dynamic> decodedJson = jsonDecode(json);
      final List<Team> teamList = (decodedJson['teamList'] as List<dynamic>? ?? [])
          .map((e) => Team.fromJson(e as Map<String, dynamic>))
          .toList();

      final Content content = Content()
        ..version = decodedJson["version"] as String? ?? "1"
        ..createType = decodedJson["createType"] as String? ?? "Flutter"
        ..teamList = teamList;

      final rawMatchList = decodedJson['matchList'];
      content.matchList = (rawMatchList is List<dynamic>)
          ? rawMatchList
              .map((e) => Match.fromJson(e as Map<String, dynamic>))
              .toList()
          : [];

      final rawMatchNodeList = decodedJson['matchNodeList'];
      content.matchNodeList = (rawMatchNodeList is List<dynamic>)
          ? rawMatchNodeList
              .map((e) => MatchNode.fromJson(e as Map<String, dynamic>))
              .toList()
          : [];
      content.rootMatchId = decodedJson['rootMatchId'] as String? ?? '';

      return content;
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'teamList': teamList.map((team) => team.toJson()).toList(),
      'matchList': matchList.map((match) => match.toJson()).toList(),
      'matchNodeList': matchNodeList.map((node) => node.toJson()).toList(),
      'matchTree': matchNodeList.map((node) => node.toJson()).toList(),
      'rootMatchId': rootMatchId,
    };
  }
```

### `define/match_result_type.dart` identifiers

```dart
enum MatchResultType {
  initial('initial'),
  win('win'),
  lose('lose'),
  draw('draw'),
  noContest('no_contest');
```

### `data/entity/match.dart`

```dart
  static Match fromJson(Map<String, dynamic> json) {
    return Match(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      team1Id: json['team1Id'] as String? ?? '',
      team2Id: json['team2Id'] as String? ?? '',
      resultType: MatchResultType.fromId(json['resultType'] ?? ''),
      team1Score: (json['team1Score'] as num?)?.toDouble() ?? 0,
      team2Score: (json['team2Score'] as num?)?.toDouble() ?? 0,
      note: json['note'] as String? ?? '',
      priority: PriorityType.fromId(json['priority'] ?? ''),
      weather: WeatherType.fromId(json['weather'] ?? ''),
      startDateTime: json['startDateTime'] != null ? DateTime.parse(json['startDateTime']) : null,
      endDateTime: json['endDateTime'] != null ? DateTime.parse(json['endDateTime']) : null,
      link: json['link'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      imageBase64: json['imageBase64'] as String? ?? '',
      complete: CompleteType.fromId(json['complete'] ?? ''),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'team1Id': team1Id,
      'team2Id': team2Id,
      'resultType': resultType.id,
      'team1Score': team1Score,
      'team2Score': team2Score,
      'note': note,
      'priority': priority.id,
      'weather': weather.id,
      'startDateTime': startDateTime?.toIso8601String(),
      'endDateTime': endDateTime?.toIso8601String(),
      'link': link,
      'colorHex': colorHex,
      'imageBase64': imageBase64,
      'complete': complete.id,
    };
  }
```

### `data/entity/match_node.dart`

```dart
  static MatchNode fromJson(Map<String, dynamic> json) {
    return MatchNode(
      matchId: json['matchId'] as String? ?? '',
      parentMatchId: json['parentMatchId'] as String?,
      slot: json['slot'] as int?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'matchId': matchId,
      'parentMatchId': parentMatchId,
      'slot': slot,
    };
  }
```

### `data/entity/team.dart`

```dart
  static Team fromJson(Map<String, dynamic> json) {

    return Team(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      name: json['name'] as String? ?? '',
      note: json['note'] as String? ?? '',
      link: json['link'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      imageBase64: json['imageBase64'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = {
      'id': id,
      'name': name,
      'note': note,
      'link': link,
      'colorHex': colorHex,
      'imageBase64': imageBase64,
    };

    return data;
  }
```

### `define/complete_type.dart` identifiers

```dart
enum CompleteType {
  initial("initial"),
  progress_0("progress_0"),
  progress_25("progress_25"),
  progress_50("progress_50"),
  progress_75("progress_75"),
  progress_100("progress_100");
```

### `define/priority_type.dart` identifiers

```dart
enum PriorityType {
  initial('initial'),
  priority_1('priority_1'),
  priority_2('priority_2'),
  priority_3('priority_3'),
  priority_4('priority_4'),
  priority_5('priority_5');
```

### `define/weather_type.dart` identifiers

```dart
enum WeatherType {
  initial('initial'),
  sunny('sunny'),
  cloudy('cloudy'),
  rainy('rainy');
```
