"""M22–M25: real generated banners, empty decorative blocks and explicit links.
Usage: python scripts/check-article-next.py BUILD_DIR [M22|M23|M24|M25]
"""
from pathlib import Path
from html.parser import HTMLParser
import sys
import unittest

BUILD=Path(sys.argv.pop(1))
CASE=sys.argv.pop(1) if len(sys.argv)>1 else None

class Banner(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.depth=0
        self.blocks=[]
        self.current=None
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'article-next-banner' in attrs.get('class','').split():
            self.current={'tag':tag,'attrs':attrs,'text':'','children':[]}
            self.blocks.append(self.current)
            self.depth=1
        elif self.depth:
            self.current['children'].append((tag,attrs))
            if tag not in ['br','hr','img','input','source','meta','link']:
                self.depth+=1
    def handle_endtag(self,tag):
        if self.depth:
            self.depth-=1
    def handle_data(self,text):
        if self.depth:
            self.current['text']+=text

def banner(slug):
    parser=Banner((BUILD/'blog'/slug/'index.html').read_text())
    assert len(parser.blocks)==1, (slug,parser.blocks)
    return parser.blocks[0]

class Recipe(unittest.TestCase):
    def empty(self,slug):
        b=banner(slug)
        self.assertEqual(b['text'].strip(),'','the coloured band must remain genuinely empty')
        self.assertEqual(b['children'],[],'no title, label, arrow or invisible link')
        self.assertEqual(b['attrs'].get('aria-hidden'),'true')
        self.assertNotIn('aria-labelledby',b['attrs'])

    def linked(self,slug,target,title):
        b=banner(slug)
        links=[a for tag,a in b['children'] if tag=='a']
        self.assertEqual(len(links),1)
        self.assertEqual(links[0]['href'],'/blog/'+target+'/')
        self.assertTrue((BUILD/'blog'/target/'index.html').is_file())
        self.assertIn(title,b['text'])
        self.assertIn('A LIRE AUSSI',b['text'])
        self.assertEqual(b['attrs'].get('aria-labelledby'),'article-next-title')
        self.assertNotEqual(b['attrs'].get('aria-hidden'),'true')

    def test_M22(self):
        self.empty('classe-virtuelle-la-modalite-qui-n-a-rien-d-un-plan-b')
    def test_M23(self):
        self.linked('avec-le-marketing-learning-place-a-l-action','marketing-learning-ne-sarrete-jamais','Pourquoi le marketing learning ne s’arrête jamais ?')
    def test_M24(self):
        self.linked('marketing-learning-ne-sarrete-jamais','marketing-formation-avant-postes-engagement','Le marketing learning aux avant-postes de l’engagement')
    def test_M25(self):
        self.empty('marketing-formation-avant-postes-engagement')

if __name__=='__main__':
    suite=unittest.TestSuite([Recipe('test_'+CASE)]) if CASE else unittest.defaultTestLoader.loadTestsFromTestCase(Recipe)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
