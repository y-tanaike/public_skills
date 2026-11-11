# Content format

- App ID: `inknote`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Use `layers[].strokes[]` for handwriting. Colors are integers; coordinates and pressure values are numeric. Stroke `color` is required for reconstruction. Keep at least one layer, a valid `activeLayerIndex`, and coordinates within the canvas. Follow the example for point arrays.

## Root keys

| Key | JSON type |
|---|---|
| `activeLayerIndex` | integer |
| `createType` | string |
| `height` | number |
| `layers` | array |
| `ruling` | string |
| `type` | string |
| `version` | integer |
| `width` | number |

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
    final dynamic decoded = jsonDecode(json);
    if (decoded is! Map) throw const FormatException('Invalid ink note file');
    final Map<String, dynamic> data = _migrate(Map<String, dynamic>.from(decoded));
    final dynamic width = data['width'];
    final dynamic height = data['height'];
    final dynamic layers = data['layers'];
    if (width is! num || height is! num || !width.isFinite || !height.isFinite || width <= 0 || height <= 0) {
      throw const FormatException('Invalid page size');
    }
    if (layers is! List || layers.isEmpty) throw const FormatException('Invalid layers');
    final List<InkLayer> parsedLayers = layers.map(InkLayer.fromJson).toList();
    final dynamic activeLayerIndex = data['activeLayerIndex'];
    if (activeLayerIndex != null && (activeLayerIndex is! int || activeLayerIndex < 0 || activeLayerIndex >= parsedLayers.length)) {
      throw const FormatException('Invalid active layer');
    }
    final dynamic ruling = data['ruling'];
    if (ruling != null && ruling is! String) throw const FormatException('Invalid ruling');
    return Content(
      width: width.toDouble(),
      height: height.toDouble(),
      layers: parsedLayers,
      activeLayerIndex: activeLayerIndex as int?,
      ruling: PageRuling.fromId(ruling as String?),
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'version': currentVersion,
      'type': fileType,
      'createType': 'Flutter',
      'width': width,
      'height': height,
      'layers': layers.map((InkLayer layer) => layer.toJson()).toList(),
      'activeLayerIndex': activeLayerIndex,
      if (ruling != PageRuling.none) 'ruling': ruling.id,
    };
  }
```

### `define/page_ruling.dart` identifiers

```dart
enum PageRuling {
  none('none', 'ruling_none', 0),
  lined('lined', 'ruling_lined', 7),
  grid('grid', 'ruling_grid', 5),
  dotted('dotted', 'ruling_dotted', 5);
```

### `data/entity/ink_layer.dart`

```dart
  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'id': id,
      'name': name,
      'isVisible': isVisible,
      'isLocked': isLocked,
      'strokes': strokes.map((Stroke stroke) => stroke.toJson()).toList(),
      if (texts.isNotEmpty) 'texts': texts.map((TextItem text) => text.toJson()).toList(),
    };
  }

  static InkLayer fromJson(dynamic json) {
    if (json is! Map || json['id'] is! String || json['name'] is! String || json['strokes'] is! List) {
      throw const FormatException('Invalid layer');
    }
    if (json['isVisible'] != null && json['isVisible'] is! bool) throw const FormatException('Invalid layer visibility');
    if (json['isLocked'] != null && json['isLocked'] is! bool) throw const FormatException('Invalid layer lock');
    if (json['texts'] != null && json['texts'] is! List) throw const FormatException('Invalid layer texts');
    return InkLayer(
      id: json['id'] as String,
      name: json['name'] as String,
      isVisible: json['isVisible'] as bool? ?? true,
      isLocked: json['isLocked'] as bool? ?? false,
      strokes: (json['strokes'] as List<dynamic>).map(Stroke.fromJson).toList(),
      texts: (json['texts'] as List<dynamic>? ?? <dynamic>[]).map(TextItem.fromJson).toList(),
    );
  }
