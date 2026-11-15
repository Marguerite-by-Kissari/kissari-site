"""Check an actual Atelier ZIP in an isolated Hugo copy, never in live content.
Usage: python scripts/check-atelier-bundle.py /path/to/export.zip
"""
from pathlib import Path
import argparse
import hashlib
import re
import shutil
import subprocess
import tempfile
import zipfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('archive', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
scratch = Path.home() / '.hermes/cache/scratch'
scratch.mkdir(parents=True, exist_ok=True)
work = Path(tempfile.mkdtemp(prefix='kissari-bundle-qa-', dir=scratch))
site = work / 'site'
site.mkdir()
for name in ['content', 'layouts', 'static', 'data']:
    shutil.copytree(root / name, site / name)
shutil.copy2(root / 'hugo.toml', site / 'hugo.toml')
with zipfile.ZipFile(args.archive) as z:
    names = z.namelist()
    assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names)
    assert len(names) == len(set(names)), 'Duplicate ZIP entries'
    indexes = [n for n in names if n.endswith('/index.md')]
    assert len(indexes) == 1, names
    bundle_name = indexes[0].split('/')[0]
    assert re.fullmatch(r'\d{2}-\d{2}-\d{4}-[a-z0-9-]+', bundle_name)
    assert not (site / 'content/blog' / bundle_name).exists(), 'Bundle already exists'
    z.extractall(site / 'content/blog')
bundle = site / 'content/blog' / bundle_name
article = bundle / 'index.md'
text = article.read_text()
slug = re.search(r'^slug: "([a-z0-9-]+)"$', text, re.M)[1]
image = re.search(r'^image: "([^"/]+)"$', text, re.M)[1]
assert (bundle / image).is_file()
assert text.count('\n---') == 1
assert not (site / 'content/blog' / slug).exists()

def build(label, draft=False):
    out = work / label
    cmd = ['hugo', '--source', str(site), '--destination', str(out), '--baseURL', 'http://localhost:1314/']
    if draft:
        cmd.append('--buildDrafts')
    result = subprocess.run(cmd, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    return out

# Exercise the real exported status, then both states and a future publication.
original_draft = 'draft: true' in text
out = build('export-status')
assert (out / 'blog' / slug / 'index.html').exists() != original_draft
print('PASS actual export status')
ready = re.sub(r'^draft: (true|false)$', 'draft: false', text, flags=re.M)
article.write_text(ready)
out = build('ready')
page = (out / 'blog' / slug / 'index.html').read_text()
listing = (out / 'blog/index.html').read_text()
image_url = f'/blog/{slug}/{image}'
assert f'src="{image_url}"' in page
assert f'src="{image_url}"' in listing
assert f'href="/blog/{slug}/"' in listing
assert hashlib.sha256((out / 'blog' / slug / image).read_bytes()).digest() == hashlib.sha256((bundle / image).read_bytes()).digest()
for old in root.glob('content/blog/*.md'):
    if old.name != '_index.md':
        assert (out / 'blog' / old.stem / 'index.html').exists()
for old in root.glob('content/blog/*.md'):
    if old.name != '_index.md':
        legacy = re.search(r'^image: "([^"]+)"$', old.read_text(), re.M)
        if legacy:
            assert f'src="/{legacy[1]}"' in listing
print('PASS ready page, card, local image bytes, clean URL, legacy articles and images')
article.write_text(ready.replace('draft: false', 'draft: true'))
out = build('draft')
assert not (out / 'blog' / slug / 'index.html').exists()
assert f'href="/blog/{slug}/"' not in (out / 'blog/index.html').read_text()
out = build('draft-preview', draft=True)
assert (out / 'blog' / slug / 'index.html').exists()
print('PASS draft excluded from normal build, visible with --buildDrafts')
article.write_text(re.sub(r'^publishDate:.*$', 'publishDate: "2099-01-01"', ready, flags=re.M))
out = build('future')
assert not (out / 'blog' / slug / 'index.html').exists()
assert f'href="/blog/{slug}/"' not in (out / 'blog/index.html').read_text()
print('PASS future publication excluded')
print('QA artifacts:', work)
