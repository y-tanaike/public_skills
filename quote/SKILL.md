---
name: quote
description: Create or edit content for Quote and generate a URL that embeds the content for Quote. Use when the user wants to open generated content in this app. Excludes Google Drive file sharing.
---

# Create Quote content with an embedded URL

Return a clickable URL containing the requested content. Generate URLs offline using Python 3.10+ and the standard library; no external API, login, Flutter SDK, or app checkout is required.

## Language

Use the language explicitly requested by the user for both the response and generated content. Otherwise, use the user's language. The English instructions do not imply English output. Translate display text only: preserve JSON keys, IDs, enum values, URL parameter names, code syntax, and the app's date/number formats. See the [English example](examples/sample.en.json) and [Japanese example](examples/sample.ja.json); do not load both unless comparing languages.

## Workflow

1. Read the [data format](references/content-format.md). Create the app-specific JSON described in the reference. Use the matching example as a starting point and save the input as UTF-8.
2. Resolve paths from this skill's actual location and run the bundled tool:

   ```bash
   python3 <skill-directory>/scripts/create_url.py /tmp/content.json --name 'File name'
   ```

   To try the example, use `<skill-directory>/examples/sample.en.json` as the input. Successful stdout is one URL line.
3. Return a Markdown link using the generated URL and a short description in the user's language. Do not invent, manually edit, or insert line breaks into the compressed URL.
4. To edit an existing link, use `python3 <skill-directory>/scripts/create_url.py --decode-url 'URL'`, edit the decoded content, and generate a new URL. Existing links and saved files are unchanged. When using a custom `--base-url`, use the same deployment for decoding.

## Sharing, persistence, and limits

- Opening the URL creates an unsaved, editable preview. Do not claim that a persistent file was created or saved. The user can import it in the app; available save actions depend on the environment and login state.
- Do not embed image attachments, Base64 images, or local recordings. For image-centered apps, describe the result as a layout with slots, headings, and captions. Pixel-art color data and handwriting point arrays remain valid content where supported.
- Keep URLs at or below 8,000 characters. The script rejects longer URLs without silently dropping fields. If necessary, reorganize or split content according to the user's intent; do not remove requested information without agreement.
- Compression is not encryption. Anyone with the URL can recover the content.
- The script checks basic input structure, URL length, and encoding round trips. It does not validate every nested field, text syntax, or rendered result. Claim visual verification or successful saving only after actually checking it in the app.
