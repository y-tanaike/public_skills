# Content format

- App ID: `expence`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `expenseItemList` | array |
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
      final expenseItemList = (decodedJson['expenseItemList'] as List<dynamic>? ?? [])
          .map((e) => ExpenseItem.fromJson(e as Map<String, dynamic>))
          .toList();

      return Content()
        ..version = decodedJson["version"] as String? ?? "1"
        ..createType = decodedJson["createType"] as String? ?? "Flutter"
        ..expenseItemList = expenseItemList
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
      'expenseItemList': expenseItemList.map((expenseItem) => expenseItem.toJson()).toList(),
    };
  }
```

### `data/entity/expense_item.dart`

```dart
  static ExpenseItem fromJson(Map<String, dynamic> json) {
    final String paymentDateTimeString = json['paymentDateTime'] as String? ?? '';
    return ExpenseItem(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      title: json['title'] as String? ?? '',
      itemType: ItemType.fromId(json['itemType'] as String? ?? ''),
      type: ExpenseType.fromId(json['type'] as String? ?? ''),
      price: (json['price'] as num?)?.toDouble() ?? 0,
      label: json['label'] as String? ?? '',
      note: json['note'] as String? ?? '',
      priority: PriorityType.fromId(json['priority'] as String? ?? ''),
      paymentDateTime: paymentDateTimeString.isEmpty ? null : DateTime.tryParse(paymentDateTimeString),
      isAllDay: json['isAllDay'] as bool? ?? true,
      colorHex: json['colorHex'] as String? ?? '',
      paymentMethod: json['paymentMethod'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'itemType': itemType.id,
      'type': type.id,
      'price': price,
      'label': label,
      'note': note,
      'priority': priority.id,
      'paymentDateTime': paymentDateTime?.toIso8601String() ?? '',
      'isAllDay': isAllDay,
      'colorHex': colorHex,
      'paymentMethod': paymentMethod,
    };
  }
```

### `define/expense_type.dart` identifiers

```dart
enum ExpenseType {
  plus('plus'),
  minus('minus');
```

### `define/item_type.dart` identifiers

```dart
enum ItemType {
  item('item'),
  header('header');
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
