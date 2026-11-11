# Content format

- App ID: `resume`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Preserve list order, item IDs, and references. Use the conversion definitions below to check nested keys, types, enum IDs, and date formats.

## Root keys

| Key | JSON type |
|---|---|
| `additionalInformation` | string |
| `address1` | string |
| `address2` | string |
| `affiliations` | string |
| `availableStartDate` | string |
| `awardItems` | array |
| `birthDate` | string |
| `businessExperience` | string |
| `careerSummary` | string |
| `certificationItems` | array |
| `city` | string |
| `commuteMethod` | string |
| `commuteTime` | string |
| `contactAddress1` | string |
| `contactAddress2` | string |
| `contactCity` | string |
| `contactCountry` | string |
| `contactPhone` | string |
| `contactPostalCode` | string |
| `contactPrefecture` | string |
| `country` | string |
| `createType` | string |
| `currentCompany` | string |
| `currentDepartment` | string |
| `currentJobTitle` | string |
| `currentOccupation` | string |
| `currentSalary` | string |
| `dependents` | integer |
| `desiredEmploymentType` | string |
| `desiredIndustry` | string |
| `desiredJobTitle` | string |
| `desiredOccupation` | string |
| `desiredSalary` | string |
| `desiredWorkLocation` | string |
| `documentDate` | string |
| `documentTitle` | string |
| `drivingLicense` | string |
| `educationItems` | array |
| `email` | string |
| `gender` | string |
| `githubUrl` | string |
| `hasCar` | boolean |
| `hasSpouse` | boolean |
| `hobbies` | string |
| `industryExperience` | string |
| `interests` | string |
| `languageItems` | array |
| `layoutType` | string |
| `linkedinUrl` | string |
| `links` | array |
| `managementExperience` | string |
| `militaryService` | string |
| `mobile` | string |
| `motivation` | string |
| `name` | string |
| `nameReading` | string |
| `nationality` | string |
| `nearestStation` | string |
| `note` | string |
| `objective` | string |
| `overtimePreference` | string |
| `patents` | string |
| `phone` | string |
| `portfolioUrl` | string |
| `postalCode` | string |
| `prefecture` | string |
| `presentations` | string |
| `professionalSummary` | string |
| `projectItems` | array |
| `publications` | string |
| `referenceItems` | array |
| `relocationPreference` | string |
| `remoteWorkPreference` | string |
| `requests` | string |
| `selfPromotion` | string |
| `skillItems` | array |
| `specialSkills` | string |
| `spouseSupportObligation` | boolean |
| `strengths` | string |
| `technicalExperience` | string |
| `themeColor` | string |
| `useContactAddress` | boolean |
| `version` | string |
| `visaExpirationDate` | string |
| `visaStatus` | string |
| `volunteerExperience` | string |
| `weaknesses` | string |
| `website` | string |
| `workAuthorization` | string |
| `workItems` | array |
| `workingDaysPreference` | string |
| `workingHoursPreference` | string |

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
      return fromMap(decodedJson);
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  static Content fromMap(Map<String, dynamic> json) {
    String str(String key) => ResumeItemUtil.str(json[key]);

    return Content()
      ..version = ResumeItemUtil.str(json["version"]).isEmpty ? "1" : str("version")
      ..createType = ResumeItemUtil.str(json["createType"]).isEmpty ? "Flutter" : str("createType")
      ..documentTitle = str("documentTitle")
      ..documentDate = str("documentDate")
      ..layoutType = ResumeLayoutType.fromId(str("layoutType")).id
      ..themeColor = str("themeColor")
      ..name = _resolveName(json)
      ..nameReading = str("nameReading")
      ..birthDate = str("birthDate")
      ..gender = str("gender")
      ..nationality = str("nationality")
      ..photoImageBase64 = str("photoImageBase64")
      ..postalCode = str("postalCode")
      ..prefecture = str("prefecture")
      ..city = str("city")
      ..address1 = str("address1")
      ..address2 = str("address2")
      ..country = str("country")
      ..phone = str("phone")
      ..mobile = str("mobile")
      ..email = str("email")
      ..useContactAddress = ResumeItemUtil.flag(json["useContactAddress"])
      ..contactPostalCode = str("contactPostalCode")
      ..contactPrefecture = str("contactPrefecture")
      ..contactCity = str("contactCity")
      ..contactAddress1 = str("contactAddress1")
      ..contactAddress2 = str("contactAddress2")
      ..contactCountry = str("contactCountry")
      ..contactPhone = str("contactPhone")
      ..website = str("website")
      ..portfolioUrl = str("portfolioUrl")
      ..linkedinUrl = str("linkedinUrl")
      ..githubUrl = str("githubUrl")
      ..links = ResumeItemUtil.listFromJson(json["links"], ResumeLinkItem.fromJson)
      ..currentCompany = str("currentCompany")
      ..currentDepartment = str("currentDepartment")
      ..currentJobTitle = str("currentJobTitle")
      ..currentOccupation = str("currentOccupation")
      ..desiredJobTitle = str("desiredJobTitle")
      ..desiredOccupation = str("desiredOccupation")
      ..desiredIndustry = str("desiredIndustry")
      ..desiredEmploymentType = str("desiredEmploymentType")
      ..desiredWorkLocation = str("desiredWorkLocation")
      ..currentSalary = str("currentSalary")
      ..desiredSalary = str("desiredSalary")
      ..availableStartDate = str("availableStartDate")
      ..educationItems = ResumeItemUtil.listFromJson(json["educationItems"], ResumeEducationItem.fromJson)
      ..workItems = ResumeItemUtil.listFromJson(json["workItems"], ResumeWorkItem.fromJson)
      ..skillItems = ResumeItemUtil.listFromJson(json["skillItems"], ResumeSkillItem.fromJson)
      ..certificationItems = ResumeItemUtil.listFromJson(json["certificationItems"], ResumeCertificationItem.fromJson)
      ..languageItems = ResumeItemUtil.listFromJson(json["languageItems"], ResumeLanguageItem.fromJson)
      ..projectItems = ResumeItemUtil.listFromJson(json["projectItems"], ResumeProjectItem.fromJson)
      ..awardItems = ResumeItemUtil.listFromJson(json["awardItems"], ResumeAwardItem.fromJson)
      ..professionalSummary = str("professionalSummary")
      ..careerSummary = str("careerSummary")
      ..objective = str("objective")
      ..motivation = str("motivation")
      ..selfPromotion = str("selfPromotion")
      ..strengths = str("strengths")
      ..weaknesses = str("weaknesses")
      ..managementExperience = str("managementExperience")
      ..technicalExperience = str("technicalExperience")
      ..businessExperience = str("businessExperience")
      ..industryExperience = str("industryExperience")
      ..hobbies = str("hobbies")
      ..interests = str("interests")
      ..specialSkills = str("specialSkills")
      ..nearestStation = str("nearestStation")
      ..commuteTime = str("commuteTime")
      ..commuteMethod = str("commuteMethod")
      ..dependents = ResumeItemUtil.number(json["dependents"])
      ..hasSpouse = ResumeItemUtil.flag(json["hasSpouse"])
      ..spouseSupportObligation = ResumeItemUtil.flag(json["spouseSupportObligation"])
      ..workingHoursPreference = str("workingHoursPreference")
      ..workingDaysPreference = str("workingDaysPreference")
      ..remoteWorkPreference = str("remoteWorkPreference")
      ..relocationPreference = str("relocationPreference")
      ..overtimePreference = str("overtimePreference")
      ..visaStatus = str("visaStatus")
      ..workAuthorization = str("workAuthorization")
      ..visaExpirationDate = str("visaExpirationDate")
      ..drivingLicense = str("drivingLicense")
      ..hasCar = ResumeItemUtil.flag(json["hasCar"])
      ..militaryService = str("militaryService")
      ..volunteerExperience = str("volunteerExperience")
      ..affiliations = str("affiliations")
      ..publications = str("publications")
      ..patents = str("patents")
      ..presentations = str("presentations")
      ..referenceItems = ResumeItemUtil.listFromJson(json["referenceItems"], ResumeReferenceItem.fromJson)
      ..requests = str("requests")
      ..additionalInformation = str("additionalInformation")
      ..note = str("note");
  }

  Map<String, dynamic> toJson() {
    return {
      'version': version,
      'createType': createType,
      'documentTitle': documentTitle,
      'documentDate': documentDate,
      'layoutType': layoutType,
      'themeColor': themeColor,
      'name': name,
      'nameReading': nameReading,
      'birthDate': birthDate,
      'gender': gender,
      'nationality': nationality,
      'photoImageBase64': photoImageBase64,
      'postalCode': postalCode,
      'prefecture': prefecture,
      'city': city,
      'address1': address1,
      'address2': address2,
      'country': country,
      'phone': phone,
      'mobile': mobile,
      'email': email,
      'useContactAddress': useContactAddress,
      'contactPostalCode': contactPostalCode,
      'contactPrefecture': contactPrefecture,
      'contactCity': contactCity,
      'contactAddress1': contactAddress1,
      'contactAddress2': contactAddress2,
      'contactCountry': contactCountry,
      'contactPhone': contactPhone,
      'website': website,
      'portfolioUrl': portfolioUrl,
      'linkedinUrl': linkedinUrl,
      'githubUrl': githubUrl,
      'links': links.map((item) => item.toJson()).toList(),
      'currentCompany': currentCompany,
      'currentDepartment': currentDepartment,
      'currentJobTitle': currentJobTitle,
      'currentOccupation': currentOccupation,
      'desiredJobTitle': desiredJobTitle,
      'desiredOccupation': desiredOccupation,
      'desiredIndustry': desiredIndustry,
      'desiredEmploymentType': desiredEmploymentType,
      'desiredWorkLocation': desiredWorkLocation,
      'currentSalary': currentSalary,
      'desiredSalary': desiredSalary,
      'availableStartDate': availableStartDate,
      'educationItems': educationItems.map((item) => item.toJson()).toList(),
      'workItems': workItems.map((item) => item.toJson()).toList(),
      'skillItems': skillItems.map((item) => item.toJson()).toList(),
      'certificationItems': certificationItems.map((item) => item.toJson()).toList(),
      'languageItems': languageItems.map((item) => item.toJson()).toList(),
      'projectItems': projectItems.map((item) => item.toJson()).toList(),
      'awardItems': awardItems.map((item) => item.toJson()).toList(),
      'professionalSummary': professionalSummary,
      'careerSummary': careerSummary,
      'objective': objective,
      'motivation': motivation,
      'selfPromotion': selfPromotion,
      'strengths': strengths,
      'weaknesses': weaknesses,
      'managementExperience': managementExperience,
      'technicalExperience': technicalExperience,
      'businessExperience': businessExperience,
      'industryExperience': industryExperience,
      'hobbies': hobbies,
      'interests': interests,
      'specialSkills': specialSkills,
      'nearestStation': nearestStation,
      'commuteTime': commuteTime,
      'commuteMethod': commuteMethod,
      'dependents': dependents,
      'hasSpouse': hasSpouse,
      'spouseSupportObligation': spouseSupportObligation,
      'workingHoursPreference': workingHoursPreference,
      'workingDaysPreference': workingDaysPreference,
      'remoteWorkPreference': remoteWorkPreference,
      'relocationPreference': relocationPreference,
      'overtimePreference': overtimePreference,
      'visaStatus': visaStatus,
      'workAuthorization': workAuthorization,
      'visaExpirationDate': visaExpirationDate,
      'drivingLicense': drivingLicense,
      'hasCar': hasCar,
      'militaryService': militaryService,
      'volunteerExperience': volunteerExperience,
      'affiliations': affiliations,
      'publications': publications,
      'patents': patents,
      'presentations': presentations,
      'referenceItems': referenceItems.map((item) => item.toJson()).toList(),
      'requests': requests,
      'additionalInformation': additionalInformation,
      'note': note,
    };
  }
