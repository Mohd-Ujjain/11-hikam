#!/usr/bin/env python3
"""Assemble the modular Hikam dossier into the published GitHub Pages PWA.

    python src/build.py             # writes index.html, src/philosophy_study_notes.html, service-worker.js
    python src/build.py --check     # verifies generated outputs match the exact source

The authored book content is at src/main.html + src/chapters/subtopic-*.html.
The published root index.html inlines styles/scripts for reliable offline caching.
"""
from __future__ import annotations
import hashlib
import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
CHAPTERS = SRC / 'chapters'
INCLUDE_RE = re.compile(r'<!--\s*INCLUDE:(\S+?)\s*-->')


def outputs() -> dict[Path, str]:
    main = (SRC / 'main.html').read_text(encoding='utf-8')

    def replace_include(match: re.Match[str]) -> str:
        name = match.group(1)
        if Path(name).name != name or not re.fullmatch(r'subtopic-\d+-\d+\.html', name):
            raise ValueError(f'Unsafe or unexpected include marker: {name}')
        return (CHAPTERS / name).read_text(encoding='utf-8')

    html = INCLUDE_RE.sub(replace_include, main)

    # Embed separately authored Companion metadata in the canonical HTML.
    # There is no online JSON dependency: the installed PWA is one atomic edition.
    manifest = json.loads((SRC / 'reading_companions.json').read_text(encoding='utf-8'))
    if manifest.get('version') != 1 or not isinstance(manifest.get('companions'), list):
        raise ValueError('Invalid Reading Companion manifest')
    ids = [entry.get('id') for entry in manifest['companions']]
    if any(not isinstance(value, str) or not value for value in ids) or len(ids) != len(set(ids)):
        raise ValueError('Duplicate/invalid Reading Companion identifiers')
    marker = '<!-- HIKAM_READING_COMPANIONS_DATA -->'
    if html.count(marker) != 1:
        raise ValueError('Reading Companion data insertion point missing/duplicated')
    payload = json.dumps(manifest, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    html = html.replace(marker, '<script type="application/json" id="hikamReadingCompanionsData">' + payload + '</script>')
    css = (SRC / 'philosophy_notes.css').read_text(encoding='utf-8')
    js = (SRC / 'philosophy_notes.js').read_text(encoding='utf-8')
    companions = (SRC / 'reading_companions.js').read_text(encoding='utf-8')
    offline = (SRC / 'offline-reader.js').read_text(encoding='utf-8')
    index = html
    for old, new in (
        ('<link rel="stylesheet" href="philosophy_notes.css">', '<style>\n' + css + '\n</style>'),
        ('<script src="philosophy_notes.js"></script>', '<script>\n' + js + '\n</script>'),
        ('<script src="reading_companions.js"></script>', '<script>\n' + companions + '\n</script>'),
        ('<script src="offline-reader.js" defer></script>', '<script>\n' + offline + '\n</script>'),
    ):
        if old not in index:
            raise ValueError(f'Missing expected inlining marker: {old}')
        index = index.replace(old, new, 1)

    # A new release changes its cache name whenever a public resource changes.
    # Source-file moves alone do not affect the content or meaning of the book.
    assets = [
        SRC / 'philosophy_notes.css', SRC / 'philosophy_notes.js',
        SRC / 'reading_companions.js', SRC / 'reading_companions.json',
        SRC / 'offline-reader.js', ROOT / 'manifest.webmanifest',
        ROOT / 'icons/icon-192.png', ROOT / 'icons/icon-512.png',
        ROOT / 'og-image.jpg', ROOT / '404.html', ROOT / 'sitemap.xml',
        ROOT / 'robots.txt', SRC / 'service-worker.template.js'
    ]
    digest = hashlib.sha256(index.encode('utf-8'))
    for asset in assets:
        digest.update(asset.read_bytes())
    revision = digest.hexdigest()[:12]
    worker_template = (SRC / 'service-worker.template.js').read_text(encoding='utf-8')
    if worker_template.count('__REVISION__') != 1:
        raise ValueError('Service worker revision marker missing or duplicated')
    worker = worker_template.replace('__REVISION__', revision)

    return {
        ROOT / 'index.html': index,
        SRC / 'philosophy_study_notes.html': html,
        ROOT / 'service-worker.js': worker,
    }


def main() -> None:
    check = '--check' in sys.argv
    try:
        rendered = outputs()
        for path, content in rendered.items():
            if check:
                if not path.is_file() or path.read_text(encoding='utf-8') != content:
                    expected = re.search(r"const CACHE_NAME = PREFIX \+ '([a-f0-9]{12})'", rendered[ROOT / 'service-worker.js'])
                    suffix = f" (expected reader edition {expected.group(1)})" if expected else ""
                    sys.exit(f'Outdated or missing publication file: {path.relative_to(ROOT)}{suffix}. Run python src/build.py')
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding='utf-8')
    except (OSError, ValueError) as exc:
        sys.exit(f'Build error: {exc}')
    print(('Verified' if check else 'Built') + ': ' + ', '.join(str(p.relative_to(ROOT)) for p in rendered))


if __name__ == '__main__':
    main()
