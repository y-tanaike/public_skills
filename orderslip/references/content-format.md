# Content format

- App ID: `orderslip`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `orderItemList` | array |
| `orderSlipList` | array |
| `orderTableList` | array |
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
      final orderItemList = (decodedJson['orderItemList'] as List<dynamic>? ?? [])
          .map((e) => OrderItem.fromJson(e as Map<String, dynamic>))
          .toList();
      final orderTableList = (decodedJson['orderTableList'] as List<dynamic>? ?? [])
          .map((e) => OrderTable.fromJson(e as Map<String, dynamic>))
          .toList();
      final orderSlipList = (decodedJson['orderSlipList'] as List<dynamic>? ?? [])
          .map((e) => OrderSlip.fromJson(e as Map<String, dynamic>))
          .toList();

      return Content()
        ..version = decodedJson["version"] as String? ?? "1"
        ..createType = decodedJson["createType"] as String? ?? "Flutter"
        ..orderItemList = orderItemList
        ..orderTableList = orderTableList
        ..orderSlipList = orderSlipList
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
      'orderItemList': orderItemList.map((orderItem) => orderItem.toJson()).toList(),
      'orderTableList': orderTableList.map((orderTable) => orderTable.toJson()).toList(),
      'orderSlipList': orderSlipList.map((orderSlip) => orderSlip.toJson()).toList(),
    };
  }
```

### `define/order_item_status.dart` identifiers

```dart
enum OrderItemStatus {
  active("active"),
  inactive("inactive"),
  deleted("deleted"),
  ;
```

### `define/order_slip_status.dart` identifiers

```dart
enum OrderSlipStatus {
  active("active"),
  cancelled("cancelled"),
  ;
```

### `define/order_table_status.dart` identifiers

```dart
enum OrderTableStatus {
  active("active"),
  inactive("inactive"),
  deleted("deleted"),
  ;
```

### `data/entity/order_item.dart`

```dart
  static OrderItem fromJson(Map<String, dynamic> json) {
    return OrderItem(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      itemType: ItemType.fromId(json['itemType'] as String? ?? ''),
      title: json['title'] as String? ?? '',
      label: json['label'] as String? ?? '',
      imageBase64: json['imageBase64'] as String? ?? '',
      note: json['note'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      status: OrderItemStatus.fromId(json['status'] as String? ?? ''),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'itemType': itemType.id,
      'title': title,
      'label': label,
      'imageBase64': imageBase64,
      'note': note,
      'colorHex': colorHex,
      'status': status.id,
    };
  }
```

### `data/entity/order_line.dart`

```dart
  static OrderLine fromJson(Map<String, dynamic> json) {
    final String servedAtString = json['servedAt'] as String? ?? '';
    return OrderLine(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      orderItemId: json['orderItemId'] as String? ?? '',
      quantity: (json['quantity'] as num?)?.toInt() ?? 0,
      note: json['note'] as String? ?? '',
      servedAt: DateTime.tryParse(servedAtString),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'orderItemId': orderItemId,
      'quantity': quantity,
      'note': note,
      'servedAt': servedAt?.toIso8601String() ?? '',
    };
  }
```

### `data/entity/order_slip.dart`

```dart
  static OrderSlip fromJson(Map<String, dynamic> json) {
    final String orderedAtString = json['orderedAt'] as String? ?? '';
    return OrderSlip(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      slipNumber: (json['slipNumber'] as num?)?.toInt() ?? 0,
      tableId: json['tableId'] as String? ?? '',
      tableName: json['tableName'] as String? ?? '',
      orderedAt: DateTime.tryParse(orderedAtString) ?? DateTime.now(),
      orderLineList: (json['orderLineList'] as List<dynamic>? ?? [])
          .map((e) => OrderLine.fromJson(e as Map<String, dynamic>))
          .toList(),
      note: json['note'] as String? ?? '',
      status: OrderSlipStatus.fromId(json['status'] as String? ?? ''),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'slipNumber': slipNumber,
      'tableId': tableId,
      'tableName': tableName,
      'orderedAt': orderedAt.toIso8601String(),
      'orderLineList': orderLineList.map((orderLine) => orderLine.toJson()).toList(),
      'note': note,
      'status': status.id,
    };
  }
```

### `data/entity/order_table.dart`

```dart
  static OrderTable fromJson(Map<String, dynamic> json) {
    return OrderTable(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      name: json['name'] as String? ?? '',
      note: json['note'] as String? ?? '',
      status: OrderTableStatus.fromId(json['status'] as String? ?? ''),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'note': note,
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
