# Content format

- App ID: `trip`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `createType` | string |
| `expenseItemList` | See conversion definitions below |
| `tripItemList` | array |
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
      final List<dynamic> itemJsonList = decodedJson['tripItemList'] as List<dynamic>?
          ?? decodedJson['expenseItemList'] as List<dynamic>?
          ?? [];
      final List<TripItem> tripItemList = itemJsonList
          .map((e) => TripItem.fromJson(e as Map<String, dynamic>))
          .toList();

      return Content()
        ..version = decodedJson["version"] as String? ?? "1"
        ..createType = decodedJson["createType"] as String? ?? "Flutter"
        ..tripItemList = tripItemList
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
      'tripItemList': tripItemList.map((tripItem) => tripItem.toJson()).toList(),
    };
  }
```

### `data/entity/trip_item.dart`

```dart
  static TripItem fromJson(Map<String, dynamic> json) {
    final String dateTimeString = json['dateTime'] as String?
        ?? json['paymentDateTime'] as String?
        ?? '';
    return TripItem(
      id: json['id'] as String? ?? Uuid.v4().toString(),
      title: json['title'] as String? ?? '',
      iconType: TripIconType.fromId(json['iconType'] as String? ?? ''),
      location: json['location'] as String? ?? '',
      latitude: (json['latitude'] as num?)?.toDouble(),
      longitude: (json['longitude'] as num?)?.toDouble(),
      label: json['label'] as String? ?? '',
      phone: json['phone'] as String? ?? '',
      url: json['url'] as String? ?? '',
      imageBase64: json['imageBase64'] as String? ?? '',
      cost: (json['cost'] as num?)?.toDouble() ?? 0,
      note: json['note'] as String? ?? '',
      priority: PriorityType.fromId(json['priority'] as String? ?? ''),
      dateTime: dateTimeString.isEmpty ? null : DateTime.tryParse(dateTimeString),
      isAllDay: json['isAllDay'] as bool? ?? true,
      colorHex: json['colorHex'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'iconType': iconType.id,
      'location': location,
      'latitude': latitude,
      'longitude': longitude,
      'label': label,
      'phone': phone,
      'url': url,
      'imageBase64': imageBase64,
      'cost': cost,
      'note': note,
      'priority': priority.id,
      'dateTime': dateTime?.toIso8601String() ?? '',
      'isAllDay': isAllDay,
      'colorHex': colorHex,
    };
  }
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

### `define/trip_icon_type.dart` identifiers

```dart
enum TripIconType {
  place('place', Icons.place_outlined, Colors.grey),
  flight('flight', Icons.flight_outlined, Colors.blue),
  train('train', Icons.train_outlined, Colors.indigo),
  subway('subway', Icons.subway_outlined, Colors.deepPurple),
  bus('bus', Icons.directions_bus_outlined, Colors.orange),
  car('car', Icons.directions_car_outlined, Colors.teal),
  ship('ship', Icons.directions_boat_outlined, Colors.cyan),
  bike('bike', Icons.directions_bike_outlined, Colors.lightGreen),
  walk('walk', Icons.directions_walk_outlined, Colors.green),
  hiking('hiking', Icons.hiking_outlined, Colors.brown),
  hotel('hotel', Icons.hotel_outlined, Colors.blueGrey),
  restaurant('restaurant', Icons.restaurant_outlined, Colors.deepOrange),
  cafe('cafe', Icons.local_cafe_outlined, Colors.amber),
  bar('bar', Icons.local_bar_outlined, Colors.purple),
  shopping('shopping', Icons.shopping_bag_outlined, Colors.pink),
  camera('camera', Icons.photo_camera_outlined, Colors.blueAccent),
  museum('museum', Icons.museum_outlined, Colors.indigoAccent),
  temple('temple', Icons.temple_buddhist_outlined, Colors.orangeAccent),
  park('park', Icons.park_outlined, Color(0xFF558B2F)),
  beach('beach', Icons.beach_access_outlined, Colors.lightBlue),
  hotSpring('hot_spring', Icons.hot_tub_outlined, Colors.redAccent),
  ticket('ticket', Icons.confirmation_number_outlined, Colors.deepPurpleAccent),
  money('money', Icons.payments_outlined, Color(0xFF00796B)),
  luggage('luggage', Icons.luggage_outlined, Color(0xFF5D4037)),
  map('map', Icons.map_outlined, Color(0xFF00838F)),
  event('event', Icons.event_outlined, Colors.pinkAccent);
```
