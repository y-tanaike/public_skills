# Content format

- App ID: `stamp`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

`stampCount` must be between 1 and 30. Include the requested reward, expiration, and stamp-slot instructions in the corresponding text fields.

## Root keys

| Key | JSON type |
|---|---|
| `address` | string |
| `businessHours` | string |
| `cardType` | string |
| `createType` | string |
| `customCardTitle` | string |
| `email` | string |
| `expirationDate` | See conversion definitions below |
| `expirationText` | string |
| `expirationType` | string |
| `isDoubleSided` | boolean |
| `layoutType` | string |
| `note` | string |
| `orientation` | string |
| `phone` | string |
| `postalCode` | string |
| `qrUrl` | string |
| `regularHoliday` | string |
| `shopName` | string |
| `showCustomerName` | boolean |
| `showStampNumbers` | boolean |
| `snsLinks` | array |
| `stampCount` | integer |
| `stampNote` | string |
| `stampSlotNotes` | array |
| `version` | string |
| `website` | string |

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

      return Content()
        ..version = (decodedJson["version"] ?? "1").toString()
        ..createType = (decodedJson["createType"] ?? "Flutter").toString()
        ..cardType = StampCardType.fromId((decodedJson["cardType"] ?? "").toString()).id
        ..customCardTitle = (decodedJson["customCardTitle"] ?? "").toString()
        ..shopName = (decodedJson["shopName"] ?? "").toString()
        ..logoImageBase64 = (decodedJson["logoImageBase64"] ?? "").toString()
        ..postalCode = (decodedJson["postalCode"] ?? "").toString()
        ..address = (decodedJson["address"] ?? "").toString()
        ..phone = (decodedJson["phone"] ?? "").toString()
        ..email = (decodedJson["email"] ?? "").toString()
        ..website = (decodedJson["website"] ?? "").toString()
        ..businessHours = (decodedJson["businessHours"] ?? "").toString()
        ..regularHoliday = (decodedJson["regularHoliday"] ?? "").toString()
        ..note = (decodedJson["note"] ?? "").toString()
        ..qrUrl = (decodedJson["qrUrl"] ?? "").toString()
        ..snsLinks = _parseSnsLinks(decodedJson)
        ..stampCount = _parseStampCount(decodedJson["stampCount"])
        ..showStampNumbers = decodedJson["showStampNumbers"] != false
        ..stampSlotNotes = _parseStampSlotNotes(decodedJson)
        ..stampNote = (decodedJson["stampNote"] ?? "").toString()
        ..showCustomerName = decodedJson["showCustomerName"] == true
        ..expirationType = ExpirationType.fromId((decodedJson["expirationType"] ?? "").toString()).id
        ..expirationDate = DateTime.tryParse((decodedJson["expirationDate"] ?? "").toString())
        ..expirationText = (decodedJson["expirationText"] ?? "").toString()
        ..isDoubleSided = decodedJson["isDoubleSided"] != false
        ..layoutType = CardLayoutType.fromId((decodedJson["layoutType"] ?? CardLayoutType.simple.id).toString()).id
        ..orientation = CardOrientation.fromId((decodedJson["orientation"] ?? CardOrientation.landscape.id).toString()).id;
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  static int _parseStampCount(dynamic value) {
    int count = int.tryParse((value ?? "").toString()) ?? defaultStampCount;
    return count.clamp(minStampCount, maxStampCount);
  }

  static List<SnsLink> _parseSnsLinks(Map<String, dynamic> decodedJson) {
    final dynamic rawList = decodedJson["snsLinks"];
    if (rawList is! List) {
      return [];
    }
    return rawList
        .whereType<Map<String, dynamic>>()
        .map(SnsLink.fromJson)
        .take(SnsLink.maxCount)
        .toList();
  }

  static List<StampSlotNote> _parseStampSlotNotes(Map<String, dynamic> decodedJson) {
    final dynamic rawList = decodedJson["stampSlotNotes"];
    if (rawList is! List) {
      return [];
    }
    return rawList
        .whereType<Map<String, dynamic>>()
        .map(StampSlotNote.fromJson)
        .toList();
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'cardType': cardType,
      'customCardTitle': customCardTitle,
      'shopName': shopName,
      'logoImageBase64': logoImageBase64,
      'postalCode': postalCode,
      'address': address,
      'phone': phone,
      'email': email,
      'website': website,
      'businessHours': businessHours,
      'regularHoliday': regularHoliday,
      'note': note,
      'qrUrl': qrUrl,
      'snsLinks': snsLinks.map((e) => e.toJson()).toList(),
      'stampCount': stampCount,
      'showStampNumbers': showStampNumbers,
      'stampSlotNotes': stampSlotNotes.map((e) => e.toJson()).toList(),
      'stampNote': stampNote,
      'showCustomerName': showCustomerName,
      'expirationType': expirationType,
      'expirationDate': expirationDate == null ? "" : _formatIsoDate(expirationDate!),
      'expirationText': expirationText,
      'isDoubleSided': isDoubleSided,
      'layoutType': layoutType,
      'orientation': orientation,
    };
  }