```

### `define/resume_layout_type.dart` identifiers

```dart
enum ResumeTemplateCategory {
  resume,

  cv,

  creative,

  japanese;
```

### `data/entity/resume_award_item.dart`

```dart
  static ResumeAwardItem fromJson(Map<String, dynamic> json) {
    return ResumeAwardItem(
      id: ResumeItemUtil.str(json["id"]).isEmpty ? ResumeItemUtil.newId() : ResumeItemUtil.str(json["id"]),
      year: ResumeItemUtil.str(json["year"]),
      month: ResumeItemUtil.str(json["month"]),
      name: ResumeItemUtil.str(json["name"]),
      organization: ResumeItemUtil.str(json["organization"]),
      description: ResumeItemUtil.str(json["description"]),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "year": year,
      "month": month,
      "name": name,
      "organization": organization,
      "description": description,
    };
  }
```

### `data/entity/resume_certification_item.dart`

```dart
  static ResumeCertificationItem fromJson(Map<String, dynamic> json) {
    return ResumeCertificationItem(
      id: ResumeItemUtil.str(json["id"]).isEmpty ? ResumeItemUtil.newId() : ResumeItemUtil.str(json["id"]),
      year: ResumeItemUtil.str(json["year"]),
      month: ResumeItemUtil.str(json["month"]),
      name: ResumeItemUtil.str(json["name"]),
      organization: ResumeItemUtil.str(json["organization"]),
      credentialId: ResumeItemUtil.str(json["credentialId"]),
      credentialUrl: ResumeItemUtil.str(json["credentialUrl"]),
      expirationYear: ResumeItemUtil.str(json["expirationYear"]),
      expirationMonth: ResumeItemUtil.str(json["expirationMonth"]),
      description: ResumeItemUtil.str(json["description"]),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "year": year,
      "month": month,
      "name": name,
      "organization": organization,
      "credentialId": credentialId,
      "credentialUrl": credentialUrl,
      "expirationYear": expirationYear,
      "expirationMonth": expirationMonth,
      "description": description,
    };
  }
```

### `data/entity/resume_education_item.dart`

```dart
  static ResumeEducationItem fromJson(Map<String, dynamic> json) {
    return ResumeEducationItem(
      id: ResumeItemUtil.str(json["id"]).isEmpty ? ResumeItemUtil.newId() : ResumeItemUtil.str(json["id"]),
      startYear: ResumeItemUtil.str(json["startYear"]),
      startMonth: ResumeItemUtil.str(json["startMonth"]),
      endYear: ResumeItemUtil.str(json["endYear"]),
      endMonth: ResumeItemUtil.str(json["endMonth"]),
      schoolName: ResumeItemUtil.str(json["schoolName"]),
      faculty: ResumeItemUtil.str(json["faculty"]),
      department: ResumeItemUtil.str(json["department"]),
      course: ResumeItemUtil.str(json["course"]),
      degree: ResumeItemUtil.str(json["degree"]),
      major: ResumeItemUtil.str(json["major"]),
      status: ResumeItemUtil.str(json["status"]),
      description: ResumeItemUtil.str(json["description"]),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "startYear": startYear,
      "startMonth": startMonth,
      "endYear": endYear,
      "endMonth": endMonth,
      "schoolName": schoolName,
      "faculty": faculty,
      "department": department,
      "course": course,
      "degree": degree,
      "major": major,
      "status": status,
      "description": description,
    };
  }
```

### `data/entity/resume_language_item.dart`

```dart
  static ResumeLanguageItem fromJson(Map<String, dynamic> json) {
    return ResumeLanguageItem(
      id: ResumeItemUtil.str(json["id"]).isEmpty ? ResumeItemUtil.newId() : ResumeItemUtil.str(json["id"]),
      language: ResumeItemUtil.str(json["language"]),
      level: ResumeItemUtil.str(json["level"]),
      speakingLevel: ResumeItemUtil.str(json["speakingLevel"]),
      listeningLevel: ResumeItemUtil.str(json["listeningLevel"]),
      readingLevel: ResumeItemUtil.str(json["readingLevel"]),
      writingLevel: ResumeItemUtil.str(json["writingLevel"]),
      testName: ResumeItemUtil.str(json["testName"]),
      testScore: ResumeItemUtil.str(json["testScore"]),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "language": language,
      "level": level,
      "speakingLevel": speakingLevel,
      "listeningLevel": listeningLevel,
      "readingLevel": readingLevel,
      "writingLevel": writingLevel,
      "testName": testName,
      "testScore": testScore,
    };
  }
```

### `data/entity/resume_link_item.dart`

```dart
  static ResumeLinkItem fromJson(Map<String, dynamic> json) {
    return ResumeLinkItem(
      id: ResumeItemUtil.str(json["id"]).isEmpty ? ResumeItemUtil.newId() : ResumeItemUtil.str(json["id"]),
      title: ResumeItemUtil.str(json["title"]),
      url: ResumeItemUtil.str(json["url"]),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "title": title,
      "url": url,
    };
  }
```

### `data/entity/resume_profile.dart`

```dart
  static ResumeProfile fromJson(Map<String, dynamic> json) {
    String str(String key) => ResumeItemUtil.str(json[key]);
    return ResumeProfile(
      name: str("name"),
      nameReading: str("nameReading"),
      birthDate: str("birthDate"),
      gender: str("gender"),
      nationality: str("nationality"),
      photoImageBase64: str("photoImageBase64"),
      postalCode: str("postalCode"),
      prefecture: str("prefecture"),
      city: str("city"),
      address1: str("address1"),
      address2: str("address2"),
      country: str("country"),
      phone: str("phone"),
      mobile: str("mobile"),
      email: str("email"),
      website: str("website"),
      portfolioUrl: str("portfolioUrl"),
      linkedinUrl: str("linkedinUrl"),
      githubUrl: str("githubUrl"),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "name": name,
      "nameReading": nameReading,
      "birthDate": birthDate,
      "gender": gender,
      "nationality": nationality,
      "photoImageBase64": photoImageBase64,
      "postalCode": postalCode,
      "prefecture": prefecture,
      "city": city,
      "address1": address1,
      "address2": address2,
      "country": country,
      "phone": phone,
      "mobile": mobile,
      "email": email,
      "website": website,
      "portfolioUrl": portfolioUrl,
      "linkedinUrl": linkedinUrl,
      "githubUrl": githubUrl,
    };
  }

