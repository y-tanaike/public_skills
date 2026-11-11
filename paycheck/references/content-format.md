# Content format

- App ID: `paycheck`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `absenceDays` | number |
| `attendanceDays` | number |
| `company` | object |
| `createType` | string |
| `deductions` | array |
| `earnings` | array |
| `employee` | object |
| `holidayWorkingHours` | number |
| `hourlyWage` | number |
| `lateNightHours` | number |
| `layoutType` | string |
| `note` | string |
| `overtimeHours` | number |
| `paidLeaveDays` | number |
| `paymentDate` | string |
| `paymentYearMonth` | string |
| `version` | string |
| `workingDays` | number |
| `workingHours` | number |

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
        ..paymentYearMonth = (decodedJson["paymentYearMonth"] ?? "").toString()
        ..paymentDate = _parseDate(decodedJson["paymentDate"])
        ..company = CompanyProfile.fromContentJson(decodedJson)
        ..employee = EmployeeProfile.fromContentJson(decodedJson)
        ..workingDays = _parseDouble(decodedJson["workingDays"])
        ..attendanceDays = _parseDouble(decodedJson["attendanceDays"])
        ..absenceDays = _parseDouble(decodedJson["absenceDays"])
        ..paidLeaveDays = _parseDouble(decodedJson["paidLeaveDays"])
        ..workingHours = _parseDouble(decodedJson["workingHours"])
        ..overtimeHours = _parseDouble(decodedJson["overtimeHours"])
        ..lateNightHours = _parseDouble(decodedJson["lateNightHours"])
        ..holidayWorkingHours = _parseDouble(decodedJson["holidayWorkingHours"])
        ..earnings = PayrollItem.listFromJson(decodedJson["earnings"])
        ..deductions = PayrollItem.listFromJson(decodedJson["deductions"])
        ..hourlyWage = _parseDouble(decodedJson["hourlyWage"])
        ..note = (decodedJson["note"] ?? "").toString()
        ..layoutType = PayslipLayoutType.fromId((decodedJson["layoutType"] ?? PayslipLayoutType.standard.id).toString()).id;
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  static DateTime? _parseDate(Object? value) {
    if (value == null) {
      return null;
    }
    final String text = value.toString();
    if (text.isEmpty) {
      return null;
    }
    return DateTime.tryParse(text);
  }

  static double _parseDouble(Object? value) {
    if (value is num) {
      return value.toDouble();
    }
    return double.tryParse((value ?? "").toString()) ?? 0;
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'paymentYearMonth': paymentYearMonth,
      'paymentDate': paymentDate?.toIso8601String() ?? "",
      'company': company.toJson(),
      'employee': employee.toJson(),
      'workingDays': workingDays,
      'attendanceDays': attendanceDays,
      'absenceDays': absenceDays,
      'paidLeaveDays': paidLeaveDays,
      'workingHours': workingHours,
      'overtimeHours': overtimeHours,
      'lateNightHours': lateNightHours,
      'holidayWorkingHours': holidayWorkingHours,
      'earnings': earnings.map((e) => e.toJson()).toList(),
      'deductions': deductions.map((e) => e.toJson()).toList(),
      'hourlyWage': hourlyWage,
      'note': note,
      'layoutType': layoutType,
    };
  }
```

### `define/paper_orientation.dart` identifiers

```dart
enum PaperOrientation {
  portrait("tate", 210, 297),
  landscape("yoko", 297, 210);
```

### `define/payslip_layout_type.dart` identifiers

```dart
enum PayslipLayoutType {
  standard("standard", PaperOrientation.landscape),

  standardVertical("standard_vertical", PaperOrientation.portrait),

  simple("simple", PaperOrientation.portrait),

  detail("detail", PaperOrientation.portrait),

  twoColumn("two_column", PaperOrientation.portrait),

  summaryFirst("summary_first", PaperOrientation.portrait),

  attendanceFirst("attendance_first", PaperOrientation.portrait),

  payFirst("pay_first", PaperOrientation.portrait),

  statement("statement", PaperOrientation.portrait),

  table("table", PaperOrientation.landscape),

  card("card", PaperOrientation.portrait),

  hourly("hourly", PaperOrientation.portrait),

  smallBusiness("small_business", PaperOrientation.portrait);
```

### `data/entity/company_profile.dart`

```dart
  static CompanyProfile fromJson(Map<String, dynamic> json) {
    final String companyId = (json["id"] ?? "").toString();
    return CompanyProfile(
      id: companyId.isNotEmpty ? companyId : Uuid.v4().toString(),
      name: (json["name"] ?? "").toString(),
      address: (json["address"] ?? "").toString(),
      logoImageBase64: (json["logoImageBase64"] ?? "").toString(),
    );
  }

