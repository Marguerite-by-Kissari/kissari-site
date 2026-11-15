"""Loopback-only test service. Builds disposable previews; no Git, apply or deploy API."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
import argparse, base64, csv, datetime, hashlib, hmac, io, json, re, secrets, shutil, subprocess, tempfile, threading, uuid, zipfile
from urllib.parse import urlsplit
from editorial_config import load_json, validate_config, validate_patch

from html.parser import HTMLParser

class RubricHTML(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.rows=[]; self.depth=0; self.heading=False; self.current=None
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='section' and attrs.get('data-category')=='editorial':
            self.current={'title':'','links':[],'labels':[]};self.rows.append(self.current);self.depth=1
        elif self.depth:
            if tag not in ('img','br','input','source','meta','link','hr'):self.depth+=1
            if tag=='h2' and attrs.get('id')=='editorial-title':self.heading=True
            if tag=='a':self.current['links'].append(attrs.get('href'))
            if tag=='button':self.current['labels'].append(attrs.get('aria-label',''))
    def handle_endtag(self,tag):
        if self.depth:
            if tag=='h2':self.heading=False
            self.depth-=1
    def handle_data(self,text):
        if self.depth and self.heading:self.current['title']+=text

ROOT = Path(__file__).resolve().parents[1]
SCRATCH = Path.home()/'.hermes/cache/scratch'

class SafeFiles(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        self.send_error(404); return None
    def send_head(self):
        if self.headers.get('Host')!='127.0.0.1:'+str(self.server.server_port):
            self.send_error(403); return None
        target = Path(self.translate_path(self.path)).resolve()
        if not target.is_relative_to(Path(self.directory).resolve()):
            self.send_error(403); return None
        return super().send_head()
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Robots-Tag', 'noindex, nofollow')
        super().end_headers()
    def log_message(self, fmt, *args): pass

class PreviewRunner:
    def __init__(self, root=ROOT):
        self.root = Path(root).resolve()
        self.lock = threading.Lock()
        self.servers = []
        self.report_dir = self.root/'livrables/test-reports'
        self.report_dir.mkdir(parents=True,exist_ok=True)
    def close(self):
        for server in self.servers:
            server.shutdown(); server.server_close()
        self.servers.clear()
    def fingerprint(self):
        paths = [self.root/'hugo.toml']
        for folder in ['content', 'data']:
            paths += sorted((self.root/folder).rglob('*'))
        return {str(p.relative_to(self.root)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in paths if p.is_file()}
    def install_article(self, site, encoded):
        if not isinstance(encoded,str) or len(encoded)>23*1024*1024:
            raise ValueError('Archive trop volumineuse.')
        try: raw=base64.b64decode(encoded,validate=True)
        except Exception: raise ValueError('Archive ZIP invalide.')
        if len(raw)>16*1024*1024: raise ValueError('ZIP limité à 16 Mio.')
        def content():
            p=subprocess.run(['hugo','list','all','--source',str(site)],capture_output=True,text=True,timeout=60)
            if p.returncode: raise ValueError('Métadonnées Hugo invalides : '+p.stderr[-1500:])
            return list(csv.DictReader(io.StringIO(p.stdout)))
        existing={r['slug'] for r in content() if r['kind']=='page'}
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                infos=z.infolist(); names=[i.filename for i in infos]
                if len(infos)!=2 or len(set(names))!=2 or sum(i.file_size for i in infos)>16*1024*1024:
                    raise ValueError('Le ZIP doit contenir uniquement index.md et son image, dans un dossier.')
                indexes=[n for n in names if re.fullmatch(r'\d{2}-\d{2}-\d{4}-[a-z0-9-]+/index\.md',n)]
                if len(indexes)!=1: raise ValueError('Structure du ZIP article invalide.')
                folder=indexes[0].split('/')[0]
                other=next(n for n in names if n!=indexes[0])
                if not re.fullmatch(re.escape(folder)+r'/[A-Za-z0-9][A-Za-z0-9._-]*\.(?:png|jpe?g|webp|gif|avif)',other,re.I):
                    raise ValueError('Image locale PNG/JPEG/WebP/GIF/AVIF attendue ; aucun chemin arbitraire.')
                image=z.read(other); suffix=Path(other).suffix.lower()
                valid=(suffix=='.png' and image.startswith(bytes.fromhex('89504e470d0a1a0a')) or suffix in ('.jpg','.jpeg') and image.startswith(bytes.fromhex('ffd8ff')) or suffix=='.gif' and image.startswith((b'GIF87a',b'GIF89a')) or suffix=='.webp' and image[:4]==b'RIFF' and image[8:12]==b'WEBP' or suffix=='.avif' and b'ftyp' in image[:16] and (b'avif' in image[:32] or b'avis' in image[:32]))
                if not valid: raise ValueError('Le contenu de l’image ne correspond pas à son format.')
                markdown=z.read(indexes[0])
                if len(markdown)>2*1024*1024: raise ValueError('Article trop volumineux.')
                markdown.decode('utf-8')
                target=site/'content/blog'/folder
                if target.exists(): raise ValueError('Cet article existe déjà : modification en place non disponible dans ce prototype.')
                target.mkdir(); (target/'index.md').write_bytes(markdown); (target/Path(other).name).write_bytes(image)
        except (zipfile.BadZipFile,UnicodeError,RuntimeError) as e:
            raise ValueError('ZIP illisible : '+str(e))
        rows=[r for r in content() if r['path'].replace('\\','/').endswith('/'+folder+'/index.md')]
        if len(rows)!=1: raise ValueError('Article non reconnu par Hugo.')
        row=rows[0]
        if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',row['slug']) or row['slug'] in existing:
            raise ValueError('Adresse absente, invalide ou déjà utilisée ; aucun article existant ne sera écrasé.')
        path=urlsplit(row['permalink']).path
        if path!='/blog/'+row['slug']+'/': raise ValueError('Adresse canonique inattendue.')
        publication=datetime.datetime.fromisoformat(row['publishDate'].replace('Z','+00:00'))
        if publication.tzinfo is None: raise ValueError('Fuseau horaire absent.')
        draft=row['draft']=='true'; future=publication>datetime.datetime.now(datetime.timezone.utc)
        return {'path':path,'file':Path('blog')/row['slug']/'index.html','image':Path(other).name,
                'image_bytes':image,'draft':draft,'future':future,'date':publication,
                'state':'draft' if draft else 'scheduled' if future else 'ready'}
    def run(self, request):
        if not self.lock.acquire(blocking=False):
            raise ValueError('Un test est déjà en cours. Réessayez après son résultat.')
        before = self.fingerprint()
        try:
            if not isinstance(request,dict) or request.get('kind') not in ('rubric','article') or set(request)!=({'kind','patch'} if request.get('kind')=='rubric' else {'kind','zip_base64'}):
                raise ValueError('Demande de test inconnue.')
            patch=validate_patch(request['patch']) if request['kind']=='rubric' else None
            original=(self.root/'data/blog_editorial.json').read_bytes()
            if patch and hashlib.sha256(original).hexdigest()!=patch['base_config_sha256']:
                raise ValueError('Conflit : actualisez l’état du blog avant de refaire ce test.')
            cfg=validate_config({**load_json(original.decode()),**(patch['changes'] if patch else {})})
            SCRATCH.mkdir(parents=True, exist_ok=True)
            if shutil.disk_usage(SCRATCH).free < 300*1024*1024:
                raise ValueError('Espace de travail insuffisant pour une prévisualisation isolée.')
            work = Path(tempfile.mkdtemp(prefix='m15-connected-', dir=SCRATCH))
            site = work/'site'; site.mkdir()
            for folder in ['content', 'layouts', 'static', 'data']:
                shutil.copytree(self.root/folder, site/folder)
            shutil.copy2(self.root/'hugo.toml', site/'hugo.toml')
            out = work/'public'
            checks = []
            def command(name, argv):
                p = subprocess.run(argv, capture_output=True, text=True, timeout=120)
                if p.returncode:
                    raise ValueError(name+' : '+(p.stdout+p.stderr)[-2500:])
                checks.append({'name':name,'status':'passed'})
            command('Construction Hugo de référence', ['hugo','--source',str(site),'--destination',str(work/'reference')])
            cat = load_json((work/'reference/blog/catalogue-editorial.json').read_text())
            known = {a['path'] for a in cat['articles']}
            if patch and 'article_paths' in patch['changes'] and any(p not in known for p in cfg['article_paths']):
                raise ValueError('Sélection non publiable : actualisez les articles disponibles.')
            article=self.install_article(site,request['zip_base64']) if request['kind']=='article' else None
            (site/'data/blog_editorial.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
            server = ThreadingHTTPServer(('127.0.0.1',0), partial(SafeFiles,directory=str(out)))
            base = 'http://127.0.0.1:'+str(server.server_port)
            try:
                command('Construction Hugo avec vos modifications', ['hugo','--source',str(site),'--destination',str(out),'--baseURL',base+'/'])
                rendered = load_json((out/'blog/catalogue-editorial.json').read_text())
                if rendered['config'] != cfg:
                    raise ValueError('Les réglages générés ne correspondent pas aux réglages demandés.')
                rows=RubricHTML((out/'blog/index.html').read_text()).rows
                visible=[p for p in cfg['article_paths'] if p in known]
                if cfg['enabled'] and visible:
                    if len(rows)!=1 or rows[0]['title']!=cfg['title']:
                        raise ValueError('Titre réel du blog incorrect.')
                    if rows[0]['links']!=visible:
                        raise ValueError('Sélection ou ordre réel des cartes incorrect.')
                    if len(rows[0]['labels'])!=2 or any(not s.startswith(cfg['title']+' : ') for s in rows[0]['labels']):
                        raise ValueError('Libellés accessibles des flèches incorrects.')
                elif rows:
                    raise ValueError('La rubrique vide ou désactivée apparaît encore.')
                checks.append({'name':'Titre, sélection, ordre et flèches vérifiés dans le vrai HTML','status':'passed'})
                for script, label in [('check-navigation-recette.py','Navigation'),('check-article-next.py','Relations entre articles M22–M25'),('check-recette-visual-notes.py','Gabarits et notes validés')]:
                    command(label,['python',str(self.root/'scripts'/script),str(out)])
                if article:
                    included=not article['draft'] and not article['future']
                    if (out/article['file']).exists()!=included:
                        raise ValueError('Le statut ou la date de publication ne masque pas correctement cet article.')
                    for public_file in [out/'blog/index.html',out/'index.xml',out/'sitemap.xml',out/'blog/catalogue-editorial.json']:
                        if not included and public_file.exists() and article['path'] in public_file.read_text():
                            raise ValueError('Un contenu non publiable fuit dans une liste publique.')
                    checks.append({'name':'Statut et date respectés dans le build public','status':'passed'})
                    if article['future'] and not article['draft']:
                        later=work/'after-date'
                        clock=(article['date']+datetime.timedelta(seconds=1)).isoformat()
                        command('Simulation de la date future avec Hugo', ['hugo','--source',str(site),'--destination',str(later),'--clock',clock])
                        if not (later/article['file']).is_file(): raise ValueError('Article absent après son échéance simulée.')
                        checks.append({'name':'Article présent après échéance simulée','status':'passed'})
                    if not included:
                        # This output is a private loopback preview, never a deployable public artifact.
                        command('Prévisualisation privée des brouillons et articles futurs', ['hugo','--source',str(site),'--destination',str(out),'--baseURL',base+'/','--buildDrafts','--buildFuture'])
                    html=(out/article['file']).read_text()
                    image_file=out/'blog'/article['file'].parts[1]/article['image']
                    if not image_file.is_file() or image_file.read_bytes()!=article['image_bytes'] or article['image'] not in html:
                        raise ValueError('Image absente ou différente dans la page générée.')
                    checks.append({'name':'Page réelle et image locale vérifiées','status':'passed'})
                if self.fingerprint() != before:
                    raise ValueError('Les sources ont changé pendant le test ; relancez sur leur nouvel état.')
                checks.append({'name':'Sources du prototype conservées, aucune publication','status':'passed'})
            except Exception:
                server.server_close(); raise
            threading.Thread(target=server.serve_forever,daemon=True).start()
            self.servers.append(server)
            if len(self.servers)>4:
                old=self.servers.pop(0); old.shutdown(); old.server_close()
            report = {'id':uuid.uuid4().hex,'status':'success','kind':request['kind'],
                'at':datetime.datetime.now().astimezone().isoformat(),'checks':checks,
                'blog_url':base+'/blog/','preview_url':base+(article['path'] if article else '/blog/'),
                'message':'Test réussi — rien n’est publié. Prévisualisation locale isolée.',
                'base_config_sha256':hashlib.sha256(original).hexdigest(),
                'publication_state':article['state'] if article else None,
                'future_hidden':bool(article and article['future']),
                'publication_date':article['date'].isoformat() if article else None}
            (self.report_dir/(report['id']+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
            return report
        finally:
            self.lock.release()

def serve(port=1335):
    runner = PreviewRunner(ROOT)
    nonce = secrets.token_urlsafe(32)
    origin = 'http://127.0.0.1:'+str(port)
    class Handler(SafeFiles):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,directory=str(ROOT/'public'),**kwargs)
        def valid_host(self):
            return self.headers.get('Host') == '127.0.0.1:'+str(port)
        def reply(self, code, data):
            raw=json.dumps(data,ensure_ascii=False).encode()
            self.send_response(code); self.send_header('Content-Type','application/json; charset=utf-8')
            self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
        def do_GET(self):
            if not self.valid_host(): return self.reply(403,{'error':'Hôte non autorisé.'})
            if self.path == '/api/test-session':
                if self.headers.get('Origin',origin) != origin:
                    return self.reply(403,{'error':'Origine non autorisée.'})
                return self.reply(200,{'csrf':nonce,'capabilities':['rubric','article'],'publishes':False})
            if self.path.startswith('/api/'): return self.reply(404,{'error':'Route inconnue.'})
            return super().do_GET()
        def do_POST(self):
            if not self.valid_host() or self.headers.get('Origin') != origin or not hmac.compare_digest(self.headers.get('X-Atelier-CSRF',''),nonce):
                return self.reply(403,{'error':'Requête non autorisée. Rouvrez l’atelier connecté.'})
            if self.path != '/api/test': return self.reply(404,{'error':'Route inconnue.'})
            if self.headers.get('Content-Type','').split(';')[0] != 'application/json':
                return self.reply(415,{'error':'JSON attendu.'})
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=24*1024*1024: raise ValueError('Demande vide ou trop volumineuse.')
                raw=self.rfile.read(length)
                # Strict duplicate-key parsing is shared; article payload limit will be separate.
                def unique(pairs):
                    data={}
                    for k,v in pairs:
                        if k in data: raise ValueError('Clé JSON en double.')
                        data[k]=v
                    return data
                data=json.loads(raw.decode(),object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('Constante JSON invalide.')))
                report=runner.run(data)
                return self.reply(200,report)
            except (ValueError, UnicodeError) as e: return self.reply(422,{'error':str(e)})
            except (OSError,subprocess.SubprocessError) as e: return self.reply(500,{'error':'Test interrompu : '+str(e)})
    httpd=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    print('Atelier de test : '+origin+'/atelier-article/ ; aucune API de publication.',flush=True)
    try: httpd.serve_forever()
    finally: httpd.server_close(); runner.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--port',type=int,default=1335)
    serve(parser.parse_args().port)
