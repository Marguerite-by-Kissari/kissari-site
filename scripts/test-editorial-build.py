"""M15 builds in a throwaway copy; never alters the delivered configuration."""
from pathlib import Path
import json,shutil,subprocess,tempfile
root=Path(__file__).resolve().parents[1]
work=Path(tempfile.mkdtemp(prefix='m15-build-test-',dir=Path.home()/'.hermes/cache/scratch'))
site=work/'site';site.mkdir()
for folder in ['content','layouts','static','data']:shutil.copytree(root/folder,site/folder)
shutil.copy2(root/'hugo.toml',site/'hugo.toml')
config=json.loads((site/'data/blog_editorial.json').read_text())
def build(label,cfg,flags=()):
    (site/'data/blog_editorial.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
    out=work/label
    p=subprocess.run(['hugo','--source',str(site),'--destination',str(out),*flags],capture_output=True,text=True)
    assert p.returncode==0,p.stdout+p.stderr
    return out
out=build('normal',config)
assert (out/'blog/catalogue-editorial.json').is_file(),'M15: catalogue public non généré'
cat=json.loads((out/'blog/catalogue-editorial.json').read_text())
assert len(cat['articles'])==5
html=(out/'blog/index.html').read_text()
assert 'id="editorial-title"' in html and 'Zoom sur le marketing learning' in html
section=html.split('id="editorial-title"',1)[1].split('</section>',1)[0]
positions=[section.index('href="'+p+'"') for p in config['article_paths']]
assert positions==sorted(positions)
print('PASS normal catalogue, stable DOM id, three selected articles in order')
for label,edit in [('empty',{'article_paths':[]}),('disabled',{'enabled':False}),('missing',{'article_paths':['/blog/missing/']})]:
    out=build(label,{**config,**edit})
    assert 'id="editorial-title"' not in (out/'blog/index.html').read_text()
    print('PASS',label,'hidden, no all-article fallback')
out=build('literal',{**config,'title':"l'actu <script>alert(1)</script>"})
h=(out/'blog/index.html').read_text();assert '<script>alert(1)</script>' not in h and '&lt;script&gt;' in h
print('PASS free title escaped as text')
for slug,extra in [('qa-draft','draft: true'),('qa-future','publishDate: "2099-01-01"')]:
    (site/f'content/blog/{slug}.md').write_text(f'---\ntitle: {slug}\nslug: {slug}\ncategories: [outils]\nimage: images/blog/photo-femme.png\n{extra}\n---\n\nFixture privée de contrôle.\n')
out=build('preview',config,['--buildDrafts','--buildFuture'])
cat=json.loads((out/'blog/catalogue-editorial.json').read_text())
assert len(cat['articles'])==5 and all('qa-' not in a['path'] for a in cat['articles'])
print('PASS catalogue excludes draft/future even in a preview build')
print('QA artifacts:',work)
