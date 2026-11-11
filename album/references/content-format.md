# Content format

- App ID: `album`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Share photo slots, page headings, captions, and layout settings. Image files are excluded. Do not describe the result as a complete album containing photographs.

## Root keys

| Key | JSON type |
|---|---|
| `albumSubtitle` | See conversion definitions below |
| `albumTitle` | See conversion definitions below |
| `backgroundColor` | string |
| `backgroundStyle` | string |
| `bookTemplateId` | string |
| `canvasRatio` | string |
| `cornerRadius` | integer |
| `createType` | string |
| `frameColor` | string |
| `frameWidth` | integer |
| `pages` | array |
| `photoGap` | integer |
| `showPageNumber` | boolean |
| `showShadow` | boolean |
| `textColor` | string |
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
    if (json.trim().isEmpty) {
      return Content();
    }
    final Map<String, dynamic> decodedJson = jsonDecode(json) as Map<String, dynamic>;
    final String legacyAlbumTitle = (decodedJson['albumTitle'] ?? '').toString();
    final String legacyAlbumSubtitle = (decodedJson['albumSubtitle'] ?? '').toString();
    final Content content = Content()
      ..version = (decodedJson['version'] ?? '1').toString()
      ..createType = (decodedJson['createType'] ?? 'Flutter').toString()
      ..canvasRatio = _canvasOrientationFromId((decodedJson['canvasRatio'] ?? '').toString())
      ..showPageNumber = decodedJson['showPageNumber'] == true
      ..backgroundStyle = (decodedJson['backgroundStyle'] ?? _legacyPageValue(decodedJson, 'backgroundStyle') ?? 'plain').toString()
      ..backgroundImageBase64 = (decodedJson['backgroundImageBase64'] ?? _legacyPageValue(decodedJson, 'backgroundImageBase64') ?? '').toString()
      ..backgroundColor = (decodedJson['backgroundColor'] ?? _legacyPageValue(decodedJson, 'backgroundColor') ?? '').toString()
      ..frameColor = (decodedJson['frameColor'] ?? _legacyPageValue(decodedJson, 'frameColor') ?? '').toString()
      ..textColor = (decodedJson['textColor'] ?? _legacyPageValue(decodedJson, 'textColor') ?? '').toString()
      ..frameWidth = _toInt(decodedJson['frameWidth'] ?? _legacyPageValue(decodedJson, 'frameWidth'), 0).clamp(0, maxFrameWidth)
      ..photoGap = _toInt(decodedJson['photoGap'] ?? _legacyPageValue(decodedJson, 'photoGap'), 6).clamp(0, maxPhotoGap)
      ..cornerRadius = _toInt(decodedJson['cornerRadius'] ?? _legacyPageValue(decodedJson, 'cornerRadius'), 8).clamp(0, maxCornerRadius)
      ..showShadow = _toBool(decodedJson['showShadow'] ?? _legacyPageValue(decodedJson, 'showShadow'), false);
    content.bookTemplateId = AlbumBookTemplates.fromId((decodedJson['bookTemplateId'] ?? AlbumBookTemplates.customId).toString()).id;
    if (decodedJson['pages'] is List) {
      content.pages = (decodedJson['pages'] as List<dynamic>)
          .map((dynamic page) => AlbumPage.fromJson(page as Map<String, dynamic>)).toList();
    }
    content.normalizePages();
    final AlbumPage frontCover = content.pages.first;
    bool migratedAlbumInformation = false;
    if (frontCover.title.isEmpty && legacyAlbumTitle.isNotEmpty) {
      frontCover.title = legacyAlbumTitle;
      migratedAlbumInformation = true;
    }
    if (frontCover.subtitle.isEmpty && legacyAlbumSubtitle.isNotEmpty) {
      frontCover.subtitle = legacyAlbumSubtitle;
      migratedAlbumInformation = true;
    }
    if (migratedAlbumInformation) {
      frontCover.showTitle = true;
    }
    return content;
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'canvasRatio': canvasRatio,
      'showPageNumber': showPageNumber,
      'bookTemplateId': bookTemplateId,
      'backgroundStyle': backgroundStyle,
      'backgroundImageBase64': backgroundImageBase64,
      'backgroundColor': backgroundColor,
      'frameColor': frameColor,
      'textColor': textColor,
      'frameWidth': frameWidth,
      'photoGap': photoGap,
      'cornerRadius': cornerRadius,
      'showShadow': showShadow,
      'pages': pages.map((AlbumPage page) => page.toJson()).toList(),
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

### `data/entity/album_page.dart`

```dart
  static AlbumPage fromJson(Map<String, dynamic> decodedJson) {
    try {
      final List<CollagePhotoItem> photoItems = (decodedJson['photoItems'] as List<dynamic>? ?? [])
          .map((e) => CollagePhotoItem.fromJson(e as Map<String, dynamic>))
          .toList();

      return AlbumPage()
        ..id = (decodedJson["id"] ?? "").toString().isEmpty ? Uuid.v4().toString() : decodedJson["id"].toString()
        ..pageType = AlbumPageType.fromId((decodedJson["pageType"] ?? "").toString()).id
        ..backgroundStyle = (decodedJson["backgroundStyle"] ?? "plain").toString()
        ..backgroundImageBase64 = (decodedJson["backgroundImageBase64"] ?? "").toString()
        ..title = (decodedJson["title"] ?? "").toString()
        ..subtitle = (decodedJson["subtitle"] ?? "").toString()
        ..caption = (decodedJson["caption"] ?? "").toString()
        ..showTitle = _toBool(decodedJson["showTitle"], true)
        ..photoItems = photoItems
        ..showPhotos = _toBool(decodedJson["showPhotos"], true)
        ..layoutType = CollageLayouts.fromId((decodedJson["layoutType"] ?? CollageLayouts.defaultLayoutId).toString()).id
        ..backgroundColor = (decodedJson["backgroundColor"] ?? "").toString()
        ..frameColor = (decodedJson["frameColor"] ?? "").toString()
        ..textColor = (decodedJson["textColor"] ?? "").toString()
        ..frameWidth = _toInt(decodedJson["frameWidth"], 0).clamp(0, maxFrameWidth)
        ..photoGap = _toInt(decodedJson["photoGap"], 6).clamp(0, maxPhotoGap)
        ..cornerRadius = _toInt(decodedJson["cornerRadius"], 8).clamp(0, maxCornerRadius)
        ..showShadow = _toBool(decodedJson["showShadow"], false);
    } catch (e) {
      logger.e("error fromJson: $e");
      return AlbumPage();
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'pageType': pageType,
      'backgroundStyle': backgroundStyle,
      'backgroundImageBase64': backgroundImageBase64,
      'title': title,
      'subtitle': subtitle,
      'caption': caption,
      'showTitle': showTitle,
      'photoItems': photoItems.map((item) => item.toJson()).toList(),
      'showPhotos': showPhotos,
      'layoutType': layoutType,
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
