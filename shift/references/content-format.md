# Content format

- App ID: `shift`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `customColorHexList` | array |
| `customLabelList` | array |
| `dateItemList` | array |
| `endDateTime` | string |
| `personList` | array |
| `shiftItemList` | array |
| `startDateTime` | string |
| `typeId` | string |
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
      final personList = (decodedJson['personList'] as List<dynamic>? ?? [])
          .map((e) => Person.fromJson(e as Map<String, dynamic>))
          .toList();
      final dateItemList = (decodedJson['dateItemList'] as List<dynamic>? ?? [])
          .map((e) => DateItem.fromJson(e as Map<String, dynamic>))
          .toList();
      final shiftItemList = (decodedJson['shiftItemList'] as List<dynamic>? ?? [])
          .map((e) => ShiftItem.fromJson(e as Map<String, dynamic>))
          .toList();

      return Content()
        ..version = decodedJson["version"] as String? ?? "1"
        ..createType = decodedJson["createType"] as String? ?? "Flutter"
        ..startDateTime = decodedJson["startDateTime"] != null ? DateTime.parse(decodedJson["startDateTime"]) : DateTime(DateTime.now().year, DateTime.now().month, DateTime.now().day)
        ..endDateTime = decodedJson["endDateTime"] != null ? DateTime.parse(decodedJson["endDateTime"]) : DateTime(DateTime.now().year, DateTime.now().month, DateTime.now().day).add(const Duration(days: 6))
        ..typeId = decodedJson["typeId"] as String? ?? "workOnlyShift"
        ..customLabelList = (decodedJson['customLabelList'] as List<dynamic>? ?? ShiftType.defaultCustomLabelList).map((e) => e.toString()).toList()
        ..customColorHexList = (decodedJson['customColorHexList'] as List<dynamic>? ?? ShiftType.defaultCustomColorHexList).map((e) => e.toString()).toList()
        ..personList = personList
        ..dateItemList = dateItemList
        ..shiftItemList = shiftItemList
      ;

    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'startDateTime': startDateTime.toIso8601String(),
      'endDateTime': endDateTime.toIso8601String(),
      'typeId': typeId,
      'customLabelList': customLabelList,
      'customColorHexList': customColorHexList,
      'personList': personList.map((person) => person.toJson()).toList(),
      'dateItemList': dateItemList.map((dateItem) => dateItem.toJson()).toList(),
      'shiftItemList': shiftItemList.map((shiftItem) => shiftItem.toJson()).toList(),
    };
  }
