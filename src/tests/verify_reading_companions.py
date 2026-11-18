#!/usr/bin/env python3
"""Source/anchor/edition checks for the Hikam Reading Companion pilot."""
from __future__ import annotations

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'src'
manifest = json.loads((SRC / 'reading_companions.json').read_text(encoding='utf-8'))
chapters = '\n'.join(p.read_text(encoding='utf-8') for p in sorted((SRC/'chapters').glob('subtopic-*.html')))
main = (SRC/'main.html').read_text(encoding='utf-8')
built = (ROOT/'index.html').read_text(encoding='utf-8')
ref = (SRC/'philosophy_study_notes.html').read_text(encoding='utf-8')
reader = (SRC/'reading_companions.js').read_text(encoding='utf-8')
assert manifest['version'] == 1
assert '<!-- HIKAM_READING_COMPANIONS_DATA -->' in main
assert 'id="hikamReadingCompanionsData"' in built
assert 'id="hikamReadingCompanionsData"' in ref
assert '<script src="reading_companions.js"></script>' not in built
assert 'window.__hikamReadingCompanions' in built
assert 'fetch(' not in reader, 'Companions must not depend on a network request'
assert all(k not in main for k in ('lit-companion-trigger', 'lit-evidence-trigger'))

def normalized(text: str) -> str:
    return ' '.join(unescape(text).split())

def get_paragraphs(html: str) -> list[tuple[str, str, list[str]]]:
    paragraphs = []
    for p in re.finditer(r'<p(?:\s[^>]*)?>([\s\S]*?)</p>', html):
        raw = p.group(1)
        plain = normalized(re.sub(r'<[^>]+>', '', raw))
        pieces = [unescape(x) for x in re.split(r'<[^>]+>', raw)]
        paragraphs.append((raw, plain, pieces))
    return paragraphs

seen = set()
for item in manifest['companions']:
    ident = item['id']
    assert ident not in seen, f'Duplicate ID {ident}'
    seen.add(ident)
    assert re.fullmatch(r'ch\d+-\d+-\d+', item['chapter']), ident
    assert item['source']['printedPages'], f'No primary page reference: {ident}'
    assert item['source']['author'] in ('Dermot Moran', 'Rowland Stout'), ident
    assert 20 <= len(item['explanation'].split()) <= 110, f'Explanation out of pilot range: {ident}'
    assert item['added_value'].strip(), ident
    start = chapters.find(f'<section class="chapter" id="{item["chapter"]}"')
    end = chapters.find('</section>', start)
    assert start >= 0 and end > start, item['chapter']
    body = chapters[start:end]
    body = body[body.index('<div class="chapter-body">'):]
    # On these pilots the exact passage is unique across ALL chapter paragraphs.
    matches = [p for p in get_paragraphs(body) if normalized(item['passage']) in p[1]]
    assert len(matches) == 1, f'Missing/ambiguous paragraph for {ident}: {len(matches)}'
    hits = [node for node in matches[0][2] if item['text'] in node]
    assert len(hits) == 1 and hits[0].count(item['text']) == 1, f'Missing/ambiguous text node: {ident}'
    assert ident in built, f'Manifest item not published: {ident}'
assert len(seen) == 3, f'Expected the three approved pilot entries, got {len(seen)}'
print(f'PASS: {len(seen)} source-anchored Companions, original chapter text intact, single-file offline embedding')
