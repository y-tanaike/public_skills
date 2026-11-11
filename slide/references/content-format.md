# Content format

- App ID: `slide`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `author` | string |
| `confidentialityLevel` | string |
| `contentLicenseType` | string |
| `customLicenseText` | string |
| `fontScaleType` | string |
| `footer` | string |
| `licenseHolder` | string |
| `pageNumberDisplayType` | string |
| `slideLayoutType` | string |
| `slideList` | array |
| `themeColorHex` | string |
| `themeType` | string |
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
      final Map<String, dynamic> decodedJson = jsonDecode(json);
      final slideList = (decodedJson['slideList'] as List<dynamic>? ?? [])
          .map((e) => Slide.fromJson(e as Map<String, dynamic>))
          .toList();

      return Content()
        ..version = decodedJson['version'] as String? ?? '1'
        ..slideList = slideList
        ..footer = decodedJson['footer'] as String? ?? ''
        ..author = decodedJson['author'] as String? ?? ''
        ..themeColorHex = decodedJson['themeColorHex'] as String? ?? ''
        ..themeType = ThemeType.fromId(decodedJson['themeType'] as String? ?? '')
        ..pageNumberDisplayType = PageNumberDisplayType.fromId(
            decodedJson['pageNumberDisplayType'] as String? ?? '')
        ..slideLayoutType = SlideLayoutType.fromId(
            decodedJson['slideLayoutType'] as String? ?? '')
        ..fontScaleType = SlideFontScaleType.fromId(
            decodedJson['fontScaleType'] as String? ?? '')
        ..confidentialityLevel = ConfidentialityLevel.fromId(
            decodedJson['confidentialityLevel'] as String? ?? '')
        ..contentLicenseType = ContentLicenseType.fromId(
            decodedJson['contentLicenseType'] as String? ?? '')
        ..customLicenseText = decodedJson['customLicenseText'] as String? ?? ''
        ..licenseHolder = decodedJson['licenseHolder'] as String? ?? '';
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'slideList': slideList.map((slide) => slide.toJson()).toList(),
      'footer': footer,
      'author': author,
      'themeColorHex': themeColorHex,
      'themeType': themeType.id,
      'pageNumberDisplayType': pageNumberDisplayType.id,
      'slideLayoutType': slideLayoutType.id,
      'fontScaleType': fontScaleType.id,
      'confidentialityLevel': confidentialityLevel.id,
      'contentLicenseType': contentLicenseType.id,
      'customLicenseText': customLicenseText,
      'licenseHolder': licenseHolder,
    };
  }
```

### `define/confidentiality_level.dart` identifiers

```dart
enum ConfidentialityLevel {
  none('none'),
  internal('internal'),
  confidential('confidential'),
  strictlyConfidential('strictly_confidential');
```

### `define/content_license_type.dart` identifiers

```dart
enum ContentLicenseType {
  none('none'),
  allRightsReserved('all_rights_reserved'),
  doNotDistribute('do_not_distribute'),
  publicDomain('public_domain'),
  cc0('cc0'),
  ccBy('cc_by'),
  ccBySa('cc_by_sa'),
  ccByNc('cc_by_nc'),
  ccByNcSa('cc_by_nc_sa'),
  ccByNd('cc_by_nd'),
  ccByNcNd('cc_by_nc_nd'),
  custom('custom');
```

### `define/page_number_display_type.dart` identifiers

```dart
enum PageNumberDisplayType {
  hidden('hidden'),
  pageOnly('page_only'),
  pageWithTotal('page_with_total');
```

### `define/slide_font_scale_type.dart` identifiers

```dart
enum SlideFontScaleType {
  extraSmall('extra_small', 0.8),
  small('small', 0.9),
  medium('medium', 1.0),
  large('large', 1.15),
  extraLarge('extra_large', 1.3);
```

### `define/slide_layout_type.dart` identifiers

```dart
enum SlideLayoutType {
  screen4x3('screen_4x3', '4:3', 480, 360),
  screen16x9('screen_16x9', '16:9', 480, 270),
  screen16x10('screen_16x10', '16:10', 480, 300),
  screenWide('screen_wide', 'Wide', 640, 360);
```

### `define/theme_type.dart` identifiers

```dart
enum ThemeCategory {
  simple('simple'),
  modern('modern'),
  pop('pop');
```

### `data/entity/slide.dart`

```dart
  static Slide fromJson(Map<String, dynamic> json) {
    final Slide slide = _fromJsonRaw(json);
    if (slide.slideType.usesColumnItems && !slide.hasColumnItems && slide.bulletList.isNotEmpty) {
      slide.bodyList = List<String>.from(slide.bulletList);
      slide.bulletList = <String>[];
    }
    if (slide.slideType.usesKpiItems && slide.bodyList.isEmpty && slide.body.isNotEmpty) {
      slide.bodyList = <String>[slide.body];
    }
    if (slide.slideType.usesBulletDepth &&
        slide.bulletDepthList.isEmpty &&
        slide.bulletList.length > 1) {
      slide.bulletDepthList = <String>[
        '0',
        for (int i = 1; i < slide.bulletList.length; i++) '1',
      ];
    }
    return slide;
  }

