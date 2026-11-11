# Content format

- App ID: `quote`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `currencyCode` | string |
| `discountAmount` | number |
| `discountLabel` | string |
| `documentNumber` | string |
| `documentTitle` | string |
| `expirationDate` | string |
| `issueDate` | string |
| `layoutType` | string |
| `lineItems` | array |
| `note` | string |
| `recipient` | object |
| `sender` | object |
| `taxRate` | number |
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
      final List<LineItem> lineItems = (decodedJson['lineItems'] as List<dynamic>? ?? [])
          .map((e) => LineItem.fromJson(e as Map<String, dynamic>))
          .toList();
      final Object? taxRateValue = decodedJson["taxRate"];
      final Object? discountAmountValue = decodedJson["discountAmount"];
      final double taxRate = taxRateValue is num ? taxRateValue.toDouble() : double.tryParse((taxRateValue ?? "").toString()) ?? defaultTaxRate;
      final double discountAmount = discountAmountValue is num ? discountAmountValue.toDouble() : double.tryParse((discountAmountValue ?? "").toString()) ?? 0;

      return Content()
        ..version = (decodedJson["version"] ?? "1").toString()
        ..createType = (decodedJson["createType"] ?? "Flutter").toString()
        ..documentTitle = (decodedJson["documentTitle"] ?? "").toString()
        ..documentNumber = (decodedJson["documentNumber"] ?? "").toString()
        ..issueDate = (decodedJson["issueDate"] ?? "").toString()
        ..expirationDate = (decodedJson["expirationDate"] ?? "").toString()
        ..currencyCode = (decodedJson["currencyCode"] ?? "USD").toString()
        ..layoutType = (decodedJson["layoutType"] ?? QuoteLayoutType.normal.id).toString()
        ..sender = Sender.fromContentJson(decodedJson)
        ..recipient = Recipient.fromContentJson(decodedJson)
        ..lineItems = lineItems
        ..taxRate = taxRate
        ..discountLabel = (decodedJson["discountLabel"] ?? "").toString()
        ..discountAmount = discountAmount
        ..note = (decodedJson["note"] ?? "").toString();
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'documentTitle': documentTitle,
      'documentNumber': documentNumber,
      'issueDate': issueDate,
      'expirationDate': expirationDate,
      'currencyCode': currencyCode,
      'layoutType': layoutType,
      'sender': sender.toJson(),
      'recipient': recipient.toJson(),
      'lineItems': lineItems.map((item) => item.toJson()).toList(),
      'taxRate': taxRate,
      'discountLabel': discountLabel,
      'discountAmount': discountAmount,
      'note': note,
    };
  }
```

### `define/quote_layout_type.dart` identifiers

```dart
enum QuoteLayoutType {
  simple("simple"),
  normal("normal"),
  colorful("colorful"),
  cat("cat"),
  flower("flower");
```

### `data/entity/line_item.dart`

```dart
  static LineItem fromJson(Map<String, dynamic> json) {
    final Object? quantityValue = json['quantity'];
    final Object? unitPriceValue = json['unitPrice'];
    return LineItem(
      id: (json['id'] ?? '').toString(),
      description: (json['description'] ?? '').toString(),
      details: (json['details'] ?? '').toString(),
      quantity: quantityValue is num ? quantityValue.toDouble() : double.tryParse((quantityValue ?? "").toString()) ?? 1,
      unitLabel: (json['unitLabel'] ?? '').toString(),
      unitPrice: unitPriceValue is num ? unitPriceValue.toDouble() : double.tryParse((unitPriceValue ?? "").toString()) ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'description': description,
      'details': details,
      'quantity': quantity,
      'unitLabel': unitLabel,
      'unitPrice': unitPrice,
    };
  }
```

### `data/entity/recipient.dart`

```dart
  static Recipient fromJson(Map<String, dynamic> json) {
    final String honorificTypeId = (json["honorificType"] ?? "").toString();
    return Recipient(
      id: (json["id"] ?? "").toString().isNotEmpty ? (json["id"] ?? "").toString() : Uuid.v4().toString(),
      name: (json["name"] ?? "").toString(),
      address: (json["address"] ?? "").toString(),
      email: (json["email"] ?? "").toString(),
      phone: (json["phone"] ?? "").toString(),
      taxId: (json["taxId"] ?? "").toString(),
      honorificType: HonorificType.fromId(honorificTypeId),
    );
  }

