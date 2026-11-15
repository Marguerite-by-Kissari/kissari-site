"""Regression: inline notes in body and all callout variants, in an isolated Hugo site."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
work = Path(tempfile.mkdtemp(prefix='kissari-inline-notes-', dir=Path.home()/'.hermes/cache/scratch'))
site = work/'site'
site.mkdir()
for name in ['layouts','content','static','data']:
    shutil.copytree(root/name, site/name)
shutil.copy2(root/'hugo.toml', site/'hugo.toml')
body = '''---
title: Notes regression
slug: notes-regression
categories: [jusdecerveau]
image: images/blog/photo-femme.png
---
Body reference[^note-body], repeated[^note-body].

'''
for color in ['pink','yellow','black']:
    body += '{{< callout color="'+color+'" title="Test '+color+'" >}}\n'
    body += 'A **formatted** reference[^note-'+color+'].\n{{< /callout >}}\n\n'
for label in ['body','pink','yellow','black']:
    body += '[^note-'+label+']: Definition '+label+'.\n    Continuation '+label+'.\n\n'
(site/'content/blog/notes-regression.md').write_text(body)
subprocess.run(['hugo','--source',str(site),'--destination',str(work/'out')], check=True)
html=(work/'out/blog/notes-regression/index.html').read_text()
assert '[^note-' not in html, 'Unresolved reference'
assert html.count('class="footnote-ref"') == 5
assert html.count('class="footnote-backref"') == 5
ids=re.findall(r' id="([^"]+)"',html)
assert len(ids)==len(set(ids)), 'Duplicate note IDs'
references=re.findall(r'<a href="#fn:([^"]+)" class="footnote-ref"[^>]*>(\d+)</a>',html)
assert [n for _,n in references] == ['1','1','2','3','4'], references
for target,number in references:
    assert re.search(r'<li id="fn:'+re.escape(target)+r'" tabindex="-1"><a class="footnote-number"[^>]*>'+number+r'</a>',html), (target,number)
for tag in re.findall(r'<sup id="fnref[^"]*"[^>]*>',html):
    assert 'tabindex="-1"' in tag, tag
for color in ['pink','yellow','black']:
    assert 'Definition '+color+'.' in html
    assert html.index('Definition '+color+'.') > html.rindex('</aside>'), 'Note is inside a callout'
    assert 'Continuation '+color+'.' in html
print('PASS 4 globally numbered notes, 5 references including a repeat, callouts, return targets, multiline definitions and unique IDs')
print('Artifacts:',work)
