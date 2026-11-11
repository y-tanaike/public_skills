# ガントチャート・図解・文書などの内容を作成するAI Skills

[English](README.md) | 日本語

棚池祐樹が提供する、ガントチャート・マインドマップ・図解・名刺などのアプリ向けAI Skillsです。各Skillに手順・データ仕様・サンプル・オフラインでのURL生成ツールをまとめています。

内容をURLへ埋め込み、各アプリで開くためのSkill集です。Google Drive上のファイル作成・共有・権限設定は対象外です。

2026-11-11時点のローカル実装を調査し、内容埋め込み共有を持つ全71アプリを収録しています。69アプリはWeb版URLの定義あり、2アプリは配信先の指定が必要です。受信機能が未実装のアプリは末尾にまとめています。開発用サンプル・試作・同一アプリの旧版リポジトリは重複収録していません。

## 作りたいものから探す

- **ガントチャート・工程表：** [iGanttChartの使い方](ganttchart/README.ja.md)、[AI Gantt Chart](ganttchartai/SKILL.md)
- **マインドマップ・目標：** [BulletsMind](bulletsmind/SKILL.md)、[Mandala Manager](mandalachart/SKILL.md)
- **フローチャート・図解：** [Simple Flowchart](simpleflowchart/SKILL.md)、[ER図](er/SKILL.md)、[シーケンス図](sequenceflow/SKILL.md)
- **カード・印刷物：** [名刺](meishi/SKILL.md)、[ショップカード](shopcard/SKILL.md)、[チラシ](leaflet/SKILL.md)
- **文書・スライド：** [Markdown Editor](markdown/SKILL.md)、[要件定義](requirement/SKILL.md)、[Slides](slide/SKILL.md)
- **表・予定表：** [スプレッドシート](spreadsheet/SKILL.md)、[シフト表](shift/SKILL.md)、[時間割](timetable/SKILL.md)

