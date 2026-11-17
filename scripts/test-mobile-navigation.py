"""Shared mobile disclosure and homepage separator on a real minified build.
Interactive/geometry checks are recorded separately in the browser QA artifacts.
"""
from pathlib import Path
from html.parser import HTMLParser
import subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
    def __init__(self,html):super().__init__();self.tags=[];self.feed(html)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
class MobileNavigationTests(unittest.TestCase):
    def test_all_shared_headers(self):
        with tempfile.TemporaryDirectory(prefix='kissari-mobile-',dir=Path.home()/'.hermes/cache/scratch') as folder:
            run=subprocess.run(['hugo','--source',str(ROOT),'--minify','--destination',folder],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            pages=[p for p in Path(folder).rglob('*.html') if '<header class=site-header' in p.read_text() or '<header class="site-header"' in p.read_text()]
            self.assertEqual(len(pages),8)
            for page in pages:
                with self.subTest(page=page.relative_to(folder)):
                    html=page.read_text();tags=Tags(html).tags
                    navs=[a for t,a in tags if t=='nav' and a.get('id')=='primary-navigation']
                    self.assertEqual(len(navs),1)
                    buttons=[a for t,a in tags if t=='button' and a.get('class')=='mobile-nav-toggle']
                    self.assertEqual(len(buttons),1)
                    self.assertEqual(buttons[0]['type'],'button')
                    self.assertEqual(buttons[0]['aria-expanded'],'false')
                    self.assertEqual(buttons[0]['aria-controls'],'primary-navigation')
                    self.assertIn('hidden',buttons[0])
                    self.assertTrue(any(t=='script' and '/js/mobile-navigation.js?' in a.get('src','') for t,a in tags))
                    self.assertTrue(any(t=='link' and '/css/mobile.css?' in a.get('href','') for t,a in tags))
                    self.assertEqual(sum(t=='hr' and a.get('class')=='hero-mobile-divider' for t,a in tags),int(page==Path(folder)/'index.html'))
if __name__=='__main__':unittest.main(verbosity=2)
