"""Local Git publication primitive. No credentials in this module; uses the workstation SSH agent."""
import base64, hashlib, io, json, os, re, secrets, subprocess, threading, time, zipfile
from pathlib import Path
from editorial_config import load_json, validate_config, validate_patch

REMOTE='git@github.com:Marguerite-by-Kissari/kissari-site.git'
LIMIT=16*1024*1024

def allowed(path):
    return path=='data/blog_editorial.json' or bool(re.fullmatch(r'content/blog/[a-z0-9][a-z0-9-]*/(?:index\.md|[A-Za-z0-9][A-Za-z0-9._-]*\.(?:png|jpe?g|webp|gif|avif))',path))

class Publisher:
    def __init__(self,remote,state,name,email,env=None):
        self.remote=remote;self.state=Path(state);self.repo=self.state/'repository.git'
        self.name=name;self.email=email;self.env={**os.environ,**(env or {}),'GIT_TERMINAL_PROMPT':'0'}
        self.env.update(GIT_AUTHOR_NAME=name,GIT_COMMITTER_NAME=name,GIT_AUTHOR_EMAIL=email,GIT_COMMITTER_EMAIL=email)
        self.pending={};self.lock=threading.Lock()
    def git(self,*args,input=None,extra=None):
        p=subprocess.run(['git','--git-dir',str(self.repo),'-c','core.hooksPath='+os.devnull,*args],input=input,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**self.env,**(extra or {})},timeout=180)
        if p.returncode:raise ValueError('Git/SSH a refusé l’opération. Vérifiez connexion, agent, droit Write et conflit de version. Aucun forçage effectué.')
        return p.stdout
    def sync(self):
        self.state.mkdir(parents=True,exist_ok=True)
        if not self.repo.exists():
            self.git('init','--bare',str(self.repo));self.git('remote','add','origin',self.remote)
        if self.git('remote','get-url','origin').decode().strip()!=self.remote:raise ValueError('Dépôt inattendu : arrêt.')
        self.git('fetch','--filter=blob:none','--no-tags','--depth=1','origin','refs/heads/main')
        return self.git('rev-parse','FETCH_HEAD').decode().strip()
    def read(self,base,path):return self.git('show',base+':'+path)
    def prepare(self,base,files,message):
        if not re.fullmatch('[a-f0-9]{40,64}',base):raise ValueError('Révision invalide.')
        if not files or len(files)>4 or any(not allowed(p) for p in files):raise ValueError('Chemin ou nombre de fichiers interdit.')
        if sum(len(b) for b in files.values())>LIMIT:raise ValueError('Contenu limité à 16 Mio.')
        if not self.name.strip() or not self.email.strip() or any(c in self.name+self.email for c in '\r\n<>'):raise ValueError('Configurez le nom et le courriel Git sur ce poste.')
        if self.sync()!=base:raise ValueError('Conflit : le dépôt a changé. Actualisez avant de confirmer.')
        index=self.state/('index-'+secrets.token_hex(12));env={'GIT_INDEX_FILE':str(index)}
        try:
            self.git('read-tree',base,extra=env)
            for p,b in sorted(files.items()):
                sha=self.git('hash-object','-w','--stdin',input=b).decode().strip()
                self.git('update-index','--add','--cacheinfo','100644',sha,p,extra=env)
            tree=self.git('write-tree',extra=env).decode().strip()
            if tree==self.git('rev-parse',base+'^{tree}').decode().strip():raise ValueError('Aucune modification à envoyer.')
            commit=self.git('commit-tree',tree,'-p',base,input=(message+'\n').encode()).decode().strip()
        finally:
            index.unlink(missing_ok=True);Path(str(index)+'.lock').unlink(missing_ok=True)
        token=secrets.token_urlsafe(32);self.pending={token:(base,commit,time.monotonic()+300)}
        return {'token':token,'base':base,'commit':commit,'files':sorted(files),'expires_in':300,'status':'prepared'}
    def publish(self,token):
        pending=self.pending.pop(token,None)
        if not pending or pending[2]<time.monotonic():raise ValueError('Confirmation expirée : préparez de nouveau.')
        base,commit,_=pending
        if self.sync()!=base:raise ValueError('Conflit : une autre publication a changé main. Rien envoyé.')
        self.git('push','origin',commit+':refs/heads/main')
        remote=self.git('ls-remote','origin','refs/heads/main').decode().split()
        if not remote or remote[0]!=commit:raise ValueError('Envoi effectué mais confirmation distante incertaine : consulter GitHub avant de réessayer.')
        return {'status':'source_sent','commit':commit,'actions_url':'https://github.com/Marguerite-by-Kissari/kissari-site/actions','message':'Source enregistrée sur GitHub. Consulter le build et le déploiement ; ce statut ne signifie pas publié.'}

def article_files(encoded):
    if not isinstance(encoded,str) or len(encoded)>24*1024*1024:raise ValueError('Article trop volumineux.')
    raw=base64.b64decode(encoded,validate=True)
    if len(raw)>LIMIT:raise ValueError('ZIP trop volumineux.')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        infos=z.infolist();names=[i.filename for i in infos]
        if len(infos)!=2 or len(set(names))!=2 or sum(i.file_size for i in infos)>LIMIT:raise ValueError('Deux fichiers article/image attendus.')
        index=next((n for n in names if re.fullmatch(r'\d{2}-\d{2}-\d{4}-[a-z0-9-]+/index\.md',n)),None)
        if not index:raise ValueError('Structure article invalide.')
        folder=index.split('/')[0];other=next(n for n in names if n!=index)
        if '/' not in other or other.split('/')[0]!=folder or not allowed('content/blog/'+other):raise ValueError('Chemin média invalide.')
        for i in infos:
            if ((i.external_attr>>16)&0o170000)==0o120000:raise ValueError('Lien symbolique interdit.')
        md=z.read(index);image=z.read(other);text=md.decode('utf-8')
        if len(md)>2*1024*1024 or not text.startswith('---\n') or '\ndraft: false\n' not in text:raise ValueError('Choisissez « Validé — publier à la date choisie » avant de publier.')
        if any(tag not in ('callout','/callout') for tag in re.findall(r'{{[%<]\s*(/?[A-Za-z0-9_-]+)',text)):raise ValueError('Shortcode non autorisé.')
        suffix=Path(other).suffix.lower()
        valid=(suffix=='.png' and image.startswith(bytes.fromhex('89504e470d0a1a0a')) or suffix in ('.jpg','.jpeg') and image.startswith(bytes.fromhex('ffd8ff')) or suffix=='.gif' and image.startswith((b'GIF87a',b'GIF89a')) or suffix=='.webp' and image[:4]==b'RIFF' and image[8:12]==b'WEBP' or suffix=='.avif' and b'ftyp' in image[:16] and b'avif' in image[:32])
        if not valid:raise ValueError('Format réel de l’image invalide.')
        return {'content/blog/'+index:md,'content/blog/'+other:image}

def rubric_files(pub,base,patch):
    patch=validate_patch(patch);old=pub.read(base,'data/blog_editorial.json')
    if hashlib.sha256(old).hexdigest()!=patch['base_config_sha256']:raise ValueError('Réglages distants modifiés. Actualisez l’état du blog avant publication.')
    new=validate_config({**load_json(old.decode()),**patch['changes']})
    return {'data/blog_editorial.json':(json.dumps(new,ensure_ascii=False,indent=2)+'\n').encode()}