  static ResumeProfile fromJsonString(String jsonString) {
    if (jsonString.isEmpty) {
      return ResumeProfile.initEmpty();
    }

    try {
      final Map<dynamic, dynamic> dynamicMap = jsonDecode(jsonString) as Map<dynamic, dynamic>;
      return ResumeProfile.fromJson(dynamicMap.map((key, value) => MapEntry(key.toString(), value)));
    } catch (_) {
      return ResumeProfile.initEmpty();
    }
  }

  static String toJsonString(ResumeProfile profile) {
    return jsonEncode(profile.toJson());
  }
```

### `data/entity/resume_project_item.dart`

```dart
  static ResumeProjectItem fromJson(Map<String, dynamic> json) {
    return ResumeProjectItem(
      id: ResumeItemUtil.str(json["id"]).isEmpty ? ResumeItemUtil.newId() : ResumeItemUtil.str(json["id"]),
      name: ResumeItemUtil.str(json["name"]),
      startYear: ResumeItemUtil.str(json["startYear"]),
      startMonth: ResumeItemUtil.str(json["startMonth"]),
      endYear: ResumeItemUtil.str(json["endYear"]),
      endMonth: ResumeItemUtil.str(json["endMonth"]),
      role: ResumeItemUtil.str(json["role"]),
      organization: ResumeItemUtil.str(json["organization"]),
      description: ResumeItemUtil.str(json["description"]),
      achievements: ResumeItemUtil.str(json["achievements"]),
      technologies: ResumeItemUtil.str(json["technologies"]),
      url: ResumeItemUtil.str(json["url"]),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "name": name,
      "startYear": startYear,
      "startMonth": startMonth,
      "endYear": endYear,
      "endMonth": endMonth,
      "role": role,
      "organization": organization,
      "description": description,
      "achievements": achievements,
      "technologies": technologies,
      "url": url,
    };
  }
```

### `data/entity/resume_reference_item.dart`

```dart
  static ResumeReferenceItem fromJson(Map<String, dynamic> json) {
    return ResumeReferenceItem(
      id: ResumeItemUtil.str(json["id"]).isEmpty ? ResumeItemUtil.newId() : ResumeItemUtil.str(json["id"]),
      name: ResumeItemUtil.str(json["name"]),
      companyName: ResumeItemUtil.str(json["companyName"]),
      jobTitle: ResumeItemUtil.str(json["jobTitle"]),
      relationship: ResumeItemUtil.str(json["relationship"]),
      phone: ResumeItemUtil.str(json["phone"]),
      email: ResumeItemUtil.str(json["email"]),
      note: ResumeItemUtil.str(json["note"]),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "name": name,
      "companyName": companyName,
      "jobTitle": jobTitle,
      "relationship": relationship,
      "phone": phone,
      "email": email,
      "note": note,
    };
  }
```

### `data/entity/resume_skill_item.dart`

```dart
  static ResumeSkillItem fromJson(Map<String, dynamic> json) {
    return ResumeSkillItem(
      id: ResumeItemUtil.str(json["id"]).isEmpty ? ResumeItemUtil.newId() : ResumeItemUtil.str(json["id"]),
      name: ResumeItemUtil.str(json["name"]),
      category: ResumeItemUtil.str(json["category"]),
      level: ResumeItemUtil.str(json["level"]),
      yearsOfExperience: ResumeItemUtil.str(json["yearsOfExperience"]),
      description: ResumeItemUtil.str(json["description"]),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "name": name,
      "category": category,
      "level": level,
      "yearsOfExperience": yearsOfExperience,
      "description": description,
    };
  }
```

### `data/entity/resume_work_item.dart`

```dart
  static ResumeWorkItem fromJson(Map<String, dynamic> json) {
    return ResumeWorkItem(
      id: ResumeItemUtil.str(json["id"]).isEmpty ? ResumeItemUtil.newId() : ResumeItemUtil.str(json["id"]),
      startYear: ResumeItemUtil.str(json["startYear"]),
      startMonth: ResumeItemUtil.str(json["startMonth"]),
      endYear: ResumeItemUtil.str(json["endYear"]),
      endMonth: ResumeItemUtil.str(json["endMonth"]),
      isCurrent: ResumeItemUtil.flag(json["isCurrent"]),
      companyName: ResumeItemUtil.str(json["companyName"]),
      companyDescription: ResumeItemUtil.str(json["companyDescription"]),
      industry: ResumeItemUtil.str(json["industry"]),
      department: ResumeItemUtil.str(json["department"]),
      jobTitle: ResumeItemUtil.str(json["jobTitle"]),
      employmentType: ResumeItemUtil.str(json["employmentType"]),
      location: ResumeItemUtil.str(json["location"]),
      responsibilities: ResumeItemUtil.str(json["responsibilities"]),
      achievements: ResumeItemUtil.str(json["achievements"]),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "startYear": startYear,
      "startMonth": startMonth,
      "endYear": endYear,
      "endMonth": endMonth,
      "isCurrent": isCurrent,
      "companyName": companyName,
      "companyDescription": companyDescription,
      "industry": industry,
      "department": department,
      "jobTitle": jobTitle,
      "employmentType": employmentType,
      "location": location,
      "responsibilities": responsibilities,
      "achievements": achievements,
    };
  }
```
