# Content format

- App ID: `spreadsheetai`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Use root `fileEntity`, `colList`, `rowList`, and `cellList`. Provide at least one column and row. Cell `col` and `row` are zero-based indexes within those arrays. Do not send IDs, file IDs, storage timestamps, or images. Use `title` for cell text and `completeId` for progress.

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
    String colorHex = json['colorHex'] as String? ?? '';
    colorHex = RegExp(r'^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$').hasMatch(colorHex) ? colorHex : '';
    DateTime created = _parseDateTime(json['created']) ?? DateTime.now();
    DateTime modified = _parseDateTime(json['modified']) ?? created;
    return CellEntity(Uuid.v4().toString(), fileId, created, modified)
      ..col = json['col'] ?? -1
      ..row = json['row'] ?? -1
      ..title = json['title'] ?? ""
      ..note = json['note'] ?? ""
      ..link = json['link'] ?? ""
      ..colorHex = colorHex
      ..imageBase64 = json['imageBase64'] ?? ""
      ..completeId = json['completeId'] ?? ""
      ..icon = json['icon'] ?? ""
      ..fonttype = json['fonttype'] ?? ""
      ..verticalAlign = json['verticalAlign'] ?? ""
      ..horizontalAlign = json['horizontalAlign'] ?? "";
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id.toString(),
      'fileId': fileId.toString(),
      'col': col,
      'row': row,
      'title': title,
      'note': note,
      'link': link,
      'colorHex': colorHex,
      'imageBase64': imageBase64,
      'completeId': completeId,
      'icon': icon,
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
    ;
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id.toString(),
      'fileId': fileId.toString(),
      'isCol': isCol,
      'size': size,
      'created': created.toIso8601String(),
      'modified': modified.toIso8601String(),
    };
  }
```

### `data/entity/file_entity_ex.dart`

```dart
  Map<String, dynamic> toJson() {
    return {
      'id': id.toString(),
      'name': name,
      'fixCol': fixCol,
      'fixRow': fixRow,
      'borderColorHex': borderColorHex,
      'created': created.toIso8601String(),
      'modified': modified.toIso8601String(),
    };
  }

  static FileEntity fromJson(Map<String, dynamic> json, String fileId) {
    return FileEntity(fileId, json['name'] ?? '', DateTime.now(), DateTime.now(),)
      ..fixCol = json['fixCol'] ?? -1
      ..fixRow = json['fixRow'] ?? -1
      ..borderColorHex = json['borderColorHex'] ?? "";
  }
```

### `define/complete_type.dart` identifiers

```dart
enum CompleteType {
  initial("initial"),
  zero("zero"),
  half("half"),
  completed("completed");
```
