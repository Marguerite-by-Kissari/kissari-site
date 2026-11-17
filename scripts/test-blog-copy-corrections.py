"""Acceptance for requested blog copy edits and the two-line yellow callout title."""
from pathlib import Path
from html import unescape
import json,re,subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
def text(html):return ' '.join(unescape(re.sub('<[^>]+>',' ',html)).split())
class BlogCopyTests(unittest.TestCase):
    def test_requested_changes_in_real_build(self):
        with tempfile.TemporaryDirectory(prefix='kissari-blog-copy-',dir=Path.home()/'.hermes/cache/scratch') as folder:
            result=subprocess.run(['hugo','--source',str(ROOT),'--minify','--destination',folder,'--baseURL','https://kissari.com/'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            site=Path(folder)
            blog=(site/'blog/index.html').read_text()
            self.assertIn('Zoom sur le marketing learning',text(blog))
            why=(site/'blog/marketing-learning-ne-sarrete-jamais/index.html').read_text()
            expected='Du coup, une petite idée de la mission du marketing learning by KISSARI ? Bingo ! C’est bien de révéler cette envie, la nourrir et l’entretenir.'
            self.assertIn(expected,text(why))
            self.assertNotIn('Là toute la mission',text(why))
            renamed=(site/'blog/marketing-formation-avant-postes-engagement/index.html').read_text()
            match=re.search(r'<h1[^>]*>(.*?)</h1>',renamed,re.S)
            assert match is not None
            title=match.group(1)
            self.assertEqual(text(title),'Le marketing learning aux avant-postes de l’engagement')
            self.assertIn('Le marketing learning aux avant-postes de l’engagement',text(why))
            virtual=(site/'blog/classe-virtuelle-la-modalite-qui-n-a-rien-d-un-plan-b/index.html').read_text()
            self.assertIn('Car, à distance, l’apprenant dispose d’armes de distraction massive :',text(virtual))
            self.assertNotIn('son frigo J.',text(virtual))
            match=re.search(r'<aside[^>]*article-callout--yellow.*?</aside>',virtual,re.S)
            assert match is not None
            yellow=match.group(0)
            match=re.search(r'<p class=[\"\']?article-callout__title[\"\']?>(.*?)</p>',yellow,re.S)
            assert match is not None
            heading=match.group(1)
            lines=re.split(r'<br\s*/?>',heading)
            self.assertEqual([text(line) for line in lines],['Et pour éviter le fameux Vous êtes toujours là…','voici cinq incontournables ...'])
            self.assertEqual(text(virtual).count('Et pour éviter le fameux Vous êtes toujours là…'),1)
            self.assertNotIn('Vous êtes toujours là ?',text(virtual))
            catalogue=json.loads((site/'blog/catalogue-editorial.json').read_text())
            self.assertEqual(catalogue['config']['title'],'Zoom sur le marketing learning')
            self.assertIn('Le marketing learning aux avant-postes de l’engagement',json.dumps(catalogue,ensure_ascii=False))
if __name__=='__main__':unittest.main(verbosity=2)
