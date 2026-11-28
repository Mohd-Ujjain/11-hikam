#!/usr/bin/env python3
"""Regression: Umayri 3.1.5 source-specific semantic study aids and prior archive."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
raw = (ROOT / "chapters/subtopic-3-1.html").read_text(encoding="utf-8")
start = raw.index('<section class="chapter rtl" id="ch3-1-5" lang="ar" style="--hue:308;">')
chapter = raw[start:raw.index("\n</section>", start) + len("\n</section>")]
archive = ROOT / "archive/pre-redevelopment-2026-11-21/dossier-3.1.5-before-2026-11-28-source-redevelopment.html"
original = archive.read_bytes()
blob = hashlib.sha1(b"blob " + str(len(original)).encode() + b"\0" + original).hexdigest()
assert blob == "654d736715575ab88301f67d7e2f899dbaef2395", blob
assert original.decode().count('class="endh"') == 6
assert original.decode().count('class="comparison"') == 7

class Aids(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.words = [0, 0]
    def handle_starttag(self, tag, attrs):
        if tag not in {"br", "hr", "img", "input", "meta", "link"}:
            cls = set(dict(attrs).get("class", "").split())
            self.stack.append((tag, bool(cls & {"box","checkpoint","comparison","tbl-wrap","section-objective","golden-quote","hierarchy","analogy","concept-rel"})))
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
    def handle_data(self, value):
        self.words[int(any(aid for _, aid in self.stack))] += len(value.split())

body = chapter.split('<div class="chapter-body">',1)[1].split('<nav class="chapter-endnav"',1)[0]
body = re.sub(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', '', body)
aids = Aids()
aids.feed(body)
assert 650 <= aids.words[0] <= 850, aids.words
assert 850 <= aids.words[1] <= 1150, aids.words
assert 1500 <= sum(aids.words) <= 2000, aids.words
assert chapter.count('class="endh"') == 6
assert chapter.count('class="examq-cat"') == 5
assert chapter.count('class="hikam-source-depth-inline"') == 6
assert chapter.count('class="hierarchy"') == 3
assert chapter.count('class="comparison"') == 4
assert chapter.count('class="concept-rel"') >= 1
assert all(bad not in chapter for bad in ('class="hier-row"', 'class="hier-title"', 'class="hier-node"'))
for phrase in ('المعلومات', 'المسوغ الترابطي', 'فرويد', 'الخوف', 'الجهل', 'الطوطم', 'التطور البيولوجي'):
    assert phrase in body, phrase
for caption in ('مقارنة حقيقية: الخوف والجهل في تفسير نشأة الدين', 'مقارنة أصلية: المذهب الحيوي ودوركايم'):
    assert caption in chapter
for class_name in ('box mistake','box memory','box tip','h-node l1','h-tag','h-val','rel-row'):
    assert f'class="{class_name}"' in chapter
assert raw.index('id="ch3-1-4"') < start
assert (ROOT / 'docs/editorial/READING_3_1_5_UMAYRI_SOURCE_AND_PEDAGOGY_AUDIT.md').exists()
print(f'PASS 3.1.5: archive={blob}, visible prose/aids={aids.words}; 3 hierarchies, 4 comparisons, 6 source depths; complete revision')
