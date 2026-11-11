# Content format

- App ID: `shopcard`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `access` | string |
| `address` | string |
| `backNote` | string |
| `businessHours` | string |
| `catchphrase` | string |
| `companyName` | string |
| `createType` | string |
| `department` | string |
| `email` | string |
| `fax` | string |
| `isDoubleSided` | boolean |
| `jobTitle` | string |
| `latitude` | number |
| `layoutType` | string |
| `longitude` | number |
| `mobile` | string |
| `name` | string |
| `nameReading` | string |
| `note` | string |
| `orientation` | string |
| `phone` | string |
| `postalCode` | string |
| `qrNote` | string |
| `qrUrl` | string |
| `regularHoliday` | string |
| `reservationUrl` | string |
| `snsLinks` | array |
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
        ..name = (decodedJson["name"] ?? "").toString()
        ..nameReading = (decodedJson["nameReading"] ?? "").toString()
        ..companyName = (decodedJson["companyName"] ?? "").toString()
        ..department = (decodedJson["department"] ?? "").toString()
        ..jobTitle = (decodedJson["jobTitle"] ?? "").toString()
        ..postalCode = (decodedJson["postalCode"] ?? "").toString()
        ..address = (decodedJson["address"] ?? "").toString()
        ..phone = (decodedJson["phone"] ?? "").toString()
        ..mobile = (decodedJson["mobile"] ?? "").toString()
        ..fax = (decodedJson["fax"] ?? "").toString()
        ..email = (decodedJson["email"] ?? "").toString()
        ..website = (decodedJson["website"] ?? "").toString()
        ..catchphrase = (decodedJson["catchphrase"] ?? "").toString()
        ..businessHours = (decodedJson["businessHours"] ?? "").toString()
        ..regularHoliday = (decodedJson["regularHoliday"] ?? "").toString()
        ..access = (decodedJson["access"] ?? "").toString()
        ..reservationUrl = (decodedJson["reservationUrl"] ?? "").toString()
        ..latitude = _parseDouble(decodedJson["latitude"])
        ..longitude = _parseDouble(decodedJson["longitude"])
        ..note = (decodedJson["note"] ?? "").toString()
        ..logoImageBase64 = (decodedJson["logoImageBase64"] ?? "").toString()
        ..isDoubleSided = decodedJson["isDoubleSided"] == true
        ..backImageBase64 = (decodedJson["backImageBase64"] ?? "").toString()
        ..qrUrl = (decodedJson["qrUrl"] ?? "").toString()
        ..qrNote = (decodedJson["qrNote"] ?? "").toString()
        ..snsLinks = _parseSnsLinks(decodedJson)
        ..backNote = (decodedJson["backNote"] ?? "").toString()
        ..layoutType = CardLayoutType.fromId((decodedJson["layoutType"] ?? CardLayoutType.detail.id).toString()).id
        ..orientation = CardOrientation.fromId((decodedJson["orientation"] ?? CardOrientation.landscape.id).toString()).id;
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  static double? _parseDouble(dynamic value) {
    if (value == null) return null;
    if (value is num) return value.toDouble();
    return double.tryParse(value.toString());
  }

  static List<SnsLink> _parseSnsLinks(Map<String, dynamic> decodedJson) {
    final dynamic rawList = decodedJson["snsLinks"];
    if (rawList is List) {
      return rawList
          .whereType<Map<String, dynamic>>()
          .map(SnsLink.fromJson)
          .take(SnsLink.maxCount)
          .toList();
    }

    final String legacySnsUrl = (decodedJson["snsUrl"] ?? "").toString();
    if (legacySnsUrl.isNotEmpty) {
      return [SnsLink(SnsType.fromUrl(legacySnsUrl).id, legacySnsUrl)];
    }
    return [];
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'name': name,
      'nameReading': nameReading,
      'companyName': companyName,
      'department': department,
      'jobTitle': jobTitle,
      'postalCode': postalCode,
      'address': address,
      'phone': phone,
      'mobile': mobile,
      'fax': fax,
      'email': email,
      'website': website,
      'catchphrase': catchphrase,
      'businessHours': businessHours,
      'regularHoliday': regularHoliday,
      'access': access,
      'reservationUrl': reservationUrl,
      'latitude': latitude,
      'longitude': longitude,
      'note': note,
      'logoImageBase64': logoImageBase64,
      'isDoubleSided': isDoubleSided,
      'backImageBase64': backImageBase64,
      'qrUrl': qrUrl,
      'qrNote': qrNote,
      'snsLinks': snsLinks.map((e) => e.toJson()).toList(),
      'backNote': backNote,
      'layoutType': layoutType,
      'orientation': orientation,
    };
  }
```

### `define/card_layout_type.dart` identifiers

```dart
enum CardLayoutType {
  simple("simple"),
  detail("detail"),
  colorful("colorful"),
  flower("flower"),
  cat("cat"),
  elegant("elegant"),
  minimal("minimal"),
  bold("bold"),
  stripe("stripe"),
  circle("circle"),
  diagonal("diagonal"),
  frame("frame"),
  wave("wave"),
  grid("grid"),
  monochrome("monochrome"),
  pastel("pastel"),
  botanical("botanical"),
  tech("tech"),
  craft("craft"),
  luxe("luxe"),
  pop("pop"),
  japanese("japanese"),
  line("line"),
  night("night");
```

### `define/card_orientation.dart` identifiers

```dart
enum CardOrientation {
  landscape("yoko", 91, 55),
  portrait("tate", 55, 91);
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