```

### `define/shift_type.dart` identifiers

```dart
enum ShiftType {
  workOnlyShift('workOnlyShift'),
  workRestShift('workRestShift'),
  attendanceOnlyShift('attendanceOnlyShift'),
  attendanceAbsenceShift('attendanceAbsenceShift'),
  dayNightShift('dayNightShift'),
  dayNightRestShift('dayNightRestShift'),
  dayEveningDeepNightShift('dayEveningDeepNightShift'),
  dayEveningDeepNightRestShift('dayEveningDeepNightRestShift'),
  earlyLateShift('earlyLateShift'),
  earlyLateRestShift('earlyLateRestShift'),
  earlyMiddleLateShift('earlyMiddleLateShift'),
  earlyMiddleLateRestShift('earlyMiddleLateRestShift'),
  earlyDayLateShift('earlyDayLateShift'),
  earlyDayLateRestShift('earlyDayLateRestShift'),
  dayNightAfterShift('dayNightAfterShift'),
  dayNightAfterRestShift('dayNightAfterRestShift'),
  morningAfternoonShift('morningAfternoonShift'),
  morningAfternoonRestShift('morningAfternoonRestShift'),
  morningAfternoonFullDayShift('morningAfternoonFullDayShift'),
  morningAfternoonFullDayRestShift('morningAfternoonFullDayRestShift'),
  hallKitchenShift('hallKitchenShift'),
  hallKitchenRestShift('hallKitchenRestShift'),
  hallKitchenDishwashingShift('hallKitchenDishwashingShift'),
  hallKitchenDishwashingRestShift('hallKitchenDishwashingRestShift'),
  cashierStockingShift('cashierStockingShift'),
  cashierStockingRestShift('cashierStockingRestShift'),
  custom('custom');
```

### `data/entity/date_item.dart`

```dart
  static DateItem fromJson(Map<String, dynamic> json) {
    return DateItem(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      currentDateTime: json['currentDateTime'] != null ? DateTime.parse(json['currentDateTime']) : DateTime.now(),
      label: json['label'] as String? ?? '',
      note: json['note'] as String? ?? '',
      link: json['link'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'currentDateTime': currentDateTime.toIso8601String(),
      'label': label,
      'note': note,
      'link': link,
      'colorHex': colorHex,
    };
  }
```

### `data/entity/person.dart`

```dart
  static Person fromJson(Map<String, dynamic> json) {
    return Person(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      name: json['name'] as String? ?? '',
      note: json['note'] as String? ?? '',
      priority: PriorityType.fromId(json['priority'] ?? ''),
      link: json['link'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'note': note,
      'priority': priority.id,
      'link': link,
      'colorHex': colorHex,
    };
  }
```

### `data/entity/shift_item.dart`

```dart
  static ShiftItem fromJson(Map<String, dynamic> json) {
    return ShiftItem(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      personId: json['personId'] as String? ?? '',
      currentDateTime: json['currentDateTime'] != null ? DateTime.parse(json['currentDateTime']) : DateTime.now(),
      note: json['note'] as String? ?? '',
      link: json['link'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      workOnlyShiftTypeId: json['workOnlyShiftTypeId'] as String? ?? '',
      workRestShiftTypeId: json['workRestShiftTypeId'] as String? ?? '',
      attendanceOnlyShiftTypeId: json['attendanceOnlyShiftTypeId'] as String? ?? '',
      attendanceAbsenceShiftTypeId: json['attendanceAbsenceShiftTypeId'] as String? ?? '',
      dayNightShiftTypeId: json['dayNightShiftTypeId'] as String? ?? '',
      dayNightRestShiftTypeId: json['dayNightRestShiftTypeId'] as String? ?? '',
      dayEveningDeepNightShiftTypeId: json['dayEveningDeepNightShiftTypeId'] as String? ?? '',
      dayEveningDeepNightRestShiftTypeId: json['dayEveningDeepNightRestShiftTypeId'] as String? ?? '',
      earlyLateShiftTypeId: json['earlyLateShiftTypeId'] as String? ?? '',
      earlyLateRestShiftTypeId: json['earlyLateRestShiftTypeId'] as String? ?? '',
      earlyMiddleLateShiftTypeId: json['earlyMiddleLateShiftTypeId'] as String? ?? '',
      earlyMiddleLateRestShiftTypeId: json['earlyMiddleLateRestShiftTypeId'] as String? ?? '',
      earlyDayLateShiftTypeId: json['earlyDayLateShiftTypeId'] as String? ?? '',
      earlyDayLateRestShiftTypeId: json['earlyDayLateRestShiftTypeId'] as String? ?? '',
      dayNightAfterShiftTypeId: json['dayNightAfterShiftTypeId'] as String? ?? '',
      dayNightAfterRestShiftTypeId: json['dayNightAfterRestShiftTypeId'] as String? ?? '',
      morningAfternoonShiftTypeId: json['morningAfternoonShiftTypeId'] as String? ?? '',
      morningAfternoonRestShiftTypeId: json['morningAfternoonRestShiftTypeId'] as String? ?? '',
      morningAfternoonFullDayShiftTypeId: json['morningAfternoonFullDayShiftTypeId'] as String? ?? '',
      morningAfternoonFullDayRestShiftTypeId: json['morningAfternoonFullDayRestShiftTypeId'] as String? ?? '',
      hallKitchenShiftTypeId: json['hallKitchenShiftTypeId'] as String? ?? '',
      hallKitchenRestShiftTypeId: json['hallKitchenRestShiftTypeId'] as String? ?? '',
      hallKitchenDishwashingShiftTypeId: json['hallKitchenDishwashingShiftTypeId'] as String? ?? '',
      hallKitchenDishwashingRestShiftTypeId: json['hallKitchenDishwashingRestShiftTypeId'] as String? ?? '',
      cashierStockingShiftTypeId: json['cashierStockingShiftTypeId'] as String? ?? '',
      cashierStockingRestShiftTypeId: json['cashierStockingRestShiftTypeId'] as String? ?? '',
      customShiftTypeId: json['customShiftTypeId'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'personId': personId,
      'currentDateTime': currentDateTime.toIso8601String(),
      'note': note,
      'link': link,
      'colorHex': colorHex,
      'workOnlyShiftTypeId': workOnlyShiftTypeId,
      'workRestShiftTypeId': workRestShiftTypeId,
      'attendanceOnlyShiftTypeId': attendanceOnlyShiftTypeId,
      'attendanceAbsenceShiftTypeId': attendanceAbsenceShiftTypeId,
      'dayNightShiftTypeId': dayNightShiftTypeId,
      'dayNightRestShiftTypeId': dayNightRestShiftTypeId,
      'dayEveningDeepNightShiftTypeId': dayEveningDeepNightShiftTypeId,
      'dayEveningDeepNightRestShiftTypeId': dayEveningDeepNightRestShiftTypeId,
      'earlyLateShiftTypeId': earlyLateShiftTypeId,
      'earlyLateRestShiftTypeId': earlyLateRestShiftTypeId,
      'earlyMiddleLateShiftTypeId': earlyMiddleLateShiftTypeId,
      'earlyMiddleLateRestShiftTypeId': earlyMiddleLateRestShiftTypeId,
      'earlyDayLateShiftTypeId': earlyDayLateShiftTypeId,
      'earlyDayLateRestShiftTypeId': earlyDayLateRestShiftTypeId,
      'dayNightAfterShiftTypeId': dayNightAfterShiftTypeId,
      'dayNightAfterRestShiftTypeId': dayNightAfterRestShiftTypeId,
      'morningAfternoonShiftTypeId': morningAfternoonShiftTypeId,
      'morningAfternoonRestShiftTypeId': morningAfternoonRestShiftTypeId,
      'morningAfternoonFullDayShiftTypeId': morningAfternoonFullDayShiftTypeId,
      'morningAfternoonFullDayRestShiftTypeId': morningAfternoonFullDayRestShiftTypeId,
      'hallKitchenShiftTypeId': hallKitchenShiftTypeId,
      'hallKitchenRestShiftTypeId': hallKitchenRestShiftTypeId,
      'hallKitchenDishwashingShiftTypeId': hallKitchenDishwashingShiftTypeId,
      'hallKitchenDishwashingRestShiftTypeId': hallKitchenDishwashingRestShiftTypeId,
      'cashierStockingShiftTypeId': cashierStockingShiftTypeId,
      'cashierStockingRestShiftTypeId': cashierStockingRestShiftTypeId,
      'customShiftTypeId': customShiftTypeId,
    };
  }
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
