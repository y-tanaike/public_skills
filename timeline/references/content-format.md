# Content format

- App ID: `timeline`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `anchorDate` | object |
| `anchorStyle` | string |
| `categoryList` | array |
| `createType` | string |
| `eventList` | array |
| `isDescending` | boolean |
| `layoutStyle` | string |
| `layoutType` | string |
| `version` | string |
| `yearColorHex` | string |

Types use JSON terminology. Check nullability, nested elements, and defaults against the conversion definitions below. Image fields are out of scope even where they appear in the app's serializer.

## Nested elements, identifiers, and date conversions

The excerpts below preserve serialization statements from the app implementation checked on 2026-11-11; source comments are omitted. You do not need to execute Dart. `fromJson` specifies accepted types and defaults; `toJson` specifies output keys. Follow the actual date conversion units rather than assuming ISO timestamps. The excerpts are reference fragments, not standalone Dart programs.

### `data/entity/content.dart`

```dart
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
      final Map<String, dynamic> decodedJson = jsonDecode(json);
      return fromJsonMap(decodedJson);
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  static Content fromJsonMap(Map<String, dynamic> json) {
    return Content(
      eventList: (json['eventList'] as List<dynamic>?)
              ?.map((e) => TimelineEvent.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      categoryList: (json['categoryList'] as List<dynamic>?)
              ?.map((e) => TimelineCategory.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      isDescending: json['isDescending'] as bool? ?? false,
      layoutType: TimelineLayoutType.fromId(json['layoutType'] as String? ?? ''),
      layoutStyle: TimelineLayoutStyle.fromId(json['layoutStyle'] as String? ?? ''),
      yearColorHex: json['yearColorHex'] as String? ?? '',
      anchorDate: EventDate.fromJsonNullable(json['anchorDate']),
      anchorStyle: AnchorStyle.fromId(json['anchorStyle'] as String? ?? ''),
    )
      ..version = json['version'] as String? ?? currentVersion
      ..createType = json['createType'] as String? ?? "Flutter";
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'eventList': eventList.map((e) => e.toJson()).toList(),
      'categoryList': categoryList.map((e) => e.toJson()).toList(),
      'isDescending': isDescending,
      'layoutType': layoutType.id,
      'layoutStyle': layoutStyle.id,
      'yearColorHex': yearColorHex,
      'anchorDate': anchorDate?.toJson(),
      'anchorStyle': anchorStyle.id,
    };
  }
```

### `define/anchor_style.dart` identifiers

```dart
enum AnchorStyle {
  age("age"),
  yearCount("year_count"),
  ;
```

### `define/timeline_layout_style.dart` identifiers

```dart
enum TimelineLayoutStyle {
  card("card"),
  compact("compact"),
  alternate("alternate"),
  photo("photo"),
  ;
```

### `define/timeline_layout_type.dart` identifiers

```dart
enum TimelineLayoutType {
  vertical("vertical"),
  horizontal("horizontal"),
  ;
```

### `data/entity/event_date.dart`

```dart
  Map<String, dynamic> toJson() {
    return {
      'year': year,
      'month': month,
      'day': day,
    };
  }

  static EventDate fromJson(Map<String, dynamic> json) {
    return EventDate(
      json['year'] as int? ?? DateTime.now().year,
      json['month'] as int?,
      json['day'] as int?,
    );
  }

  static EventDate? fromJsonNullable(dynamic json) {
    if (json is Map<String, dynamic>) {
      return fromJson(json);
    }
    return null;
  }
```

### `data/entity/timeline_category.dart`

```dart
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'colorHex': colorHex,
    };
  }

  static TimelineCategory fromJson(Map<String, dynamic> json) {
    return TimelineCategory(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      name: json['name'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? presetColorHexList.first,
    );
  }
```

### `data/entity/timeline_event.dart`

```dart
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'date': date.toJson(),
      'endDate': endDate?.toJson(),
      'title': title,
      'note': note,
      'place': place,
      'link': link,
      'imageList': imageList,
      'categoryId': categoryId,
      'colorHex': colorHex,
      'isHighlight': isHighlight,
    };
  }

  static TimelineEvent fromJson(Map<String, dynamic> json) {
    return TimelineEvent(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      date: EventDate.fromJsonNullable(json['date']) ?? EventDate.today(),
      endDate: EventDate.fromJsonNullable(json['endDate']),
      title: json['title'] as String? ?? '',
      note: json['note'] as String? ?? '',
      place: json['place'] as String? ?? '',
      link: json['link'] as String? ?? '',
      imageList: (json['imageList'] as List<dynamic>?)?.whereType<String>().toList() ?? [],
      categoryId: json['categoryId'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      isHighlight: json['isHighlight'] as bool? ?? false,
    );
  }
```