  static Recipient fromContentJson(Map<String, dynamic> decodedJson) {
    Map<String, dynamic> recipientJson = <String, dynamic>{};
    if (decodedJson["recipient"] is Map) {
      recipientJson = (decodedJson["recipient"] as Map<dynamic, dynamic>).map((key, value) => MapEntry(key.toString(), value));
    }

    final String recipientId = (recipientJson["id"] ?? "").toString();
    final String recipientName = (recipientJson["name"] ?? "").toString();
    final String recipientAddress = (recipientJson["address"] ?? "").toString();
    final String recipientEmail = (recipientJson["email"] ?? "").toString();
    final String recipientPhone = (recipientJson["phone"] ?? "").toString();
    final String recipientTaxId = (recipientJson["taxId"] ?? "").toString();
    final String recipientHonorificTypeId = (recipientJson["honorificType"] ?? "").toString();
    final HonorificType recipientHonorificType = HonorificType.fromId(recipientHonorificTypeId);

    return Recipient(
      id: recipientId.isNotEmpty ? recipientId : Uuid.v4().toString(),
      name: recipientName,
      address: recipientAddress,
      email: recipientEmail,
      phone: recipientPhone,
      taxId: recipientTaxId,
      honorificType: recipientHonorificType,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "name": name,
      "address": address,
      "email": email,
      "phone": phone,
      "taxId": taxId,
      "honorificType": honorificType.id,
    };
  }

  static List<Recipient> listFromJsonString(String jsonString) {
    if (jsonString.isEmpty) {
      return <Recipient>[];
    }

    try {
      List<dynamic> jsonList = jsonDecode(jsonString) as List<dynamic>;
      List<Recipient> recipientList = <Recipient>[];
      for (dynamic item in jsonList) {
        if (item is! Map) {
          continue;
        }
        Map<String, dynamic> json = item.map((key, value) => MapEntry(key.toString(), value));
        Recipient recipient = Recipient.fromJson(json);
        if (recipient.isSavable) {
          recipientList.add(recipient);
        }
      }
      return recipientList;
    } catch (_) {
      return <Recipient>[];
    }
  }

  static String listToJsonString(List<Recipient> recipientList) {
    return jsonEncode(recipientList.map((item) => item.toJson()).toList());
  }
```

### `data/entity/sender.dart`

```dart
  static Sender fromJson(Map<String, dynamic> json) {
    return Sender(
      id: (json["id"] ?? "").toString().isNotEmpty ? (json["id"] ?? "").toString() : Uuid.v4().toString(),
      name: (json["name"] ?? "").toString(),
      address: (json["address"] ?? "").toString(),
      email: (json["email"] ?? "").toString(),
      phone: (json["phone"] ?? "").toString(),
      taxId: (json["taxId"] ?? "").toString(),
      bank: (json["bank"] ?? "").toString(),
      imageBase64: (json["imageBase64"] ?? "").toString(),
    );
  }

  static Sender fromContentJson(Map<String, dynamic> decodedJson) {
    Map<String, dynamic> senderJson = <String, dynamic>{};
    if (decodedJson["sender"] is Map) {
      senderJson = (decodedJson["sender"] as Map<dynamic, dynamic>).map((key, value) => MapEntry(key.toString(), value));
    }

    final String senderId = (senderJson["id"] ?? "").toString();
    final String senderName = (senderJson["name"] ?? "").toString();
    final String senderAddress = (senderJson["address"] ?? "").toString();
    final String senderEmail = (senderJson["email"] ?? "").toString();
    final String senderPhone = (senderJson["phone"] ?? "").toString();
    final String senderTaxId = (senderJson["taxId"] ?? "").toString();
    final String senderBank = (senderJson["bank"] ?? "").toString();
    final String senderImageBase64 = (senderJson["imageBase64"] ?? "").toString();

    return Sender(
      id: senderId.isNotEmpty ? senderId : Uuid.v4().toString(),
      name: senderName,
      address: senderAddress,
      email: senderEmail,
      phone: senderPhone,
      taxId: senderTaxId,
      bank: senderBank,
      imageBase64: senderImageBase64,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "name": name,
      "address": address,
      "email": email,
      "phone": phone,
      "taxId": taxId,
      "bank": bank,
      "imageBase64": imageBase64,
    };
  }

  static Sender fromJsonString(String jsonString) {
    if (jsonString.isEmpty) {
      return Sender.initEmpty();
    }

    try {
      Map<dynamic, dynamic> dynamicMap = jsonDecode(jsonString) as Map<dynamic, dynamic>;
      Map<String, dynamic> json = dynamicMap.map((key, value) => MapEntry(key.toString(), value));
      return Sender.fromJson(json);
    } catch (_) {
      return Sender.initEmpty();
    }
  }

  static String toJsonString(Sender sender) {
    return jsonEncode(sender.toJson());
  }
```

### `define/honorific_type.dart` identifiers

```dart
enum HonorificType {
  none("none"),
  sama("sama"),
  onchu("onchu"),
  ;
```