  static Slide _fromJsonRaw(Map<String, dynamic> json) {
    return Slide(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      title: json['title'] as String? ?? '',
      subtitle: json['subtitle'] as String? ?? '',
      body: json['body'] as String? ?? '',
      isHidden: json['isHidden'] as bool? ?? false,
      bulletList: _stringList(json['bulletList']),
      bulletDepthList: _stringList(json['bulletDepthList']),
      subtitleList: _stringList(json['subtitleList']),
      bodyList: _stringList(json['bodyList']),
      columnValueList: _stringList(json['columnValueList']),
      highlightItemIndex: (json['highlightItemIndex'] as num?)?.toInt() ?? -1,
      imageBase64List: _stringList(json['imageBase64List']),
      imageIconIdList: _stringList(json['imageIconIdList']),
      imageIconColorList: _stringList(json['imageIconColorList']),
      iconIdList: _stringList(json['iconIdList']),
      tableRows: (json['tableRows'] as List<dynamic>? ?? [])
          .map((row) => _stringList(row))
          .toList(),
      tableAlignList: _stringList(json['tableAlignList']),
      cellColorList: (json['cellColorList'] as List<dynamic>? ?? [])
          .map((row) => _stringList(row))
          .toList(),
      labelList: _stringList(json['labelList']),
      valueList: _stringList(json['valueList']),
      customMarkdown: json['customMarkdown'] as String? ?? '',
      note: json['note'] as String? ?? '',
      fontColorHex: _colorHex(json['fontColorHex'], json['fontColorHexList']),
      backgroundColorHex: _colorHex(json['backgroundColorHex'], json['backgroundColorHexList']),
      slideType: SlideType.fromId(json['slideType'] as String? ?? ''),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'subtitle': subtitle,
      'body': body,
      'isHidden': isHidden,
      'bulletList': bulletList,
      'bulletDepthList': bulletDepthList,
      'imageBase64List': imageBase64List,
      'imageIconIdList': imageIconIdList,
      'imageIconColorList': imageIconColorList,
      'iconIdList': iconIdList,
      'subtitleList': subtitleList,
      'bodyList': bodyList,
      'columnValueList': columnValueList,
      'highlightItemIndex': highlightItemIndex,
      'tableRows': tableRows,
      'cellColorList': cellColorList,
      'tableAlignList': tableAlignList,
      'labelList': labelList,
      'valueList': valueList,
      'customMarkdown': customMarkdown,
      'note': note,
      'fontColorHex': fontColorHex,
      'backgroundColorHex': backgroundColorHex,
      'slideType': slideType.id,
    };
  }
```

### `define/slide_icon_type.dart` identifiers

```dart
enum SlideIconType {
  lightbulb('lightbulb'),
  chartLine('chart_line'),
  bullseye('bullseye'),
  briefcase('briefcase'),
  handshake('handshake'),
  coins('coins'),
  cart('cart'),
  building('building'),
  user('user'),
  users('users'),
  comments('comments'),
  envelope('envelope'),
  phone('phone'),
  bell('bell'),
  heart('heart'),
  star('star'),
  gear('gear'),
  laptop('laptop'),
  mobile('mobile'),
  cloud('cloud'),
  database('database'),
  lock('lock'),
  robot('robot'),
  code('code'),
  check('check'),
  xmark('xmark'),
  triangleExclamation('triangle_exclamation'),
  circleQuestion('circle_question'),
  circleInfo('circle_info'),
  arrowUp('arrow_up'),
  arrowRight('arrow_right'),
  arrowDown('arrow_down'),
  clock('clock'),
  calendar('calendar'),
  mapPin('map_pin'),
  globe('globe'),
  truck('truck'),
  plane('plane'),
  book('book'),
  graduationCap('graduation_cap'),
  flask('flask'),
  palette('palette'),
  camera('camera'),
  music('music'),
  leaf('leaf'),
  fire('fire');
```

### `define/slide_type.dart` identifiers

```dart
enum SlideTypeCategory {
  basic('basic'),
  text('text'),
  image('image'),
  table('table'),
  chart('chart'),
  layout('layout'),
  business('business'),
  diagram('diagram'),
  special('special');
```

### `define/table_align_type.dart` identifiers

```dart
enum TableAlignType {
  auto('auto'),
  left('left'),
  center('center'),
  right('right');
```
