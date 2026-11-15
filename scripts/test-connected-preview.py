"""Real connected-preview acceptance tests; never modifies the reference site."""
from pathlib import Path
import hashlib, importlib.util, json, unittest, urllib.request
ROOT = Path(__file__).resolve().parents[1]

class ConnectedPreviewTests(unittest.TestCase):
    def test_rubric_build_isolated(self):
        script = ROOT/'scripts/serve-editorial-preview.py'
        self.assertTrue(script.exists(), 'Missing connected preview service')
        spec = importlib.util.spec_from_file_location('connected_preview', script)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        original = (ROOT/'data/blog_editorial.json').read_bytes()
        runner = module.PreviewRunner(ROOT)
        try:
            result = runner.run({'kind':'rubric','patch':{'schema_version':1,
                'base_config_sha256':hashlib.sha256(original).hexdigest(),
                'changes':{'title':'Recette connectée — l’actu de la semaine'}}})
            self.assertEqual(result['status'], 'success', result)
            self.assertTrue(result['checks'])
            text = urllib.request.urlopen(result['blog_url']).read().decode()
            self.assertIn('Recette connectée — l’actu de la semaine', text)
            self.assertEqual((ROOT/'data/blog_editorial.json').read_bytes(), original)
        finally:
            runner.close()

    def test_future_article_has_private_preview_but_not_public_build(self):
        import base64, io, zipfile
        script = ROOT/'scripts/serve-editorial-preview.py'
        spec = importlib.util.spec_from_file_location('connected_preview_article', script)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        original = (ROOT/'data/blog_editorial.json').read_bytes()
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer,'w') as z:
            z.writestr('12-11-2026-recette-future/index.md',
                '---\ntitle: "Recette future"\nslug: "recette-future"\ndescription: "Article de test"\nauthor: "Recette locale"\ncreation_date: "2026-11-12"\ndate: "2026-11-12"\npublishDate: "2099-01-12T09:30:00+01:00"\ncategories: [outils]\nimage: "photo.png"\ndraft: false\n---\n\nArticle créé uniquement comme fixture de test.\n')
            z.writestr('12-11-2026-recette-future/photo.png',(ROOT/'static/images/blog/photo-femme.png').read_bytes())
        runner = module.PreviewRunner(ROOT)
        try:
            try:
                result = runner.run({'kind':'article','zip_base64':base64.b64encode(buffer.getvalue()).decode()})
            except ValueError as e:
                self.fail('Article test service must accept an exported future article: '+str(e))
            self.assertEqual(result['status'],'success',result)
            self.assertEqual(result['publication_state'],'scheduled')
            self.assertTrue(result['future_hidden'])
            self.assertIn('Recette future',urllib.request.urlopen(result['preview_url']).read().decode())
            self.assertEqual((ROOT/'data/blog_editorial.json').read_bytes(),original)
        finally: runner.close()

    def test_generated_wrong_title_is_refused(self):
        import shutil, tempfile
        folder=Path(tempfile.mkdtemp(prefix='m15-corrupt-render-test-',dir=Path.home()/'.hermes/cache/scratch'))
        site=folder/'site';site.mkdir()
        for name in ['content','data','layouts','static','scripts']:shutil.copytree(ROOT/name,site/name)
        shutil.copy2(ROOT/'hugo.toml',site/'hugo.toml')
        template=site/'layouts/partials/blog-preview-row.html'
        template.write_text(template.read_text().replace('<h2 id="{{ $id }}-title">{{ .title }}</h2>','<h2 id="{{ $id }}-title">Titre incorrect</h2>'))
        script=ROOT/'scripts/serve-editorial-preview.py'
        spec=importlib.util.spec_from_file_location('connected_preview_wrong',script)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        runner=module.PreviewRunner(site)
        try:
            with self.assertRaisesRegex(ValueError,'titre|Titre'):
                runner.run({'kind':'rubric','patch':{'schema_version':1,'base_config_sha256':hashlib.sha256((site/'data/blog_editorial.json').read_bytes()).hexdigest(),'changes':{'title':'Titre attendu'}}})
        finally:runner.close()

if __name__ == '__main__': unittest.main(verbosity=2)
