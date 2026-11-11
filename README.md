# Skills for creating app content through URLs

English | [日本語](README.ja.md)

Create app content with an AI assistant and open it through a URL that embeds the content. Google Drive file creation, sharing, and permissions are outside this collection.

This collection covers all 71 apps with embedded-content sharing found in the local implementations checked on 2026-11-11. Web URLs are configured for 69 apps; two require a verified deployment URL. Apps without a receiving implementation are listed below. Prototypes, development samples, and duplicate older implementations are excluded.

## Language policy

Each app has one skill. Instructions, format references, and CLI help/errors use English. The assistant responds and generates content in the language explicitly requested by the user, or otherwise in the user's language. English instructions do not require English output.

Every app includes matching English and Japanese samples in `examples/sample.en.*` and `examples/sample.ja.*`. Translate display content, not JSON keys, IDs, enum values, code syntax, or date/number encodings. You do not need separate Japanese and English installations.

## Usage

Use the app directory as a skill and ask the assistant to follow its `SKILL.md`. Keep `scripts/`, `references/`, and `examples/` together. Each skill is self-contained and does not depend on its parent directory, an app checkout, or the author's local environment.

Example request: “Use the mandalachart skill to create reading goals in Japanese and return a URL that opens them.”

- `SKILL.md`: Workflow, language policy, and scope.
- `references/content-format.md`: App-specific data shapes, serialization definitions, identifiers, and date conversions.
- `examples/`: English and Japanese sample content.
- `scripts/create_url.py`: Offline URL generation and decoding, using Python 3.10+ and the standard library only.

```bash
python3 mandalachart/scripts/create_url.py mandalachart/examples/sample.en.json --name "Reading goals"
python3 shopcard/scripts/create_url.py shopcard/examples/sample.en.json --name "Shop card"
python3 markdown/scripts/create_url.py markdown/examples/sample.en.md --name "Reading group"
```

Successful stdout contains exactly one URL. Read the target skill's reference: some apps accept JSON while others accept plain text. To edit a link, decode it with `--decode-url`, edit the content, and generate a new URL.

## App catalog

Directory names follow the Flutter app ID in `pubspec.yaml`. For example, Mandala Goals uses `goal`, AI Mandala uses `ai`, Mandala Meeting Notes uses `giji`, and HTML Editor uses `shtml`. Source repository mappings and verification results are recorded in [apps.json](apps.json).

