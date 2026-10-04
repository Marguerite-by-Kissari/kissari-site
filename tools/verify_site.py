#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = Path('/tmp/kissari-hugo-verify')
CACHE = Path('/tmp/kissari-hugo-cache')


def assert_file(path: Path) -> None:
    assert path.exists(), f"Missing file: {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}"


def read(path: Path) -> str:
    assert_file(path)
    return path.read_text(encoding='utf-8')


def run_hugo() -> str:
    cmd = [
        'hugo', '--minify', '--cleanDestinationDir',
        '--destination', str(BUILD),
        '--cacheDir', str(CACHE),
        '--baseURL', 'https://kissari.com/',
    ]
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout + result.stderr


def test_source_truth_is_ignored() -> None:
    assert_file(ROOT / '.spec-driven/README.md')
    result = subprocess.run(
        ['git', 'check-ignore', '-q', '.spec-driven/README.md'],
        cwd=ROOT,
    )
    assert result.returncode == 0, '.spec-driven must remain ignored by Git'


def test_required_source_files_exist() -> None:
    required = [
        'hugo.toml',
        'layouts/_default/baseof.html',
        'layouts/index.html',
        'layouts/partials/header.html',
        'layouts/partials/footer.html',
        'layouts/partials/hero.html',
        'layouts/partials/manifesto.html',
        'layouts/partials/expertise-grid.html',
        'layouts/partials/blog-preview.html',
        'layouts/partials/newsletter-placeholder.html',
        'assets/scss/main.scss',
        'assets/scss/_tokens.scss',
        'assets/js/main.js',
        'static/fonts/poppins/OFL.txt',
        'content/_index.md',
        'content/blog/_index.md',
        'content/expertises/imaginer/_index.md',
        'content/expertises/transformer/_index.md',
        'content/expertises/creer/_index.md',
        'content/expertises/faire-rayonner/_index.md',
        'content/mentions-legales/_index.md',
        'content/cgv/_index.md',
    ]
    for rel in required:
        assert_file(ROOT / rel)


def test_hugo_build_contains_required_v1_content() -> None:
    run_hugo()
    html = read(BUILD / 'index.html')
    expected_strings = [
        'BIENVENUE DANS L’UNIVERS DE KISSARI',
        'Le nouveau site arrive bientôt.',
        'NOTRE MANIFESTE',
        'BOUSCULER LA FORMATION.',
        'Imaginer',
        'Transformer',
        'Créer',
        'Faire rayonner',
        'KISSARI',
    ]
    for text in expected_strings:
        assert text in html, f"Missing generated homepage text: {text}"
    assert html.count('<h1') == 1, 'Homepage must contain exactly one h1'
    assert 'https://kissari.com/' in html, 'Build must use kissari.com base URL'


def test_generated_links_and_placeholders() -> None:
    run_hugo()
    generated = [
        'blog/index.html',
        'offres/index.html',
        'projets/index.html',
        'contact/index.html',
        'presse/index.html',
        'expertises/imaginer/index.html',
        'expertises/transformer/index.html',
        'expertises/creer/index.html',
        'expertises/faire-rayonner/index.html',
        'mentions-legales/index.html',
        'cgv/index.html',
    ]
    for rel in generated:
        assert_file(BUILD / rel)


def test_compiled_css_is_real_and_sanitized() -> None:
    """Prevent the exact visual regression seen in local hugo server.

    If Sass imports leak into the served stylesheet, the browser ignores nearly
    all styling and the page appears as raw HTML/images. Also catch Hugo's
    `ZgotmplZ` sanitizer placeholder, which appears when unsafe inline CSS is
    emitted from templates.
    """
    run_hugo()
    css_files = list(BUILD.glob('scss/main*.css'))
    assert css_files, 'Compiled stylesheet must be generated under /scss/'
    css = css_files[0].read_text(encoding='utf-8')
    assert len(css) > 5000, f'Compiled stylesheet is suspiciously small: {len(css)} bytes'
    assert '@use' not in css and '@import' not in css, 'Raw Sass imports leaked into generated CSS'
    html = read(BUILD / 'index.html')
    assert 'ZgotmplZ' not in html, 'Hugo sanitized unsafe CSS into ZgotmplZ'


def test_no_forbidden_generated_or_mac_files_tracked() -> None:
    result = subprocess.run(['git', 'ls-files'], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    forbidden_patterns = [r'^public/', r'^resources/_gen/', r'\.DS_Store$', r'(^|/)__MACOSX/', r'(^|/)\._']
    for tracked in result.stdout.splitlines():
        for pattern in forbidden_patterns:
            assert not re.search(pattern, tracked), f"Forbidden tracked file: {tracked}"


def main() -> None:
    tests = [
        test_source_truth_is_ignored,
        test_required_source_files_exist,
        test_hugo_build_contains_required_v1_content,
        test_generated_links_and_placeholders,
        test_compiled_css_is_real_and_sanitized,
        test_no_forbidden_generated_or_mac_files_tracked,
    ]
    failures = []
    for test in tests:
        try:
            test()
            print(f'PASS {test.__name__}')
        except Exception as exc:  # noqa: BLE001 - standalone verifier
            failures.append((test.__name__, str(exc)))
            print(f'FAIL {test.__name__}: {exc}')
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
