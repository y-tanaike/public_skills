# Content format

- App ID: `simplecorrelation`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

`topicMap` and `relationMap` are objects keyed by ID, not arrays. Match each map key with the value's `id`. Each edge's `fromTopicId` and `toTopicId` must refer to existing topics. Use `layoutVersion: 1` for the correlation layout.

## Root keys

| Key | JSON type |
|---|---|
| `connectionPathType` | string |
| `createType` | string |
| `layoutType` | string |
| `layoutVersion` | integer |
| `relationMap` | object |
| `topicMap` | object |
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
      if (decoded is! Map<String, dynamic>) {
        return null;
      }
      final dynamic rawTopicMap = decoded['topicMap'];
      if (rawTopicMap is! Map<String, dynamic>) {
        return null;
      }
      final Map<String, Topic> topicMap = <String, Topic>{};
      rawTopicMap.forEach((String _, dynamic value) {
        if (value is Map<String, dynamic>) {
          final Topic topic = Topic.fromJson(value);
          topicMap[topic.id] = topic;
        }
      });
      if (topicMap.isEmpty) {
        return null;
      }
      final Map<String, Relation> relationMap = <String, Relation>{};
      final dynamic rawRelationMap = decoded['relationMap'];
      if (rawRelationMap is Map<String, dynamic>) {
        rawRelationMap.forEach((String _, dynamic value) {
          if (value is Map<String, dynamic>) {
            final Relation relation = Relation.fromJson(value);
            if (topicMap.containsKey(relation.fromTopicId) && topicMap.containsKey(relation.toTopicId)) {
              relationMap[relation.id] = relation;
            }
          }
        });
      }
      return Content()
        ..version = decoded['version'] as String? ?? Content().version
        ..createType = decoded['createType'] as String? ?? Content().createType
        ..layoutVersion = _readLayoutVersion(decoded)
        ..topicMap = topicMap
        ..relationMap = relationMap
        .._readLayoutOptions(decoded);
    } catch (e) {
      logger.e("error tryFromSharedJson: $e");
      return null;
    }
  }

  static Content fromJson(String json) {
    try {
      logger.d("fromJson $json");
      final Map<String, dynamic> decodedJson = jsonDecode(json);

      final rawTopicMap = decodedJson['topicMap'] as Map<String, dynamic>?;
      final topicMap = rawTopicMap == null
          ? <String, Topic>{}
          : rawTopicMap.map<String, Topic>((k, v) =>
              MapEntry(k, Topic.fromJson(v as Map<String, dynamic>)),
            );

      final rawRelationMap = decodedJson['relationMap'] as Map<String, dynamic>?;
      final relationMap = rawRelationMap == null
          ? <String, Relation>{}
          : rawRelationMap.map<String, Relation>((k, v) =>
              MapEntry(k, Relation.fromJson(v as Map<String, dynamic>)),
            );

      return Content()
        ..version = decodedJson["version"]
        ..createType = decodedJson["createType"]
        ..layoutVersion = _readLayoutVersion(decodedJson)
        ..topicMap = topicMap
        ..relationMap = relationMap
        .._readLayoutOptions(decodedJson)
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
      ...layoutOptionsToJson(),
      'topicMap':  {
        for (final e in topicMap.entries) e.key.toString(): e.value.toJson(),
      },
      'relationMap': {
        for (final e in relationMap.entries) e.key.toString(): e.value.toJson(),
      },
    };
  }

  Map<String, dynamic> layoutOptionsToJson({bool includePositions = true}) => <String, dynamic>{
    'layoutVersion': layoutVersion,
    'layoutType': layoutType.id,
    if (connectionPathType != null) 'connectionPathType': connectionPathType!.id,
    if (includePositions && layoutPositions.isNotEmpty) 'layoutPositions': <String, dynamic>{
      for (final MapEntry<String, Map<String, Offset>> entry in layoutPositions.entries) entry.key: <String, dynamic>{
        for (final MapEntry<String, Offset> point in entry.value.entries) point.key: <double>[point.value.dx, point.value.dy],
      },
    },
  };
