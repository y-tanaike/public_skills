"""Test content preservation and important rejection cases in the URL tools."""
from __future__ import annotations

import base64
import importlib.util
import json
import random
import subprocess
import sys
import unittest
import zlib
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True


def tool(app: str) -> Any:
    spec = importlib.util.spec_from_file_location('tool_' + app, ROOT / app / 'scripts/create_url.py')
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UrlToolTest(unittest.TestCase):
    def test_false_zero_unicode_and_newlines_survive(self) -> None:
        module = tool('invitation')
        content: dict[str, Any] = {'eventTitle': '日本語 & English\n招待状', 'isDoubleSided': False}
        original: str = json.dumps(content, ensure_ascii=False)
        self.assertEqual(module.decode_url(module.create_url(content, '名前 & name')), content)
        self.assertEqual(json.dumps(content, ensure_ascii=False), original)
        module = tool('invoice')
        self.assertEqual(module.decode_url(module.create_url({'documentTitle': '請求書', 'taxRate': 0}))['taxRate'], 0)

    def test_large_url_rejected_without_omitting_content(self) -> None:
        module = tool('markdown')
        rng = random.Random(20261111)
        content: str = ''.join(rng.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(18000))
        with self.assertRaisesRegex(ValueError, '8,000'):
            module.create_url(content)

    def test_json_duplicates_and_nonfinite_values_rejected(self) -> None:
        module = tool('invoice')
        for value in ('{"documentTitle":"A","documentTitle":"B"}', '{"taxRate":NaN}', '{"taxRate":Infinity}'):
            with self.assertRaises(ValueError):
                module.load_json(value)
        with self.assertRaises(ValueError):
            module.create_url({'documentTitle': '請求書', 'taxRate': float('inf')})

    def test_text_is_not_double_json_encoded(self) -> None:
        module = tool('markdown')
        text: str = '# タイトル\n\n- 文章\n'
        url: str = module.create_url(text)
        self.assertEqual(module.decode_url(url), text)
        with self.assertRaises(ValueError):
            module.create_url({'text': text})

    def test_table_outside_cell_rejected(self) -> None:
        module = tool('checksheet')
        content: dict[str, Any] = json.loads((ROOT / 'checksheet/examples/sample.ja.json').read_text())
        content['cellList'][0]['col'] = len(content['colList'])
        with self.assertRaisesRegex(ValueError, 'outside table bounds'):
            module.create_url(content)

    def test_compressed_payload_limits_and_trailing_data(self) -> None:
        module = tool('markdown')
        for raw in (zlib.compress(b'a' * (module.MAX_BYTES + 1)), zlib.compress(b'hello') + b'junk'):
            parameter: str = base64.urlsafe_b64encode(raw).decode().rstrip('=')
            url: str = module.base_url() + '?' + urlencode({'content': parameter})
            with self.assertRaises(ValueError):
                module.decode_url(url)

    def test_cli_stdout_is_url_and_decode_returns_input(self) -> None:
        script: str = str(ROOT / 'shtml/scripts/create_url.py')
        sample: Path = ROOT / 'shtml/examples/sample.ja.html'
        result = subprocess.run([sys.executable, script, str(sample), '--name', '読書会'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(result.stdout.splitlines()), 1)
        decoded = subprocess.run([sys.executable, script, '--decode-url', result.stdout.strip()], capture_output=True, text=True)
        self.assertEqual(decoded.returncode, 0, decoded.stderr)
        self.assertEqual(decoded.stdout.rstrip('\n'), sample.read_text().rstrip('\n'))

    def test_unconfigured_app_requires_explicit_endpoint(self) -> None:
        module = tool('rust')
        with self.assertRaises(ValueError):
            module.create_url('fn main() {}')
        url: str = module.create_url('fn main() {}', override='https://example.com/rust/')
        self.assertEqual(module.decode_url(url, 'https://example.com/rust/'), 'fn main() {}')
        with self.assertRaises(ValueError):
            module.create_url('fn main() {}', override='https://example.com/?drive=id')


if __name__ == '__main__':
    unittest.main()
