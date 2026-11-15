"""Build personal pilot packages. Personal archives contain explicitly authorized no-passphrase SSH keys."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,struct,zipfile
ROOT=Path(__file__).resolve().parents[1]
DOC=Path('/mnt/datas/obsidian-vault/10-Projets/20-Sociétés/10-KISS-ARI/site-web-hugo/V1')
PRIVATE=Path.home()/'.hermes/private-deliveries/kissari'
KEYS=PRIVATE/'key-material'
VERSION='2026.11.15-pilote1'
COMMON='''# Atelier Kissari — package pilote personnel

Ce package installe l’atelier et **une clé SSH privée sans phrase secrète**, personnelle, selon le choix explicite d’Eric. Toute personne qui possède ce ZIP peut utiliser cette identité tant que la clé est autorisée. Ne pas envoyer ce ZIP à Marguerite, le déposer sur GitHub, un site public ou Discord. Transfert privé par Eric uniquement. Ne pas échanger les deux packages.

## Pré-requis
Python 3.10 ou plus récent (python.org), Git (git-scm.com) et OpenSSH. Aucun Hugo ni Node n’est nécessaire pour la publication depuis ce poste. Le package ne télécharge/installe pas silencieusement ces dépendances et ne demande pas d’accès administrateur pour copier l’atelier. Une dépendance manquante doit être installée explicitement.

## Installation
Décompresser d’abord le ZIP dans un dossier local privé, puis utiliser Installer.cmd sous Windows ou Installer.command sur Mac. L’installateur copie l’application dans le profil utilisateur et la clé privée sans phrase secrète dans ~/.ssh, sans écraser une autre identité existante. Ne jamais supprimer ~/.ssh pour dépanner.

Le lanceur Demarrer utilise directement la clé personnelle, sans demande de mot de passe SSH, puis ouvre l’atelier dans le navigateur sur 127.0.0.1:1345. La première fois, saisir le courriel Git public/noreply relevé dans GitHub Settings/Emails. Fermer le terminal ou Ctrl+C arrête le service local. Ne pas lancer un autre serveur sur le même port.

Sur Windows, le client OpenSSH Windows doit être disponible. Le service ssh-agent n’est pas nécessaire : la clé est lue directement. Le lanceur n’élève pas ses privilèges et ne modifie pas les services système.

Sur macOS, /usr/bin/ssh lit directement la clé ; ssh-add et le démarrage d’un agent ne sont pas nécessaires. Git peut demander l’installation des outils Apple Command Line Tools. Si Finder refuse un .command, ouvrir par clic droit/Ouvrir selon la politique du poste ; le package ne désactive pas Gatekeeper.

## Publier un article
1. Lancer l’atelier, rédiger et charger une image. Conserver les sauvegardes locales et exporter un ZIP de secours.
2. Vérifier titre, texte, auteur, catégorie et date/heure Paris. Choisir « Validé — publier à la date choisie », pas Brouillon.
3. Cliquer **Publier sur le site** dans l’onglet article.
4. Vérifier la liste exacte des fichiers et confirmer. Annuler n’envoie rien.
5. Après « source enregistrée », ouvrir le lien du commit GitHub et vérifier les contrôles/le déploiement.
6. Ouvrir l’URL publique puis vérifier l’article. Un push réussi ne signifie jamais que le site est déjà à jour.

Pour la rubrique : modifier ses réglages puis son propre bouton **Publier sur le site**. Un conflit d’empreinte impose d’actualiser avant de reprendre ; il ne faut pas réexporter un ancien état pour contourner ce contrôle.

## Limites du pilote — à connaître avant utilisation réelle
- Accès Write et clé publique doivent être enregistrés sur le compte personnel ; workflow Pages à installer/recetter par Marguerite avec Eric. L’installateur ne crée aucun droit GitHub.
- Le moteur de publication et ses deux boutons sont implémentés ; essais réels de Git réalisés sur dépôt LOCAL de recette, pas sur GitHub avec vos identités.
- Tests Linux exécutés. Scripts Windows/macOS préparés avec contrôles de syntaxe, **pas encore exécutés sur vos deux OS**. Recette native indispensable avant de déclarer ces installations validées.
- Pas d’API GitHub privée dans le navigateur : les résultats CI se consultent via le compte GitHub authentifié.
- Le bouton « Tester sur le site » historique exige le service Hugo complet de développement ; il reste désactivé dans ce package léger. L’aperçu local et la CI après envoi sont distincts. Le test distant préalable sur branche n’est pas encore piloté par un bouton dans ce pilote.
- Création/publication d’articles et réglages de rubrique pris en charge. La réouverture depuis un article existant, la migration sans perte du Markdown historique et la restauration assistée sont des lots suivants ; ne pas recréer un ancien article sous un autre dossier pour le modifier.
- Le catalogue d’articles est un instantané de la génération du package ; les réglages et leur empreinte peuvent être actualisés depuis GitHub. Un article nouvellement publié peut manquer dans cette sélection jusqu’à mise à jour du catalogue/package.
- Articles futurs : dépendent du schedule du workflow effectivement actif. Pas de programmation autonome si Marguerite ne l’a pas installé ; une date seule ne crée pas de timer.
- Git bare avec blobs différés : pas de clone de travail complet ni de Hugo local, mais métadonnées/objets Git dans ~/.kissari-atelier. Le cache peut croître au fil des articles.

## Sécurité et support
Aucun secret dans le HTML, localStorage, les exports d’article ou Git. La clé n’a pas de phrase secrète et peut être utilisée directement. Les droits du fichier sont restreints ; le poste doit rester protégé (session verrouillée, accès disque contrôlé). Ne pas confondre ces droits avec un chiffrement de la clé. En cas de perte du ZIP ou du poste, révoquer la clé publique correspondante sur GitHub. Supprimer les copies de transfert seulement après installation/recette et validation d’Eric.

En cas d’accès refusé, vérifier invitation acceptée, compte, clé publique, présence du fichier privé et permissions. En cas de conflit, conserver le brouillon, arrêter et demander assistance : aucun force-push. En cas de coupure après confirmation, vérifier le commit distant avant de réessayer.
'''
WIN_START='''$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
if (Get-Command py -ErrorAction SilentlyContinue) { & py -3 (Join-Path $root 'atelier_service.py') --root $root } else { & python (Join-Path $root 'atelier_service.py') --root $root }
Read-Host 'Entrée pour fermer'
'''
WIN_CMD='''@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Demarrer.ps1"
'''
WIN_INSTALL='''@echo off
where py >nul 2>nul
if %errorlevel%==0 (py -3 "%~dp0install.py") else (python "%~dp0install.py")
pause
'''
MAC_START='''#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo 'Installer Python 3 depuis python.org'; read -r; exit 1; }
/usr/bin/git --version >/dev/null
python3 atelier_service.py --root "$PWD"
'''
MAC_INSTALL='''#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo 'Installer Python 3 depuis python.org'; read -r; exit 1; }
python3 install.py
'''

def put(path,content,mode=0o600):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8');path.chmod(mode)

def zip_folder(folder,dest):
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for path in sorted(folder.rglob('*')):
            if path.is_file():z.write(path,str(Path(folder.name)/path.relative_to(folder)))
    dest.chmod(0o600)
    with zipfile.ZipFile(dest) as z:assert z.testzip() is None

def main():
    PRIVATE.mkdir(mode=0o700,parents=True,exist_ok=True);PRIVATE.chmod(0o700)
    stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S');run=PRIVATE/stamp;run.mkdir(mode=0o700)
    result=[]
    for who,platform,name in [('virginie','windows','Virginie'),('christelle','macos','Christelle')]:
        folder=run/f'Kissari-{name}-{platform}-{VERSION}';app=folder/'application';app.mkdir(parents=True,mode=0o700)
        for filename in ['atelier_service.py','publication_bridge.py','editorial_config.py']:shutil.copyfile(ROOT/'scripts'/filename,app/filename)
        shutil.copyfile(ROOT/'livrables/atelier-editorial-kissari-autonome.html',app/'index.html')
        shutil.copyfile(ROOT/'livrables/catalogue-editorial.json',app/'catalogue-editorial.json')
        shutil.copyfile(ROOT/'deployment/github_known_hosts',app/'github_known_hosts');put(app/'ssh-empty.conf','')
        put(app/'profile.json',json.dumps({'profile':who,'name':name,'platform':platform,'email':'','version':VERSION},ensure_ascii=False,indent=2)+'\n')
        shutil.copyfile(ROOT/'deployment/install.py',folder/'install.py')
        put(folder/'LIRE-MOI.md',COMMON)
        if platform=='windows':
            put(app/'Demarrer.ps1',WIN_START);put(app/'Demarrer.cmd',WIN_CMD);put(folder/'Installer.cmd',WIN_INSTALL)
        else:
            put(app/'Demarrer.command',MAC_START,0o700);put(folder/'Installer.command',MAC_INSTALL,0o700)
        keyname='id_ed25519_kissari_'+who;key=KEYS/who/keyname
        # The delivery policy explicitly requires an unencrypted OpenSSH identity.
        import base64
        binary=base64.b64decode(b''.join(key.read_bytes().splitlines()[1:-1]));off=len(b'openssh-key-v1\0');n=struct.unpack('>I',binary[off:off+4])[0];cipher=binary[off+4:off+4+n]
        assert cipher==b'none','Delivery key must not require a passphrase'
        (folder/'cle').mkdir(mode=0o700)
        for f in [key,Path(str(key)+'.pub')]:shutil.copyfile(f,folder/'cle'/f.name);(folder/'cle'/f.name).chmod(0o600)
        manifest={str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.rglob('*') if p.is_file()}
        put(folder/'manifest-sha256.json',json.dumps(manifest,indent=2)+'\n')
        archive=run/(folder.name+'.zip');zip_folder(folder,archive)
        result.append({'person':name,'platform':platform,'archive':str(archive),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'private_key_encrypted':False,'passphrase_required':False,'native_os_tested':False})
    public=DOC/'Remise-Marguerite-GitHub';public.mkdir(exist_ok=True)
    shutil.copyfile(DOC/'Marguerite - Configuration GitHub et droits des redactrices.md',public/'INSTRUCTIONS-MARGUERITE.md')
    shutil.copyfile(ROOT/'deployment/kissari-pages.yml',public/'kissari-pages.yml')
    for who in ['virginie','christelle']:
        keyname='id_ed25519_kissari_'+who+'.pub';shutil.copyfile(KEYS/who/keyname,public/keyname)
    assert all(b'PRIVATE KEY' not in p.read_bytes() for p in public.iterdir() if p.is_file())
    put(run/'recu.json',json.dumps({'packages':result,'status':'PILOTE - validation GitHub et OS natifs restante','public_handover':str(public)},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'packages':result,'public_handover':str(public),'receipt':str(run/'recu.json')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