```

### `define/graph_layout_type.dart` identifiers

```dart
enum GraphLayoutType {
  flow('flow'),
  center('center'),
  circle('circle');
```

### `define/connection_path_type.dart` identifiers

```dart
enum ConnectionPathType {
  straight('straight'),
  curve('curve'),
  orthogonal('orthogonal');
```

### `data/entity/relation.dart`

```dart
  static Relation fromJson(Map<String, dynamic> json) {


    return Relation(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      title: json['title'] as String? ?? '',
      note: json['note'] as String? ?? '',
      link: json['link'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      relationArrowType: RelationArrowType.fromId(json['relationArrowType'] ?? ''),
      relationLineType:  RelationLineType.fromId(json['relationLineType'] ?? ''),
      loveType: LoveType.fromId(json['loveType'] ?? ''),
      friendType: FriendType.fromId(json['friendType'] ?? ''),
      goodBadType: GoodBadType.fromId(json['goodBadType'] ?? ''),
      fromTopicId: json['fromTopicId'] as String? ?? '',
      toTopicId: json['toTopicId'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = {
      'id': id,
      'title': title,
      'note': note,
      'link': link,
      'colorHex': colorHex,
      'relationArrowType': relationArrowType.id,
      'relationLineType': relationLineType.id,
      'loveType': loveType.id,
      'friendType': friendType.id,
      'goodBadType': goodBadType.id,
      'fromTopicId': fromTopicId,
      'toTopicId': toTopicId,
    };

    return data;
  }
```

### `data/entity/topic.dart`

```dart
  static Topic fromJson(Map<String, dynamic> json) {

    return Topic(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      title: json['title'] as String? ?? '',
      note: json['note'] as String? ?? '',
      link: json['link'] as String? ?? '',
      colorHex: json['colorHex'] as String? ?? '',
      imageBase64: json['imageBase64'] as String? ?? '',
      reserveImageSpace: json['reserveImageSpace'] == true,
      topicType: TopicType.fromId(json['topicType'] ?? ''),
      sizeType: TopicSizeType.fromId(json['sizeType'] ?? ''),
      offsetX: (json['offsetX'] as num?)?.toDouble() ?? 0,
      offsetY: (json['offsetY'] as num?)?.toDouble() ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = {
      'id': id,
      'title': title,
      'note': note,
      'link': link,
      'colorHex': colorHex,
      'imageBase64': imageBase64,
      if (reserveImageSpace) 'reserveImageSpace': true,
      'topicType': topicType.id,
      'sizeType': sizeType.id,
      'offsetX': offsetX,
      'offsetY': offsetY,
    };

    return data;
  }
```

### `define/good_bad_type.dart` identifiers

```dart
enum GoodBadType {
  initial('initial'),
  good('good'),
  bad('bad');
```

### `define/love_type.dart` identifiers

```dart
enum LoveType {
  initial('initial'),
  mutualLove('mutual_love'),
  oneSided('one_sided'),
  unrequited('unrequited'),
  ;
```

### `define/friend_type.dart` identifiers

```dart
enum FriendType {
  initial('initial'),
  handshake('handshake'),
  conflict('conflict'),
  respect('respect'),
  flame('flame'),
  ;
```

### `define/relation_arrow_type.dart` identifiers

```dart
enum RelationArrowType {
  none("none"),
  one("one"),
  both("both"),
  ;
```

### `define/relation_line_type.dart` identifiers

```dart
enum RelationLineType {
  solid("solid"),
  dotted("dotted"),
  dashDotted("dashDotted"),
  ;
```

### `define/topic_size_type.dart` identifiers

```dart
enum TopicSizeType {
  small("small", 0.7),
  standard("standard", 1.0),
  large("large", 1.35),
  extraLarge("extraLarge", 1.7),
  ;
```

### `define/topic_type.dart` identifiers

```dart
enum TopicType {
  rectangle("rectangle"),
  oval("oval"),
  circle("circle"),
  rhombus("rhombus"),
  noframe("noframe"),
  ;
```
