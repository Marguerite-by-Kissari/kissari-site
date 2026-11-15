"""Exercise M22–M25 in an isolated Hugo copy, never in the user's articles."""
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
import tempfile

root=Path(__file__).resolve().parents[1]
work=Path(tempfile.mkdtemp(prefix='kissari-next-qa-',dir=Path.home()/'.hermes/cache/scratch'))
site=work/'site'
site.mkdir()
for name in ['content','layouts','static','data']:
    shutil.copytree(root/name,site/name)
shutil.copy2(root/'hugo.toml',site/'hugo.toml')

files=[
 'content/blog/30-10-2026-classe-virtuelle-la-modalite-qui-n-a-rien-d-un-plan-b/index.md',
 'content/blog/29-10-2026-avec-le-marketing-learning-place-a-l-action/index.md',
 'content/blog/marketing-learning-ne-sarrete-jamais.md',
 'content/blog/marketing-formation-avant-postes-engagement.md',
]
# Reorder all four dates and put them in another category in this copy only.
for index,name in enumerate(files):
    p=site/name
    front,body=p.read_text().split('\n---',1)
    date=f'200{index}-01-01'
    front=re.sub(r'(?m)^date:.*$',f'date: "{date}"',front)
    front=re.sub(r'(?m)^publishDate:.*$',f'publishDate: "{date}"',front)
    front=front.replace('  - "jusdecerveau"','  - "outils"')
    p.write_text(front+'\n---'+body)

# Preserve old fallback and static teasers for articles outside the approved lot.
for slug,date,category,extra in [
 ('qa-auto-first','2000-01-01','qa-auto',''),
 ('qa-auto-second','2000-01-02','qa-auto',''),
 ('qa-teaser','2000-01-01','qa-teaser','next_teaser: "Annonce conservée"\n'),
]:
    (site/f'content/blog/{slug}.md').write_text(f'---\ntitle: "{slug}"\nslug: "{slug}"\ndate: "{date}"\ncategories: ["{category}"]\nimage: "images/blog/photo-femme.png"\n{extra}---\n\nFixture de contrôle isolée.\n')

def build(label,should_fail=False):
    out=work/label
    r=subprocess.run(['hugo','--source',str(site),'--destination',str(out)],capture_output=True,text=True)
    (work/f'{label}.log').write_text(r.stdout+r.stderr)
    if should_fail:
        assert r.returncode!=0 and 'Article suivant explicite' in r.stdout+r.stderr,r.stdout+r.stderr
    else:
        assert r.returncode==0,r.stdout+r.stderr
    return out

out=build('reordered')
subprocess.run([sys.executable,str(root/'scripts/check-article-next.py'),str(out)],check=True)
print('PASS explicit choices survive reordered dates and changed categories; empty bands stay empty')
argv=sys.argv
sys.argv=[str(root/'scripts/check-article-next.py'),str(out)]
module=runpy.run_path(str(root/'scripts/check-article-next.py'))
sys.argv=argv
first=module['banner']('qa-auto-first')
assert any(tag=='a' and a.get('href')=='/blog/qa-auto-second/' for tag,a in first['children'])
teaser=module['banner']('qa-teaser')
assert 'Annonce conservée' in teaser['text'] and not any(tag=='a' for tag,_ in teaser['children'])
print('PASS untouched automatic fallback and non-clickable teaser')

action=site/files[1]
action_original=action.read_text()
action.write_text(action_original.replace('/blog/marketing-learning-ne-sarrete-jamais','/blog/qa-nonexistent'))
build('missing-target',should_fail=True)
action.write_text(action_original)
print('PASS missing explicit target blocks generation instead of creating a wrong link')
target=site/files[2]
target_original=target.read_text()
for label,changed in [
 ('draft-target',target_original.replace('draft: false','draft: true')),
 ('future-target',re.sub(r'(?m)^publishDate:.*$','publishDate: "2099-01-01"',target_original)),
]:
    target.write_text(changed)
    build(label,should_fail=True)
    target.write_text(target_original)
    print('PASS',label,'cannot become a dead public link')
print('QA artifacts:',work)
