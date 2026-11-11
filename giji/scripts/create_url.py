#!/usr/bin/env python3
"""Generate an embedded-content mandala URL (Python 3.10+, standard library only)."""
from __future__ import annotations

import argparse
import base64
import binascii
import json
import re
import sys
import zlib
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlsplit

BASE_URL = "https://giji.mandalachart.com/"
MAX_URL_LENGTH = 8000
MAX_JSON_BYTES = 2 * 1024 * 1024
VIEWS = ("b_type", "a_type_root", *(f"a_type_{letter}" for letter in "abcdefgh"))
LAYOUTS = ("minimum", "simple", "normal")
COMPLETION_IDS = ("initial", "zero", "quarter", "half", "three_quarters", "completed")
STRING_FIELDS = ("title", "description", "link", "color", "complete")
ALLOWED_FIELDS = {*STRING_FIELDS, "childMandalaCellList"}


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(text: str) -> Any:
    return json.loads(text, object_pairs_hook=unique_object)


def validate_cell(value: Any, depth: int = 0, path: str = "root") -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{path}: a cell must be a JSON object")
    unknown = set(value) - ALLOWED_FIELDS
    if unknown:
        raise ValueError(f"{path}: unsupported keys: {', '.join(sorted(unknown))}")
    for key in STRING_FIELDS:
        if key in value and not isinstance(value[key], str):
            raise ValueError(f"{path}.{key}: expected a string")
    if depth == 0 and not value.get("title", "").strip():
        raise ValueError("root.title: provide a nonempty center title")
    color: str = value.get("color", "")
    if color and not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
        raise ValueError(f"{path}.color: use #RRGGBB format")
    link: str = value.get("link", "")
    if link:
        parsed = urlsplit(link)
        if not link.startswith(("https://", "http://")) or not parsed.hostname or any(c.isspace() for c in link):
            raise ValueError(f"{path}.link: use an absolute http(s) URL")
    if value.get("complete", "initial") not in COMPLETION_IDS:
        raise ValueError(f"{path}.complete: valid IDs are {', '.join(COMPLETION_IDS)}")
    children: Any = value.get("childMandalaCellList", [])
    if not isinstance(children, list):
        raise ValueError(f"{path}.childMandalaCellList: expected an array")
    if len(children) > 8:
        raise ValueError(f"{path}: at most eight children are allowed (got {len(children)})")
    if depth >= 2 and children:
        raise ValueError(f"{path}: action cells cannot have children")
    for index, child in enumerate(children):
        validate_cell(child, depth + 1, f"{path}.childMandalaCellList[{index}]")


def decode_url(url: str) -> dict[str, Any]:
    """Decode an existing embedded-content URL offline."""
    if len(url) > MAX_URL_LENGTH:
        raise ValueError("URL exceeds 8,000 characters")
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "giji.mandalachart.com" or parsed.path not in ("", "/"):
        raise ValueError("Provide an embedded-content sharing URL")
    values: list[str] = parse_qs(parsed.query).get("content", [])
    if len(values) != 1:
        raise ValueError("Provide exactly one content parameter")
    parameter = values[0].strip()
    if parameter.startswith("{"):
        text = parameter
    else:
        padded = parameter + "=" * (-len(parameter) % 4)
        compressed = base64.b64decode(padded, altchars=b"-_", validate=True)
        decoder = zlib.decompressobj()
        try:
            raw = decoder.decompress(compressed, MAX_JSON_BYTES + 1)
        except zlib.error as error:
            raise ValueError("Invalid compressed content") from error
        if len(raw) > MAX_JSON_BYTES or not decoder.eof or decoder.unused_data:
            raise ValueError("Compressed content is invalid or too large")
        text = raw.decode("utf-8")
    result: Any = load_json(text)
    if not isinstance(result, dict):
        raise ValueError("content must be a JSON object")
    return result


def create_url(content: dict[str, Any], name: str | None = None, view: str = "b_type", layout: str = "simple") -> str:
    validate_cell(content)
    if view not in VIEWS or layout not in LAYOUTS:
        raise ValueError("Invalid view or layout")
    text: str = json.dumps(content, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    encoded: str = base64.urlsafe_b64encode(zlib.compress(text.encode("utf-8"))).decode("ascii").rstrip("=")
    file_name: str = (name if name is not None else content["title"]).strip()
    url: str = BASE_URL + "?" + urlencode({"name": file_name, "type": view, "layout": layout, "content": encoded})
    if len(url) > MAX_URL_LENGTH:
        raise ValueError(f"URL has {len(url):,} characters and exceeds the 8,000-character limit. Reorganize or split the content; no fields were omitted.")
    if decode_url(url) != content:
        raise ValueError("Encoding round-trip verification failed")
    return url


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, help="UTF-8 JSON file containing the center cell")
    parser.add_argument("--name", help="File name (default: center title)")
    parser.add_argument("--view", choices=VIEWS, default="b_type", help="View (default: all 81 cells)")
    parser.add_argument("--layout", choices=LAYOUTS, default="simple")
    parser.add_argument("--decode-url", help="Decode a URL to JSON offline")
    args = parser.parse_args()
    if bool(args.input) == bool(args.decode_url):
        parser.error("Specify either an input JSON file or --decode-url URL")
    try:
        if args.decode_url:
            print(json.dumps(decode_url(args.decode_url), ensure_ascii=False, indent=2))
        else:
            if args.input.stat().st_size > MAX_JSON_BYTES:
                raise ValueError("Input JSON must be at most 2 MiB")
            content: Any = load_json(args.input.read_text(encoding="utf-8-sig"))
            print(create_url(content, args.name, args.view, args.layout))
    except (ValueError, OSError, zlib.error, binascii.Error, RecursionError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
