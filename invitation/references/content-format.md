# Content format

- App ID: `invitation`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `address` | string |
| `backNote` | string |
| `ceremonyAddress` | string |
| `ceremonyTime` | string |
| `ceremonyVenueName` | string |
| `createType` | string |
| `dressCode` | string |
| `email` | string |
| `eventDate` | string |
| `eventTime` | string |
| `eventTitle` | string |
| `hostName` | string |
| `isDoubleSided` | boolean |
| `layoutType` | string |
| `message` | string |
| `orientation` | string |
| `partnerOneName` | string |
| `partnerTwoName` | string |
| `phone` | string |
| `postalCode` | string |
| `programs` | See conversion definitions below |
| `qrUrl` | string |
| `receptionAddress` | string |
| `receptionTime` | string |
| `receptionVenueName` | string |
| `recipientName` | string |
| `rsvpContact` | string |
| `rsvpDeadline` | string |
| `snsLinks` | array |
| `venueName` | string |
| `version` | string |
| `website` | string |

Types use JSON terminology. Check nullability, nested elements, and defaults against the conversion definitions below. Image fields are out of scope even where they appear in the app's serializer.

## Nested elements, identifiers, and date conversions

The excerpts below preserve serialization statements from the app implementation checked on 2026-11-11; source comments are omitted. You do not need to execute Dart. `fromJson` specifies accepted types and defaults; `toJson` specifies output keys. Follow the actual date conversion units rather than assuming ISO timestamps. The excerpts are reference fragments, not standalone Dart programs.

### `data/entity/content.dart`

```dart
  static Content? tryFromJson(String json) {
    try {
      final dynamic decodedJson = jsonDecode(json);
      if (decodedJson is! Map<String, dynamic> || decodedJson["eventTitle"] is! String) {
        return null;
      }
      _parsePrograms(decodedJson);
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
      final Map<String, dynamic> decodedJson = jsonDecode(json);

      return Content()
        ..version = (decodedJson["version"] ?? "1").toString()
        ..createType = (decodedJson["createType"] ?? "Flutter").toString()
        ..eventTitle = (decodedJson["eventTitle"] ?? "").toString()
        ..recipientName = (decodedJson["recipientName"] ?? "").toString()
        ..partnerOneName = (decodedJson["partnerOneName"] ?? "").toString()
        ..partnerTwoName = (decodedJson["partnerTwoName"] ?? "").toString()
        ..ceremonyTime = (decodedJson["ceremonyTime"] ?? "").toString()
        ..ceremonyVenueName = (decodedJson["ceremonyVenueName"] ?? "").toString()
        ..ceremonyAddress = (decodedJson["ceremonyAddress"] ?? "").toString()
        ..receptionTime = (decodedJson["receptionTime"] ?? "").toString()
        ..receptionVenueName = (decodedJson["receptionVenueName"] ?? "").toString()
        ..receptionAddress = (decodedJson["receptionAddress"] ?? "").toString()
        ..hostName = (decodedJson["hostName"] ?? "").toString()
        ..eventDate = (decodedJson["eventDate"] ?? "").toString()
        ..eventTime = (decodedJson["eventTime"] ?? "").toString()
        ..postalCode = (decodedJson["postalCode"] ?? "").toString()
        ..address = (decodedJson["address"] ?? "").toString()
        ..phone = (decodedJson["phone"] ?? "").toString()
        ..venueName = (decodedJson["venueName"] ?? "").toString()
        ..rsvpDeadline = (decodedJson["rsvpDeadline"] ?? "").toString()
        ..email = (decodedJson["email"] ?? "").toString()
        ..website = (decodedJson["website"] ?? "").toString()
        ..rsvpContact = (decodedJson["rsvpContact"] ?? "").toString()
        ..dressCode = (decodedJson["dressCode"] ?? "").toString()
        ..message = (decodedJson["message"] ?? "").toString()
        ..imageBase64 = (decodedJson["imageBase64"] ?? "").toString()
        ..isDoubleSided = decodedJson["isDoubleSided"] == true
        ..backImageBase64 = (decodedJson["backImageBase64"] ?? "").toString()
        ..qrUrl = (decodedJson["qrUrl"] ?? "").toString()
        .._programs = _parsePrograms(decodedJson)
        ..snsLinks = _parseSnsLinks(decodedJson)
        ..backNote = (decodedJson["backNote"] ?? "").toString()
        ..layoutType = CardLayoutType.fromId((decodedJson["layoutType"] ?? CardLayoutType.detail.id).toString()).id
        ..orientation = CardOrientation.fromId((decodedJson["orientation"] ?? CardOrientation.landscape.id).toString()).id;
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  static List<InvitationProgram>? _parsePrograms(Map<String, dynamic> decodedJson) {
    final dynamic rawList = decodedJson["programs"];
    if (rawList == null) return null;
    if (rawList is! List || rawList.any((dynamic item) => item is! Map<String, dynamic>)) {
      throw const FormatException("Invalid programs");
    }
    final List<InvitationProgram> programs = rawList.map((dynamic item) => InvitationProgram.fromJson(item as Map<String, dynamic>)).toList();
    final Set<String> ids = {};
    for (int index = 0; index < programs.length; index++) {
      if (!ids.add(programs[index].id)) {
        final InvitationProgram original = programs[index];
        programs[index] = InvitationProgram(name: original.name, eventTime: original.eventTime, venue: original.venue, message: original.message);
        ids.add(programs[index].id);
      }
    }
    return programs;
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
      'eventTitle': eventTitle,
      'recipientName': recipientName,
      'partnerOneName': partnerOneName,
      'partnerTwoName': partnerTwoName,
      'ceremonyTime': ceremonyTime,
      'ceremonyVenueName': ceremonyVenueName,
      'ceremonyAddress': ceremonyAddress,
      'receptionTime': receptionTime,
      'receptionVenueName': receptionVenueName,
      'receptionAddress': receptionAddress,
      'hostName': hostName,
      'eventDate': eventDate,
      'eventTime': eventTime,
      'postalCode': postalCode,
      'address': address,
      'phone': phone,
      'venueName': venueName,
      'rsvpDeadline': rsvpDeadline,
      'email': email,
      'website': website,
      'message': message,
      'rsvpContact': rsvpContact,
      'dressCode': dressCode,
      'imageBase64': imageBase64,
      'isDoubleSided': isDoubleSided,
      'backImageBase64': backImageBase64,
      'qrUrl': qrUrl,
      'programs': programs.map((InvitationProgram program) => program.toJson()).toList(),
      'snsLinks': snsLinks.map((e) => e.toJson()).toList(),
      'backNote': backNote,
      'layoutType': layoutType,
      'orientation': orientation,
    };
  }
```

### `define/card_layout_type.dart` identifiers

```dart
enum CardComposition {
  centered,
  compact,
  editorial,
  split,
  photo,
  schedule,
}

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
  landscape("yoko", 148, 100),
  portrait("tate", 100, 148);
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

### `data/entity/invitation_program.dart`

```dart
  factory InvitationProgram.fromJson(Map<String, dynamic> json) {
    return InvitationProgram(
      id: json['id'] is String ? json['id'] as String : null,
      name: (json['name'] ?? "").toString(),
      eventTime: (json['eventTime'] ?? "").toString(),
      venue: (json['venue'] ?? "").toString(),
      message: (json['message'] ?? "").toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {'id': id, 'name': name, 'eventTime': eventTime, 'venue': venue, 'message': message};
  }
```
