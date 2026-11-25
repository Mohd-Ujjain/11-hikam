#!/usr/bin/env python3
"""Protect Lawson-Tancred's full-source 2.2.6 and the independent Ross credit."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
s = (SRC / "chapters/subtopic-2-2.html").read_text(encoding="utf-8")

def get_chapter(id: str) -> str:
    start = s.index(f'<section class="chapter" id="{id}"')
    end = s.index("\n</section>", start) + len("\n</section>")
    return s[start:end]

ross = get_chapter("ch2-2-5")
dossier = get_chapter("ch2-2-6")
assert "W. D. Ross" in ross and "Clarendon Press, 1924" in ross
assert "Hugh Lawson-Tancred" in dossier and "Penguin Classics, 1998" in dossier
assert "By W. D. Ross" in ross and "Hugh Lawson-Tancred, translator and introduction author" in dossier
assert "Author not identified in supplied excerpt" not in ross
assert "Metaphysics Companion" not in dossier
assert "The Architecture of Reality" not in dossier
assert 'style="--hue:208;"' in dossier
assert '<h1 class="chapter-title">Substance, Change and Intelligibility: An Introduction to Aristotle’s Metaphysics</h1>' in dossier
assert dossier.count('<h2 class="sec">') == 6
assert dossier.count('<h2 class="endh">') == 6
assert dossier.count('class="examq-cat"') == 5
assert dossier.count('class="end-block"') == 1
assert all(t in dossier for t in (
    "magnificent failures",
    "Heraclitus", "Parmenides", "Anaxagoras", "Democritus", "Nicomachus",
    "what exists, how it changes, and how it is understood",
    "Musicality requires a bearer",
    "formless", "primary matter", "hylemorphism",
    "to ti ēn einai", "what-it-was-to-be-that-thing",
    "species", "special substance", "thisness",
    "syllable", "circle segments", "universal",
    "M. L. Gill", "potential being within the actual whole",
    "Felix Grayeff", "Bekker numbers", "Kappa",
    "unmoved first mover", "preliminary translation",
)), "Required source unit missing from visible chapter, aids or optional detail"

main = dossier[dossier.index('<div class="chapter-body">'):dossier.index('<nav class="chapter-endnav"')]
details = list(re.finditer(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', main))
assert len(details) == 5
assert [int(re.search(r'data-depth-count="(\d+)"', d.group()).group(1)) for d in details] == [2,2,2,3,3]
assert main.count('class="hikam-source-depth-item"') == 12
assert main.count('class="hikam-source-depth-citation"') == 12
for d in details:
    assert main[:d.start()].rstrip().endswith("</p>"), "Source Depth should follow its prose"
    assert ' open' not in d.group().split('>',1)[0]
    assert "Hugh Lawson-Tancred" in d.group() and "PDF p" in d.group()
visible = re.sub(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', "", main)

AIDS = {"box", "section-objective", "tbl-wrap", "hierarchy", "checkpoint",
        "concept-rel", "analogy", "golden-quote"}
class WordPool(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.words = {"prose": 0, "aids": 0}
    def handle_starttag(self, tag, attrs):
        if tag not in {"br","hr","img","input","meta","link"}:
            classes = set(dict(attrs).get("class","").split())
            self.tags.append((tag,bool(classes & AIDS)))
    def handle_endtag(self, tag):
        for i in range(len(self.tags)-1,-1,-1):
            if self.tags[i][0]==tag:
                self.tags=self.tags[:i]
                return
    def handle_data(self, txt):
        n = len(re.findall(r"[^\W_]+(?:['’\-][^\W_]+)*", txt, re.UNICODE))
        k = "aids" if any(flag for _,flag in self.tags) else "prose"
        self.words[k]+=n
wc = WordPool()
wc.feed(visible)
w = wc.words
assert 650 <= w["prose"] <= 1000, w
assert 850 <= w["aids"] <= 1150, w
assert 1500 <= sum(w.values()) <= 2000, w

manifest = json.loads((SRC / "reading_companions.json").read_text(encoding="utf-8"))
items = [x for x in manifest["companions"] if x["chapter"] == "ch2-2-6"]
assert len(items)==13
assert len({x["id"] for x in items})==13
assert all(x["source"]["author"]=="Hugh Lawson-Tancred"
           and all(1<=p<=42 for p in x["source"]["printedPages"])
           and x.get("simple") and x.get("why_here") and x.get("remember")
           for x in items)
toc = (SRC / "main.html").read_text(encoding="utf-8")
assert '<span class="tt">Substance, Change and Intelligibility</span><span class="ts">Introduction</span>' in toc
coverage = (SRC / "docs/editorial/READING_2_2_6_LAWSON_TANCRED_METAPHYSICS_SOURCE_COVERAGE.md").read_text(encoding="utf-8")
assert "42 consecutive PDF pages" in coverage and "Hugh Lawson-Tancred" in coverage
assert "W. D. Ross" in coverage
print(f"PASS: Ross/Lawson-Tancred explicit authors, 42-page source map, 13 companions, 12 source records, six revisions; main={w['prose']}, aids={w['aids']}, total={sum(w.values())}")
