# Content format

- App ID: `led`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `backgroundColor` | string |
| `bold` | boolean |
| `createType` | string |
| `dotSize` | string |
| `dotStyle` | string |
| `fontType` | string |
| `frameColor` | string |
| `frameType` | string |
| `glow` | boolean |
| `messages` | array |
| `mirror` | boolean |
| `templateType` | string |
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
      final List<LedMessage> messages = (decodedJson['messages'] as List<dynamic>? ?? [])
          .map((e) => LedMessage.fromJson(e as Map<String, dynamic>))
          .toList();

      return Content()
        ..version = (decodedJson["version"] ?? "1").toString()
        ..createType = (decodedJson["createType"] ?? "Flutter").toString()
        ..messages = messages
        ..backgroundColor = (decodedJson["backgroundColor"] ?? "#000000").toString()
        ..fontType = LedFontType.fromId((decodedJson["fontType"] ?? "").toString()).id
        ..bold = _parseBool(decodedJson["bold"], true)
        ..glow = _parseBool(decodedJson["glow"], true)
        ..dotStyle = LedDotStyle.fromId((decodedJson["dotStyle"] ?? "").toString()).id
        ..dotSize = LedDotSize.fromId((decodedJson["dotSize"] ?? "").toString()).id
        ..mirror = _parseBool(decodedJson["mirror"], false)
        ..frameType = LedFrameType.fromId((decodedJson["frameType"] ?? "").toString()).id
        ..frameColor = (decodedJson["frameColor"] ?? "#FFB000").toString()
        ..templateType = LedTemplateType.fromId((decodedJson["templateType"] ?? "").toString()).id;
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'messages': messages.map((message) => message.toJson()).toList(),
      'backgroundColor': backgroundColor,
      'fontType': fontType,
      'bold': bold,
      'glow': glow,
      'dotStyle': dotStyle,
      'dotSize': dotSize,
      'mirror': mirror,
      'frameType': frameType,
      'frameColor': frameColor,
      'templateType': templateType,
    };
  }

  static bool _parseBool(Object? value, bool defaultValue) {
    if (value is bool) {
      return value;
    }
    if (value == null) {
      return defaultValue;
    }
    return value.toString() == "true";
  }
```

### `define/led_dot_style.dart` identifiers

```dart
enum LedDotStyle {
  none("none"),
  round("round"),
  square("square"),
  star("star"),
  heart("heart");
```

### `define/led_font_type.dart` identifiers

```dart
enum LedFontType {
  gothic("gothic"),
  mincho("mincho"),
  rounded("rounded"),
  mono("mono"),
  dotGothic("dotGothic", assetFileName: "DotGothic16-Regular.ttf", flutterFontFamily: "LedDotGothic16", displayName: "DotGothic16"),
  delaGothic("delaGothic", assetFileName: "DelaGothicOne-Regular.ttf", flutterFontFamily: "LedDelaGothicOne", displayName: "Dela Gothic One"),
  rocknroll("rocknroll", assetFileName: "RocknRollOne-Regular.ttf", flutterFontFamily: "LedRocknRollOne", displayName: "RocknRoll One"),
  yuseiMagic("yuseiMagic", assetFileName: "YuseiMagic-Regular.ttf", flutterFontFamily: "LedYuseiMagic", displayName: "Yusei Magic"),
  pressStart("pressStart", assetFileName: "PressStart2P-Regular.ttf", flutterFontFamily: "LedPressStart2P", displayName: "Press Start 2P", isLatinOnly: true),
  vt323("vt323", assetFileName: "VT323-Regular.ttf", flutterFontFamily: "LedVT323", displayName: "VT323", isLatinOnly: true),
  orbitron("orbitron", assetFileName: "Orbitron-Variable.ttf", flutterFontFamily: "LedOrbitron", displayName: "Orbitron", isLatinOnly: true),
  bebasNeue("bebasNeue", assetFileName: "BebasNeue-Regular.ttf", flutterFontFamily: "LedBebasNeue", displayName: "Bebas Neue", isLatinOnly: true),
  monoton("monoton", assetFileName: "Monoton-Regular.ttf", flutterFontFamily: "LedMonoton", displayName: "Monoton", isLatinOnly: true);
```

### `define/led_frame_type.dart` identifiers

```dart
enum LedFrameType {
  none("none", 0),
  line("line", 0.05),
  doubleLine("double", 0.07),
  neon("neon", 0.07),
  bulbs("bulbs", 0.12),
  chase("chase", 0.08),
  rainbow("rainbow", 0.05),
  caution("caution", 0.08),
  corners("corners", 0.06);
```

### `define/led_item_type.dart` identifiers

```dart
enum LedItemType {
  message("message"),
  effect("effect");
```

### `define/led_template_type.dart` identifiers

```dart
enum LedTemplateCategory {
  color,
  scene;
```

### `data/entity/led_message.dart`

```dart
  static LedMessage fromJson(Map<String, dynamic> json) {
    return LedMessage(
      id: (json['id'] ?? Uuid.v4().toString()).toString(),
      text: (json['text'] ?? '').toString(),
      itemType: LedItemType.fromId((json['itemType'] ?? '').toString()).id,
      effectType: LedEffectType.fromId((json['effectType'] ?? '').toString()).id,
      textColor: (json['textColor'] ?? '#FF3B30').toString(),
      rainbow: json['rainbow'] == true || json['rainbow'].toString() == 'true',
      animation: LedAnimationType.fromId((json['animation'] ?? '').toString()).id,
      speed: _clampInt(json['speed'], minSpeed, maxSpeed, 5),
      displaySeconds: _clampInt(json['displaySeconds'], minDisplaySeconds, maxDisplaySeconds, 3),
      textSizePercent: _clampInt(json['textSizePercent'], minTextSizePercent, maxTextSizePercent, 70),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'itemType': itemType,
      'effectType': effectType,
      'text': text,
      'textColor': textColor,
      'rainbow': rainbow,
      'animation': animation,
      'speed': speed,
      'displaySeconds': displaySeconds,
      'textSizePercent': textSizePercent,
    };
  }
```

### `define/led_animation_type.dart` identifiers

```dart
enum LedAnimationType {
  scrollLeft("scrollLeft"),
  scrollRight("scrollRight"),
  scrollUp("scrollUp"),
  scrollDown("scrollDown"),
  still("still"),
  blink("blink"),
  fade("fade"),
  typewriter("typewriter");
```

### `define/led_effect_type.dart` identifiers

```dart
enum LedEffectCategory {
  calm,
  lively;
```
