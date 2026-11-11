# Content format

- App ID: `timetable`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `dayLabelMap` | object |
| `topic` | object |
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
      if (jsonEncode(content.toJson()) == jsonEncode(Content(Topic.initEmpty()).toJson())) {
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
      Topic topic = Topic.fromJson(decodedJson["topic"]);
      final rawMap = decodedJson['dayLabelMap'] as Map<String, dynamic>?;
      final dayLabelMap = (rawMap == null) ? <int, String>{} : rawMap.map<int, String>((k, v) => MapEntry(int.parse(k), v as String),);
      return Content(topic)
        ..version = decodedJson["version"]
        ..createType = decodedJson["createType"]
        ..dayLabelMap = dayLabelMap
      ;
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content(Topic.initEmpty());
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'topic': topic.toJson(),
      'createType': createType,
      'dayLabelMap': {
        for (final e in dayLabelMap.entries) e.key.toString(): e.value,
      },
    };
  }
```

### `data/entity/topic.dart`

```dart
  static Topic fromJson(Map<String, dynamic> json) {

    return Topic(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      title: json['title'] as String? ?? '',
      note: json['note'] as String? ?? '',
      person: json['person'] as String? ?? '',
      priority: PriorityType.fromId(json['priority'] ?? ''),
      weather: WeatherType.fromId(json['weather'] ?? ''),
      dayIndex: json['dayIndex'] as int? ?? 0,
      startTime: json['startTime'] != null ? TimeOfDayJson.fromJson(json['startTime']) : null,
      endTime: json['endTime'] != null ? TimeOfDayJson.fromJson(json['endTime']) : null,
      link: json['link'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      imageBase64: json['imageBase64'] as String? ?? '',
      complete: CompleteType.fromId(json['complete'] ?? ''),
      isOpenChild: json['isOpenChild'] as bool? ?? false,
      childTopicList: (json['childTopicList'] as List<dynamic>?)
          ?.map((e) => Topic.fromJson(e as Map<String, dynamic>))
          .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = {
      'id': id,
      'title': title,
      'note': note,
      'person': person,
      'priority': priority.id,
      'weather': weather.id,
      'dayIndex': dayIndex,
      'startTime': startTime?.toJson(),
      'endTime': endTime?.toJson(),
      'link': link,
      'colorHex': colorHex,
      'imageBase64': imageBase64,
      'complete': complete.id,
      'isOpenChild': isOpenChild,
      'childTopicList': childTopicList.map((x) => x.toJson()).toList(),
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