| App ID / skill | App | Input | Deployment |
|---|---|---|---|
| [ai](ai/SKILL.md) | AI Mandala | Mandala cell JSON | [Web app](https://ai.mandalachart.com/) |
| [album](album/SKILL.md) | Album | App-specific JSON | [Web app](https://album.tanaike.jp/) |
| [bulletsmind](bulletsmind/SKILL.md) | BulletsMind | App-specific JSON | [Web app](https://bullets-mind.tanaike.jp/) |
| [checksheet](checksheet/SKILL.md) | Checksheet | Whole-table JSON | [Web app](https://checksheet.tanaike.jp/) |
| [collage](collage/SKILL.md) | Collage | App-specific JSON | [Web app](https://collage.tanaike.jp/) |
| [cornell](cornell/SKILL.md) | Cornell Notes | App-specific JSON | [Web app](https://cornell.tanaike.jp/) |
| [correlation](correlation/SKILL.md) | Mermaid Correlation Diagram | Plain text | [Web app](https://correlation.tanaike.jp/) |
| [correlationai](correlationai/SKILL.md) | AI Correlation Diagram | App-specific JSON | [Web app](https://correlationai.tanaike.jp/) |
| [customer](customer/SKILL.md) | Customer Manager | App-specific JSON | [Web app](https://customer.tanaike.jp/) |
| [delivery](delivery/SKILL.md) | Delivery Note | App-specific JSON | [Web app](https://delivery.tanaike.jp/) |
| [document](document/SKILL.md) | Rich Text Document | App-specific JSON | [Web app](https://document.tanaike.jp/) |
| [er](er/SKILL.md) | ER Diagram | Plain text | [Web app](https://er.tanaike.jp/) |
| [expence](expence/SKILL.md) | Expense Manager | App-specific JSON | [Web app](https://expence.tanaike.jp/) |
| [faq](faq/SKILL.md) | FAQ | App-specific JSON | [Web app](https://faq.tanaike.jp/) |
| [flowchart](flowchart/SKILL.md) | Mermaid Flowchart | Plain text | [Web app](https://flowchart.tanaike.jp/) |
| [flowchartai](flowchartai/SKILL.md) | AI Flowchart | App-specific JSON | [Web app](https://flowchartai.tanaike.jp/) |
| [ganttchart](ganttchart/SKILL.md) | Gantt Chart | App-specific JSON | [Web app](https://ganttchart.tanaike.jp/) |
| [ganttchartai](ganttchartai/SKILL.md) | AI Gantt Chart | App-specific JSON | [Web app](https://ganttchartai.tanaike.jp/) |
| [giji](giji/SKILL.md) | Mandala Meeting Notes | Mandala cell JSON | [Web app](https://giji.mandalachart.com/) |
| [goal](goal/SKILL.md) | Mandala Goals | Mandala cell JSON | [Web app](https://goal.mandalachart.com/) |
| [graph](graph/SKILL.md) | Graph | App-specific JSON | [Web app](https://graph.tanaike.jp/) |
| [htmlai](htmlai/SKILL.md) | AI HTML Editor | Plain text | [Web app](https://htmlai.tanaike.jp/) |
| [htmlslide](htmlslide/SKILL.md) | HTML Slides | App-specific JSON | [Web app](https://htmlslide.tanaike.jp/) |
| [inknote](inknote/SKILL.md) | Ink Note | App-specific JSON | [Web app](https://inknote.tanaike.jp/) |
| [invitation](invitation/SKILL.md) | Invitation | App-specific JSON | [Web app](https://invitation.tanaike.jp/) |
| [invoice](invoice/SKILL.md) | Invoice | App-specific JSON | [Web app](https://invoice.tanaike.jp/) |
| [javascript](javascript/SKILL.md) | JavaScript Editor | Plain text | [Web app](https://javascript.tanaike.jp/) |
| [leaflet](leaflet/SKILL.md) | Flyer | App-specific JSON | [Web app](https://leaflet.tanaike.jp/) |
| [led](led/SKILL.md) | LED Board | App-specific JSON | [Web app](https://led.tanaike.jp/) |
| [mandalachart](mandalachart/SKILL.md) | Mandala Manager | Mandala cell JSON | [Web app](https://app.mandalachart.com/) |
| [markdown](markdown/SKILL.md) | Markdown Editor | Plain text | [Web app](https://markdown.tanaike.jp/) |
| [marpai](marpai/SKILL.md) | AI Marp Slides | App-specific JSON | [Web app](https://marpai.tanaike.jp/) |
| [marpslide](marpslide/SKILL.md) | Marp Slides | App-specific JSON | [Web app](https://marpslide.tanaike.jp/) |
| [matchtable](matchtable/SKILL.md) | Match Table | App-specific JSON | [Web app](https://matchtable.tanaike.jp/) |
| [meishi](meishi/SKILL.md) | Business Card | App-specific JSON | [Web app](https://meishi.tanaike.jp/) |
| [menu](menu/SKILL.md) | Menu | App-specific JSON | [Web app](https://menu.tanaike.jp/) |
| [newspaper](newspaper/SKILL.md) | Newspaper | App-specific JSON | [Web app](https://newspaper.tanaike.jp/) |
| [orderform](orderform/SKILL.md) | Purchase Order | App-specific JSON | [Web app](https://orderform.tanaike.jp/) |
| [orderslip](orderslip/SKILL.md) | Order Slip | App-specific JSON | [Web app](https://orderslip.tanaike.jp/) |
| [outlineai](outlineai/SKILL.md) | AI Outline | App-specific JSON | [Web app](https://outlineai.tanaike.jp/) |
| [paycheck](paycheck/SKILL.md) | Payslip | App-specific JSON | [Web app](https://paycheck.tanaike.jp/) |
| [pixelart](pixelart/SKILL.md) | Pixel Art | App-specific JSON | [Web app](https://pixelart.tanaike.jp/) |
| [pos](pos/SKILL.md) | Point of Sale | App-specific JSON | [Web app](https://pos.tanaike.jp/) |
| [posecraft](posecraft/SKILL.md) | PoseCraft | App-specific JSON | [Web app](https://posecraft.tanaike.jp/) |
| [python](python/SKILL.md) | Python Editor | Plain text | [Web app](https://python.tanaike.jp/) |
| [quote](quote/SKILL.md) | Quote | App-specific JSON | [Web app](https://quote.tanaike.jp/) |
| [receipt](receipt/SKILL.md) | Receipt | App-specific JSON | [Web app](https://receipt.tanaike.jp/) |
| [requirement](requirement/SKILL.md) | Requirements | App-specific JSON | [Web app](https://requirement.tanaike.jp/) |
| [resume](resume/SKILL.md) | Resume | App-specific JSON | [Web app](https://resume.tanaike.jp/) |
| [rust](rust/SKILL.md) | Rust Editor | Plain text | **Verified deployment required** |
| [sales](sales/SKILL.md) | Sales Manager | App-specific JSON | [Web app](https://sales.tanaike.jp/) |
| [sequenceflow](sequenceflow/SKILL.md) | Sequence Diagram | Plain text | [Web app](https://sequenceflow.tanaike.jp/) |
| [shift](shift/SKILL.md) | Shift Schedule | App-specific JSON | [Web app](https://shift.tanaike.jp/) |
| [shopcard](shopcard/SKILL.md) | Shop Card | App-specific JSON | [Web app](https://shopcard.tanaike.jp/) |
| [shtml](shtml/SKILL.md) | HTML Editor | Plain text | [Web app](https://html.tanaike.jp/) |
| [simplecorrelation](simplecorrelation/SKILL.md) | Simple Correlation Diagram | App-specific JSON | [Web app](https://simplecorrelation.tanaike.jp/) |
| [simpleflowchart](simpleflowchart/SKILL.md) | Simple Flowchart | App-specific JSON | [Web app](https://simpleflowchart.tanaike.jp/) |
| [slide](slide/SKILL.md) | Slides | App-specific JSON | [Web app](https://slide.tanaike.jp/) |
| [slideai](slideai/SKILL.md) | AI Slides | App-specific JSON | [Web app](https://slideai.tanaike.jp/) |
| [solopodcast](solopodcast/SKILL.md) | Solo Podcast | App-specific JSON | **Verified deployment required** |
| [spreadsheet](spreadsheet/SKILL.md) | Spreadsheet | Whole-table JSON | [Web app](https://spreadsheet.tanaike.jp/) |
| [spreadsheetai](spreadsheetai/SKILL.md) | AI Spreadsheet | Whole-table JSON | [Web app](https://spreadsheetai.tanaike.jp/) |
| [stamp](stamp/SKILL.md) | Stamp Card | App-specific JSON | [Web app](https://stamp.tanaike.jp/) |
| [stock](stock/SKILL.md) | Stock Manager | App-specific JSON | [Web app](https://stock.tanaike.jp/) |
| [timeline](timeline/SKILL.md) | Timeline | App-specific JSON | [Web app](https://timeline.tanaike.jp/) |
| [timetable](timetable/SKILL.md) | Timetable | App-specific JSON | [Web app](https://timetable.tanaike.jp/) |
| [tournament](tournament/SKILL.md) | Tournament | App-specific JSON | [Web app](https://tournament.tanaike.jp/) |
| [trip](trip/SKILL.md) | Trip Planner | App-specific JSON | [Web app](https://trip.tanaike.jp/) |
| [typescript](typescript/SKILL.md) | TypeScript Editor | Plain text | [Web app](https://typescript.tanaike.jp/) |
| [visualizeai](visualizeai/SKILL.md) | Visualize AI | App-specific JSON | [Web app](https://visualizeai.tanaike.jp/) |
| [zukai](zukai/SKILL.md) | AI Diagram | Plain text | [Web app](https://zukai.tanaike.jp/) |

Rust Editor and Solo Podcast have no configured `webVersionUrl`. Use `--base-url https://your-verified-deployment/` only when the deployment is known. Do not infer a domain from the app ID.

## Persistence and content limits

Opening a URL creates an unsaved, editable preview. It does not create a persistent file or confirm a save. The user can import the preview in the app. Generating a new URL does not update an earlier link or saved file.

Image files, Base64 image attachments, local recordings, and other local attachments are excluded. Album and Collage can share photo slots, headings, and captions. Pixel-art colors and handwriting point arrays are supported JSON content. Referencing an external image in HTML or Markdown does not embed that image file into the URL.

The tool encodes UTF-8 text or JSON using zlib and base64url in the `content` parameter. Compression is not encryption. URLs longer than 8,000 characters are rejected without silently removing fields.

## Verification

```bash
python3 tools/verify_skills.py
python3 -m unittest discover -s tools -p "test_*.py"
python3 -m unittest discover -s mandalachart/scripts -p "test_*.py"
```

The verifier checks URL round trips and lengths, sample structure and protocol values across languages, and reference links for all 142 samples across 71 apps. Additional tests check Unicode/newlines, false/zero preservation, duplicate JSON keys, oversized content, invalid compressed data, out-of-range table cells, and unconfigured deployments.

English and Japanese samples are also tested against each app's local Flutter receiving code. This does not verify the currently deployed web UI, rendering, importing, or persistence. See `validation` in [apps.json](apps.json) for the recorded results.

## Apps without embedded-content URL receiving

The following implementations cannot yet open embedded-content URLs. App-side work is required, so no skill promises a working link for these apps. Google Drive sharing is not used as a substitute.

| App ID | Source repository | Status |
|---|---|---|
| `analysis` | `analysis/analysis-flutter` | Embedded-content URL receiving is not implemented. |
| `blockdoceditor` | `blockdoceditor/blockdoceditor` | Embedded-content URL receiving is not implemented. |
| `diary` | `diary/diary-flutter` | Embedded-content URL receiving is not implemented. |
| `diaryai` | `diaryai/diaryai-flutter` | Embedded-content URL receiving is not implemented. |
| `funnews` | `FunNews/funnews-flutter` | Embedded-content URL receiving is not implemented. |
| `gift` | `gift-ai/gift-ai-flutter` | Embedded-content URL receiving is not implemented. |
| `heatspotmap` | `heatspotmap/beeftongue-flutter` | Embedded-content URL receiving is not implemented. |
| `idea` | `idea-creator/idea-creator-flutter` | Embedded-content URL receiving is not implemented. |
| `keyword` | `keyword/keyword-flutter` | Embedded-content URL receiving is not implemented. |
| `life` | `mandala-life/mandala-life-flutter` | Embedded-content URL receiving is not implemented. |
| `mlb` | `mlb/mlb-flutter` | Embedded-content URL receiving is not implemented. |
| `review` | `review_replyer/review_replyer_flutter` | Embedded-content URL receiving is not implemented. |
| `story` | `story/story-flutter` | Embedded-content URL receiving is not implemented. |
