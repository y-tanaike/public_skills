# Content format

- App ID: `menu`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Follow each item field type for prices. Place category headers and products in display order in `menuItems`.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `currencyCode` | string |
| `layoutType` | string |
| `menuItems` | array |
| `note` | string |
| `paperSize` | string |
| `shopId` | string |
| `shopName` | string |
| `tagline` | string |
| `themeColor` | string |
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
      final List<MenuItem> menuItems = _menuItemsFromJson(decodedJson['menuItems'] as List<dynamic>? ?? []);
      final String shopId = (decodedJson['shopId'] ?? '').toString();

      return Content()
        ..version = (decodedJson["version"] ?? "1").toString()
        ..createType = (decodedJson["createType"] ?? "Flutter").toString()
        ..shopId = shopId.isNotEmpty ? shopId : Uuid.v4().toString()
        ..shopName = (decodedJson["shopName"] ?? "").toString()
        ..tagline = (decodedJson["tagline"] ?? "").toString()
        ..currencyCode = (decodedJson["currencyCode"] ?? "").toString()
        ..note = (decodedJson["note"] ?? "").toString()
        ..logoImageBase64 = (decodedJson["logoImageBase64"] ?? "").toString()
        ..themeColor = (decodedJson["themeColor"] ?? "").toString()
        ..menuItems = menuItems
        ..layoutType = MenuLayoutType.fromId((decodedJson["layoutType"] ?? MenuLayoutType.detail.id).toString()).id
        ..paperSize = MenuPaperSize.fromId((decodedJson["paperSize"] ?? MenuPaperSize.a4.id).toString()).id;
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  static List<MenuItem> _menuItemsFromJson(List<dynamic> menuItemsJson) {
    final List<MenuItem> menuItems = [];
    String lastCategory = "";
    for (final dynamic element in menuItemsJson) {
      final Map<String, dynamic> itemJson = element as Map<String, dynamic>;
      final MenuItem menuItem = MenuItem.fromJson(itemJson);
      if (menuItem.isHeader) {
        lastCategory = "";
        menuItems.add(menuItem);
        continue;
      }
      final String category = (itemJson['category'] ?? '').toString();
      if (category.isNotEmpty && category != lastCategory) {
        lastCategory = category;
        menuItems.add(
          MenuItem.initEmpty(id: "${menuItem.id}_category_header", type: MenuItemType.header)..name = category,
        );
      }
      menuItems.add(menuItem);
    }
    final Set<String> itemIds = {};
    for (final MenuItem item in menuItems) {
      if (item.id.isEmpty || !itemIds.add(item.id)) {
        item.id = MenuItem.initEmpty().id;
        itemIds.add(item.id);
      }
    }
    return menuItems;
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'shopId': shopId,
      'shopName': shopName,
      'tagline': tagline,
      'currencyCode': currencyCode,
      'note': note,
      'logoImageBase64': logoImageBase64,
      'themeColor': themeColor,
      'menuItems': menuItems.map((item) => item.toJson()).toList(),
      'layoutType': layoutType,
      'paperSize': paperSize,
    };
  }
```

### `define/menu_item_type.dart` identifiers

```dart
enum MenuItemType {
  item('item'),
  header('header');
```

### `define/menu_layout_type.dart` identifiers

```dart
enum MenuLayoutType {
  simple("simple"),
  detail("detail"),
  colorful("colorful"),
  cafe("cafe"),
  photo("photo"),
  handwritten("handwritten"),
  board("board"),
  bold("bold"),
  vertical("vertical"),
  chineseCard("chineseCard"),
  photoMain("photoMain"),
  magazine("magazine"),
  grid("grid"),
  split("split"),
  street("street"),
  luxury("luxury"),
  coupon("coupon"),
  cat("cat"),
  flower("flower"),
  neon("neon"),
  retro("retro"),
  washi("washi"),
  twoColumn("twoColumn"),
  threeColumn("threeColumn"),
  hero("hero"),
  bargain("bargain"),
  izakaya("izakaya"),
  oneItemPerPage("oneItemPerPage"),
  twoItemsPerPage("twoItemsPerPage"),
  threeItemsPerPage("threeItemsPerPage"),
  fourItemsPerPage("fourItemsPerPage");
```

### `define/menu_paper_size.dart` identifiers

```dart
enum MenuPaperSize {
  a4("a4", 210, 297);
```

### `data/entity/menu_item.dart`

```dart
  static MenuItem fromJson(Map<String, dynamic> json) {
    final Object? priceValue = json['price'];
    return MenuItem(
      id: (json['id'] ?? '').toString(),
      type: MenuItemType.fromId((json['type'] ?? MenuItemType.item.id).toString()).id,
      name: (json['name'] ?? '').toString(),
      description: (json['description'] ?? '').toString(),
      price: priceValue is num ? priceValue.toDouble() : double.tryParse((priceValue ?? "").toString()) ?? 0,
      imageBase64: (json['imageBase64'] ?? '').toString(),
      pageBreak: json['pageBreak'] is bool ? json['pageBreak'] as bool : false,
      featured: json['featured'] is bool ? json['featured'] as bool : false,
      badgeText: (json['badgeText'] ?? '').toString(),
      spiceLevel: json['spiceLevel'] is int ? json['spiceLevel'] as int : int.tryParse((json['spiceLevel'] ?? "").toString()) ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'type': type,
      'name': name,
      'description': description,
      'price': price,
      'imageBase64': imageBase64,
      'pageBreak': pageBreak,
      'featured': featured,
      'badgeText': badgeText,
      'spiceLevel': spiceLevel,
    };
  }
```

### `data/entity/shop_info.dart`

```dart
  static ShopInfo fromJson(Map<String, dynamic> json) {
    final String id = (json['id'] ?? '').toString();
    return ShopInfo(
      id: id.isNotEmpty ? id : Uuid.v4().toString(),
      name: (json['name'] ?? '').toString(),
      tagline: (json['tagline'] ?? '').toString(),
      currencyCode: (json['currencyCode'] ?? '').toString(),
      note: (json['note'] ?? '').toString(),
      logoImageBase64: (json['logoImageBase64'] ?? '').toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'tagline': tagline,
      'currencyCode': currencyCode,
      'note': note,
      'logoImageBase64': logoImageBase64,
    };
  }

  static List<ShopInfo> listFromJsonString(String jsonString) {
    if (jsonString.isEmpty) {
      return <ShopInfo>[];
    }

    try {
      final List<dynamic> jsonList = jsonDecode(jsonString) as List<dynamic>;
      final List<ShopInfo> shopInfoList = <ShopInfo>[];
      for (final dynamic item in jsonList) {
        if (item is! Map) {
          continue;
        }
        final Map<String, dynamic> json = item.map((key, value) => MapEntry(key.toString(), value));
        final ShopInfo shopInfo = ShopInfo.fromJson(json);
        if (shopInfo.isSavable) {
          shopInfoList.add(shopInfo);
        }
      }
      return shopInfoList;
    } catch (_) {
      return <ShopInfo>[];
    }
  }

  static String listToJsonString(List<ShopInfo> shopInfoList) {
    return jsonEncode(shopInfoList.map((ShopInfo item) => item.toJson()).toList());
  }
```
