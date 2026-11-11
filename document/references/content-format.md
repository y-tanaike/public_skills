# Content format

- App ID: `document`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

`document` is a **JSON-encoded string** containing a Quill Delta array, not the array itself. Use text inserts and end the document with a newline. Do not generate image embeds.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `document` | string |
| `version` | string |

Types use JSON terminology. Check nullability, nested elements, and defaults against the conversion definitions below. Image fields are out of scope even where they appear in the app's serializer.

## Nested elements, identifiers, and date conversions

The excerpts below preserve serialization statements from the app implementation checked on 2026-11-11; source comments are omitted. You do not need to execute Dart. `fromJson` specifies accepted types and defaults; `toJson` specifies output keys. Follow the actual date conversion units rather than assuming ISO timestamps. The excerpts are reference fragments, not standalone Dart programs.

### `data/entity/content.dart`

```dart
  static Content? tryFromJson(String json) {
    try {
      final Object? decodedJson = jsonDecode(json);
      if (decodedJson is! Map<String, dynamic>) {
        return null;
      }
      final Object? version = decodedJson["version"];
      final Object? documentJson = decodedJson["document"];
      final Object? createType = decodedJson["createType"];
      if (version is! String || documentJson is! String || createType is! String) {
        return null;
      }
      return Content(
        documentFromJson(documentJson),
        version: version,
        createType: createType,
      );
    } catch (e) {
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
      if (jsonEncode(content.toJson()) == jsonEncode(Content(Document()).toJson())) {
        return null;
      }
      return content;
    } catch (e) {
      logger.e("error tryFromSharedJson: $e");
      return null;
    }
  }

  static Content fromJson(String json) {
    final Content? content = tryFromJson(json);
    if (content == null) {
      throw const FormatException('Invalid content format.');
    }
    return content;
  }

  static Document documentFromJson(String documentJson) {
    final Object? decodedJson = jsonDecode(documentJson);
    if (decodedJson is! List<dynamic>) {
      throw const FormatException('The document must be a Quill Delta JSON array.');
    }
    return Document.fromJson(decodedJson);
  }

  String getDocumentJson() {
    return jsonEncode(document.toDelta().toJson());
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'document': getDocumentJson(),
      'createType': createType,
    };
  }
```
