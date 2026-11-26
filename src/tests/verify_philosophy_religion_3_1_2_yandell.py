#!/usr/bin/env python3
"""Regress Yandell's excerpt, archive and established study layers."""
from html.parser import HTMLParser
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
source = (SRC / "chapters/subtopic-3-1.html").read_text()
start = source.index('<section class="chapter" id="ch3-1-2"')
end = source.index("\n</section>", start) + len("\n</section>")
chapter = source[start:end]
assert chapter.startswith('<section class="chapter" id="ch3-1-2" style="--hue:248;">')
assert chapter.count('class="endh"') == 6
assert chapter.count('class="examq-cat"') == 5
assert chapter.count('class="hikam-source-depth-item"') == 10
assert chapter.count('Keith E. Yandell') >= 12
assert 'href="#ch3-1-3"' in chapter
assert 'Course Brief' not in chapter and 'Most monotheists' not in chapter
main = chapter.split('<div class="chapter-body">', 1)[1].split('<nav class="chapter-endnav"', 1)[0]
visible = re.sub(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', '', main)
for claim in ('necessarily independent', 'false ones necessarily false', 'It does not decide whether God exists',
              'Contingent atheism', 'Weak providence', 'probabilistic'):
    assert claim in visible or claim in chapter, claim

AIDS = {"box", "section-objective", "tbl-wrap", "hierarchy", "checkpoint",
        "concept-rel", "analogy", "golden-quote"}
class WordPool(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags=[]
        self.words={"prose":0, "aids":0}
    def handle_starttag(self, tag, attrs):
        if tag not in {"br","hr","img","input","meta","link"}:
            classes=set(dict(attrs).get("class", "").split())
            self.tags.append((tag, bool(classes & AIDS)))
    def handle_endtag(self, tag):
        for i in range(len(self.tags)-1,-1,-1):
            if self.tags[i][0] == tag:
                self.tags=self.tags[:i]
                return
    def handle_data(self, value):
        n=len(re.findall(r"[^\W_]+(?:['’\-][^\W_]+)*", value, re.UNICODE))
        k="aids" if any(flag for _,flag in self.tags) else "prose"
        self.words[k] += n
wc = WordPool()
wc.feed(visible)
words = wc.words
assert 650 <= words["prose"] <= 850, words
assert 850 <= words["aids"] <= 1150, words
assert 1500 <= sum(words.values()) <= 2000, words
m = json.loads((SRC / "reading_companions.json").read_text())
items = [x for x in m["companions"] if x["chapter"] == "ch3-1-2"]
assert len(items) == 11 and all(x["source"]["author"] == "Keith E. Yandell" for x in items)
coverage = (SRC / "docs/editorial/READING_3_1_2_YANDELL_PHILOSOPHY_RELIGION_SOURCE_COVERAGE.md").read_text()
assert [int(x) for x in re.findall(r"^\| (\d+) \|", coverage, re.M)] == list(range(1, 24))
assert '<span class="ts">Yandell</span>' in (SRC / "main.html").read_text()
print("PASS: Yandell 3.1.2 source map, title, scope, companions, depth, revision; visible words:", words)
