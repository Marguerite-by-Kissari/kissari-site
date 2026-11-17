"""Build the public artifact without activating or contacting GitHub Pages."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', default='public')
    args = parser.parse_args()
    destination = Path(args.destination).resolve()
    if destination == ROOT or ROOT.is_relative_to(destination):
        raise SystemExit('Refusing an unsafe destination')
    subprocess.run(['hugo', '--source', str(ROOT), '--minify', '--cleanDestinationDir',
                    '--destination', str(destination)], check=True, cwd=ROOT)
    subprocess.run(['python3', str(ROOT / 'scripts/check-navigation-recette.py'), str(destination)], check=True, cwd=ROOT)
    shutil.rmtree(destination / 'atelier-article', ignore_errors=True)
    sha = os.environ.get('GITHUB_SHA') or subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    (destination / 'deployment.json').write_text(json.dumps({'source_commit': sha}) + '\n')
    subprocess.run(['python3', str(ROOT / 'scripts/check-production-artifact.py'), str(destination)], check=True, cwd=ROOT)

if __name__ == '__main__':
    main()