```

### `define/card_layout_type.dart` identifiers

```dart
enum StampSlotShape {
  circle,
  roundedSquare,
  square,
}

enum CardLayoutType {
  simple("simple", Color(0xffffffff), Color(0xff1f2933), Color(0xff6b7280), Color(0xff374151), StampSlotShape.circle),
  cafe("cafe", Color(0xfff7f1e8), Color(0xff3f2d20), Color(0xff8a6f58), Color(0xff6b4f3a), StampSlotShape.circle),
  natural("natural", Color(0xfff4f8ef), Color(0xff26351c), Color(0xff667a57), Color(0xff4d7c0f), StampSlotShape.circle),
  pop("pop", Color(0xffffffff), Color(0xff1f2937), Color(0xff6b7280), Color(0xffec4899), StampSlotShape.roundedSquare),
  pastel("pastel", Color(0xfffdf2f8), Color(0xff4a3b52), Color(0xff8b7a93), Color(0xfff472b6), StampSlotShape.circle),
  elegant("elegant", Color(0xfffbf8f1), Color(0xff2b2620), Color(0xff8a7d6b), Color(0xffb08d57), StampSlotShape.circle),
  japanese("japanese", Color(0xfffffdf7), Color(0xff1c1917), Color(0xff78716c), Color(0xffc0392b), StampSlotShape.square),
  night("night", Color(0xff111827), Color(0xfff9fafb), Color(0xffcbd5e1), Color(0xfffbbf24), StampSlotShape.circle),
  kraft("kraft", Color(0xffe8d5b5), Color(0xff3b2f24), Color(0xff6b5846), Color(0xff5b4636), StampSlotShape.circle),
  beauty("beauty", Color(0xfffff7f5), Color(0xff4a3035), Color(0xff9c7f84), Color(0xffb76e79), StampSlotShape.circle),
  fresh("fresh", Color(0xfff0f9ff), Color(0xff0c2a3f), Color(0xff4b6477), Color(0xff0ea5e9), StampSlotShape.roundedSquare),
  bold("bold", Color(0xffffffff), Color(0xff111111), Color(0xff555555), Color(0xff111111), StampSlotShape.square);
```

### `define/card_orientation.dart` identifiers

```dart
enum CardOrientation {
  landscape("yoko", 91, 55),
  portrait("tate", 55, 91);
```

### `define/expiration_type.dart` identifiers

```dart
enum ExpirationType {
  none("none"),
  date("date"),
  blank("blank"),
  text("text");
```

### `define/stamp_card_type.dart` identifiers

```dart
enum StampCardType {
  stamp("stamp"),
  point("point"),
  member("member"),
  service("service"),
  rally("rally"),
  custom("custom");
```

### `data/entity/sns_link.dart`

```dart
  static SnsLink fromJson(Map<String, dynamic> json) {
    return SnsLink(
      SnsType.fromId((json["type"] ?? "").toString()).id,
      (json["url"] ?? "").toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'type': type,
      'url': url,
    };
  }
```

### `data/entity/stamp_slot_note.dart`

```dart
  static StampSlotNote fromJson(Map<String, dynamic> json) {
    return StampSlotNote(
      int.tryParse((json["position"] ?? "").toString()) ?? 1,
      (json["text"] ?? "").toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'position': position,
      'text': text,
    };
  }
```

### `define/sns_type.dart` identifiers

```dart
enum SnsType {
  x("x", "X"),
  instagram("instagram", "Instagram"),
  facebook("facebook", "Facebook"),
  linkedin("linkedin", "LinkedIn"),
  youtube("youtube", "YouTube"),
  tiktok("tiktok", "TikTok"),
  threads("threads", "Threads"),
  line("line", "LINE"),
  github("github", "GitHub"),
  note("note", "note");
```
