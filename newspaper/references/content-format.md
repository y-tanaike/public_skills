# Content format

- App ID: `newspaper`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

The publisher uses the legacy JSON key `shopName`. Articles use `textItems`; `verticalWriting` controls writing direction and `columns` sets column count. Photographs are excluded.

## Root keys

| Key | JSON type |
|---|---|
| `backgroundColor` | string |
| `badge` | string |
| `columns` | integer |
| `createType` | string |
| `description` | string |
| `imageItems` | array |
| `layoutType` | string |
| `newspaperStyle` | string |
| `note` | string |
| `period` | string |
| `shopName` | See conversion definitions below |
| `subtitle` | string |
| `textItems` | array |
| `title` | string |
| `version` | string |
| `verticalWriting` | boolean |

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
      final List<NewspaperTextItem> textItems = (decodedJson['textItems'] as List<dynamic>? ?? [])
          .map((e) => NewspaperTextItem.fromJson(e as Map<String, dynamic>))
          .toList();
      final List<NewspaperImageItem> imageItems = (decodedJson['imageItems'] as List<dynamic>? ?? [])
          .map((e) => NewspaperImageItem.fromJson(e as Map<String, dynamic>))
          .toList();
      return Content()
        .._legacyData = {
          for (final String key in _legacyKeys)
            if (decodedJson.containsKey(key)) key: decodedJson[key],
        }
        ..verticalWriting = decodedJson['verticalWriting'] is bool
            ? decodedJson['verticalWriting'] as bool
            : LocaleSettings.currentLocale.languageCode == 'ja'
        ..columns = (int.tryParse('${decodedJson['columns']}') ?? 3).clamp(2, 4)
        ..version = (decodedJson["version"] ?? "1").toString()
        ..createType = (decodedJson["createType"] ?? "Flutter").toString()
        ..title = (decodedJson["title"] ?? "").toString()
        ..subtitle = (decodedJson["subtitle"] ?? "").toString()
        ..period = (decodedJson["period"] ?? "").toString()
        ..description = (decodedJson["description"] ?? "").toString()
        ..mainImageBase64 = (decodedJson["mainImageBase64"] ?? "").toString()
        ..badge = (decodedJson["badge"] ?? "").toString()
        ..textItems = textItems
        ..imageItems = imageItems
        ..publisher = (decodedJson["shopName"] ?? "").toString()
        ..note = (decodedJson["note"] ?? "").toString()
        ..backgroundColor = (decodedJson["backgroundColor"] ?? "").toString()
        ..newspaperStyle = NewspaperStyle.fromId((decodedJson["newspaperStyle"] ?? "plain").toString()).name
        ..layoutType = LeafletLayoutType.fromId((decodedJson["layoutType"] ?? LeafletLayoutType.defaultForLocale(LocaleSettings.currentLocale.languageCode).id).toString()).id;
    } catch (e) {
      logger.e("error fromJson: $e");
      rethrow;
    }
  }

  Map<String, dynamic> toJson() {
    return {
      ..._legacyData,
      'verticalWriting': verticalWriting,
      'columns': columns,
      'version': version,
      'createType': createType,
      'title': title,
      'subtitle': subtitle,
      'period': period,
      'description': description,
      'mainImageBase64': mainImageBase64,
      'badge': badge,
      'textItems': textItems.map((item) => item.toJson()).toList(),
      'imageItems': imageItems.map((item) => item.toJson()).toList(),
      'shopName': publisher,
      'note': note,
      'backgroundColor': backgroundColor,
      'newspaperStyle': newspaperStyle,
      'layoutType': layoutType,
    };
  }
```

### `define/leaflet_layout_type.dart` identifiers

```dart
enum LeafletTemplateCategory {
  newspaper;
```

### `define/newspaper_style.dart` identifiers

```dart
enum NewspaperStyle {
  plain, japanese, american, british, european, letterpress, modern;
```

### `data/entity/newspaper_image_item.dart`

```dart
  static NewspaperImageItem fromJson(Map<String, dynamic> json) {
    return NewspaperImageItem(
      id: (json['id'] ?? '').toString(),
      imageBase64: (json['imageBase64'] ?? '').toString(),
      caption: (json['caption'] ?? '').toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'imageBase64': imageBase64,
      'caption': caption,
    };
  }
```

### `data/entity/newspaper_text_item.dart`

```dart
  static NewspaperTextItem fromJson(Map<String, dynamic> json) {
    return NewspaperTextItem(
      id: (json['id'] ?? '').toString(),
      title: (json['title'] ?? '').toString(),
      body: (json['body'] ?? '').toString(),
      color: (json['color'] ?? '').toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'body': body,
      'color': color,
    };
  }
```
