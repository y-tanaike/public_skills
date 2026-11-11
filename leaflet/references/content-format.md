# Content format

- App ID: `leaflet`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `address` | string |
| `backgroundColor` | string |
| `badge` | string |
| `businessHours` | string |
| `createType` | string |
| `currencyCode` | string |
| `description` | string |
| `imageItems` | array |
| `items` | array |
| `layoutType` | string |
| `note` | string |
| `period` | string |
| `phone` | string |
| `priceText` | string |
| `shopName` | string |
| `showItems` | boolean |
| `subtitle` | string |
| `textItems` | array |
| `title` | string |
| `version` | string |
| `webUrl` | string |

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
      final List<LeafletItem> items = (decodedJson['items'] as List<dynamic>? ?? [])
          .map((e) => LeafletItem.fromJson(e as Map<String, dynamic>))
          .toList();
      final List<LeafletTextItem> textItems = (decodedJson['textItems'] as List<dynamic>? ?? [])
          .map((e) => LeafletTextItem.fromJson(e as Map<String, dynamic>))
          .toList();
      final List<LeafletImageItem> imageItems = (decodedJson['imageItems'] as List<dynamic>? ?? [])
          .map((e) => LeafletImageItem.fromJson(e as Map<String, dynamic>))
          .toList();
      final Object? showItemsValue = decodedJson["showItems"];
      final bool showItems = showItemsValue is bool ? showItemsValue : (showItemsValue ?? "true").toString() == "true";

      return Content()
        ..version = (decodedJson["version"] ?? "1").toString()
        ..createType = (decodedJson["createType"] ?? "Flutter").toString()
        ..title = (decodedJson["title"] ?? "").toString()
        ..subtitle = (decodedJson["subtitle"] ?? "").toString()
        ..period = (decodedJson["period"] ?? "").toString()
        ..description = (decodedJson["description"] ?? "").toString()
        ..mainImageBase64 = (decodedJson["mainImageBase64"] ?? "").toString()
        ..badge = (decodedJson["badge"] ?? "").toString()
        ..priceText = (decodedJson["priceText"] ?? "").toString()
        ..textItems = textItems
        ..imageItems = imageItems
        ..items = items
        ..showItems = showItems
        ..shopName = (decodedJson["shopName"] ?? "").toString()
        ..address = (decodedJson["address"] ?? "").toString()
        ..phone = (decodedJson["phone"] ?? "").toString()
        ..businessHours = (decodedJson["businessHours"] ?? "").toString()
        ..webUrl = (decodedJson["webUrl"] ?? "").toString()
        ..note = (decodedJson["note"] ?? "").toString()
        ..currencyCode = (decodedJson["currencyCode"] ?? "").toString()
        ..backgroundColor = (decodedJson["backgroundColor"] ?? "").toString()
        ..layoutType = LeafletLayoutType.fromId((decodedJson["layoutType"] ?? LeafletLayoutType.event.id).toString()).id;
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'title': title,
      'subtitle': subtitle,
      'period': period,
      'description': description,
      'mainImageBase64': mainImageBase64,
      'badge': badge,
      'priceText': priceText,
      'textItems': textItems.map((item) => item.toJson()).toList(),
      'imageItems': imageItems.map((item) => item.toJson()).toList(),
      'items': items.map((item) => item.toJson()).toList(),
      'showItems': showItems,
      'shopName': shopName,
      'address': address,
      'phone': phone,
      'businessHours': businessHours,
      'webUrl': webUrl,
      'note': note,
      'currencyCode': currencyCode,
      'backgroundColor': backgroundColor,
      'layoutType': layoutType,
    };
  }
```

### `define/leaflet_layout_type.dart` identifiers

```dart
enum LeafletTemplateCategory {
  event,
  seminar,
  pop,
  product;
```

### `data/entity/leaflet_image_item.dart`

```dart
  static LeafletImageItem fromJson(Map<String, dynamic> json) {
    return LeafletImageItem(
      id: (json['id'] ?? '').toString(),
      imageBase64: (json['imageBase64'] ?? '').toString(),
      caption: (json['caption'] ?? '').toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'imageBase64': imageBase64,
      'caption': caption,
    };
  }
```

### `data/entity/leaflet_item.dart`

```dart
  static LeafletItem fromJson(Map<String, dynamic> json) {
    final Object? priceValue = json['price'];
    final Object? originalPriceValue = json['originalPrice'];
    return LeafletItem(
      id: (json['id'] ?? '').toString(),
      name: (json['name'] ?? '').toString(),
      description: (json['description'] ?? '').toString(),
      price: priceValue is num ? priceValue.toDouble() : double.tryParse((priceValue ?? "").toString()) ?? 0,
      originalPrice: originalPriceValue is num ? originalPriceValue.toDouble() : double.tryParse((originalPriceValue ?? "").toString()) ?? 0,
      badge: (json['badge'] ?? '').toString(),
      imageBase64: (json['imageBase64'] ?? '').toString(),
      color: (json['color'] ?? '').toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'price': price,
      'originalPrice': originalPrice,
      'badge': badge,
      'imageBase64': imageBase64,
      'color': color,
    };
  }
```

### `data/entity/leaflet_text_item.dart`

```dart
  static LeafletTextItem fromJson(Map<String, dynamic> json) {
    return LeafletTextItem(
      id: (json['id'] ?? '').toString(),
      title: (json['title'] ?? '').toString(),
      body: (json['body'] ?? '').toString(),
      color: (json['color'] ?? '').toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'body': body,
      'color': color,
    };
  }
```
