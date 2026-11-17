"""Production configuration contract; no network or deployment side effects."""
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ProductionConfiguration(unittest.TestCase):
    def setUp(self):
        self.config = tomllib.loads((ROOT / 'hugo.toml').read_text())

    def test_public_origin(self):
        self.assertEqual(self.config['baseURL'], 'https://kissari.com/')

    def test_production_identity(self):
        self.assertEqual(self.config['title'], 'KISSARI')
        self.assertEqual(self.config['params']['environment'], 'production')

    def test_search_engine_outputs(self):
        self.assertTrue(self.config.get('enableRobotsTXT'))
        self.assertNotIn('sitemap', self.config.get('disableKinds', []))
        self.assertNotIn('robotsTXT', self.config.get('disableKinds', []))

    def test_all_public_templates_have_canonical_links(self):
        for name in ['index.html', 'blog/list.html', 'blog/single.html', 'contact/list.html']:
            with self.subTest(template=name):
                text = (ROOT / 'layouts' / name).read_text()
                self.assertIn('rel="canonical" href="{{ .Permalink }}"', text)

if __name__ == '__main__':
    unittest.main(verbosity=2)
