# Content format

- App ID: `cornell`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

`noteDelta` is a Quill Delta array, `ink` holds handwriting, `cues` holds cue items, and `summary` holds the summary. End the main text with a newline. Unlike the Document app, do not encode the Delta array as a nested JSON string. Preserve numeric stroke `color` and `points`. Keep at least one ink layer and a valid `activeLayerIndex`, even for text notes.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `cues` | array |
| `ink` | object |
| `noteDelta` | array |
| `noteMode` | string |
| `summary` | object |
| `type` | string |
| `version` | integer |

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
    if (decoded is! Map) throw const FormatException('Invalid cornell note file');
    final Map<String, dynamic> data = _migrate(Map<String, dynamic>.from(decoded));
    final dynamic noteDelta = data['noteDelta'];
    final List<dynamic>? cues = data['cues'] is List ? data['cues'] as List<dynamic> : null;
    if (noteDelta != null && noteDelta is! List) throw const FormatException('Invalid note text');
    if (data['cues'] != null && cues == null) throw const FormatException('Invalid cues');
    return Content(
      noteMode: NoteMode.fromId(data['noteMode'] as String?),
      ink: InkPage.fromJson(data['ink']),
      noteDocument: noteDelta == null || noteDelta.isEmpty ? Document() : Document.fromJson(noteDelta),
      cues: cues?.map(CueItem.fromJson).toList(),
      summary: SummaryItem.fromJson(data['summary']),
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'version': currentVersion,
      'type': fileType,
      'createType': 'Flutter',
      'noteMode': noteMode.id,
      'ink': ink.toJson(),
      'noteDelta': noteDocument.toDelta().toJson(),
      'cues': cues.map((CueItem cue) => cue.toJson()).toList(),
      'summary': summary.toJson(),
    };
  }
```

### `define/note_mode.dart` identifiers

```dart
enum NoteMode {
  text('text', 'note_mode_text', Icons.notes),
  ink('ink', 'note_mode_ink', Icons.draw_outlined);
```

### `data/entity/cue_item.dart`

```dart
  static CueItem fromJson(dynamic json) {
    if (json is! Map) throw const FormatException('Invalid cue item');
    final dynamic id = json['id'];
    final dynamic keyword = json['keyword'];
    final dynamic note = json['note'];
    final dynamic labels = json['labels'];
    final dynamic link = json['link'];
    final dynamic color = json['color'];
    if ((color != null && color is! int) || (keyword != null && keyword is! String) || (note != null && note is! String) || (labels != null && labels is! List) || (link != null && link is! String)) {
      throw const FormatException('Invalid cue item');
    }
    return CueItem(
      id: id is String && id.isNotEmpty ? id : Uuid.v4().toString(),
      keyword: keyword as String? ?? '',
      note: note as String? ?? '',
      labels: LabelUtil.normalize(labels as List<dynamic>? ?? const <dynamic>[]),
      status: CueStatus.fromId(json['status'] as String?),
      priority: PriorityType.fromId(json['priority'] as String?),
      link: link as String? ?? '',
      color: color == null ? null : Color(color as int),
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'id': id,
      'keyword': keyword,
      if (note.isNotEmpty) 'note': note,
      if (labels.isNotEmpty) 'labels': labels,
      if (status != null) 'status': status!.id,
      if (priority.isSet) 'priority': priority.id,
      if (link.isNotEmpty) 'link': link,
      if (color != null) 'color': color!.toARGB32(),
    };
  }
```

### `data/entity/ink_page.dart`

```dart
  static InkPage fromJson(dynamic data) {
    if (data is! Map) throw const FormatException('Invalid ink page');
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
    return InkPage(
      width: width.toDouble(),
      height: height.toDouble(),
      layers: parsedLayers,
      activeLayerIndex: activeLayerIndex as int?,
      ruling: PageRuling.fromId(ruling as String?),
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'width': width,
      'height': height,
      'layers': layers.map((InkLayer layer) => layer.toJson()).toList(),
      'activeLayerIndex': activeLayerIndex,
      if (ruling != PageRuling.none) 'ruling': ruling.id,
    };
  }
```

### `data/entity/summary_item.dart`

```dart
  static SummaryItem fromJson(dynamic json) {
    if (json == null) return SummaryItem();
    if (json is String) return SummaryItem(text: json);
    if (json is! Map) throw const FormatException('Invalid summary');
    final dynamic text = json['text'];
    final dynamic color = json['color'];
    final dynamic link = json['link'];
    final dynamic labels = json['labels'];
    if ((text != null && text is! String) || (color != null && color is! int) || (link != null && link is! String) || (labels != null && labels is! List)) {
      throw const FormatException('Invalid summary');
    }
    return SummaryItem(
      text: text as String? ?? '',
      color: color == null ? null : Color(color as int),
      link: link as String? ?? '',
      labels: LabelUtil.normalize(labels as List<dynamic>? ?? const <dynamic>[]),
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'text': text,
      if (color != null) 'color': color!.toARGB32(),
      if (link.isNotEmpty) 'link': link,
      if (labels.isNotEmpty) 'labels': labels,
    };
  }
```

### `define/cue_status.dart` identifiers

```dart
enum CueStatus {
  unknown('unknown', 'cue_status_unknown', Icons.help_outline, Colors.red),
  reviewing('reviewing', 'cue_status_reviewing', Icons.autorenew, Colors.orange),
  understood('understood', 'cue_status_understood', Icons.check_circle_outline, Colors.green);
```

### `define/priority_type.dart` identifiers

```dart
enum PriorityType {
  initial('initial'),
  priority1('priority_1'),
  priority2('priority_2'),
  priority3('priority_3'),
  priority4('priority_4'),
  priority5('priority_5');
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