  static CompanyProfile fromContentJson(Map<String, dynamic> decodedJson) {
    if (decodedJson["company"] is Map) {
      final Map<String, dynamic> companyJson =
          (decodedJson["company"] as Map<dynamic, dynamic>).map((key, value) => MapEntry(key.toString(), value));
      return CompanyProfile.fromJson(companyJson);
    }

    return CompanyProfile(
      id: Uuid.v4().toString(),
      name: (decodedJson["companyName"] ?? "").toString(),
      address: (decodedJson["companyAddress"] ?? "").toString(),
      logoImageBase64: (decodedJson["logoImageBase64"] ?? "").toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "name": name,
      "address": address,
      "logoImageBase64": logoImageBase64,
    };
  }

  static List<CompanyProfile> listFromJsonString(String jsonString) {
    if (jsonString.isEmpty) {
      return <CompanyProfile>[];
    }

    try {
      List<dynamic> jsonList = jsonDecode(jsonString) as List<dynamic>;
      List<CompanyProfile> companyList = <CompanyProfile>[];
      for (dynamic item in jsonList) {
        if (item is! Map) {
          continue;
        }
        Map<String, dynamic> json = item.map((key, value) => MapEntry(key.toString(), value));
        CompanyProfile company = CompanyProfile.fromJson(json);
        if (company.isSavable) {
          companyList.add(company);
        }
      }
      return companyList;
    } catch (_) {
      return <CompanyProfile>[];
    }
  }

  static String listToJsonString(List<CompanyProfile> companyList) {
    return jsonEncode(companyList.map((item) => item.toJson()).toList());
  }
```

### `data/entity/employee_profile.dart`

```dart
  static EmployeeProfile fromJson(Map<String, dynamic> json) {
    final String employeeId = (json["id"] ?? "").toString();
    return EmployeeProfile(
      id: employeeId.isNotEmpty ? employeeId : Uuid.v4().toString(),
      name: (json["name"] ?? "").toString(),
      employeeNumber: (json["employeeNumber"] ?? "").toString(),
      department: (json["department"] ?? "").toString(),
      jobTitle: (json["jobTitle"] ?? "").toString(),
    );
  }

  static EmployeeProfile fromContentJson(Map<String, dynamic> decodedJson) {
    if (decodedJson["employee"] is Map) {
      final Map<String, dynamic> employeeJson =
          (decodedJson["employee"] as Map<dynamic, dynamic>).map((key, value) => MapEntry(key.toString(), value));
      return EmployeeProfile.fromJson(employeeJson);
    }

    return EmployeeProfile(
      id: Uuid.v4().toString(),
      name: (decodedJson["employeeName"] ?? "").toString(),
      employeeNumber: (decodedJson["employeeNumber"] ?? "").toString(),
      department: (decodedJson["department"] ?? "").toString(),
      jobTitle: (decodedJson["jobTitle"] ?? "").toString(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "name": name,
      "employeeNumber": employeeNumber,
      "department": department,
      "jobTitle": jobTitle,
    };
  }

  static List<EmployeeProfile> listFromJsonString(String jsonString) {
    if (jsonString.isEmpty) {
      return <EmployeeProfile>[];
    }

    try {
      List<dynamic> jsonList = jsonDecode(jsonString) as List<dynamic>;
      List<EmployeeProfile> employeeList = <EmployeeProfile>[];
      for (dynamic item in jsonList) {
        if (item is! Map) {
          continue;
        }
        Map<String, dynamic> json = item.map((key, value) => MapEntry(key.toString(), value));
        EmployeeProfile employee = EmployeeProfile.fromJson(json);
        if (employee.isSavable) {
          employeeList.add(employee);
        }
      }
      return employeeList;
    } catch (_) {
      return <EmployeeProfile>[];
    }
  }

  static String listToJsonString(List<EmployeeProfile> employeeList) {
    return jsonEncode(employeeList.map((item) => item.toJson()).toList());
  }
```

### `data/entity/payroll_item.dart`

```dart
  static PayrollItem fromJson(Map<String, dynamic> json) {
    final Object? amountValue = json['amount'];
    return PayrollItem(
      id: (json['id'] ?? '').toString().isEmpty ? createId() : (json['id']).toString(),
      name: (json['name'] ?? '').toString(),
      amount: amountValue is num ? amountValue.toDouble() : double.tryParse((amountValue ?? "").toString()) ?? 0,
    );
  }

  static List<PayrollItem> listFromJson(Object? rawList) {
    if (rawList is! List) {
      return [];
    }
    return rawList
        .whereType<Map<String, dynamic>>()
        .map(PayrollItem.fromJson)
        .toList();
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'amount': amount,
    };
  }
```
