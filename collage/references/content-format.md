# Content format

- App ID: `collage`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Share photo slots, headings, captions, and layout settings. Image files are excluded. Do not claim that the photographs themselves were embedded.

## Root keys

| Key | JSON type |
|---|---|
| `backgroundColor` | string |
| `canvasRatio` | string |
| `caption` | string |
| `cornerRadius` | integer |
| `createType` | string |
| `frameColor` | string |
| `frameWidth` | integer |
| `layoutType` | string |
| `photoGap` | integer |
| `photoItems` | array |
| `showShadow` | boolean |
| `showTitle` | boolean |
| `subtitle` | string |
| `textColor` | string |
| `title` | string |
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
      final List<CollagePhotoItem> photoItems = (decodedJson['photoItems'] as List<dynamic>? ?? [])
          .map((e) => CollagePhotoItem.fromJson(e as Map<String, dynamic>))
          .toList();

      return Content()
        ..version = (decodedJson["version"] ?? "1").toString()
        ..createType = (decodedJson["createType"] ?? "Flutter").toString()
        ..title = (decodedJson["title"] ?? "").toString()
        ..subtitle = (decodedJson["subtitle"] ?? "").toString()
        ..caption = (decodedJson["caption"] ?? "").toString()
        ..showTitle = _toBool(decodedJson["showTitle"], true)
        ..photoItems = photoItems
        ..layoutType = CollageLayouts.fromId((decodedJson["layoutType"] ?? CollageLayouts.defaultLayoutId).toString()).id
        ..canvasRatio = CollageCanvasRatio.fromId((decodedJson["canvasRatio"] ?? CollageCanvasRatio.square.id).toString()).id
        ..backgroundColor = (decodedJson["backgroundColor"] ?? "").toString()
        ..frameColor = (decodedJson["frameColor"] ?? "").toString()
        ..textColor = (decodedJson["textColor"] ?? "").toString()
        ..frameWidth = _toInt(decodedJson["frameWidth"], 0)
        ..photoGap = _toInt(decodedJson["photoGap"], 6)
        ..cornerRadius = _toInt(decodedJson["cornerRadius"], 8)
        ..showShadow = _toBool(decodedJson["showShadow"], false);
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'title': title,
      'subtitle': subtitle,
      'caption': caption,
      'showTitle': showTitle,
      'photoItems': photoItems.map((item) => item.toJson()).toList(),
      'layoutType': layoutType,
      'canvasRatio': canvasRatio,
      'backgroundColor': backgroundColor,
      'frameColor': frameColor,
      'textColor': textColor,
      'frameWidth': frameWidth,
      'photoGap': photoGap,
      'cornerRadius': cornerRadius,
      'showShadow': showShadow,
    };
  }
```

### `define/collage_canvas_ratio.dart` identifiers

```dart
enum CollageCanvasRatio {
  square("square", 1080, 1080, 210, 210),
  portrait("portrait", 1080, 1350, 210, 262),
  story("story", 1080, 1920, 169, 300),
  widescreen("widescreen", 1920, 1080, 300, 169),
  landscape("landscape", 1200, 800, 297, 198),
  a4("a4", 794, 1123, 210, 297),
  a4Landscape("a4_landscape", 1123, 794, 297, 210);
```

### `define/collage_layout.dart` identifiers

```dart
enum CollageTemplateCategory {
  grid,
  feature,
  comment,
  style,
  free;
```

### `data/entity/collage_photo_item.dart`

```dart
  static CollagePhotoItem fromJson(Map<String, dynamic> json) {
    return CollagePhotoItem(
      id: (json['id'] ?? '').toString(),
      imageBase64: (json['imageBase64'] ?? '').toString(),
      caption: (json['caption'] ?? '').toString(),
      scale: _toDouble(json['scale'], defaultScale),
      rotation: _toDouble(json['rotation'], 0),
      offsetX: _toDouble(json['offsetX'], 0),
      offsetY: _toDouble(json['offsetY'], 0),
      x: _toDouble(json['x'], 10),
      y: _toDouble(json['y'], 10),
      width: _toDouble(json['width'], defaultWidth),
      frameRotation: _toDouble(json['frameRotation'], 0),
      zIndex: _toInt(json['zIndex'], 0),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'imageBase64': imageBase64,
      'caption': caption,
      'scale': scale,
      'rotation': rotation,
      'offsetX': offsetX,
      'offsetY': offsetY,
      'x': x,
      'y': y,
      'width': width,
      'frameRotation': frameRotation,
      'zIndex': zIndex,
    };
  }
```
