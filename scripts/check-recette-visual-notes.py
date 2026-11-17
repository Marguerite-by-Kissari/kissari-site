"""M07–M09, M13–M14, M17–M20: inspect a real Hugo build.
Usage: python scripts/check-recette-visual-notes.py BUILD_DIR [test_M07|...]
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import re
import sys
import unittest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BUILD = Path(sys.argv.pop(1))
CASE = sys.argv.pop(1) if len(sys.argv) > 1 else None
ARTICLE = 'blog/classe-virtuelle-la-modalite-qui-n-a-rien-d-un-plan-b/index.html'
VIDEO = ROOT / 'static/videos/KISSARI-morph-1200x1200-OK.mp4'

class Element:
    def __init__(self, tag='', attrs=(), parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []
    @property
    def text(self):
        return ''.join(c if isinstance(c, str) else c.text for c in self.children)
    def all(self, predicate):
        return ([self] if predicate(self) else []) + [n for c in self.children if isinstance(c, Element) for n in c.all(predicate)]
    def cls(self, name):
        return name in self.attrs.get('class', '').split()

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.root = Element()
        self.current = self.root
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        node = Element(tag, attrs, self.current)
        self.current.children.append(node)
        if tag not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:
            self.current = node
    def handle_endtag(self, tag):
        node = self.current
        while node.parent is not None:
            if node.tag == tag:
                self.current = node.parent
                break
            node = node.parent
    def handle_data(self, data):
        self.current.children.append(data)

def doc(path):
    return Document((BUILD / path).read_text()).root

class Recipe(unittest.TestCase):
    def test_M07(self):
        videos = doc('index.html').all(lambda n:n.tag == 'video')
        self.assertEqual(len(videos), 1)
        v=videos[0]
        badges=doc('index.html').all(lambda n:n.cls('hero-media-badge'))
        self.assertEqual(badges[0].tag,'button','the drawn play badge must also be actionable')
        self.assertEqual(badges[0].attrs.get('aria-controls'),v.attrs.get('id'))
        self.assertIn('controls',v.attrs)
        self.assertIn('playsinline',v.attrs)
        for attribute in ['autoplay', 'loop', 'muted']:
            self.assertIn(attribute, v.attrs)
        self.assertEqual(v.attrs['preload'],'metadata')
        ancestor=v.parent
        while ancestor:
            self.assertNotEqual(ancestor.attrs.get('aria-hidden'),'true')
            ancestor=ancestor.parent
        source=v.all(lambda n:n.tag=='source')[0]
        dest=BUILD / source.attrs['src'].lstrip('/')
        self.assertEqual(hashlib.sha256(dest.read_bytes()).digest(),hashlib.sha256(VIDEO.read_bytes()).digest())

    def test_M08(self):
        from urllib.parse import unquote
        imgs=doc('index.html').all(lambda n:n.tag=='img' and 'Femme cheveux' in unquote(n.attrs.get('src','')))
        self.assertEqual(len(imgs),1)
        from urllib.parse import unquote
        image=Image.open(BUILD/unquote(imgs[0].attrs['src'].lstrip('/'))).convert('RGBA')
        original=Image.open(ROOT/'static/images/Femme cheveux.png').convert('RGBA')
        self.assertEqual(image.size,original.size)
        self.assertEqual(image.getpixel((image.width-1,image.height-1))[3],255,'shirt must occupy the cut corner')
        self.assertEqual(image.crop((0,0,875,900)).tobytes(),original.crop((0,0,875,900)).tobytes(),'face and upper silhouette must stay exact')

    def test_M09(self):
        for path in [p.relative_to(BUILD) for p in BUILD.rglob('index.html') if 'atelier-article' not in p.parts]:
            with self.subTest(path=path):
                taglines=doc(path).all(lambda n:n.cls('site-footer__tagline'))
                self.assertEqual(len(taglines),1)
                self.assertEqual(taglines[0].text,'Votre partenaire transformation')
                normal=taglines[0].all(lambda n:n.cls('site-footer__trans'))
                self.assertEqual([n.text for n in normal],['trans'])
                bold=taglines[0].all(lambda n:n.tag=='strong')
                self.assertEqual([n.text for n in bold],['Votre partenaire ','formation'])
                styles=doc(path).all(lambda n:n.tag=='link' and n.attrs.get('rel')=='stylesheet')
                self.assertRegex(styles[0].attrs['href'],r'/css/site\.css\?v=[a-f0-9]{64}$')
        css=(BUILD/'css/site.css').read_text()
        self.assertRegex(css,r'\.site-footer__trans\s*\{\s*font-weight:\s*400;')

    def test_M13(self):
        page=(BUILD/'blog/index.html').read_text()
        self.assertNotIn('Bienvenue dans nos idées',page)
        self.assertIn('Le blog qui remue les',page)
        self.assertIn('Tout voir',page)

    def test_M14(self):
        css=(BUILD/'css/site.css').read_text()
        self.assertRegex(css,r'\.hero h1 span:before,\s*\.blog-hero h1 span:before\s*\{')
        self.assertRegex(css,r'\.hero h1 span:after,\s*\.blog-hero h1 span:after\s*\{')
        self.assertNotIn('.blog-hero h1 span::after {',css)
        self.assertIn('--marker-reference-size: 51px;', css)
        self.assertIn('--marker-reference-size: 66px;', css)
        for factor in ['0.29', '0.16', '0.26', '0.13']:
            self.assertIn('calc(var(--marker-reference-size) * '+factor+')', css)

    def test_M17_M20(self):
        tree=doc(ARTICLE)
        refs=tree.all(lambda n:n.cls('footnote-ref'))
        self.assertEqual(len(refs),1)
        self.assertEqual(refs[0].text,'1')
        self.assertNotEqual(refs[0].parent.parent.tag,'article')
        self.assertEqual(refs[0].parent.parent.tag,'p')
        self.assertIn('76 % d’usage',refs[0].parent.parent.text)
        self.assertNotIn('¹',refs[0].parent.parent.text)
        ids={n.attrs['id']:n for n in tree.all(lambda n:'id' in n.attrs)}
        li=ids[refs[0].attrs['href'][1:]]
        self.assertEqual(li.tag,'li')
        numbers=li.all(lambda n:n.cls('footnote-number'))
        self.assertEqual([n.text for n in numbers],['1'])
        self.assertIn('Enquête ISTF',li.text)
        back=li.all(lambda n:n.cls('footnote-backref'))[0]
        self.assertEqual(back.attrs['href'],'#'+refs[0].parent.attrs['id'])
        self.assertEqual(li.attrs.get('tabindex'),'-1')
        self.assertEqual(refs[0].parent.attrs.get('tabindex'),'-1')
        self.assertIn('calc(0.75em + 4pt)',(BUILD/'css/site.css').read_text())
        self.assertNotRegex((BUILD/'css/site.css').read_text(),r'footnote[^{}]*::?(?:before|after)\s*\{\s*content:\s*"\*"')

if __name__=='__main__':
    suite=unittest.TestSuite([Recipe(CASE)]) if CASE else unittest.defaultTestLoader.loadTestsFromTestCase(Recipe)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
