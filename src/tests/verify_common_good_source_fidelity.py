#!/usr/bin/env python3
"""Dossier 2.1.2: Bird primary-source distinctions, pedagogy and publication scope."""
from __future__ import annotations

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / "src/chapters/subtopic-2-1.html").read_text(encoding="utf-8")
start = source.index('<section class="chapter" id="ch2-1-2"')
end = source.index('<section class="chapter" id="ch2-1-3"', start)
chapter = source[start:end]
body = chapter[chapter.index('<div class="chapter-body">'):chapter.index('<nav class="chapter-endnav"')]
revision = chapter[chapter.index('<div class="end-block">'):]

class LayerCounter(HTMLParser):
    aids = {"box", "analogy", "tbl-wrap", "golden-quote", "checkpoint",
            "section-objective", "concept-rel", "hierarchy", "historical-timeline"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.n = {"prose": 0, "aids": 0, "depth": 0}
    def handle_starttag(self, tag, attrs):
        names = set(dict(attrs).get("class", "").split())
        self.stack.append((tag, "hikam-source-depth-inline" in names, bool(names & self.aids)))
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                return
    def handle_data(self, data):
        k = ("depth" if any(x[1] for x in self.stack) else
             "aids" if any(x[2] for x in self.stack) else "prose")
        self.n[k] += len(re.findall(r"[\w’'-]+", data))

counter = LayerCounter()
counter.feed(body)
n = counter.n
assert 650 <= n["prose"] <= 850, n
assert 850 <= n["aids"] <= 1150, n
assert 1500 <= n["prose"] + n["aids"] <= 2000, n
assert n["depth"] >= 450, n

assert 'id="ch2-1-2" style="--hue:328;"' in chapter
assert '<h1 class="chapter-title">The Common Good</h1>' in chapter
assert 'Original author: <strong>Colin Bird</strong>' in chapter
assert '<em>An Introduction to Political Philosophy</em>' in chapter

blocks = list(re.finditer(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', body))
assert len(blocks) == 6, len(blocks)
assert body.count('class="hikam-source-depth-item"') == 6
for item in blocks:
    assert " open" not in item.group(0).split(">",1)[0], "Optional depth must start closed"
    assert body[:item.start()].rstrip().endswith("</p>"), "Depth must directly follow relevant prose"
    assert "Colin Bird" in item.group(0)
    assert "supplied primary-source extract, PDF p" in item.group(0)
    assert "hikam-source-depth-citation" in item.group(0)

visible = unescape(re.sub(r'<[^>]+>', ' ',
    re.sub(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', '', body))).lower()
source_units = (
    "marx", "introspection", "classical utilitarianism",
    "l’état, c’est moi", "louis xiv", "aristotle", "later tradition",
    "res publica", "corporate", "common good", "belgium", "poland", "1918",
    "positive morality", "likely an important part", "impersonally",
    "prior, independent recognition", "de jure", "de facto",
    "referee", "soccer", "offside", "shared responsibility",
    "slavery", "jet engine", "mutual parity and partnership", "reciprocal",
    "alienated", "factionalised", "blind contests for power",
    "virtually inescapable", "compulsory", "open-ended",
    "pacifica and atlantis", "plato", "republic",
    "justice benefits its possessor", "medical analogy",
    "how, and for whom", "common bad", "well-being",
    "liberal democratic", "if plato is right"
)
for term in source_units:
    assert term in visible, f"Missing indispensable source point: {term}"

# Preserve source-attribution and uncertainty: no certainty inflation.
assert "Bird calls the doubt powerful but postpones endorsement." in unescape(body)
assert "not a complete theory of every form of political association" in unescape(body)
assert "If Plato is right" in unescape(body)
assert "not as an already completed empirical assessment" in unescape(body)
assert "The later tradition calls" in unescape(body)
assert "Pacifica and Atlantis" in unescape(body)
for invented in ("Pacifica is egalitarian", "Atlantis enforces a caste system"):
    assert invented not in body, f"Unsupported detail inserted: {invented}"

for aid in ("box concept", "box definition", "box highyield", "box mistake",
            "box tip", "box memory", "analogy", "tbl-wrap", "comparison",
            "concept-rel", "checkpoint", "golden-quote"):
    assert f'class="{aid}"' in body, aid
headings = ("Chapter Summary", "One-Page Revision Sheet", "Key Definitions",
            "Key Table", "Memory Aids Collected", "Possible Examination Questions")
indexes = [revision.index(x) for x in headings]
assert indexes == sorted(indexes)
assert revision.count('<h2 class="endh">') == 6
assert '<table class="comparison">' in revision
for item in ("Short Answer", "Long Answer", "Comparison", "Conceptual", "Application"):
    assert f'<div class="examq-cat">{item}</div>' in revision

manifest = json.loads((ROOT/"src/reading_companions.json").read_text(encoding="utf-8"))
cues = [x for x in manifest["companions"] if x["chapter"] == "ch2-1-2"]
assert len(cues) == 12
assert all(x["source"]["author"] == "Colin Bird" for x in cues)
assert all(all(1 <= pg <= 10 for pg in x["source"]["printedPages"]) for x in cues)
assert all(x.get("simple") and x.get("why_here") and x.get("remember") for x in cues)
for cue in cues:
    if cue.get("sourceDepthId"):
        assert body.count('id="' + cue["sourceDepthId"] + '"') == 1

chapters = "\n".join(p.read_text(encoding="utf-8") for p in sorted(
    (ROOT/"src/chapters").glob("subtopic-*.html")))
assert len(re.findall(r'<section class="chapter(?: [^"]+)?" id="ch\d',chapters)) == 44
print(f"PASS Bird 2.1.2: 10-page source coverage, qualified classical argument, "
      f"12 contextual cues, 6 adjacent Depth disclosures, six revision blocks, "
      f"44 chapters; prose={n['prose']}, aids={n['aids']}, depth={n['depth']}")
