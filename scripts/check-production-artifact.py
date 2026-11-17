"""Validate the built public artifact, including local assets and SEO outputs."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

ORIGIN = 'https://kissari.com'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.canonicals, self.ids = [], [], set()
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonicals.append(a.get('href'))
        for attr in ('href', 'src', 'poster'):
            if a.get(attr):
                self.links.append(a[attr])


def check(build):
    errors, warnings = [], []
    pages = {}
    assert not (build / 'atelier-article').exists(), 'Atelier must not be shipped'
    for f in build.rglob('*.html'):
        rel = f.relative_to(build).as_posix()
        url = '/' + (rel[:-10] if rel.endswith('index.html') else rel)
        text = f.read_text()
        p = Page(text)
        pages[url] = p
        if p.canonicals != [ORIGIN + url]:
            errors.append(f'{url}: invalid canonical {p.canonicals}')
        if re.search(r'https?://(?:localhost|127\.0\.0\.1)(?::\d+)?', text):
            errors.append(f'{url}: local URL in public HTML')
        for link in p.links:
            parsed = urlsplit(link)
            if parsed.scheme == 'tel' and not re.fullmatch(r'\+?[0-9(). -]+', parsed.path):
                warnings.append(f'{url}: invalid telephone link {link}')
            absolute = urlsplit(urljoin(ORIGIN + url, link))
            if absolute.scheme not in ('http', 'https') or absolute.netloc != 'kissari.com':
                continue
            path = unquote(absolute.path)
            target = build / path.lstrip('/')
            if not target.exists():
                errors.append(f'{url}: missing local resource {path}')
            elif target.is_dir() and not (target / 'index.html').exists():
                errors.append(f'{url}: missing index {path}')
    for url, page in pages.items():
        for link in page.links:
            absolute = urlsplit(urljoin(ORIGIN + url, link))
            if absolute.netloc == 'kissari.com' and absolute.fragment and absolute.path in pages:
                if unquote(absolute.fragment) not in pages[absolute.path].ids:
                    errors.append(f'{url}: missing fragment {link}')
    tree = ET.parse(build / 'sitemap.xml')
    locations = [n.text for n in tree.findall('.//{*}loc')]
    assert locations, 'Empty sitemap'
    assert set(locations) == {ORIGIN + url for url in pages}, 'Sitemap differs from public pages'
    assert 'Sitemap: https://kissari.com/sitemap.xml' in (build / 'robots.txt').read_text()
    assert re.fullmatch(r'[0-9a-f]{40}', json.loads((build / 'deployment.json').read_text())['source_commit'])
    for error in sorted(set(errors)):
        print('ERROR:', error)
    for warning in sorted(set(warnings)):
        print('WARNING:', warning)
    print(f'Public artifact: {len(pages)} HTML pages, {len(locations)} sitemap URLs, {len(set(errors))} errors, {len(set(warnings))} warnings')
    return not errors

if __name__ == '__main__':
    raise SystemExit(0 if check(Path(sys.argv[1])) else 1)
