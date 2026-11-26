#!/usr/bin/env python3
"""Regress the source-led James Kellenberger 3.1.1 Philosophy and Religion reading."""
from __future__ import annotations

import json
import re
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
source = (SRC / "chapters/subtopic-3-1.html").read_text(encoding="utf-8")
start = source.index('<section class="chapter" id="ch3-1-1"')
end = source.index("\n</section>", start) + len("\n</section>")
chapter = source[start:end]
assert source.count('id="ch3-1-1"') == 1
assert chapter.startswith('<section class="chapter" id="ch3-1-1" style="--hue:228;">')
assert '<h1 class="chapter-title">Introduction: Philosophy and Religion</h1>' in chapter
assert "James Kellenberger" in chapter
assert "Introduction to Philosophy of Religion" in chapter
assert "Routledge" in chapter
assert "supplied PDF pp. 2–6" in chapter
assert "Philosophy and Religion: The Human Imperative" not in chapter
assert "Source: Course Brief" not in chapter
assert chapter.count('class="end-block"') == 1
assert chapter.count('<h2 class="endh">') == 6
assert chapter.count('class="examq-cat"') == 5
assert chapter.count('<h2 class="sec">') == 7

main = chapter[chapter.index('<div class="chapter-body">'):chapter.index('<nav class="chapter-endnav"')]
depth = list(re.finditer(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', main))
assert len(depth) == 7
counts = [int(re.search(r'data-depth-count="(\d+)"', d.group()).group(1)) for d in depth]
assert counts == [2, 1, 2, 1, 2, 1, 2], counts
assert main.count('class="hikam-source-depth-item"') == 11
assert main.count('class="hikam-source-depth-citation"') == 11
for d in depth:
    assert main[:d.start()].rstrip().endswith("</p>"), "Source Depth not immediately after its paragraph"
    assert ' open' not in d.group().split('>', 1)[0], "Source Depth must start closed"
    assert "James Kellenberger" in d.group() and "PDF p" in d.group()
    assert not re.search(r'supplied PDF p(?:p)?\. [^.<]*\b[789]\b', d.group()), "Source page outside range"

visible = re.sub(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', "", main)
plain = unescape(re.sub(r'<[^>]+>', ' ', visible))
plain = ' '.join(plain.split())
required = (
    "agnostic", "atheist", "do not or cannot know", "withholds belief",
    "scientific laws", "free choice", "reasonable", "unreasonable",
    "Do they prove God exists?", "religious belief", "Chapter",
    "evil", "all-good", "all-powerful", "natural", "moral",
    "burning bush", "Exodus", "scriptur", "morality", "Do not lie",
    "merciful", "Father", "Mother", "Religious Realism",
    "transcendent being", "nonrealism", "if nonrealists",
    "theism", "monotheistic", "polytheistic", "non-theistic",
    "Gautama Buddha", "five religious traditions", "sensibilities",
    "clarity", "balance", "against", "not used to settle disputes",
)
lower=plain.casefold()
assert all(x.casefold() in lower for x in required), [x for x in required if x.casefold() not in lower]

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
wc=WordPool()
wc.feed(visible)
w=wc.words
assert 650 <= w["prose"] <= 880, w
assert 850 <= w["aids"] <= 1150, w
assert 1500 <= sum(w.values()) <= 2000, w

manifest=json.loads((SRC/"reading_companions.json").read_text(encoding="utf-8"))
items=[x for x in manifest["companions"] if x["chapter"]=="ch3-1-1"]
assert len(items)==12 and len({x["id"] for x in items})==12
assert all(x["source"]["author"]=="James Kellenberger"
           and x.get("simple") and x.get("why_here") and x.get("remember")
           and all(2 <= p <= 6 for p in x["source"]["printedPages"])
           for x in items)
toc=(SRC/"main.html").read_text(encoding="utf-8")
assert '<span class="tt">Introduction: Philosophy and Religion</span><span class="ts">Kellenberger</span>' in toc
coverage=(SRC/"docs/editorial/READING_3_1_1_KELLENBERGER_PHILOSOPHY_RELIGION_SOURCE_COVERAGE.md").read_text(encoding="utf-8")
assert "James Kellenberger" in coverage and "PDF pages" in coverage
assert "e684148b7b500c424830aecbb5264f21bf88e768" in coverage
print(f"PASS: Kellenberger five-page source audit, author attribution, original archive, 12 companions, 11 source records, all revisions, main={w['prose']}, aids={w['aids']}, total={sum(w.values())}")
