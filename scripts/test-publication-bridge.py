"""Real local Git transport acceptance; never contacts GitHub."""
import importlib.util, json, os, subprocess, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PublishTest(unittest.TestCase):
    def test_publish_preserves_unrelated_files(self):
        source=ROOT/'scripts/publication_bridge.py'
        self.assertTrue(source.is_file(),'Publication bridge is not implemented')
        spec=importlib.util.spec_from_file_location('publication_bridge',source)
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory(dir=Path.home()/'.hermes/cache/scratch') as d:
            p=Path(d); seed=p/'seed';seed.mkdir()
            def git(*args,cwd=seed):
                return subprocess.run(['git',*args],cwd=cwd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.decode().strip()
            git('init','-b','main');git('config','user.name','Fixture');git('config','user.email','fixture@example.invalid')
            (seed/'keep.txt').write_text('UNCHANGED');git('add','.');git('commit','-m','Initial')
            remote=p/'remote.git';git('clone','--bare',str(seed),str(remote))
            pub=mod.Publisher(str(remote),p/'client','Virginie','fixture@example.invalid')
            base=pub.sync()
            candidate=pub.prepare(base,{'content/blog/fixture/index.md':b'---\ntitle: Fixture\n---\nHello\n'},'Article fixture')
            result=pub.publish(candidate['token'])
            self.assertEqual(result['status'],'source_sent')
            self.assertEqual(git('--git-dir',str(remote),'show','main:keep.txt'),'UNCHANGED')
            self.assertIn('Hello',git('--git-dir',str(remote),'show','main:content/blog/fixture/index.md'))
    def test_article_allows_existing_callout_format(self):
        import base64,io,zipfile
        spec=importlib.util.spec_from_file_location('publication_bridge',ROOT/'scripts/publication_bridge.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        md=b'---\ntitle: Fixture\ndraft: false\n---\n{{< callout color="pink" title="Citation" >}}\nHello\n{{< /callout >}}\n'
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,'w') as z:
            z.writestr('15-11-2026-fixture/index.md',md);z.writestr('15-11-2026-fixture/image.png',bytes.fromhex('89504e470d0a1a0a'))
        files=mod.article_files(base64.b64encode(buf.getvalue()).decode())
        self.assertEqual(len(files),2)

    def test_http_rejects_foreign_origin(self):
        import sys, threading, urllib.request, urllib.error
        sys.path.insert(0,str(ROOT/'scripts'))
        service=ROOT/'scripts/atelier_service.py'
        self.assertTrue(service.is_file(),'Local publication HTTP service is not implemented')
        spec=importlib.util.spec_from_file_location('atelier_service',service);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory(dir=Path.home()/'.hermes/cache/scratch') as d:
            p=Path(d);(p/'index.html').write_text('<html>Atelier</html>')
            server=mod.make_server(p,{},port=0)
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            try:
                url='http://127.0.0.1:'+str(server.server_port)
                session=json.load(urllib.request.urlopen(url+'/api/publication/session'))
                self.assertIn('csrf',session)
                req=urllib.request.Request(url+'/api/publication/publish',data=b'{}',headers={'Content-Type':'application/json','Origin':'https://evil.invalid','X-Atelier-CSRF':session['csrf']})
                with self.assertRaises(urllib.error.HTTPError) as err:urllib.request.urlopen(req)
                self.assertEqual(err.exception.code,403);err.exception.close()
            finally:server.shutdown();server.server_close();thread.join()

if __name__=='__main__': unittest.main(verbosity=2)
