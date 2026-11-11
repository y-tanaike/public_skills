#!/usr/bin/env python3
"""Verify bilingual samples, URL round trips, rejection cases, and reference links."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True


def check_sample(entry: dict[str, Any], sample_path: str) -> None:
    folder: Path = ROOT / entry['id']
    source: Path = folder / 'scripts/create_url.py'
    spec = importlib.util.spec_from_file_location('share_' + entry['id'], source)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sample: Path = folder / sample_path
    text: str = sample.read_text(encoding='utf-8')
    content: Any = text if entry['kind'] == 'text' else json.loads(text)
    override: str | None = None if entry['base_url'] else 'https://example.com/test/'
    if entry['kind'] == 'mandala':
        url: str = module.create_url(content, '日本語 & English / 例')
        assert module.decode_url(url) == content
    else:
        url = module.create_url(content, '日本語 & English / 例', override)
        assert module.decode_url(url, override) == content
        if not entry['base_url']:
            try:
                module.create_url(content)
            except ValueError:
                pass
            else:
                raise AssertionError('Unconfigured deployment was not rejected')
        for invalid in ('https://wrong.example/?content=x', module.base_url(override) + '?content=broken', url + '&content=duplicate'):
            try:
                module.decode_url(invalid, override)
            except ValueError:
                pass
            else:
                raise AssertionError('Invalid URL was not rejected')
        try:
            module.validate_content('' if entry['kind'] == 'text' else {'unsupported': 'value'})
        except ValueError:
            pass
        else:
            raise AssertionError('Empty text or unknown keys were not rejected')
        if entry['kind'] != 'text':
            invalid_content: dict[str, Any] = dict(content)
            invalid_content['imageBase64'] = 'test'
            try:
                module.validate_content(invalid_content)
            except ValueError:
                pass
            else:
                raise AssertionError('Image attachment was not rejected')
    assert len(url) <= 8000
    skill: str = (folder / 'SKILL.md').read_text(encoding='utf-8')
    assert re.search(r'^name: ' + re.escape(entry['id']) + '$', skill, re.M)
    for document in (folder / 'SKILL.md', folder / 'references/content-format.md'):
        for link in re.findall(r'\]\(([^)]+)\)', document.read_text(encoding='utf-8')):
            if '://' in link or link.startswith('#') or link == 'GENERATED_URL':
                continue
            assert (document.parent / link.split('#')[0]).is_file(), f'Broken reference: {document}: {link}'


def check_locale_structure(english: Any, japanese: Any, path: str = 'root') -> None:
    assert type(english) is type(japanese), f'{path}: locale sample types differ'
    if isinstance(english, dict):
        assert english.keys() == japanese.keys(), f'{path}: locale sample keys differ'
        fixed_keys: set[str] = {'id', 'type', 'createType', 'version', 'topicType', 'sizeType', 'itemType', 'status', 'modelId', 'fromTopicId', 'toTopicId', 'axisId', 'personId', 'categoryId', 'matchId', 'parentMatchId', 'rootMatchId', 'team1Id', 'team2Id', 'orderItemId', 'registerItemId', 'tableId'}
        for key in english:
            if key in fixed_keys:
                assert english[key] == japanese[key], f'{path}.{key}: protocol value changed'
            check_locale_structure(english[key], japanese[key], f'{path}.{key}')
    elif isinstance(english, list):
        assert len(english) == len(japanese), f'{path}: locale sample lengths differ'
        for index, (left, right) in enumerate(zip(english, japanese)):
            check_locale_structure(left, right, f'{path}[{index}]')


def check_app(entry: dict[str, Any]) -> None:
    assert set(entry['examples']) == {'en', 'ja'}, 'Both English and Japanese examples are required'
    assert entry['example'] == entry['examples']['en'], 'Default example must be English'
    for sample_path in entry['examples'].values():
        check_sample(entry, sample_path)
    folder: Path = ROOT / entry['id']
    if entry['kind'] != 'text':
        english: Any = json.loads((folder / entry['examples']['en']).read_text(encoding='utf-8'))
        japanese: Any = json.loads((folder / entry['examples']['ja']).read_text(encoding='utf-8'))
        check_locale_structure(english, japanese)
    for path in (folder / 'SKILL.md', folder / 'references/content-format.md', folder / 'scripts/create_url.py'):
        assert not re.search('[ぁ-んァ-ヶ一-龠]', path.read_text(encoding='utf-8')), f'{path}: English source contains untranslated Japanese'


def main() -> int:
    entries: list[dict[str, Any]] = json.loads((ROOT / 'apps.json').read_text(encoding='utf-8'))['apps']
    failures: list[str] = []
    for entry in entries:
        try:
            check_app(entry)
        except Exception as error:
            failures.append(f"{entry['id']}: {error}")
    for failure in failures:
        print(failure, file=sys.stderr)
    print(f'{len(entries) - len(failures)}/{len(entries)} apps passed bilingual sample checks ({2 * len(entries)} samples)')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
