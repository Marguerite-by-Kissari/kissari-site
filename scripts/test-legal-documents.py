"""M10/M11: verify every built site footer and exact supplied PDF bytes.
Usage: python scripts/test-legal-documents.py BUILD_DIR
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import hashlib,json,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
BUILD=Path(sys.argv.pop(1)).resolve()
MANIFEST=ROOT/'data/legal_documents.json'
class Footer(HTMLParser):
    def __init__(self,text):
        super().__init__();self.inside=False;self.links=[];self.current=None;self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='nav' and 'site-footer__links' in attrs.get('class','').split():self.inside=True
        if tag=='a' and self.inside:self.current=dict(attrs,text='')
    def handle_data(self,text):
        if self.current is not None:self.current['text']+=text
    def handle_endtag(self,tag):
        if tag=='a' and self.current is not None:self.links.append(self.current);self.current=None
        if tag=='nav':self.inside=False
class LegalDocuments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages={str(p.relative_to(BUILD)):Footer(p.read_text()).links for p in sorted(BUILD.rglob('index.html')) if 'atelier-article' not in p.parts}
        for required in ['index.html','blog/index.html','contact/index.html']:
            assert required in cls.pages,required
        assert len(cls.pages)>=4,'Missing article pages'
    def document(self,label,name):
        for path,links in self.pages.items():
            with self.subTest(page=path,label=label):
                targets=[a for a in links if a['text']==label]
                self.assertEqual(len(targets),1)
                href=unquote(urlsplit(targets[0]['href']).path)
                self.assertEqual(href,'/documents/'+name)
                self.assertTrue((BUILD/href.lstrip('/')).is_file())
        expected=json.loads(MANIFEST.read_text())[name]['sha256']
        for installed in [ROOT/'static/documents'/name,BUILD/'documents'/name]:
            self.assertEqual(expected,hashlib.sha256(installed.read_bytes()).hexdigest())
            self.assertTrue(installed.read_bytes().startswith(b'%PDF-'))
    def test_connected_preview_documents(self):
        import importlib.util,urllib.request
        from urllib.parse import urljoin,quote
        spec=importlib.util.spec_from_file_location('legal_preview',ROOT/'scripts/serve-editorial-preview.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        runner=module.PreviewRunner(ROOT)
        original=(ROOT/'data/blog_editorial.json').read_bytes()
        try:
            result=runner.run({'kind':'rubric','patch':{'schema_version':1,'base_config_sha256':hashlib.sha256(original).hexdigest(),'changes':{'title':'Contrôle M10/M11 — aperçu local'}}})
            self.assertEqual(result['status'],'success')
            html=urllib.request.urlopen(result['blog_url'],timeout=15).read().decode()
            links=Footer(html).links
            manifest=json.loads(MANIFEST.read_text())
            for label,name in [('Mentions légales','Mentions_légales_KISSARI.pdf'),('RGPD','RGPD.pdf')]:
                href=next(a['href'] for a in links if a['text']==label)
                with urllib.request.urlopen(urljoin(result['blog_url'],quote(unquote(href),safe='/')),timeout=15) as response:
                    self.assertEqual(response.headers.get_content_type(),'application/pdf')
                    self.assertEqual(hashlib.sha256(response.read()).hexdigest(),manifest[name]['sha256'])
            self.assertEqual((ROOT/'data/blog_editorial.json').read_bytes(),original)
        finally:
            runner.close()
    def test_M10_mentions_legales(self):
        self.document('Mentions légales','Mentions_légales_KISSARI.pdf')
    def test_M11_rgpd_replaces_cgv(self):
        self.document('RGPD','RGPD.pdf')
        for path,links in self.pages.items():
            with self.subTest(page=path):
                self.assertNotIn('CGV',[a['text'] for a in links])
                self.assertTrue(all(unquote(urlsplit(a['href']).path)!='/cgv/' for a in links))
                self.assertEqual(sum(a['text']=='Nous contacter' and a['href']=='/contact/' for a in links),1)
if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(LegalDocuments))
    if result.wasSuccessful():
        out=ROOT/'livrables/recette-M10-M11/footer-inventory.json'
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps({'count':len(LegalDocuments.pages),'pages':LegalDocuments.pages},ensure_ascii=False,indent=2)+'\n')
        print('Verified footer pages:',len(LegalDocuments.pages))
    sys.exit(not result.wasSuccessful())
