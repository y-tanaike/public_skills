# Content format

- App ID: `marpslide`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Put Marp front matter, such as `marp: true`, in root `frame`; put each slide's Markdown in `pageList[].markdown`. Give each page a unique `id`. This is an app-specific JSON format, not the raw-text sharing format.

## Root keys

| Key | JSON type |
|---|---|
| `frame` | string |
| `pageList` | array |
| `version` | string |

Types use JSON terminology. Check nullability, nested elements, and defaults against the conversion definitions below. Image fields are out of scope even where they appear in the app's serializer.

## Nested elements, identifiers, and date conversions

The excerpts below preserve serialization statements from the app implementation checked on 2026-11-11; source comments are omitted. You do not need to execute Dart. `fromJson` specifies accepted types and defaults; `toJson` specifies output keys. Follow the actual date conversion units rather than assuming ISO timestamps. The excerpts are reference fragments, not standalone Dart programs.

### `data/entity/content.dart`

```dart
  static SlidePage fromJson(Map<String, dynamic> json) {
    final String id = json['id'] as String? ?? '';
    return SlidePage(
      id: id.trim().isEmpty ? Uuid.v4().toString() : id,
      markdown: json['markdown'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'markdown': markdown,
    };
  }

  static SlidePageUpdate fromJson(Map<String, dynamic> json) {
    final String insertAfterId = json['insertAfterId'] as String? ?? '';
    return SlidePageUpdate(
      page: SlidePage.fromJson(json),
      insertAfterId: insertAfterId.trim().isEmpty ? null : insertAfterId,
    );
  }

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
      if (json.trim().isEmpty) {
        return Content();
      }
      final Map<String, dynamic> decodedJson = jsonDecode(json);
      final List<SlidePage> pageList = (decodedJson['pageList'] as List<dynamic>? ?? [])
          .map((e) => SlidePage.fromJson(e as Map<String, dynamic>))
          .toList();
      final Set<String> pageIdSet = <String>{};
      for (final SlidePage page in pageList) {
        while (!pageIdSet.add(page.id)) {
          page.id = Uuid.v4().toString();
        }
      }
      return Content()
        ..version = decodedJson['version'] as String? ?? '1'
        ..frame = decodedJson['frame'] as String? ?? ''
        ..pageList = pageList;
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'frame': frame,
      'pageList': pageList.map((page) => page.toJson()).toList(),
    };
  }
```
