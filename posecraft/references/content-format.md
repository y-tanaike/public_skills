# Content format

- App ID: `posecraft`
- `content`: The app-specific JSON below, encoded as UTF-8, compressed with zlib, then encoded as base64url without trailing `=`.
- `name`: File name, not a Google Drive file ID.
- Use the same root shape as the [English example](../examples/sample.en.json) or [Japanese example](../examples/sample.ja.json). Do not add an outer file-name or storage wrapper.
- Include actual content or items. Format metadata alone or unknown fields alone may be rejected by the app.

Use a bundled `modelId`; do not embed GLB files. Follow the example and conversion definitions for bone keys, rotation units, and numeric arrays. Humanoid and quadruped models use different rigs.

## Root keys

| Key | JSON type |
|---|---|
| `camera` | See conversion definitions below |
| `light` | See conversion definitions below |
| `modelId` | string |
| `pose` | object |
| `version` | integer |

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
      if (json.trim().isEmpty) {
        return Content();
      }
      final Map<String, dynamic> decodedJson = jsonDecode(json) as Map<String, dynamic>;
      return fromMap(decodedJson);
    } catch (e) {
      logger.e("error fromJson: $e");
      return Content();
    }
  }

  static Content fromMap(Map<String, dynamic> decodedJson) {
    final Content content = Content();
    content.version = JsonUtil.toInt(decodedJson['version'], currentVersion);
    content.modelId = PoseModelType.fromId(decodedJson['modelId'] as String? ?? '').id;
    content.pose = parsePose(decodedJson['pose'], content.rigType);
    final Object? cameraJson = decodedJson['camera'];
    content.camera = cameraJson is Map<String, dynamic> ? CameraSetting.fromJson(cameraJson) : null;
    final Object? lightJson = decodedJson['light'];
    content.light = lightJson is Map<String, dynamic> ? LightSetting.fromJson(lightJson) : LightSetting.defaultSetting;
    content.extraMap = <String, dynamic>{
      for (final MapEntry<String, dynamic> entry in decodedJson.entries)
        if (!_knownKeySet.contains(entry.key)) entry.key: entry.value,
    };
    return content;
  }

  static Map<String, PoseBoneTransform> parsePose(Object? poseJson, PoseRigType rigType) {
    return <String, PoseBoneTransform>{
      ...buildInitialPose(rigType),
      ...parsePoseUpdate(poseJson, rigType),
    };
  }

  static Map<String, PoseBoneTransform> parsePoseUpdate(Object? poseJson, PoseRigType rigType) {
    final Map<String, PoseBoneTransform> pose = <String, PoseBoneTransform>{};
    if (poseJson is! Map) {
      return pose;
    }
    poseJson.forEach((Object? key, Object? value) {
      final String boneKey = key?.toString() ?? '';
      if (!rigType.isValidBoneKey(boneKey)) {
        logger.d("parsePoseUpdate skip bone not in ${rigType.name}: $boneKey");
        return;
      }
      if (value is Map) {
        pose[boneKey] = PoseBoneTransform.fromJson(Map<String, dynamic>.from(value));
      } else if (value is List) {
        pose[boneKey] = PoseBoneTransform.fromRotationJson(value);
      }
    });
    return pose;
  }

  Map<String, dynamic> poseToJson() {
    return <String, dynamic>{
      for (final MapEntry<String, PoseBoneTransform> entry in pose.entries) entry.key: entry.value.toJson(),
    };
  }

  Map<String, dynamic> poseToCompactJson() {
    return <String, dynamic>{
      for (final MapEntry<String, PoseBoneTransform> entry in pose.entries)
        if (!entry.value.isZero) entry.key: entry.value.toJson(),
    };
  }

  Map<String, dynamic> toJson() {
    final CameraSetting? currentCamera = camera;
    return <String, dynamic>{
      ...extraMap,
      'version': version,
      'modelId': modelId,
      'pose': poseToJson(),
      if (currentCamera != null) 'camera': currentCamera.toJson(),
      if (!light.isDefault) 'light': light.toJson(),
    };
  }
```

### `define/pose_bone.dart` identifiers

```dart
enum PoseBone {
  hips('hips', PoseBoneGroup.body),
  spine('spine', PoseBoneGroup.body),
  chest('chest', PoseBoneGroup.body),
  upperChest('upperChest', PoseBoneGroup.body),
  neck('neck', PoseBoneGroup.body),
  head('head', PoseBoneGroup.body),

  leftShoulder('leftShoulder', PoseBoneGroup.leftArm),
  leftUpperArm('leftUpperArm', PoseBoneGroup.leftArm),
  leftLowerArm('leftLowerArm', PoseBoneGroup.leftArm),
  leftHand('leftHand', PoseBoneGroup.leftArm),

