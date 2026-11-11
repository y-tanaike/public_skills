# Content format

- App ID: `pixelart`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

`layers[].pixels` is a map from the string index `y * width + x` to an integer ARGB color. This is pixel data, not an image attachment. Include `version: "1"` and `type: "pixelart"`; keep supported square dimensions and pixel indexes within bounds.

## Root keys

| Key | JSON type |
|---|---|
| `activeLayerIndex` | integer |
| `createType` | string |
| `height` | integer |
| `layers` | array |
| `pixels` | See conversion definitions below |
| `type` | string |
| `version` | string |
| `width` | integer |

Types use JSON terminology. Check nullability, nested elements, and defaults against the conversion definitions below. Image fields are out of scope even where they appear in the app's serializer.

## Nested elements, identifiers, and date conversions

The excerpts below preserve serialization statements from the app implementation checked on 2026-11-11; source comments are omitted. You do not need to execute Dart. `fromJson` specifies accepted types and defaults; `toJson` specifies output keys. Follow the actual date conversion units rather than assuming ISO timestamps. The excerpts are reference fragments, not standalone Dart programs.

### `data/entity/content.dart`

```dart
  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'name': name,
      'isVisible': isVisible,
      'pixels': pixels.map((int key, int value) => MapEntry<String, int>('$key', value)),
    };
  }

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
    final Map<String, dynamic> data = jsonDecode(json) as Map<String, dynamic>;
    if (data['version'] != '1' || data['type'] != 'pixelart' ||
        data['width'] is! int || data['width'] != data['height'] ||
        !supportedSizes.contains(data['width'])) {
      throw const FormatException('Invalid pixel art file');
    }
    final int size = data['width'] as int;
    if (data['pixels'] != null) {
      if (data['pixels'] is! Map) throw const FormatException('Invalid pixels');
      _parsePixels(Map<String, dynamic>.from(data['pixels'] as Map), size);
    }
    if (data['layers'] != null) {
      if (data['layers'] is! List || (data['layers'] as List<dynamic>).isEmpty) throw const FormatException('Invalid layers');
      final List<PixelLayer> layers = <PixelLayer>[];
      for (final dynamic layerData in data['layers'] as List<dynamic>) {
        if (layerData is! Map || layerData['name'] is! String || layerData['pixels'] is! Map) throw const FormatException('Invalid layer');
        if (layerData['isVisible'] != null && layerData['isVisible'] is! bool) throw const FormatException('Invalid layer visibility');
        layers.add(PixelLayer(
          name: layerData['name'] as String,
          isVisible: layerData['isVisible'] as bool? ?? true,
          pixels: _parsePixels(Map<String, dynamic>.from(layerData['pixels'] as Map), size),
        ));
      }
      final dynamic activeLayerIndex = data['activeLayerIndex'];
      if (activeLayerIndex != null && (activeLayerIndex is! int || activeLayerIndex < 0 || activeLayerIndex >= layers.length)) {
        throw const FormatException('Invalid active layer');
      }
      return Content(size: size, layers: layers, activeLayerIndex: activeLayerIndex as int?);
    }
    if (data['pixels'] is! Map) throw const FormatException('Invalid pixels');
    return Content(size: size, pixels: _parsePixels(Map<String, dynamic>.from(data['pixels'] as Map), size));
  }

  static Map<int, int> _parsePixels(Map<String, dynamic> values, int size) {
    final Map<int, int> pixels = <int, int>{};
    for (final MapEntry<String, dynamic> entry in values.entries) {
      final int? index = int.tryParse(entry.key);
      final dynamic color = entry.value;
      if (index == null || index < 0 || index >= size * size ||
          color is! int || color < 0 || color > 0xffffffff) {
        throw const FormatException('Invalid pixel');
      }
      if (color != 0) pixels[index] = color;
    }
    return pixels;
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'version': '1',
      'type': 'pixelart',
      'createType': 'Flutter',
      'width': width,
      'height': height,
      'pixels': compositePixels.map((int key, int value) => MapEntry<String, int>('$key', value)),
      'layers': layers.map((PixelLayer layer) => layer.toJson()).toList(),
      'activeLayerIndex': activeLayerIndex,
    };
  }
```