```

### `data/entity/stroke.dart`

```dart
  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'id': id,
      'toolId': toolId,
      'color': color.toARGB32(),
      'size': size,
      'thinning': thinning,
      'smoothing': smoothing,
      'streamline': streamline,
      'startCap': startCap,
      'startTaperEnabled': startTaperEnabled,
      'startCustomTaper': startCustomTaper,
      'endCap': endCap,
      'endTaperEnabled': endTaperEnabled,
      'endCustomTaper': endCustomTaper,
      'points': points.map((InkPoint point) => point.toJson()).toList(),
      if (shapeType != null) 'shapeType': shapeType,
      if (isFilled) 'isFilled': true,
    };
  }

  static Stroke fromJson(dynamic json) {
    if (json is! Map) throw const FormatException('Invalid stroke');
    final dynamic id = json['id'];
    final dynamic toolId = json['toolId'];
    final dynamic color = json['color'];
    final dynamic points = json['points'];
    if (id is! String || id.isEmpty || toolId is! String) throw const FormatException('Invalid stroke');
    if (color is! int || color < 0 || color > 0xffffffff) throw const FormatException('Invalid stroke color');
    if (points is! List) throw const FormatException('Invalid stroke points');
    final dynamic shapeType = json['shapeType'];
    final dynamic isFilled = json['isFilled'];
    if (shapeType != null && shapeType is! String) throw const FormatException('Invalid stroke shapeType');
    if (isFilled != null && isFilled is! bool) throw const FormatException('Invalid stroke isFilled');
    return Stroke(
      id: id,
      toolId: toolId,
      color: Color(color),
      size: _readDouble(json['size'], 'size'),
      thinning: _readDouble(json['thinning'], 'thinning'),
      smoothing: _readDouble(json['smoothing'], 'smoothing'),
      streamline: _readDouble(json['streamline'], 'streamline'),
      startCap: _readBool(json['startCap'], 'startCap'),
      startTaperEnabled: _readBool(json['startTaperEnabled'], 'startTaperEnabled'),
      startCustomTaper: _readNullableDouble(json['startCustomTaper'], 'startCustomTaper'),
      endCap: _readBool(json['endCap'], 'endCap'),
      endTaperEnabled: _readBool(json['endTaperEnabled'], 'endTaperEnabled'),
      endCustomTaper: _readNullableDouble(json['endCustomTaper'], 'endCustomTaper'),
      points: points.map(InkPoint.fromJson).toList(),
      shapeType: shapeType as String?,
      isFilled: isFilled as bool? ?? false,
    );
  }
```

### `data/entity/text_item.dart`

```dart
  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'id': id,
      'text': text,
      'x': x,
      'y': y,
      'fontSize': fontSize,
      'color': color.toARGB32(),
      if (bold) 'bold': true,
      if (italic) 'italic': true,
      if (underline) 'underline': true,
      if (rotation != 0) 'rotation': rotation,
    };
  }

  static TextItem fromJson(dynamic json) {
    if (json is! Map || json['id'] is! String || json['text'] is! String) throw const FormatException('Invalid text');
    final dynamic color = json['color'];
    if (color is! int || color < 0 || color > 0xffffffff) throw const FormatException('Invalid text color');
    final double fontSize = _readDouble(json['fontSize'], 'fontSize');
    if (fontSize <= 0) throw const FormatException('Invalid text fontSize');
    return TextItem(
      id: json['id'] as String,
      text: json['text'] as String,
      x: _readDouble(json['x'], 'x'),
      y: _readDouble(json['y'], 'y'),
      fontSize: fontSize,
      color: Color(color),
      bold: _readBool(json['bold'], 'bold'),
      italic: _readBool(json['italic'], 'italic'),
      underline: _readBool(json['underline'], 'underline'),
      rotation: json['rotation'] == null ? 0 : _readDouble(json['rotation'], 'rotation'),
    );
  }
```

### `data/entity/ink_point.dart`

```dart
  List<num> toJson() {
    return pressure == null ? <num>[x, y] : <num>[x, y, pressure!];
  }

  static InkPoint fromJson(dynamic json) {
    if (json is! List || json.length < 2 || json.length > 3) throw const FormatException('Invalid point');
    final dynamic x = json[0];
    final dynamic y = json[1];
    final dynamic pressure = json.length == 3 ? json[2] : null;
    if (x is! num || y is! num || !x.isFinite || !y.isFinite) throw const FormatException('Invalid point');
    if (pressure != null && (pressure is! num || !pressure.isFinite)) throw const FormatException('Invalid pressure');
    return InkPoint(
      x: x.toDouble(),
      y: y.toDouble(),
      pressure: (pressure as num?)?.toDouble().clamp(0.0, 1.0),
    );
  }
```