  rightShoulder('rightShoulder', PoseBoneGroup.rightArm),
  rightUpperArm('rightUpperArm', PoseBoneGroup.rightArm),
  rightLowerArm('rightLowerArm', PoseBoneGroup.rightArm),
  rightHand('rightHand', PoseBoneGroup.rightArm),

  leftUpperLeg('leftUpperLeg', PoseBoneGroup.leftLeg),
  leftLowerLeg('leftLowerLeg', PoseBoneGroup.leftLeg),
  leftFoot('leftFoot', PoseBoneGroup.leftLeg),

  rightUpperLeg('rightUpperLeg', PoseBoneGroup.rightLeg),
  rightLowerLeg('rightLowerLeg', PoseBoneGroup.rightLeg),
  rightFoot('rightFoot', PoseBoneGroup.rightLeg),

  leftThumb1('leftThumb1', PoseBoneGroup.leftFingers, finger: PoseFinger.thumb, fingerJoint: 1),
  leftThumb2('leftThumb2', PoseBoneGroup.leftFingers, finger: PoseFinger.thumb, fingerJoint: 2),
  leftThumb3('leftThumb3', PoseBoneGroup.leftFingers, finger: PoseFinger.thumb, fingerJoint: 3),
  leftIndex1('leftIndex1', PoseBoneGroup.leftFingers, finger: PoseFinger.indexFinger, fingerJoint: 1),
  leftIndex2('leftIndex2', PoseBoneGroup.leftFingers, finger: PoseFinger.indexFinger, fingerJoint: 2),
  leftIndex3('leftIndex3', PoseBoneGroup.leftFingers, finger: PoseFinger.indexFinger, fingerJoint: 3),
  leftMiddle1('leftMiddle1', PoseBoneGroup.leftFingers, finger: PoseFinger.middle, fingerJoint: 1),
  leftMiddle2('leftMiddle2', PoseBoneGroup.leftFingers, finger: PoseFinger.middle, fingerJoint: 2),
  leftMiddle3('leftMiddle3', PoseBoneGroup.leftFingers, finger: PoseFinger.middle, fingerJoint: 3),
  leftRing1('leftRing1', PoseBoneGroup.leftFingers, finger: PoseFinger.ring, fingerJoint: 1),
  leftRing2('leftRing2', PoseBoneGroup.leftFingers, finger: PoseFinger.ring, fingerJoint: 2),
  leftRing3('leftRing3', PoseBoneGroup.leftFingers, finger: PoseFinger.ring, fingerJoint: 3),
  leftLittle1('leftLittle1', PoseBoneGroup.leftFingers, finger: PoseFinger.little, fingerJoint: 1),
  leftLittle2('leftLittle2', PoseBoneGroup.leftFingers, finger: PoseFinger.little, fingerJoint: 2),
  leftLittle3('leftLittle3', PoseBoneGroup.leftFingers, finger: PoseFinger.little, fingerJoint: 3),

  rightThumb1('rightThumb1', PoseBoneGroup.rightFingers, finger: PoseFinger.thumb, fingerJoint: 1),
  rightThumb2('rightThumb2', PoseBoneGroup.rightFingers, finger: PoseFinger.thumb, fingerJoint: 2),
  rightThumb3('rightThumb3', PoseBoneGroup.rightFingers, finger: PoseFinger.thumb, fingerJoint: 3),
  rightIndex1('rightIndex1', PoseBoneGroup.rightFingers, finger: PoseFinger.indexFinger, fingerJoint: 1),
  rightIndex2('rightIndex2', PoseBoneGroup.rightFingers, finger: PoseFinger.indexFinger, fingerJoint: 2),
  rightIndex3('rightIndex3', PoseBoneGroup.rightFingers, finger: PoseFinger.indexFinger, fingerJoint: 3),
  rightMiddle1('rightMiddle1', PoseBoneGroup.rightFingers, finger: PoseFinger.middle, fingerJoint: 1),
  rightMiddle2('rightMiddle2', PoseBoneGroup.rightFingers, finger: PoseFinger.middle, fingerJoint: 2),
  rightMiddle3('rightMiddle3', PoseBoneGroup.rightFingers, finger: PoseFinger.middle, fingerJoint: 3),
  rightRing1('rightRing1', PoseBoneGroup.rightFingers, finger: PoseFinger.ring, fingerJoint: 1),
  rightRing2('rightRing2', PoseBoneGroup.rightFingers, finger: PoseFinger.ring, fingerJoint: 2),
  rightRing3('rightRing3', PoseBoneGroup.rightFingers, finger: PoseFinger.ring, fingerJoint: 3),
  rightLittle1('rightLittle1', PoseBoneGroup.rightFingers, finger: PoseFinger.little, fingerJoint: 1),
  rightLittle2('rightLittle2', PoseBoneGroup.rightFingers, finger: PoseFinger.little, fingerJoint: 2),
  rightLittle3('rightLittle3', PoseBoneGroup.rightFingers, finger: PoseFinger.little, fingerJoint: 3),

