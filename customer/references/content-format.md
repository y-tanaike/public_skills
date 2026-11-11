# Content format

- App ID: `customer`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `activities` | array |
| `address` | string |
| `age` | integer |
| `alcoholTolerance` | string |
| `background` | string |
| `birthday` | string |
| `birthdayYearUnknown` | boolean |
| `bloodType` | string |
| `children` | integer |
| `cigaretteBrand` | string |
| `closeness` | number |
| `company` | string |
| `createType` | string |
| `currencyCode` | string |
| `customerName` | string |
| `education` | string |
| `email` | string |
| `favoriteAlcohol` | string |
| `favoriteBrand` | string |
| `favoriteFood` | string |
| `hobbies` | string |
| `hometown` | string |
| `housing` | string |
| `jobDescription` | string |
| `kind` | string |
| `maritalStatus` | string |
| `moneyLevel` | number |
| `note` | string |
| `occupation` | string |
| `partner` | string |
| `phone` | string |
| `position` | string |
| `skills` | string |
| `smoking` | string |
| `version` | string |

Types use JSON terminology. Check nullability, nested elements, and defaults against the conversion definitions below. Image fields are out of scope even where they appear in the app's serializer.

## Nested elements, identifiers, and date conversions

The excerpts below preserve serialization statements from the app implementation checked on 2026-11-11; source comments are omitted. You do not need to execute Dart. `fromJson` specifies accepted types and defaults; `toJson` specifies output keys. Follow the actual date conversion units rather than assuming ISO timestamps. The excerpts are reference fragments, not standalone Dart programs.

### `data/entity/content.dart`

```dart
  static Content? tryFromJson(String json) {
    try {
      return fromJson(json);
    } catch (_) {
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
    final Map<String, dynamic> data = jsonDecode(json) as Map<String, dynamic>;
    if (data['kind'] != 'customer' || data['activities'] is! List) {
      throw const FormatException('Invalid customer file');
    }
    return Content()
      ..version = data['version'] as String? ?? "1"
      ..createType = data['createType'] as String? ?? "Flutter"
      ..customerName = data['customerName'] as String? ?? ""
      ..phone = data['phone'] as String? ?? ""
      ..email = data['email'] as String? ?? ""
      ..company = data['company'] as String? ?? ""
      ..address = data['address'] as String? ?? ""
      ..note = data['note'] as String? ?? ""
      ..currencyCode = data['currencyCode'] as String? ?? ""
      ..imageBase64 = data['imageBase64'] as String? ?? ""
      ..occupation = data['occupation'] as String? ?? ""
      ..cigaretteBrand = data['cigaretteBrand'] as String? ?? ""
      ..hometown = data['hometown'] as String? ?? ""
      ..background = data['background'] as String? ?? ""
      ..education = data['education'] as String? ?? ""
      ..favoriteAlcohol = data['favoriteAlcohol'] as String? ?? ""
      ..favoriteFood = data['favoriteFood'] as String? ?? ""
      ..favoriteBrand = data['favoriteBrand'] as String? ?? ""
      ..skills = data['skills'] as String? ?? ""
      ..hobbies = data['hobbies'] as String? ?? ""
      ..position = data['position'] as String? ?? ""
      ..jobDescription = data['jobDescription'] as String? ?? ""
      ..birthday = data['birthday'] == null ? null : DateTime.parse(data['birthday'] as String)
      ..birthdayYearUnknown = data['birthdayYearUnknown'] as bool? ?? false
      .._age = _optionalCount(data['age'])
      ..children = _optionalCount(data['children'])
      ..moneyLevel = _profileLevel(data['moneyLevel'])
      ..closeness = _profileLevel(data['closeness'])
      ..smoking = SmokingStatus.fromName(data['smoking'] as String?)
      ..bloodType = BloodType.fromName(data['bloodType'] as String?)
      ..alcoholTolerance = AlcoholTolerance.fromName(data['alcoholTolerance'] as String?)
      ..partner = PartnerStatus.fromName(data['partner'] as String?)
      ..maritalStatus = MaritalStatus.fromName(data['maritalStatus'] as String?)
      ..housing = HousingType.fromName(data['housing'] as String?)
      ..activities = (data['activities'] as List<dynamic>).map((dynamic item) => CustomerActivity.fromJson(item as Map<String, dynamic>)).toList();
  }

  Map<String, dynamic> toJson() {
    return {
      'kind': 'customer',
      'version': version,
      'createType': createType,
      'customerName': customerName,
      'phone': phone,
      'email': email,
      'company': company,
      'address': address,
      'note': note,
      'currencyCode': currencyCode,
      'imageBase64': imageBase64,
      'occupation': occupation,
      'cigaretteBrand': cigaretteBrand,
      'hometown': hometown,
      'background': background,
      'education': education,
      'favoriteAlcohol': favoriteAlcohol,
      'favoriteFood': favoriteFood,
      'favoriteBrand': favoriteBrand,
      'skills': skills,
      'hobbies': hobbies,
      'position': position,
      'jobDescription': jobDescription,
      'age': age,
      'children': children,
      'moneyLevel': moneyLevel,
      'closeness': closeness,
      'birthday': birthday?.toIso8601String(),
      'birthdayYearUnknown': birthdayYearUnknown,
      'smoking': smoking.name,
      'bloodType': bloodType.name,
      'alcoholTolerance': alcoholTolerance.name,
      'partner': partner.name,
      'maritalStatus': maritalStatus.name,
      'housing': housing.name,
      'activities': activities.map((CustomerActivity item) => item.toJson()).toList(),
    };
  }
```

### `define/customer_profile_type.dart` identifiers

```dart
enum SmokingStatus {
  unset, smoker, nonSmoker;
```

### `data/entity/customer_activity.dart`

```dart
  factory CustomerActivity.fromJson(Map<String, dynamic> json) {
    final double amount = (json['amount'] as num).toDouble();
    if (!amount.isFinite || amount < 0) {
      throw const FormatException('Invalid activity amount');
    }
    final num rating = json['rating'] as num? ?? 0;
    if (!rating.isFinite) throw const FormatException('Invalid activity rating');
    return CustomerActivity(
      id: json['id'] as String,
      date: DateTime.parse(json['date'] as String),
      description: json['description'] as String? ?? "",
      amount: amount,
      isAllDay: json['isAllDay'] as bool? ?? true,
      rating: (rating.clamp(0, 5) * 10).round() / 10,
      note: json['note'] as String? ?? "",
      priority: PriorityType.fromName(json['priority'] as String?),
      colorValue: json['colorValue'] as int?,
    );
  }

  Map<String, dynamic> toJson() {
    return {'id': id, 'date': date.toIso8601String(), 'description': description, 'amount': amount, 'isAllDay': isAllDay, 'rating': rating, 'note': note, 'priority': priority.name, 'colorValue': colorValue};
  }
```

### `define/priority_type.dart` identifiers

```dart
enum PriorityType {
  initial, priority1, priority2, priority3, priority4, priority5;
```
