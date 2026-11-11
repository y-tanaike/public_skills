# Content format

- App ID: `graph`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Match IDs in `axisList` with `graphValueList[].axisId` and graph axis references. Put numeric data in `graphItemList`, not only display settings in `graphList`.

## Root keys

| Key | JSON type |
|---|---|
| `axisList` | array |
| `createType` | string |
| `graphItemList` | array |
| `graphList` | array |
| `headerHeight` | integer |
| `headerWidth` | integer |
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
      final List<GraphItem> graphItemList = (decodedJson['graphItemList'] as List<dynamic>? ?? [])
          .map((e) => GraphItem.fromJson(e as Map<String, dynamic>))
          .toList();

      final List<GraphAxis> axisList = (decodedJson['axisList'] as List<dynamic>? ?? [])
          .map((e) => GraphAxis.fromJson(e as Map<String, dynamic>))
          .toList();

      final List<Graph> graphList = (decodedJson['graphList'] as List<dynamic>? ?? [])
          .map((e) => Graph.fromJson(e as Map<String, dynamic>))
          .toList();

      final Content content = Content()
        ..version = decodedJson["version"] as String? ?? "1"
        ..createType = decodedJson["createType"] as String? ?? "Flutter"
        ..graphItemList = graphItemList
        ..axisList = axisList
        ..graphList = graphList
        ..headerWidth = decodedJson["headerWidth"] as int? ?? AppConfigurator.itemTitleDefaultColSize.toInt()
        ..headerHeight = decodedJson["headerHeight"] as int? ?? AppConfigurator.headerColSize.toInt()
      ;
      if (content.graphList.isEmpty) {
        content.graphList.addAll(content.axisList.map((axis) => _createDefaultGraph(axis)));
      }
      return content;

    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'graphItemList': graphItemList.map((graphItem) => graphItem.toJson()).toList(),
      'axisList': axisList.map((axis) => axis.toJson()).toList(),
      'graphList': graphList.map((graph) => graph.toJson()).toList(),
      'headerWidth': headerWidth,
      'headerHeight': headerHeight,
    };
  }
```

### `define/value_type.dart` identifiers

```dart
enum ValueType {
  integer('integer'),
  decimal('decimal'),
  boolean('boolean'),
  date('date'),
  datetime('datetime'),
  string('string');
```

### `data/entity/graph.dart`

```dart
  static Graph fromJson(Map<String, dynamic> json) {
    return Graph(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      title: json['title'] as String? ?? '',
      xAxisId: json['xAxisId'] as String? ?? '',
      yAxisIdList: (json['yAxisIdList'] as List<dynamic>? ?? []).map((e) => e.toString()).toList(),
      graphType: GraphType.fromId(json['graphType'] ?? ''),
      graphSortType: GraphSortType.fromId(json['graphSortType'] ?? ''),
      sortAxisId: json['sortAxisId'] as String? ?? '',
      showTitle: json['showTitle'] as bool? ?? false,
      showLegend: json['showLegend'] as bool? ?? true,
      showDataLabel: json['showDataLabel'] as bool? ?? false,
      showGridLine: json['showGridLine'] as bool? ?? true,
      showXAxisTitle: json['showXAxisTitle'] as bool? ?? false,
      showYAxisTitle: json['showYAxisTitle'] as bool? ?? false,
      legendPosition: GraphLegendPosition.fromId(json['legendPosition'] ?? ''),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'xAxisId': xAxisId,
      'yAxisIdList': yAxisIdList,
      'graphType': graphType.id,
      'graphSortType': graphSortType.id,
      'sortAxisId': sortAxisId,
      'showTitle': showTitle,
      'showLegend': showLegend,
      'showDataLabel': showDataLabel,
      'showGridLine': showGridLine,
      'showXAxisTitle': showXAxisTitle,
      'showYAxisTitle': showYAxisTitle,
      'legendPosition': legendPosition.id,
    };
  }
```

### `data/entity/graph_axis.dart`

```dart
  static GraphAxis fromJson(Map<String, dynamic> json) {
    return GraphAxis(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      title: json['title'] as String? ?? '',
      note: json['note'] as String? ?? '',
      link: json['link'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      unit: json['unit'] as String? ?? '',
      valueType: ValueType.fromId(json['valueType'] ?? ''),
      minValue: (json['minValue'] as num?)?.toDouble(),
      maxValue: (json['maxValue'] as num?)?.toDouble(),
      minDateTime: json['minDateTime'] != null ? DateTime.parse(json['minDateTime']) : null,
      maxDateTime: json['maxDateTime'] != null ? DateTime.parse(json['maxDateTime']) : null,
      width: json['width'] as int? ?? AppConfigurator.colRowSize.toInt(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'note': note,
      'link': link,
      'colorHex': colorHex,
      'unit': unit,
      'valueType': valueType.id,
      'minValue': minValue,
      'maxValue': maxValue,
      'minDateTime': minDateTime?.toIso8601String(),
      'maxDateTime': maxDateTime?.toIso8601String(),
      'width': width,
    };
  }
```

### `data/entity/graph_item.dart`

```dart
  static GraphItem fromJson(Map<String, dynamic> json) {
    return GraphItem(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      title: json['title'] as String? ?? '',
      note: json['note'] as String? ?? '',
      priority: PriorityType.fromId(json['priority'] ?? ''),
      link: json['link'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      graphValueList: (json['graphValueList'] as List<dynamic>? ?? [])
          .map((e) => GraphValue.fromJson(e as Map<String, dynamic>))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'note': note,
      'priority': priority.id,
      'link': link,
      'colorHex': colorHex,
      'graphValueList': graphValueList.map((graphValue) => graphValue.toJson()).toList(),
    };
  }
```

### `data/entity/graph_value.dart`

```dart
  static GraphValue fromJson(Map<String, dynamic> json) {
    return GraphValue(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      axisId: json['axisId'] as String? ?? '',
      value: (json['value'] as num?)?.toDouble(),
      boolValue: json['boolValue'] as bool?,
      datetime: json['datetime'] != null ? DateTime.parse(json['datetime']) : null,
      label: json['label'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'axisId': axisId,
      'value': value,
      'boolValue': boolValue,
      'datetime': datetime?.toIso8601String(),
      'label': label,
    };
  }
```

### `define/graph_legend_position.dart` identifiers

```dart
enum GraphLegendPosition {
  top('top'),
  bottom('bottom'),
  left('left'),
  right('right');
```

### `define/graph_sort_type.dart` identifiers

```dart
enum GraphSortType {
  input('input'),
  asc('asc'),
  desc('desc');
```

### `define/graph_type.dart` identifiers

```dart
enum GraphType {
  bar('bar'),
  line('line'),
  area('area'),
  scatter('scatter'),
  pie('pie');
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