  tail1('tail1', PoseBoneGroup.tail),
  tail2('tail2', PoseBoneGroup.tail),

  leftFrontUpperLeg('leftFrontUpperLeg', PoseBoneGroup.leftFrontLeg),
  leftFrontLowerLeg('leftFrontLowerLeg', PoseBoneGroup.leftFrontLeg),
  leftFrontPaw('leftFrontPaw', PoseBoneGroup.leftFrontLeg),

  rightFrontUpperLeg('rightFrontUpperLeg', PoseBoneGroup.rightFrontLeg),
  rightFrontLowerLeg('rightFrontLowerLeg', PoseBoneGroup.rightFrontLeg),
  rightFrontPaw('rightFrontPaw', PoseBoneGroup.rightFrontLeg),

  leftHindUpperLeg('leftHindUpperLeg', PoseBoneGroup.leftHindLeg),
  leftHindLowerLeg('leftHindLowerLeg', PoseBoneGroup.leftHindLeg),
  leftHindPaw('leftHindPaw', PoseBoneGroup.leftHindLeg),

  rightHindUpperLeg('rightHindUpperLeg', PoseBoneGroup.rightHindLeg),
  rightHindLowerLeg('rightHindLowerLeg', PoseBoneGroup.rightHindLeg),
  rightHindPaw('rightHindPaw', PoseBoneGroup.rightHindLeg);
```

### `define/pose_model_type.dart` identifiers

```dart
enum PoseModelType {
  humanFemale('human_female', PoseRigType.humanoid),
  humanMale('human_male', PoseRigType.humanoid),
  humanChild('human_child', PoseRigType.humanoid),

  mannequin('mannequin', PoseRigType.humanoid),

  dog('dog', PoseRigType.quadruped),
  sheep('sheep', PoseRigType.quadruped),
  pig('pig', PoseRigType.quadruped),
  cow('cow', PoseRigType.quadruped),
  horse('horse', PoseRigType.quadruped),
  zebra('zebra', PoseRigType.quadruped),
  llama('llama', PoseRigType.quadruped);
```

### `define/pose_rig_type.dart` identifiers

```dart
enum PoseRigType {
  humanoid,

  quadruped;
```

### `data/entity/camera_setting.dart`

```dart
  static CameraSetting fromJson(Map<String, dynamic> json) {
    return CameraSetting(
      position: JsonUtil.toVector3(json['position'], fallback.position),
      target: JsonUtil.toVector3(json['target'], fallback.target),
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{'position': position, 'target': target};
  }
```

### `data/entity/light_setting.dart`

```dart
  static LightSetting fromJson(Map<String, dynamic> json) {
    return LightSetting(
      intensity: _clamp(
        JsonUtil.toDouble(json['intensity'], defaultSetting.intensity),
        minIntensity,
        maxIntensity,
      ),
      azimuthDegree: _clamp(
        JsonUtil.toDouble(json['azimuth'], defaultSetting.azimuthDegree),
        minAzimuthDegree,
        maxAzimuthDegree,
      ),
      elevationDegree: _clamp(
        JsonUtil.toDouble(json['elevation'], defaultSetting.elevationDegree),
        minElevationDegree,
        maxElevationDegree,
      ),
      ambient: _clamp(JsonUtil.toDouble(json['ambient'], defaultSetting.ambient), minAmbient, maxAmbient),
    );
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'intensity': intensity,
      'azimuth': azimuthDegree,
      'elevation': elevationDegree,
      'ambient': ambient,
    };
  }
```

### `data/entity/pose_bone_transform.dart`

```dart
  static PoseBoneTransform fromJson(Map<String, dynamic> json) {
    return PoseBoneTransform(rotation: JsonUtil.toVector3(json['rotation'], _zeroRotation));
  }

  static PoseBoneTransform fromRotationJson(Object? rotationJson) {
    return PoseBoneTransform(rotation: JsonUtil.toVector3(rotationJson, _zeroRotation));
  }

  Map<String, dynamic> toJson() {
    return <String, dynamic>{'rotation': rotation};
  }
```
