# Content format

- App ID: `stock`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `stockItemList` | array |
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
      final stockItemList = (decodedJson['stockItemList'] as List<dynamic>? ?? [])
          .map((e) => StockItem.fromJson(e as Map<String, dynamic>))
          .toList();

      return Content()
        ..version = decodedJson["version"] as String? ?? "1"
        ..createType = decodedJson["createType"] as String? ?? "Flutter"
        ..stockItemList = stockItemList
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
      'stockItemList': stockItemList.map((stockItem) => stockItem.toJson()).toList(),
    };
  }
```

### `data/entity/stock_item.dart`

```dart
  static StockItem fromJson(Map<String, dynamic> json) {
    return StockItem(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      title: json['title'] as String? ?? '',
      note: json['note'] as String? ?? '',
      priority: PriorityType.fromId(json['priority'] as String? ?? ''),
      link: json['link'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      type: ItemType.fromId(json['type'] as String? ?? ''),
      label: json['label'] as String? ?? '',
      quantity: (json['quantity'] as num?)?.toDouble() ?? 0,
      unit: json['unit'] as String? ?? '',
      minQuantity: (json['minQuantity'] as num?)?.toDouble() ?? 0,
      quantityType: QuantityType.fromId(json['quantityType'] as String? ?? ''),
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
      'type': type.id,
      'label': label,
      'quantity': quantity,
      'unit': unit,
      'minQuantity': minQuantity,
      'quantityType': quantityType.id,
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

### `define/quantity_type.dart` identifiers

```dart
enum QuantityType {
  integer('integer'),
  decimal('decimal');
```

### `define/item_type.dart` identifiers

```dart
enum ItemType {
  item('item'),
  header('header');
```
