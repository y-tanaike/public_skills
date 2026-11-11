#!/usr/bin/env python3
"""Generate or decode embedded-content URLs (Python 3.10+, standard library only)."""
from __future__ import annotations

import argparse
import base64
import binascii
import json
import math
import sys
import zlib
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlsplit

CONFIG: dict[str, Any] = json.loads((Path(__file__).resolve().parent / 'app.json').read_text(encoding='utf-8'))
MAX_BYTES = 2 * 1024 * 1024
MAX_URL_LENGTH = 8000


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def load_json(text: str) -> Any:
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f'Invalid JSON number: {value}')))


def check_values(value: Any, path: str = 'root') -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if any(part in key.lower() for part in ('base64', 'imagepath', 'imageurl')) or key == 'imageList':
                raise ValueError(f'{path}.{key}: image attachments are outside this sharing skill')
            check_values(child, f'{path}.{key}')
    elif isinstance(value, list):
        for index, child in enumerate(value):
            check_values(child, f'{path}[{index}]')
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f'{path}: expected a finite number')


def validate_content(content: Any) -> None:
    if CONFIG['kind'] == 'text':
        if not isinstance(content, str) or not content.strip():
            raise ValueError('Provide nonempty text content')
        return
    if not isinstance(content, dict) or not content:
        raise ValueError('Content must be a nonempty JSON object')
    unknown: set[str] = set(content) - set(CONFIG['root_keys'])
    if unknown:
        raise ValueError(f'Unsupported root keys: {", ".join(sorted(unknown))}')
    check_values(content)
    for key, expected in CONFIG.get('root_types', {}).items():
        if key not in content or content[key] is None:
            continue
        value: Any = content[key]
        valid: bool = {'string': isinstance(value, str), 'object': isinstance(value, dict),
                       'array': isinstance(value, list), 'boolean': isinstance(value, bool),
                       'number': isinstance(value, (int, float)) and not isinstance(value, bool),
                       'integer': isinstance(value, int) and not isinstance(value, bool)}[expected]
        if not valid:
            raise ValueError(f'{key}: expected JSON type {expected}')
    if not any(value not in ('', None, [], {}) for key, value in content.items() if key not in CONFIG.get('metadata_keys', [])):
        raise ValueError('Provide content or items, not just format metadata')
    if CONFIG['kind'] == 'table':
        if not isinstance(content.get('fileEntity'), dict) or not content.get('colList') or not content.get('rowList'):
            raise ValueError('fileEntity and nonempty colList and rowList are required')
        for cell in content.get('cellList', []):
            if not isinstance(cell, dict):
                raise ValueError('Each cellList item must be an object')
            for key, limit in (('col', len(content['colList'])), ('row', len(content['rowList']))):
                index: Any = cell.get(key)
                if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < limit:
                    raise ValueError(f'Cell {key} is outside table bounds')


def base_url(override: str | None = None) -> str:
    value: str = override if override is not None else CONFIG['base_url']
    if not value:
        raise ValueError('This app has no configured web URL. Pass a verified deployment with --base-url')
    parsed = urlsplit(value)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.query or parsed.fragment or parsed.username or parsed.password:
        raise ValueError('Deployment must be an http(s) URL without a query, fragment, or credentials')
    return value.rstrip('/') + '/'


def decode_url(url: str, override: str | None = None) -> Any:
    if len(url) > MAX_URL_LENGTH:
        raise ValueError('URL exceeds 8,000 characters')
    parsed = urlsplit(url)
    expected = urlsplit(base_url(override))
    if (parsed.scheme, parsed.netloc, parsed.path.rstrip('/')) != (expected.scheme, expected.netloc, expected.path.rstrip('/')):
        raise ValueError('Provide an embedded-content sharing URL for this app')
    values: list[str] = parse_qs(parsed.query, keep_blank_values=True).get('content', [])
    if len(values) != 1 or not values[0]:
        raise ValueError('Provide exactly one content parameter')
    parameter: str = values[0].strip()
    if CONFIG['kind'] != 'text' and parameter.startswith('{'):
        text: str = parameter
    else:
        compressed: bytes = base64.b64decode(parameter + '=' * (-len(parameter) % 4), altchars=b'-_', validate=True)
        decoder = zlib.decompressobj()
        try:
            raw: bytes = decoder.decompress(compressed, MAX_BYTES + 1)
        except zlib.error as error:
            raise ValueError('Invalid compressed content') from error
        if len(raw) > MAX_BYTES or not decoder.eof or decoder.unused_data:
            raise ValueError('Compressed content is invalid or too large')
        text = raw.decode('utf-8')
    return text if CONFIG['kind'] == 'text' else load_json(text)


def create_url(content: Any, name: str = '', override: str | None = None) -> str:
    validate_content(content)
    text: str = content if CONFIG['kind'] == 'text' else json.dumps(content, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
    raw: bytes = text.encode('utf-8')
    if len(raw) > MAX_BYTES:
        raise ValueError('Content must be at most 2 MiB')
    encoded: str = base64.urlsafe_b64encode(zlib.compress(raw)).decode('ascii').rstrip('=')
    result: str = base_url(override) + '?' + urlencode({'name': name.strip(), 'content': encoded})
    if len(result) > MAX_URL_LENGTH:
        raise ValueError(f'URL has {len(result):,} characters and exceeds the 8,000-character limit. Reorganize or split the content; no fields were omitted.')
    if decode_url(result, override) != content:
        raise ValueError('Encoding round-trip verification failed')
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', type=Path, help='UTF-8 text or JSON input file, as specified by this app')
    parser.add_argument('--name', default='', help='File name')
    parser.add_argument('--decode-url', help='Decode the content of a URL offline')
    parser.add_argument('--base-url', help='Verified deployment (default: the app web URL)')
    args = parser.parse_args()
    if bool(args.input) == bool(args.decode_url):
        parser.error('Specify either an input file or --decode-url URL')
    try:
        if args.decode_url:
            content: Any = decode_url(args.decode_url, args.base_url)
            print(content if isinstance(content, str) else json.dumps(content, ensure_ascii=False, indent=2))
        else:
            if args.input.stat().st_size > MAX_BYTES:
                raise ValueError('Input file must be at most 2 MiB')
            text: str = args.input.read_text(encoding='utf-8-sig')
            content = text if CONFIG['kind'] == 'text' else load_json(text)
            print(create_url(content, args.name, args.base_url))
    except (ValueError, OSError, zlib.error, binascii.Error, RecursionError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
