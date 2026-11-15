import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
class ConfigTests(unittest.TestCase):
    def setUp(self):
        path=ROOT/'scripts/editorial_config.py'
        self.assertTrue(path.is_file(),'M15: validation des réglages non implémentée')
        spec=importlib.util.spec_from_file_location('editorial_config',path)
        self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
        self.config={'schema_version':1,'title':'Zoom sur nos idées','enabled':True,'article_paths':['/blog/exemple/']}
    def test_valid(self):
        self.assertEqual(self.m.validate_config(self.config),self.config)
    def test_title_trim(self):
        c={**self.config,'title':"  l'actu de la semaine  "}
        self.assertEqual(self.m.validate_config(c)['title'],"l'actu de la semaine")
    def test_bad_titles(self):
        for value in ['', 'x'*101,'ligne\nligne',False]:
            with self.subTest(value=str(value)[:20]),self.assertRaises(ValueError): self.m.validate_config({**self.config,'title':value})
    def test_schema_and_types(self):
        for edit in [{'schema_version':True},{'enabled':1},{'other':1},{'article_paths':'x'}]:
            with self.subTest(edit=edit),self.assertRaises(ValueError):self.m.validate_config({**self.config,**edit})
    def test_paths(self):
        for paths in [['/blog/a/','/blog/a/'],['https://example.org/x'],['/blog/../x/'],['/blog/%2e%2e/x/'],['/blog/a/?x=1']]:
            with self.subTest(paths=paths),self.assertRaises(ValueError):self.m.validate_config({**self.config,'article_paths':paths})
    def test_duplicate_json(self):
        with self.assertRaises(ValueError):self.m.load_json('{"x":1,"x":2}')
    def test_patch_title_only(self):
        patch={'schema_version':1,'base_config_sha256':'a'*64,'changes':{'title':'Le point'}}
        self.assertEqual(self.m.validate_patch(patch)['changes'],{'title':'Le point'})
    def test_patch_rejects(self):
        for edits in [{'base_config_sha256':'bad'},{'schema_version':True},{'changes':{}},{'changes':{'output':'/etc/passwd'}},{'changes':{'enabled':0}}]:
            p={'schema_version':1,'base_config_sha256':'a'*64,'changes':{'title':'Nouveau'},**edits}
            with self.subTest(p=p),self.assertRaises(ValueError):self.m.validate_patch(p)
if __name__=='__main__':unittest.main(verbosity=2)
