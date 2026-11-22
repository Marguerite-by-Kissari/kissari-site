"""Checks M01–M05 against an actual public Hugo build.
Usage: python scripts/check-navigation-recette.py BUILD_DIR [M01|M02|M03|M04|M05]
"""
from pathlib import Path
from html.parser import HTMLParser
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUILD = Path(sys.argv.pop(1))
CASE = sys.argv.pop(1) if len(sys.argv) > 1 else None

class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.nav = False
        self.current = None
        self.links = []
        self.ids = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'nav' and 'site-nav' in attrs.get('class', '').split():
            self.nav = True
        if tag == 'a' and self.nav:
            self.current = dict(attrs, text='')

    def handle_data(self, text):
        if self.current is not None:
            self.current['text'] += text

    def handle_endtag(self, tag):
        if tag == 'a' and self.current is not None:
            self.links.append(self.current)
            self.current = None
        if tag == 'nav':
            self.nav = False

class NavigationRecette(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = [p for p in BUILD.rglob('index.html') if 'atelier-article' not in p.parts]
        assert len(cls.pages) >= 7, f'Incomplete Hugo build: {cls.pages}'
        cls.home = Page((BUILD / 'index.html').read_text())


    def links(self, path):
        return Page(path.read_text()).links

    def check_anchor(self, label, anchor):
        self.assertEqual(self.home.ids.count(anchor), 1)
        for path in self.pages:
            with self.subTest(page=str(path)):
                link = next((a for a in self.links(path) if a['text'] == label), None)
                self.assertIsNotNone(link, f'Missing menu entry: {label}')
                self.assertEqual(link['href'], '/#' + anchor)


    def test_M01(self):
        self.check_anchor('Notre manifeste', 'notre-manifeste')

    def test_M02(self):
        self.check_anchor('Ce qui nous anime', 'ce-qui-nous-anime')

    def test_M03(self):
        for path in self.pages:
            with self.subTest(page=str(path)):
                links = self.links(path)
                link = next((a for a in links if a['text'] == 'Le blog par KA'), None)
                self.assertIsNotNone(link)
                self.assertEqual(link['href'], '/blog/')
                self.assertNotIn('Le blog', [a['text'] for a in links])


    def test_M04(self):
        for path in self.pages:
            with self.subTest(page=str(path)):
                links = self.links(path)
                if path.parent.name == 'contact':
                    # Nouvelle page demandée : seul son propre menu porte l’état Contact.
                    contact = [a for a in links if a['text'] == 'Contact']
                    self.assertEqual(len(contact), 1)
                    self.assertEqual(contact[0]['href'], '/contact/')
                    self.assertEqual(contact[0].get('aria-current'), 'page')
                else:
                    self.assertNotIn('Contact', [a['text'] for a in links])
                self.assertIn('>Nous contacter</a>', path.read_text())


    def test_M05(self):
        for path in self.pages:
            with self.subTest(page=str(path)):
                link = next(a for a in self.links(path) if a['text'] == 'Presse')
                self.assertIn('nav-link--muted', link.get('class', '').split())
                self.assertEqual(link['href'], '/')
                self.assertNotIn('aria-disabled', link)
        css = (BUILD / 'css/site.css').read_text()
        self.assertRegex(css, r'\.site-nav\s+\.nav-link--muted\s*\{\s*color:\s*#bebebe\s*;\s*\}')


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(NavigationRecette)
    if CASE:
        suite = unittest.TestSuite([NavigationRecette('test_' + CASE)])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
