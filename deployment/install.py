"""Install a personal atelier package without overwriting other SSH identities."""
import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path

def install(source,target,home,windows=False):
    profile=json.loads((source/'application/profile.json').read_text(encoding='utf-8'))
    who=profile['profile']
    if who not in ('virginie','christelle'):raise ValueError('Package personnel inconnu.')
    ssh=home/'.ssh';ssh.mkdir(mode=0o700,parents=True,exist_ok=True)
    name='id_ed25519_kissari_'+who
    key=ssh/name
    incoming=source/'cle'/name
    # Copy only the named personal identity; never print private-key bytes.
    if key.exists() and hashlib.sha256(key.read_bytes()).digest()!=hashlib.sha256(incoming.read_bytes()).digest():raise ValueError('Une autre clé existe déjà à cet emplacement. Arrêt sans écrasement.')
    if not key.exists():shutil.copyfile(incoming,key)
    shutil.copyfile(source/'cle'/(name+'.pub'),ssh/(name+'.pub'))
    key.chmod(0o600)
    if windows:
        account=subprocess.check_output(['whoami'],text=True).strip()
        subprocess.run(['icacls',str(key),'/inheritance:r','/grant:r',account+':F'],check=True,stdout=subprocess.DEVNULL)
        ssh_exe=Path(os.environ['WINDIR'])/'System32/OpenSSH/ssh.exe'
        if not ssh_exe.is_file():raise ValueError('Installer le client OpenSSH Windows avant de lancer l’atelier.')
        profile['ssh']=str(ssh_exe)
    target.mkdir(parents=True,exist_ok=True)
    old=target/'profile.json'
    if old.exists():profile['email']=json.loads(old.read_text(encoding='utf-8')).get('email','')
    for item in (source/'application').iterdir():
        if item.name!='profile.json' and item.is_file():shutil.copyfile(item,target/item.name)
    old.write_text(json.dumps(profile,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not windows:(target/'Demarrer.command').chmod(0o700)
    return target

def main():
    here=Path(__file__).resolve().parent;profile=json.loads((here/'application/profile.json').read_text(encoding='utf-8'))
    expected=profile['platform']
    if (expected=='windows' and sys.platform!='win32') or (expected=='macos' and sys.platform!='darwin'):raise SystemExit('Ce package est prévu pour '+expected+', pas pour ce système.')
    if not shutil.which('git'):raise SystemExit('Installez Git depuis git-scm.com, puis relancez.')
    home=Path.home()
    target=(Path(os.environ['LOCALAPPDATA'])/'KissariAtelier') if sys.platform=='win32' else home/'Library/Application Support/KissariAtelier'
    result=install(here,target,home,sys.platform=='win32')
    print('Atelier et clé SSH sans phrase secrète installés dans votre compte utilisateur. Aucun accès GitHub accordé par cette installation.')
    print('Application : '+str(result))
    print('Démarrer : '+str(result/('Demarrer.cmd' if sys.platform=='win32' else 'Demarrer.command')))
    print('Aucune phrase secrète SSH requise. Protégez le poste et le package de transfert.')
    input('Appuyez sur Entrée pour fermer. ')
if __name__=='__main__':main()
