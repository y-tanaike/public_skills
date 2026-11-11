# Content format

- App ID: `checksheet`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Use root `fileEntity`, `colList`, `rowList`, and `cellList`. Provide at least one column and row. Cell `col` and `row` are zero-based indexes within those arrays. Do not send IDs, file IDs, storage timestamps, or images. Set `fileEntity.checkTypeId` and the corresponding cell state such as `tickId`.

## Root keys

| Key | JSON type |
|---|---|
| `cellList` | array |
| `colList` | array |
| `fileEntity` | object |
| `rowList` | array |

Types use JSON terminology. Check nullability, nested elements, and defaults against the conversion definitions below. Image fields are out of scope even where they appear in the app's serializer.

## Nested elements, identifiers, and date conversions

The excerpts below preserve serialization statements from the app implementation checked on 2026-11-11; source comments are omitted. You do not need to execute Dart. `fromJson` specifies accepted types and defaults; `toJson` specifies output keys. Follow the actual date conversion units rather than assuming ISO timestamps. The excerpts are reference fragments, not standalone Dart programs.

### `data/entity/file_full_entity.dart`

```dart
  Map<String, dynamic> toJson() {
    return {
      'fileEntity': fileEntity.toJson(),
      'cellList': cellList.map((cell) => cell.toJson()).toList(),
      'colList': colList.map((col) => col.toJson()).toList(),
      'rowList': rowList.map((row) => row.toJson()).toList(),
    };
  }

  static FileFullEntity? tryFromJson(String json, String newFileId) {
    try {
      logger.d("import json $json");
      final Map<String, dynamic> decodedJson = jsonDecode(json);
      FileEntity fileEntity = FileEntityEx.fromJson(decodedJson["fileEntity"], newFileId);
      List<CellEntity> cellList = [];
      if (decodedJson['cellList'] != null) {
        cellList = List.from(decodedJson['cellList'])
            .map((cellJson) => CellEntityEx.fromJson(cellJson, newFileId))
            .toList();
      }
      List<ColRowEntity> colList = [];
      if (decodedJson['colList'] != null) {
        colList = List.from(decodedJson['colList'])
            .map((colJson) => ColRowEntityEx.fromJson(colJson, newFileId))
            .toList();
      }
      List<ColRowEntity> rowList = [];
      if (decodedJson['rowList'] != null) {
        rowList = List.from(decodedJson['rowList'])
            .map((rowJson) => ColRowEntityEx.fromJson(rowJson, newFileId))
            .toList();
      }
      return FileFullEntity(fileEntity, cellList, colList, rowList);

    } catch (e) {
      logger.e("error tryFromJson: $e");
      return null;
    }
  }

  static FileFullEntity fromJson(String json, String newFileId) {
    return tryFromJson(json, newFileId) ?? FileFullEntity(FileEntityEx.init(name: ""), [], [], []);
  }
```

### `data/entity/cell_entity_ex.dart`

```dart
  static DateTime? _parseDateTime(dynamic value) {
    return value is String ? DateTime.tryParse(value) : null;
  }

  static CellEntity fromJson(Map<String, dynamic> json, String fileId) {
    DateTime created = _parseDateTime(json['created']) ?? DateTime.now();
    DateTime modified = _parseDateTime(json['modified']) ?? created;
    return CellEntity(Uuid.v4().toString(), fileId, created, modified)
      ..col = json['col'] ?? -1
      ..row = json['row'] ?? -1
      ..title = json['title'] ?? ""
      ..note = json['note'] ?? ""
      ..link = json['link'] ?? ""
      ..colorHex = json['colorHex'] ?? ""
      ..imageBase64 = json['imageBase64'] ?? ""
      ..tickId = json['tickId'] ?? ""
      ..circleCrossId = json['circleCrossId'] ?? ""
      ..circleTriangleCrossId = json['circleTriangleCrossId'] ?? ""
      ..tickCrossId = json['tickCrossId'] ?? ""
      ..flagId = json['flagId'] ?? ""
      ..personId = json['personId'] ?? ""
      ..peopleId = json['peopleId'] ?? ""
      ..starId = json['starId'] ?? ""
      ..priorityId = json['priorityId'] ?? ""
      ..weatherId = json['weatherId'] ?? ""
      ..completeId = json['completeId'] ?? ""
      ..goodBadId = json['goodBadId'] ?? ""
      ..handId = json['handId'] ?? ""
      ..trunpId = json['trunpId'] ?? ""
      ..batteryId = json['batteryId'] ?? ""
      ..faceId = json['faceId'] ?? ""
      ..customTextId = json['customTextId'] ?? ""
      ..customIconId = json['customIconId'] ?? ""
      ..fonttype = json['fonttype'] ?? ""
      ..verticalAlign = json['verticalAlign'] ?? ""
      ..horizontalAlign = json['horizontalAlign'] ?? "";
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'fileId': fileId,
      'col': col,
      'row': row,
      'title': title,
      'note': note,
      'link': link,
      'colorHex': colorHex,
      'imageBase64': imageBase64,
      'tickId': tickId,
      'circleCrossId': circleCrossId,
      'circleTriangleCrossId': circleTriangleCrossId,
      'tickCrossId': tickCrossId,
      'flagId': flagId,
      'personId': personId,
      'peopleId': peopleId,
      'starId': starId,
      'priorityId': priorityId,
      'weatherId': weatherId,
      'completeId': completeId,
      'goodBadId': goodBadId,
      'handId': handId,
      'trunpId': trunpId,
      'batteryId': batteryId,
      'faceId': faceId,
      'customTextId': customTextId,
      'customIconId': customIconId,
      'fonttype': fonttype,
      'verticalAlign': verticalAlign,
      'horizontalAlign': horizontalAlign,
      'created': created.toIso8601String(),
      'modified': modified.toIso8601String(),
    };
  }
```

