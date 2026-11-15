"""On-demand loopback publication service; serves no repository or key files."""
import argparse, hashlib, hmac, json, os, secrets, shlex, shutil, sys, webbrowser, zipfile, subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from publication_bridge import Publisher, REMOTE, article_files, rubric_files

def make_server(root,config,port=1345):
    root=Path(root).resolve();csrf=secrets.token_urlsafe(32)
    name=config.get('name','');email=config.get('email','')
    who=config.get('profile','');state=Path.home()/'.kissari-atelier'/who
    env={}
    if who:
        key=Path.home()/'.ssh'/('id_ed25519_kissari_'+who)
        known=root/'github_known_hosts';ssh=config.get('ssh',shutil.which('ssh') or 'ssh')
        empty=root/'ssh-empty.conf'
        env['GIT_SSH_COMMAND']=' '.join(shlex.quote(str(x)) for x in [ssh,'-F',empty,'-i',key,'-o','IdentitiesOnly=yes','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(known)])
    pub=Publisher(REMOTE,state,name,email,env)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def own(self):return 'http://127.0.0.1:'+str(self.server.server_port)
        def host_ok(self):return self.headers.get('Host')=='127.0.0.1:'+str(self.server.server_port)
        def send(self,status,data,kind='application/json; charset=utf-8'):
            raw=data if isinstance(data,bytes) else json.dumps(data,ensure_ascii=False).encode()
            self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(raw)))
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('X-Frame-Options','DENY');self.send_header('Referrer-Policy','no-referrer');self.end_headers();self.wfile.write(raw)
        def do_GET(self):
            if not self.host_ok() or self.headers.get('Origin',self.own())!=self.own():return self.send(403,{'error':'Origine refusée.'})
            if self.path in ('/','/atelier-article/','/atelier-article/index.html'):
                return self.send(200,(root/'index.html').read_bytes(),'text/html; charset=utf-8')
            if self.path=='/api/publication/session':return self.send(200,{'csrf':csrf,'name':name,'configured':bool(name and email and who),'capabilities':['article','rubric'],'repository':REMOTE})
            if self.path=='/blog/catalogue-editorial.json':
                if not pub.lock.acquire(blocking=False):return self.send(409,{'error':'Opération déjà en cours.'})
                try:
                    base=pub.sync();raw=pub.read(base,'data/blog_editorial.json')
                    catalogue=json.loads((root/'catalogue-editorial.json').read_text(encoding='utf-8'));catalogue['config']=json.loads(raw);catalogue['base_config_sha256']=hashlib.sha256(raw).hexdigest()
                    catalogue['generated_at']='réglages GitHub à jour ; liste articles : instantané du package'
                    return self.send(200,catalogue)
                except (ValueError,OSError):return self.send(409,{'error':'Actualisation GitHub impossible. Vérifiez la configuration et l’agent SSH.'})
                finally:pub.lock.release()
            return self.send(404,{'error':'Ressource non disponible dans le package.'})
        def do_POST(self):
            if not self.host_ok() or self.headers.get('Origin')!=self.own() or not hmac.compare_digest(self.headers.get('X-Atelier-CSRF',''),csrf):return self.send(403,{'error':'Origine ou session refusée.'})
            if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.send(415,{'error':'JSON requis.'})
            try:length=int(self.headers.get('Content-Length','0'))
            except ValueError:return self.send(400,{'error':'Taille invalide.'})
            if not 0<length<=24*1024*1024:return self.send(413,{'error':'Requête limitée à 24 Mio.'})
            if not pub.lock.acquire(blocking=False):return self.send(409,{'error':'Une publication est déjà en cours.'})
            try:
                payload=json.loads(self.rfile.read(length))
                if not isinstance(payload,dict):raise ValueError('Objet JSON requis.')
                if self.path=='/api/publication/prepare':
                    if not name or not email or not who:raise ValueError('Complétez le profil avec le lanceur de configuration avant publication.')
                    base=pub.sync()
                    if payload.get('kind')=='article' and set(payload)=={'kind','zip_base64'}:files=article_files(payload['zip_base64'])
                    elif payload.get('kind')=='rubric' and set(payload)=={'kind','patch'}:files=rubric_files(pub,base,payload['patch'])
                    else:raise ValueError('Demande inconnue.')
                    return self.send(200,pub.prepare(base,files,'Publication atelier — '+name))
                if self.path=='/api/publication/publish' and set(payload)=={'token'}:return self.send(200,pub.publish(payload['token']))
                return self.send(404,{'error':'Action inconnue.'})
            except (ValueError,OSError,KeyError,TypeError,zipfile.BadZipFile,subprocess.TimeoutExpired) as e:return self.send(409,{'error':str(e)[:350]})
            finally:pub.lock.release()
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);parser.add_argument('--port',type=int,default=1345);parser.add_argument('--setup',action='store_true');args=parser.parse_args()
    profile=args.root/'profile.json';config=json.loads(profile.read_text(encoding='utf-8-sig'))
    if args.setup or not config.get('email'):
        print('Configuration Git locale. Aucun mot de passe ni clé privée à saisir ici.')
        config['email']=input('Courriel Git (adresse publique ou noreply GitHub copiée depuis Settings/Emails) : ').strip()
        if not config['email'] or any(c in config['email'] for c in '\r\n<>'):raise SystemExit('Courriel Git manquant/invalide.')
        profile.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    server=make_server(args.root,config,args.port);url=f'http://127.0.0.1:{server.server_port}/atelier-article/'
    print('Atelier local : '+url+' — fermer avec Ctrl+C. La publication nécessite les accès GitHub et le workflow Pages actif.')
    webbrowser.open(url)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
if __name__=='__main__':main()
