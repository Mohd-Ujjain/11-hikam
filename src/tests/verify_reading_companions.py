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
assert len(seen) == len(manifest['companions']), f'Missing manifest entries: {len(seen)} vs {len(manifest["companions"])}'
# Context-first Moran pilot: extra source details are preserved separately,
# not delivered as surprising new intellectual branches in the popup.
moran = [x for x in manifest['companions'] if x['chapter'] == 'ch1-1-1']
stout = [x for x in manifest['companions'] if x['chapter'] == 'ch1-1-2']
assert len(moran) == 10 and len(stout) == 24, 'Changed pilot coverage without audit'
first = chapters.index('<section class="chapter" id="ch1-1-1"')
second = chapters.index('<section class="chapter" id="ch1-1-2"')
moran_html = chapters[first:second]
body_end = moran_html.index('<!-- ================= END OF CHAPTER BLOCK')
main_body = moran_html[moran_html.index('<div class="chapter-body">'):body_end]
depth = moran_html[moran_html.index('<details class="hikam-source-depth"'):body_end]
assert moran_html.count('<details class="hikam-source-depth"') == 1
assert depth.count('<details class="hikam-source-depth-item"') == 10
assert 'A short historical sequence</caption>' not in main_body
assert main_body.count('class="historical-timeline-event"') == 4
assert main_body.index('1900s') < main_body.index('1914–1918') < main_body.index('1930s–1940s') < main_body.index('After 1945')
assert 'The One Thread to Follow' in main_body
assert 'The four thinkers below are not four unrelated stories.' in main_body
for item in moran:
    assert all(isinstance(item.get(k), str) and item[k].strip() for k in
               ('simple','why_here','remember','sourceDepthId')), item['id']
    assert item['sourceDepthId'] == 'source-depth-' + item['id'], item['id']
    assert depth.count('id="' + item['sourceDepthId'] + '"') == 1, item['id']
    card = depth.split('id="' + item['sourceDepthId'] + '"', 1)[1].split('</details>', 1)[0]
    for page in item['source']['printedPages']:
        assert str(page) in card, (item['id'], page)
    assert len(normalized(re.sub(r'<[^>]+>', ' ', card))) > 130, item['id']
assert 'hikam-companion-context-field' in reader
assert 'item.simple && item.why_here && item.remember' in reader
assert '.hikam-source-depth {display:none!important;}' in (SRC/'philosophy_notes.css').read_text(encoding='utf-8')
assert 'hikam-source-depth-ch1-1-1' in built
assert 'class="historical-timeline"' in built

print(f'PASS: {len(seen)} source-anchored Companions, source anchors intact, single-file offline embedding')
