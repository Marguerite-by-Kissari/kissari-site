"""Real HTTP security acceptance tests on a separate loopback service."""
from pathlib import Path
import hashlib, json, socket, subprocess, time, unittest, urllib.error, urllib.request
ROOT=Path(__file__).resolve().parents[1]

def request(url, payload=None, headers=None, raw=None):
    h=dict(headers or {})
    if payload is not None: raw=json.dumps(payload).encode()
    if raw is not None:h.setdefault('Content-Type','application/json')
    req=urllib.request.Request(url,data=raw,headers=h)
    try:
        with urllib.request.urlopen(req,timeout=40) as r:code=r.status;body=r.read()
    except urllib.error.HTTPError as e:
        with e:code=e.code;body=e.read()
    try:body=json.loads(body)
    except (ValueError,UnicodeError):pass
    return code,body

class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
        cls.base='http://127.0.0.1:'+str(port)
        cls.process=subprocess.Popen(['python',str(ROOT/'scripts/serve-editorial-preview.py'),'--port',str(port)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        for _ in range(100):
            try:
                code,session=request(cls.base+'/api/test-session')
                if code==200:break
            except OSError:time.sleep(.05)
        else:
            cls.process.terminate();cls.process.wait();raise RuntimeError('Local test server did not start')
        cls.headers={'Origin':cls.base,'X-Atelier-CSRF':session['csrf']}
        cls.original=(ROOT/'data/blog_editorial.json').read_bytes()
        cls.payload={'kind':'rubric','patch':{'schema_version':1,'base_config_sha256':hashlib.sha256(cls.original).hexdigest(),'changes':{'title':'Recette HTTP'}}}
        code,cls.report=request(cls.base+'/api/test',cls.payload,cls.headers)
        if code!=200:raise RuntimeError(str(cls.report))
    @classmethod
    def tearDownClass(cls):
        cls.process.terminate();cls.process.wait(timeout=10)
        cls.process.stdout.close();cls.process.stderr.close()
    def tearDown(self):
        self.assertEqual((ROOT/'data/blog_editorial.json').read_bytes(),self.original)
    def test_missing_origin_or_nonce(self):
        code,_=request(self.base+'/api/test',self.payload)
        self.assertEqual(code,403)
        code,_=request(self.base+'/api/test',self.payload,{'Origin':self.base,'X-Atelier-CSRF':'incorrect'})
        self.assertEqual(code,403)
    def test_foreign_origin(self):
        code,_=request(self.base+'/api/test',self.payload,{**self.headers,'Origin':'https://attacker.invalid'})
        self.assertEqual(code,403)
    def test_stale_reference(self):
        payload=json.loads(json.dumps(self.payload));payload['patch']['base_config_sha256']='0'*64
        code,body=request(self.base+'/api/test',payload,self.headers)
        self.assertEqual(code,422);self.assertIn('Conflit',body['error'])
    def test_invalid_field_and_duplicate_json(self):
        payload=json.loads(json.dumps(self.payload));payload['patch']['changes']={'output':'/etc/passwd'}
        self.assertEqual(request(self.base+'/api/test',payload,self.headers)[0],422)
        self.assertEqual(request(self.base+'/api/test',headers=self.headers,raw=b'{"kind":"rubric","kind":"article"}')[0],422)
    def test_zip_traversal(self):
        import base64,io,zipfile
        data=io.BytesIO()
        with zipfile.ZipFile(data,'w') as z:z.writestr('../outside.md','must never be extracted')
        code,_=request(self.base+'/api/test',{'kind':'article','zip_base64':base64.b64encode(data.getvalue()).decode()},self.headers)
        self.assertEqual(code,422)
    def test_no_publish_or_git_endpoint(self):
        for route in ['/api/publish','/api/git','/api/apply']:
            self.assertEqual(request(self.base+route,{},self.headers)[0],404)
    def test_preview_rejects_forged_host(self):
        code,_=request(self.report['preview_url'],headers={'Host':'attacker.invalid'})
        self.assertEqual(code,403,'Preview must resist DNS rebinding, not just the API')

if __name__=='__main__':unittest.main(verbosity=2)
