# Text and URL format

- App ID: `flowchart`
- Input: **plain UTF-8 Mermaid flowchart text**. Do not wrap it in a JSON object or JSON string.
- `name` is the file name. `content` contains zlib-compressed UTF-8 text encoded as base64url without trailing `=`.
- The script preserves newlines, whitespace, and string literals. Include Markdown code fences only when they belong in the document itself.
- Content is not partially omitted to fit a URL; URLs longer than 8,000 characters are rejected.
- The script does not parse source syntax, execute code, or verify rendered HTML. Follow the target language's syntax.

Use the [English example](../examples/sample.en.mermaid) or [Japanese example](../examples/sample.ja.mermaid).

Start Mermaid text with the diagram type. Keep node or participant IDs unique and separate from translated display labels. Ensure references resolve. Do not invent unsupported syntax.
