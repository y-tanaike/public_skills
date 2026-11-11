# Content format

- App ID: `faq`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `description` | string |
| `documentTypeId` | string |
| `faqItemList` | array |
| `footer` | string |
| `htmlLayoutTypeId` | string |
| `isDescriptionMarkdown` | boolean |
| `pdfLayoutTypeId` | string |
| `showLabel` | boolean |
| `showLink` | boolean |
| `showPriority` | boolean |
| `title` | string |
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
      final faqItemList = (decodedJson['faqItemList'] as List<dynamic>? ?? [])
          .map((e) => FaqItem.fromJson(e as Map<String, dynamic>))
          .toList();

      return Content()
        ..version = decodedJson["version"] as String? ?? "1"
        ..createType = decodedJson["createType"] as String? ?? "Flutter"
        ..faqItemList = faqItemList
        ..documentTypeId = decodedJson["documentTypeId"] as String? ?? DocumentType.html.id
        ..htmlLayoutTypeId = decodedJson["htmlLayoutTypeId"] as String? ?? HtmlLayoutType.accordion.id
        ..pdfLayoutTypeId = decodedJson["pdfLayoutTypeId"] as String? ?? PdfLayoutType.list.id
        ..title = decodedJson["title"] as String? ?? ""
        ..description = decodedJson["description"] as String? ?? ""
        ..isDescriptionMarkdown = decodedJson["isDescriptionMarkdown"] as bool? ?? false
        ..footer = decodedJson["footer"] as String? ?? ""
        ..showLabel = decodedJson["showLabel"] as bool? ?? true
        ..showPriority = decodedJson["showPriority"] as bool? ?? true
        ..showLink = decodedJson["showLink"] as bool? ?? true
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
      'faqItemList': faqItemList.map((faqItem) => faqItem.toJson()).toList(),
      'documentTypeId': documentTypeId,
      'htmlLayoutTypeId': htmlLayoutTypeId,
      'pdfLayoutTypeId': pdfLayoutTypeId,
      'title': title,
      'description': description,
      'isDescriptionMarkdown': isDescriptionMarkdown,
      'footer': footer,
      'showLabel': showLabel,
      'showPriority': showPriority,
      'showLink': showLink,
    };
  }
```

### `define/document_type.dart` identifiers

```dart
enum DocumentType {
  html("html"),
  pdf("pdf");
```

### `define/html_layout_type.dart` identifiers

```dart
enum HtmlLayoutType {
  accordion("accordion"),
  card("card"),
  table("table"),
  tab("tab");
```

### `define/pdf_layout_type.dart` identifiers

```dart
enum PdfLayoutType {
  list("list"),
  card("card"),
  table("table");
```

### `data/entity/faq_item.dart`

```dart
  static FaqItem fromJson(Map<String, dynamic> json) {
    final String publishedDateString = json['publishedDate'] as String? ?? '';
    final String statusId = json['status'] as String? ?? '';
    return FaqItem(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      question: json['question'] as String? ?? '',
      answer: json['answer'] as String? ?? '',
      itemType: ItemType.fromId(json['itemType'] as String? ?? ''),
      person: json['person'] as String? ?? '',
      label: json['label'] as String? ?? '',
      note: json['note'] as String? ?? '',
      link: json['link'] as String? ?? '',
      priority: PriorityType.fromId(json['priority'] as String? ?? ''),
      publishedDate: publishedDateString.isEmpty ? null : DateTime.tryParse(publishedDateString),
      colorHex: json['colorHex'] as String? ?? '',
      isExpanded: json['isExpanded'] as bool? ?? true,
      status: statusId.isEmpty ? null : FaqStatus.fromId(statusId),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'question': question,
      'answer': answer,
      'itemType': itemType.id,
      'person': person,
      'label': label,
      'note': note,
      'link': link,
      'priority': priority.id,
      'publishedDate': publishedDate?.toIso8601String() ?? '',
      'colorHex': colorHex,
      'isExpanded': isExpanded,
      'status': status?.id ?? '',
    };
  }
```

### `define/faq_status.dart` identifiers

```dart
enum FaqStatus {
  draft('draft'),
  review('review'),
  published('published'),
  hidden('hidden'),
  deprecated('deprecated');
```

### `define/item_type.dart` identifiers

```dart
enum ItemType {
  item('item'),
  header('header');
```

### `define/priority_type.dart` identifiers

```dart
enum PriorityType {
  initial('initial'),
  priority_1('priority_1'),
  priority_2('priority_2'),
  priority_3('priority_3'),
  priority_4('priority_4'),
  priority_5('priority_5');
```
