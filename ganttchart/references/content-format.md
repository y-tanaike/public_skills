# Content format

- App ID: `ganttchart`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

`startDate` and `endDate` are seconds since 2001-01-01 UTC, not Unix seconds or ISO strings. Subtract 978307200 from Unix seconds. Nest tasks in `topic.childTopicList`; use `predecessorTopicIdList` for dependencies. IDs must be unique and references must resolve to existing tasks. Set `isOpenChild: true` on expanded parents.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `topic` | object |
| `version` | string |

Types use JSON terminology. Check nullability, nested elements, and defaults against the conversion definitions below. Image fields are out of scope even where they appear in the app's serializer.

## Nested elements, identifiers, and date conversions

The excerpts below preserve serialization statements from the app implementation checked on 2026-11-11; source comments are omitted. You do not need to execute Dart. `fromJson` specifies accepted types and defaults; `toJson` specifies output keys. Follow the actual date conversion units rather than assuming ISO timestamps. The excerpts are reference fragments, not standalone Dart programs.

### `data/entity/content.dart`

```dart
  static Content? tryFromJson(String json) {
    try {
      logger.d("tryFromJson $json");
      final Map<String, dynamic> decodedJson = jsonDecode(json);
      Topic topic = Topic.fromJson(decodedJson["topic"]);
      return Content(topic)
        ..version = decodedJson["version"]
        ..createType = decodedJson["createType"]
      ;
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
    return tryFromJson(json) ?? Content(Topic.initEmpty());
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'topic': topic.toJson(),
      'createType': createType,
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
      startDate: json['startDate'] != null ? DateTime.fromMillisecondsSinceEpoch(json['startDate'] * 1000 + 978307200 * 1000) : null,
      endDate: json['endDate'] != null ? DateTime.fromMillisecondsSinceEpoch(json['endDate'] * 1000 + 978307200 * 1000) : null,
      link: json['link'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      complete: CompleteType.fromId(json['complete'] ?? ''),
      isOpenChild: json['isOpenChild'] as bool? ?? false,
      predecessorTopicIdList: (json['predecessorTopicIdList'] as List<dynamic>?)?.whereType<String>().toList() ?? [],
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
      'link': link,
      'colorHex': colorHex,
      'complete': complete.id,
      'isOpenChild': isOpenChild,
      'predecessorTopicIdList': predecessorTopicIdList,
      'childTopicList': childTopicList.map((x) => x.toJson()).toList(),
    };

    if (startDate != null) {
      data['startDate'] = (startDate!.millisecondsSinceEpoch - 978307200 * 1000) ~/ 1000;
    }
    if (endDate != null) {
      data['endDate'] = (endDate!.millisecondsSinceEpoch - 978307200 * 1000) ~/ 1000;
    }

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
