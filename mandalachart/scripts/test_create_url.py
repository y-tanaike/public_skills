"""Run: python3 -m unittest discover -s scripts -p 'test_*.py'"""
import json
import random
import string
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from create_url import create_url, decode_url, load_json


class CreateUrlTest(unittest.TestCase):
    def test_example_round_trip(self) -> None:
        sample = json.loads((Path(__file__).parents[1] / 'examples/sample.ja.json').read_text(encoding='utf-8'))
        url = create_url(sample, name='読書 & Learning / 2026')
        self.assertEqual(decode_url(url), sample)
        self.assertEqual(parse_qs(urlsplit(url).query)['name'], ['読書 & Learning / 2026'])

    def test_full_mandala_and_empty_positions(self) -> None:
        content = {'title': '中心', 'childMandalaCellList': [
            {'title': f'テーマ{i}', 'childMandalaCellList': [{'title': f'行動{i}-{j}'} for j in range(8)]}
            for i in range(8)
        ]}
        content['childMandalaCellList'][2]['childMandalaCellList'][3] = {}
        self.assertEqual(decode_url(create_url(content)), content)

    def test_optional_fields_and_display(self) -> None:
        content = {'title': 'Test', 'description': '説明\n2行目', 'link': 'https://example.com/?a=1&b=2', 'color': '#12abEF', 'complete': 'half'}
        url = create_url(content, view='a_type_root', layout='normal')
        self.assertEqual(decode_url(url), content)
        self.assertEqual(parse_qs(urlsplit(url).query)['type'], ['a_type_root'])
        self.assertEqual(parse_qs(urlsplit(url).query)['layout'], ['normal'])

    def test_invalid_content_is_not_silently_discarded(self) -> None:
        cases = [
            {'title': 'a', 'childMandalaCellList': [{}] * 9},
            {'title': 'a', 'childMandalaCellList': [{'childMandalaCellList': [{'childMandalaCellList': [{}]}]}]},
            {'title': 'a', 'imageBase64': 'abc'},
            {'title': 'a', 'complete': '50'},
            {'title': 'a', 'color': 'red'},
            {'title': 'a', 'link': 'javascript:alert(1)'},
            {'title': 'a', 'description': 1},
            {'title': 'a', 'childMandalaCellList': None},
            {'title': 3}, {},
        ]
        for content in cases:
            with self.subTest(content=content), self.assertRaises(ValueError):
                create_url(content)

    def test_oversized_url_fails_without_omission(self) -> None:
        generator = random.Random(42)
        description = ''.join(generator.choices(string.ascii_letters + string.digits, k=15000))
        content = {'title': 'a', 'description': description}
        with self.assertRaisesRegex(ValueError, '8,000'):
            create_url(content)
        self.assertEqual(content['description'], description)

    def test_duplicate_json_keys_fail(self) -> None:
        with self.assertRaises(ValueError):
            load_json('{"title":"a","title":"b"}')

    def test_drive_links_and_invalid_compression_fail(self) -> None:
        for url in ['https://app.mandalachart.com/drive/abc', 'https://app.mandalachart.com/?content=invalid', 'https://example.com/?content=abc']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                decode_url(url)


if __name__ == '__main__':
    unittest.main()