### `data/entity/col_row_entity_ex.dart`

```dart
  static ColRowEntity fromJson(Map<String, dynamic> json, String fileId) {
    return ColRowEntity(Uuid.v4().toString(), fileId, DateTime.now(), DateTime.now(),)
      ..isCol = json['isCol'] ?? 0
      ..size = json['size'] ?? 1
      ..title = json['title'] ?? ""
      ..note = json['note'] ?? ""
      ..link = json['link'] ?? ""
      ..colorHex = json['colorHex'] ?? ""
      ..imageBase64 = json['imageBase64'] ?? ""
    ;
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'fileId': fileId,
      'isCol': isCol,
      'size': size,
      'title': title,
      'note': note,
      'link': link,
      'colorHex': colorHex,
      'imageBase64': imageBase64,
      'created': created.toIso8601String(),
      'modified': modified.toIso8601String(),
    };
  }
```

### `data/entity/file_entity_ex.dart`

```dart
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'fixCol': fixCol,
      'fixRow': fixRow,
      'borderColorHex': borderColorHex,
      'checkTypeId': checkTypeId,
      'customLabelList': customLabelList.toList(),
      'customLabelColorHexList': customLabelColorHexList.toList(),
      'customIconIdList': customIconIdList.toList(),
      'customIconColorHexList': customIconColorHexList.toList(),
      'colLabelSize': colLabelSize,
      'rowLabelSize': rowLabelSize,
      'created': created.toIso8601String(),
      'modified': modified.toIso8601String(),
    };
  }

  static FileEntity fromJson(Map<String, dynamic> json, String fileId) {
    return FileEntity(fileId, json['name'] ?? '', DateTime.now(), DateTime.now(),)
      ..fixCol = json['fixCol'] ?? -1
      ..fixRow = json['fixRow'] ?? -1
      ..borderColorHex = json['borderColorHex'] ?? ""
      ..checkTypeId = json['checkTypeId'] ?? ""
      ..customLabelList.addAll((json['customLabelList'] as List?)?.whereType<String>() ?? <String>[])
      ..customLabelColorHexList.addAll((json['customLabelColorHexList'] as List?)?.whereType<String>() ?? <String>[])
      ..customIconIdList.addAll((json['customIconIdList'] as List?)?.whereType<String>() ?? <String>[])
      ..customIconColorHexList.addAll((json['customIconColorHexList'] as List?)?.whereType<String>() ?? <String>[])
      ..colLabelSize = json['colLabelSize'] ?? AppConfigurator.colDefaultSize
      ..rowLabelSize = json['rowLabelSize'] ?? AppConfigurator.rowDefaultSize
    ;
  }
```

### `define/check_type.dart` identifiers

```dart
enum CheckType {
  tick('tick'),
  circle_cross('circle_cross'),
  circle_triangle_cross('circle_triangle_cross'),
  tick_cross('tick_cross'),
  flag('flag'),
  person('person'),
  people('people'),
  star('star'),
  priority('priority'),
  weather('weather'),
  complete('complete'),
  good_bad('good_bad'),
  hand('hand'),
  trunp('trunp'),
  battery('battery'),
  face('face'),
  custom_text('custom_text'),
  custom_icon('custom_icon');
```
