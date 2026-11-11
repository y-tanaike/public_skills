# Content format

- App ID: `pos`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `registerItemList` | array |
| `saleTransactionList` | array |
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
      final registerItemList = (decodedJson['registerItemList'] as List<dynamic>? ?? [])
          .map((e) => RegisterItem.fromJson(e as Map<String, dynamic>))
          .toList();
      final saleTransactionList = (decodedJson['saleTransactionList'] as List<dynamic>? ?? [])
          .map((e) => SaleTransaction.fromJson(e as Map<String, dynamic>))
          .toList();

      return Content()
        ..version = decodedJson["version"] as String? ?? "1"
        ..createType = decodedJson["createType"] as String? ?? "Flutter"
        ..registerItemList = registerItemList
        ..saleTransactionList = saleTransactionList
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
      'registerItemList': registerItemList.map((registerItem) => registerItem.toJson()).toList(),
      'saleTransactionList': saleTransactionList.map((saleTransaction) => saleTransaction.toJson()).toList(),
    };
  }
```

### `define/register_item_status.dart` identifiers

```dart
enum RegisterItemStatus {
  active("active"),
  inactive("inactive"),
  deleted("deleted"),
  ;
```

### `define/sale_transaction_status.dart` identifiers

```dart
enum SaleTransactionStatus {
  completed("completed"),
  cancelled("cancelled"),
  ;
```

### `data/entity/register_item.dart`

```dart
  static RegisterItem fromJson(Map<String, dynamic> json) {
    return RegisterItem(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      itemType: ItemType.fromId(json['itemType'] as String? ?? ''),
      title: json['title'] as String? ?? '',
      unitPrice: (json['unitPrice'] as num?)?.toDouble() ?? 0,
      unit: json['unit'] as String? ?? '',
      label: json['label'] as String? ?? '',
      imageBase64: json['imageBase64'] as String? ?? '',
      note: json['note'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      status: RegisterItemStatus.fromId(json['status'] as String? ?? ''),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'itemType': itemType.id,
      'title': title,
      'unitPrice': unitPrice,
      'unit': unit,
      'label': label,
      'imageBase64': imageBase64,
      'note': note,
      'colorHex': colorHex,
      'status': status.id,
    };
  }
```

### `data/entity/sale_line.dart`

```dart
  static SaleLine fromJson(Map<String, dynamic> json) {
    return SaleLine(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      registerItemId: json['registerItemId'] as String? ?? '',
      quantity: (json['quantity'] as num?)?.toDouble() ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'registerItemId': registerItemId,
      'quantity': quantity,
    };
  }
```

### `data/entity/sale_transaction.dart`

```dart
  static SaleTransaction fromJson(Map<String, dynamic> json) {
    final String soldAtString = json['soldAt'] as String? ?? '';
    return SaleTransaction(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      soldAt: DateTime.tryParse(soldAtString) ?? DateTime.now(),
      saleLineList: (json['saleLineList'] as List<dynamic>? ?? [])
          .map((e) => SaleLine.fromJson(e as Map<String, dynamic>))
          .toList(),
      label: json['label'] as String? ?? '',
      note: json['note'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      status: SaleTransactionStatus.fromId(json['status'] as String? ?? ''),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'soldAt': soldAt.toIso8601String(),
      'saleLineList': saleLineList.map((saleLine) => saleLine.toJson()).toList(),
      'label': label,
      'note': note,
      'colorHex': colorHex,
      'status': status.id,
    };
  }
```

### `define/item_type.dart` identifiers

```dart
enum ItemType {
  item('item'),
  header('header');
```