[開発者について](https://tanaike.jp/profile?hl=ja) · [アプリ一覧](https://tanaike.jp/?hl=ja)

## 言語の扱い

各アプリのSkill・仕様書・CLIのヘルプ／エラーは英語を基準にしています。Skillはユーザーが指定した言語で応答・生成し、指定がなければユーザーの言語を使います。日本語の依頼には日本語の内容を生成します。JSONキー・ID・列挙値などの技術的な値は翻訳しません。

`examples/sample.en.*` と `examples/sample.ja.*` に同じ構成の日英サンプルを同梱しています。言語別のSkillを二重にインストールする必要はありません。

## 会話で作りたいものを形にする

最初から仕様を完成させる必要はありません。「来月のWebサイト公開までの工程表を作りたい。足りない情報は質問して」と伝えて始められます。AIの質問に答え、「実装をもっと細かく分けて」「確認の期間を1週間長くして」などと会話で調整し、まとまったらアプリで開けるURLを返してもらいます。

### まずはSkillを追加せずに試す

作りたいものと一緒に、対象アプリの手順URLをプロンプトへ貼り付けます。リンク先のデータ仕様とURL生成ツールも参照するよう伝えてください。iGanttChartの場合は、次のように依頼できます。

> https://github.com/y-tanaike/public_skills/blob/main/ganttchart/SKILL.md の手順と、そこからリンクされているデータ仕様・URL生成ツールを参照してください。来月のWebサイト公開に向けたガントチャートを作りたいです。足りない情報は質問しながら、会話でタスクと日程を整理してください。工程名は日本語にして、まとまったらiGanttChartで開けるURLを返してください。

手順の本文を直接貼り付ける方法もあります。この方法ではSkillのインストールは不要です。他のアプリでは、下の一覧にある対象の `SKILL.md` のURLを使ってください。

URL生成には、手順・参照ファイルの取得と、Pythonなどのコード実行に対応したAI環境を使ってください。URLを参照できない場合は、手順と参照先のファイルを直接渡します。URLを貼ることで閲覧機能や実行機能が追加されるわけではありません。

### 繰り返し使うならSkillを導入する

Skillに対応したAI環境に、対象アプリのディレクトリを `SKILL.md`・`scripts/`・`references/`・`examples/` ごと追加します。導入方法は環境によって異なります。導入して利用可能になった後は、次のように依頼できます。

> ganttchartのSkillを使って、来月のWebサイト公開までの計画を一緒に整理してください。足りない情報は質問して、iGanttChartで開けるURLを返してください。

毎回手順の全文やURLを貼り付ける手間を省き、作りたいものを会話で伝えられます。Skillが自動で選ばれない環境では、使うSkillの名前も明示してください。

## 使い方

目的のアプリのディレクトリをSkillとして利用し、`SKILL.md` を読ませて依頼します。各ディレクトリは単独で利用でき、親ディレクトリやアプリのソースコードに依存しません。`scripts`・`references`・`examples` を含めて配置してください。

例: 「`mandalachart` のSkillを使って、読書を習慣にするマンダラを作り、開けるURLを返してください」。

- `SKILL.md`: 作成・修正の手順と対象範囲。
- `references/content-format.md`: アプリ固有のデータ形式。JSON型では変換定義・列挙値・日付形式を同梱。
- `examples/`: 実際に生成できるサンプル。
- `scripts/create_url.py`: URL生成・復号。Python 3.10以降の標準ライブラリのみ。

```bash
python3 mandalachart/scripts/create_url.py mandalachart/examples/sample.ja.json --name "読書の目標"
python3 shopcard/scripts/create_url.py shopcard/examples/sample.ja.json --name "お店のカード"
python3 markdown/scripts/create_url.py markdown/examples/sample.ja.md --name "読書会"
```

標準出力に共有URLを1行返します。JSON型と本文型は入力が異なるため、必ず対象Skillの仕様を確認してください。既存URLの修正は `--decode-url` で内容を戻し、編集後に新しいURLを作ります。

## 対応アプリ一覧

ディレクトリ名には原則としてFlutterの `pubspec.yaml` のアプリIDを使います。例: マンダラ目標=`goal`、AIマンダラ=`ai`、マンダラ議事録=`giji`、HTML編集=`shtml`。元のリポジトリとの対応は [apps.json](apps.json) に記録しています。

| アプリID・Skill | アプリ | 入力形式 | 配信先 |
|---|---|---|---|
| [ai](ai/SKILL.md) | AIマンダラ | マンダラのセルJSON | [Web版](https://ai.mandalachart.com/) |
| [album](album/SKILL.md) | アルバム | アプリ専用JSON | [Web版](https://album.tanaike.jp/) |
| [bulletsmind](bulletsmind/SKILL.md) | BulletsMind（階層アウトライン） | アプリ専用JSON | [Web版](https://bullets-mind.tanaike.jp/) |
| [checksheet](checksheet/SKILL.md) | チェックシート | 表全体のJSON | [Web版](https://checksheet.tanaike.jp/) |
| [collage](collage/SKILL.md) | コラージュ | アプリ専用JSON | [Web版](https://collage.tanaike.jp/) |
| [cornell](cornell/SKILL.md) | コーネル式ノート | アプリ専用JSON | [Web版](https://cornell.tanaike.jp/) |
| [correlation](correlation/SKILL.md) | Mermaid相関図 | 本文テキスト | [Web版](https://correlation.tanaike.jp/) |
| [correlationai](correlationai/SKILL.md) | AI相関図 | アプリ専用JSON | [Web版](https://correlationai.tanaike.jp/) |
| [customer](customer/SKILL.md) | 顧客管理 | アプリ専用JSON | [Web版](https://customer.tanaike.jp/) |
| [delivery](delivery/SKILL.md) | 納品書 | アプリ専用JSON | [Web版](https://delivery.tanaike.jp/) |
| [document](document/SKILL.md) | リッチテキスト文書 | アプリ専用JSON | [Web版](https://document.tanaike.jp/) |
| [er](er/SKILL.md) | ER図 | 本文テキスト | [Web版](https://er.tanaike.jp/) |
| [expence](expence/SKILL.md) | 経費管理 | アプリ専用JSON | [Web版](https://expence.tanaike.jp/) |
| [faq](faq/SKILL.md) | FAQ作成 | アプリ専用JSON | [Web版](https://faq.tanaike.jp/) |
| [flowchart](flowchart/SKILL.md) | Mermaidフローチャート | 本文テキスト | [Web版](https://flowchart.tanaike.jp/) |
| [flowchartai](flowchartai/SKILL.md) | AIフローチャート | アプリ専用JSON | [Web版](https://flowchartai.tanaike.jp/) |
| [ganttchart](ganttchart/SKILL.md) | ガントチャート | アプリ専用JSON | [Web版](https://ganttchart.tanaike.jp/) |
| [ganttchartai](ganttchartai/SKILL.md) | AIガントチャート | アプリ専用JSON | [Web版](https://ganttchartai.tanaike.jp/) |
| [giji](giji/SKILL.md) | マンダラ議事録 | マンダラのセルJSON | [Web版](https://giji.mandalachart.com/) |
| [goal](goal/SKILL.md) | マンダラ目標 | マンダラのセルJSON | [Web版](https://goal.mandalachart.com/) |
| [graph](graph/SKILL.md) | グラフ作成 | アプリ専用JSON | [Web版](https://graph.tanaike.jp/) |
| [htmlai](htmlai/SKILL.md) | AI HTML編集 | 本文テキスト | [Web版](https://htmlai.tanaike.jp/) |
| [htmlslide](htmlslide/SKILL.md) | HTMLスライド | アプリ専用JSON | [Web版](https://htmlslide.tanaike.jp/) |
| [inknote](inknote/SKILL.md) | 手書きノート | アプリ専用JSON | [Web版](https://inknote.tanaike.jp/) |
| [invitation](invitation/SKILL.md) | 招待状 | アプリ専用JSON | [Web版](https://invitation.tanaike.jp/) |
| [invoice](invoice/SKILL.md) | 請求書 | アプリ専用JSON | [Web版](https://invoice.tanaike.jp/) |
| [javascript](javascript/SKILL.md) | JavaScript編集 | 本文テキスト | [Web版](https://javascript.tanaike.jp/) |
| [leaflet](leaflet/SKILL.md) | チラシ・POP | アプリ専用JSON | [Web版](https://leaflet.tanaike.jp/) |
| [led](led/SKILL.md) | LED電光掲示板 | アプリ専用JSON | [Web版](https://led.tanaike.jp/) |
| [mandalachart](mandalachart/SKILL.md) | マンダラ | マンダラのセルJSON | [Web版](https://app.mandalachart.com/) |
| [markdown](markdown/SKILL.md) | Markdown編集 | 本文テキスト | [Web版](https://markdown.tanaike.jp/) |
| [marpai](marpai/SKILL.md) | AI Marpスライド | アプリ専用JSON | [Web版](https://marpai.tanaike.jp/) |
| [marpslide](marpslide/SKILL.md) | Marpスライド | アプリ専用JSON | [Web版](https://marpslide.tanaike.jp/) |
| [matchtable](matchtable/SKILL.md) | 対戦表 | アプリ専用JSON | [Web版](https://matchtable.tanaike.jp/) |
| [meishi](meishi/SKILL.md) | 名刺 | アプリ専用JSON | [Web版](https://meishi.tanaike.jp/) |
| [menu](menu/SKILL.md) | メニュー表 | アプリ専用JSON | [Web版](https://menu.tanaike.jp/) |
| [newspaper](newspaper/SKILL.md) | 新聞 | アプリ専用JSON | [Web版](https://newspaper.tanaike.jp/) |
| [orderform](orderform/SKILL.md) | 発注書 | アプリ専用JSON | [Web版](https://orderform.tanaike.jp/) |
| [orderslip](orderslip/SKILL.md) | 注文伝票 | アプリ専用JSON | [Web版](https://orderslip.tanaike.jp/) |
| [outlineai](outlineai/SKILL.md) | AIアウトライン | アプリ専用JSON | [Web版](https://outlineai.tanaike.jp/) |
| [paycheck](paycheck/SKILL.md) | 給与明細 | アプリ専用JSON | [Web版](https://paycheck.tanaike.jp/) |
| [pixelart](pixelart/SKILL.md) | ドット絵 | アプリ専用JSON | [Web版](https://pixelart.tanaike.jp/) |
| [pos](pos/SKILL.md) | レジ・会計 | アプリ専用JSON | [Web版](https://pos.tanaike.jp/) |
| [posecraft](posecraft/SKILL.md) | PoseCraft（3Dポーズ） | アプリ専用JSON | [Web版](https://posecraft.tanaike.jp/) |
| [python](python/SKILL.md) | Python編集 | 本文テキスト | [Web版](https://python.tanaike.jp/) |
| [quote](quote/SKILL.md) | 見積書 | アプリ専用JSON | [Web版](https://quote.tanaike.jp/) |
| [receipt](receipt/SKILL.md) | 領収書 | アプリ専用JSON | [Web版](https://receipt.tanaike.jp/) |
| [requirement](requirement/SKILL.md) | 要件整理 | アプリ専用JSON | [Web版](https://requirement.tanaike.jp/) |
| [resume](resume/SKILL.md) | 履歴書 | アプリ専用JSON | [Web版](https://resume.tanaike.jp/) |
| [rust](rust/SKILL.md) | Rust編集 | 本文テキスト | **配信先の指定が必要** |
| [sales](sales/SKILL.md) | 売上管理 | アプリ専用JSON | [Web版](https://sales.tanaike.jp/) |
| [sequenceflow](sequenceflow/SKILL.md) | シーケンス図 | 本文テキスト | [Web版](https://sequenceflow.tanaike.jp/) |
| [shift](shift/SKILL.md) | シフト表 | アプリ専用JSON | [Web版](https://shift.tanaike.jp/) |
| [shopcard](shopcard/SKILL.md) | ショップカード | アプリ専用JSON | [Web版](https://shopcard.tanaike.jp/) |
| [shtml](shtml/SKILL.md) | HTML編集 | 本文テキスト | [Web版](https://html.tanaike.jp/) |
| [simplecorrelation](simplecorrelation/SKILL.md) | シンプル相関図 | アプリ専用JSON | [Web版](https://simplecorrelation.tanaike.jp/) |
| [simpleflowchart](simpleflowchart/SKILL.md) | シンプルフローチャート | アプリ専用JSON | [Web版](https://simpleflowchart.tanaike.jp/) |
| [slide](slide/SKILL.md) | スライド | アプリ専用JSON | [Web版](https://slide.tanaike.jp/) |
| [slideai](slideai/SKILL.md) | AIスライド | アプリ専用JSON | [Web版](https://slideai.tanaike.jp/) |
| [solopodcast](solopodcast/SKILL.md) | ひとりポッドキャスト | アプリ専用JSON | **配信先の指定が必要** |
| [spreadsheet](spreadsheet/SKILL.md) | 表作成 | 表全体のJSON | [Web版](https://spreadsheet.tanaike.jp/) |
| [spreadsheetai](spreadsheetai/SKILL.md) | AI表作成 | 表全体のJSON | [Web版](https://spreadsheetai.tanaike.jp/) |
| [stamp](stamp/SKILL.md) | スタンプカード | アプリ専用JSON | [Web版](https://stamp.tanaike.jp/) |
| [stock](stock/SKILL.md) | 在庫管理 | アプリ専用JSON | [Web版](https://stock.tanaike.jp/) |
| [timeline](timeline/SKILL.md) | 年表 | アプリ専用JSON | [Web版](https://timeline.tanaike.jp/) |
| [timetable](timetable/SKILL.md) | 時間割・タイムテーブル | アプリ専用JSON | [Web版](https://timetable.tanaike.jp/) |
| [tournament](tournament/SKILL.md) | tournament | アプリ専用JSON | [Web版](https://tournament.tanaike.jp/) |
| [trip](trip/SKILL.md) | 旅のしおり | アプリ専用JSON | [Web版](https://trip.tanaike.jp/) |
| [typescript](typescript/SKILL.md) | TypeScript編集 | 本文テキスト | [Web版](https://typescript.tanaike.jp/) |
| [visualizeai](visualizeai/SKILL.md) | AIビジュアライズ | アプリ専用JSON | [Web版](https://visualizeai.tanaike.jp/) |
| [zukai](zukai/SKILL.md) | AI図解 | 本文テキスト | [Web版](https://zukai.tanaike.jp/) |

Rustとひとりポッドキャストは実装の `webVersionUrl` が空です。確認済みの配信先がある場合だけ `--base-url https://配信先/` を指定してください。ドメインを推測したURLは生成しません。

## 作成できるものと制約

URLを開くと保存前のプレビューになります。永続的なファイル作成や保存完了を意味しません。保存したい場合は、ユーザーがアプリ内でインポートします。元のURLや既存ファイルの更新機能ではありません。

画像ファイル・Base64画像・端末内の録音や添付ファイルは対象外です。アルバム・コラージュ等は写真枠や見出しなどの構成を作れます。ドット絵の画素や手書きの点群はJSONの内容として扱います。本文型のHTML・Markdownで外部画像を参照する場合、その画像データ自体がURLに入るわけではありません。

共有URLはUTF-8本文またはJSONをzlib圧縮し、base64urlに変換して `content` に入れます。暗号化ではありません。生成スクリプトは8,000文字を超えるURLを拒否し、情報を黙って削りません。

## 検証

```bash
python3 tools/verify_skills.py
python3 -m unittest discover -s tools -p "test_*.py"
python3 -m unittest discover -s mandalachart/scripts -p "test_*.py"
```

全71アプリの同梱サンプルについて、生成・復号の一致、URL長、参照ファイルを検証します。追加テストは文字列・改行・false・0の保持、重複JSONキー、過大な入力、不正な圧縮データ、範囲外セル、未設定配信先の拒否を確認します。

日英142サンプルについて、各アプリのFlutter読み込み処理との互換性もローカルで検証します。公開Web版での画面表示・インポート・保存は別途確認が必要です。検証状況は [apps.json](apps.json) の `validation` を参照してください。

## 内容埋め込みURLが未実装のアプリ

これらは、現時点のアプリにURLの内容を読み込む処理がありません。アプリ側への対応が必要なため、開けるリンクを約束するSkillは作成していません。Google Drive共有で代用しません。

| アプリID | 確認したリポジトリ | 状況 |
|---|---|---|
| `analysis` | `analysis/analysis-flutter` | 内容埋め込みURLの受信処理が未実装 |
| `blockdoceditor` | `blockdoceditor/blockdoceditor` | 内容埋め込みURLの受信処理が未実装 |
| `diary` | `diary/diary-flutter` | 内容埋め込みURLの受信処理が未実装 |
| `diaryai` | `diaryai/diaryai-flutter` | 内容埋め込みURLの受信処理が未実装 |
| `funnews` | `FunNews/funnews-flutter` | 内容埋め込みURLの受信処理が未実装 |
| `gift` | `gift-ai/gift-ai-flutter` | 内容埋め込みURLの受信処理が未実装 |
| `heatspotmap` | `heatspotmap/beeftongue-flutter` | 内容埋め込みURLの受信処理が未実装 |
| `idea` | `idea-creator/idea-creator-flutter` | 内容埋め込みURLの受信処理が未実装 |
| `keyword` | `keyword/keyword-flutter` | 内容埋め込みURLの受信処理が未実装 |
| `life` | `mandala-life/mandala-life-flutter` | 内容埋め込みURLの受信処理が未実装 |
| `mlb` | `mlb/mlb-flutter` | 内容埋め込みURLの受信処理が未実装 |
| `review` | `review_replyer/review_replyer_flutter` | 内容埋め込みURLの受信処理が未実装 |
| `story` | `story/story-flutter` | 内容埋め込みURLの受信処理が未実装 |
