# Text and URL format

- App ID: `typescript`
- Input: **plain UTF-8 TypeScript text**. Do not wrap it in a JSON object or JSON string.
- `name` is the file name. `content` contains zlib-compressed UTF-8 text encoded as base64url without trailing `=`.
- The script preserves newlines, whitespace, and string literals. Include Markdown code fences only when they belong in the document itself.
- Content is not partially omitted to fit a URL; URLs longer than 8,000 characters are rejected.
- The script does not parse source syntax, execute code, or verify rendered HTML. Follow the target language's syntax.

Use the [English example](../examples/sample.en.ts) or [Japanese example](../examples/sample.ja.ts).
