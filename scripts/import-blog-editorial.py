"""Preview/apply an M15 export to THIS prototype only. Never deploys."""
import argparse,datetime,fcntl,hashlib,json,os,subprocess,tempfile
from pathlib import Path
from editorial_config import load_json,validate_config,validate_patch
ROOT=Path(__file__).resolve().parents[1]
SCRATCH=Path.home()/'.hermes/cache/scratch'
def atomic(path,raw):
    fd,name=tempfile.mkstemp(prefix='.editorial-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        os.replace(name,path)
    finally:
        if os.path.exists(name):os.unlink(name)
def catalogue():
    out=Path(tempfile.mkdtemp(prefix='m15-import-build-',dir=SCRATCH))
    r=subprocess.run(['hugo','--source',str(ROOT),'--destination',str(out)],capture_output=True,text=True)
    if r.returncode:raise ValueError('Build refusé : '+(r.stdout+r.stderr)[-2500:])
    return load_json((out/'blog/catalogue-editorial.json').read_text())
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export',type=Path);parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    patch=validate_patch(load_json(args.export.read_text(encoding='utf-8')))
    path=ROOT/'data/blog_editorial.json'
    with (ROOT/'.editorial-import.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        original=path.read_bytes();before=validate_config(load_json(original.decode()))
        digest=hashlib.sha256(original).hexdigest()
        if digest!=patch['base_config_sha256']:raise ValueError('Conflit : la configuration a changé. Recharger l’état actuel, sans forçage.')
        after=validate_config({**before,**patch['changes']})
        current=catalogue();known={a['path'] for a in current['articles']}
        missing=[p for p in after['article_paths'] if p not in known]
        if missing and 'article_paths' in patch['changes']:raise ValueError('Sélection non publiable : '+', '.join(missing))
        if missing:print('AVERTISSEMENT : références historiques indisponibles conservées',missing)
        print(json.dumps({'prototype':str(ROOT),'changes':patch['changes'],'apply':args.apply},ensure_ascii=False,indent=2))
        if not args.apply:
            print('DRY-RUN : aucun réglage modifié. Ajouter --apply pour intégrer dans cette copie.');return
        history=ROOT/'livrables/editorial-history';history.mkdir(parents=True,exist_ok=True)
        backup=history/(digest+'.json')
        if not backup.exists():backup.write_bytes(original)
        atomic(path,(json.dumps(after,ensure_ascii=False,indent=2)+'\n').encode())
        try:catalogue()
        except Exception:
            atomic(path,original);raise
        with (history/'journal.jsonl').open('a') as f:
            f.write(json.dumps({'at':datetime.datetime.now().astimezone().isoformat(),'before':digest,'after':hashlib.sha256(path.read_bytes()).hexdigest(),'changes':patch['changes']},ensure_ascii=False)+'\n')
        print('ENREGISTRÉ dans le prototype, build vérifié, NON PUBLIÉ. Régénérer le livrable avec build-editorial-prototype.py.')
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,json.JSONDecodeError) as e:raise SystemExit('REFUS : '+str(e))
