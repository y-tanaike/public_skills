# Content format

- App ID: `requirement`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

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
      return Content(topic)
        ..version = decodedJson["version"]
        ..createType = decodedJson["createType"]
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
    };
  }
```

### `data/entity/topic.dart`

```dart
  static List<String> _stringListFromJson(dynamic value) {
    return (value as List<dynamic>?)?.map((e) => e.toString()).toList() ?? [];
  }

  static DateTime? _dateFromJson(dynamic value) {
    if (value == null) {
      return null;
    }
    if (value is int) {
      return DateTime.fromMillisecondsSinceEpoch(value);
    }
    return DateTime.tryParse(value.toString());
  }

  static Topic fromJson(Map<String, dynamic> json) {
    return Topic(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      title: json['title'] as String? ?? '',
      note: json['note'] as String? ?? '',
      person: json['person'] as String? ?? '',
      labelList: _stringListFromJson(json['labelList']),
      relatedTopicIdList: _stringListFromJson(json['relatedTopicIdList']),
      priority: PriorityType.fromId(json['priority'] ?? ''),
      link: json['link'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      status: SpecificationStatus.fromId(json['status'] ?? ''),
      itemType: ItemType.fromId(json['itemType'] ?? ''),
      isOpenChild: json['isOpenChild'] as bool? ?? false,
      releaseDate: _dateFromJson(json['releaseDate']),
      releaseVersion: json['releaseVersion'] as String? ?? '',
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
      'labelList': labelList,
      'relatedTopicIdList': relatedTopicIdList,
      'priority': priority.id,
      'link': link,
      'colorHex': colorHex,
      'status': status.id,
      'itemType': itemType.id,
      'isOpenChild': isOpenChild,
      'releaseVersion': releaseVersion,
      'childTopicList': childTopicList.map((x) => x.toJson()).toList(),
    };

    if (releaseDate != null) {
      data['releaseDate'] = DateTime(releaseDate!.year, releaseDate!.month, releaseDate!.day).toIso8601String();
    }

    return data;
  }
```

### `define/item_type.dart` identifiers

```dart
enum ItemType {
  item('item'),
  header('header');
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

### `define/specification_status.dart` identifiers

```dart
enum SpecificationStatus {
  draft('draft'),
  review('review'),
  approved('approved'),
  implemented('implemented'),
  released('released'),
  deprecated('deprecated');
```
