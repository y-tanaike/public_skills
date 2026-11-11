# Mandala data and sharing URL

## Root cell JSON

Pass the center cell directly as the root object. Do not wrap it in `mandalaCell` or a file ID. See the [English example](../examples/sample.en.json) and [Japanese example](../examples/sample.ja.json).

The hierarchy has three levels: center, themes, and actions (depth 0–2). A cell may have at most eight children; actions cannot have children. The app pads missing trailing cells. Use `{}` to preserve an empty position in the middle. The 81-cell view repeats the center/themes; the input has at most 73 distinct cells (1 + 8 + 64).

| Key | Type or accepted values | Default |
|---|---|---|
| `title` | String; the center title must be nonempty | Empty for child cells |
| `description` | String for notes or explanation | Empty |
| `link` | Absolute `http://` or `https://` URL | No link |
| `color` | Six-digit `#RRGGBB` | Unspecified |
| `complete` | `initial`, `zero`, `quarter`, `half`, `three_quarters`, `completed` | `initial` |
| `childMandalaCellList` | Array of at most eight cells | Empty array |

Completion IDs mean unspecified, 0%, 25%, 50%, 75%, and 100%, respectively. The script rejects other keys and invalid types. Although the app can accept eight-digit colors and a wrapped storage format, this skill deliberately uses the subset above. Do not send `imageBase64`, `person`, `startDate`, `endDate`, or `id`.

## Position order

Child array indexes map to these positions around the center. The same mapping applies to a theme's action cells.

```text
5  2  6
1  C  3
4  0  7
```

Convert visual ordering to these indexes; do not assume the array runs clockwise from the top-left.

## URL parameters

- Web app: `https://goal.mandalachart.com/`
- `name`: File name; defaults to the center title.
- `content`: UTF-8 cell JSON, compressed with zlib, encoded as base64url without trailing `=`.
- `type`: `b_type` for the full 81-cell view (default), `a_type_root` for the center and eight themes, or `a_type_a` through `a_type_h` for the theme at array index 0–7 and its actions.
- `layout`: `minimum`, `simple` (default), or `normal`.

Display parameters do not modify saved settings. Keep the full URL at or below 8,000 characters. The app also accepts raw JSON in `content`, but use compression normally.

```bash
python3 scripts/create_url.py examples/sample.en.json --name 'Reading goals' --view b_type --layout simple
```

## Compatibility baseline

Checked against the app implementation on 2026-11-11. When updating, check URL encoding/decoding in `SharedContentCodec`, hierarchy normalization in `Content.tryFromSharedJson`, values in `MandalaCell.fromJson`, position mapping in `MandalaType.getRootXY` / `getATypeSubIndex`, and IDs in `MandalaLayoutType` / `CompleteType`. App source code is not needed to use this skill.
