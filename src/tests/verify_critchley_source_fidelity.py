#!/usr/bin/env python3
"""Source, pedagogy, disclosure and revision checks for Critchley 1.1.5."""
from __future__ import annotations

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / "src/chapters/subtopic-1-1.html").read_text(encoding="utf-8")
start = source.index('<section class="chapter" id="ch1-1-5"')
chapter = source[start:]
body = chapter[chapter.index('<div class="chapter-body">'):chapter.index('<nav class="chapter-endnav"')]
revision = chapter[chapter.index('<div class="end-block">'):]

class LayerCounter(HTMLParser):
    aid_names = {"box", "analogy", "tbl-wrap", "golden-quote", "checkpoint",
                 "section-objective", "concept-rel", "hierarchy", "historical-timeline"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.counts = {"prose": 0, "aids": 0, "depth": 0}
    def handle_starttag(self, tag, attrs):
        classes = set(dict(attrs).get("class", "").split())
        self.stack.append((tag, "hikam-source-depth-inline" in classes,
                           bool(self.aid_names & classes)))
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                break
    def handle_data(self, text):
        n = len(re.findall(r"[\w’'-]+", text))
        category = ("depth" if any(x[1] for x in self.stack)
                    else "aids" if any(x[2] for x in self.stack) else "prose")
        self.counts[category] += n

counter = LayerCounter()
counter.feed(body)
c = counter.counts
assert 650 <= c['prose'] <= 850, c
assert 850 <= c['aids'] <= 1150, c
assert 1500 <= c['prose']+c['aids'] <= 2000, c

assert 'id="ch1-1-5" style="--hue:288;"' in chapter
assert "Simon Critchley" in chapter
assert 'The Gap Between Knowledge and Wisdom' in chapter
assert body.count('class="hikam-source-depth-inline"') == 5
assert body.count('class="hikam-source-depth-item"') == 5
blocks = list(re.finditer(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', body))
assert len(blocks) == 5
for b in blocks:
    assert " open" not in b.group(0).split(">",1)[0]
    assert body[:b.start()].rstrip().endswith("</p>"), "Depth must directly follow a prose paragraph"
    assert "Simon Critchley" in b.group(0)
    assert "hikam-source-depth-citation" in b.group(0)

visible = unescape(re.sub(r"<[^>]+>", " ",
    re.sub(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', "", body))).lower()
for term in (
    "socrates", "aristotle", "stoics", "polis", "contemplation",
    "the unlived life", "party", "folk psychology", "scientia",
    "theoros", "epistemology", "locke", "under-labourer",
    "naturalistic ontology", "evolutionary epistemology",
    "not an explanatory gap", "felt gap", "affluence", "brecht",
    "nihilism", "teleological", "final cause", "descartes", "pascal",
    "disenchantment", "weber", "scientism", "obscurantism",
    "serbian nationalism", "mill", "hegel", "nietzsche", "marx",
    "freud", "heidegger", "sartre", "camus", "levinas",
    "wittgenstein", "not sufficient", "necessary condition",
):
    assert term in visible, f"Missing source-essential topic: {term}"

for text in (
    "Philosophers become janitors in the Crystal Palace of the sciences.",
    "The eternal silence of infinite spaces fills me with dread.",
    "the one doctrine is accused of making men beasts, the other lunatics",
):
    assert text.lower() in visible, f"Source quotation absent: {text}"

for aid in ("box concept", "box definition", "box highyield", "box mistake",
            "box tip", "analogy", "tbl-wrap", "comparison", "concept-rel",
            "checkpoint", "golden-quote"):
    assert f'class="{aid}"' in body, f"Study aid absent: {aid}"

headings = ("Chapter Summary", "One-Page Revision Sheet", "Key Definitions",
            "Key Table", "Memory Aids Collected", "Possible Examination Questions")
indexes = [revision.index(x) for x in headings]
assert indexes == sorted(indexes)
assert revision.count('<h2 class="endh">') == 6
assert '<table class="comparison">' in revision, "Key Table must stand alone"
for group in ("Short Answer", "Long Answer", "Comparison", "Conceptual", "Application"):
    assert f'<div class="examq-cat">{group}</div>' in revision

manifest = json.loads((ROOT / "src/reading_companions.json").read_text(encoding="utf-8"))
items = [x for x in manifest['companions'] if x['chapter'] == 'ch1-1-5']
assert len(items) == 9
assert all(x['source']['author'] == 'Simon Critchley' for x in items)
assert all(all(1 <= pg <= 8 for pg in x['source']['printedPages']) for x in items)
assert all(x.get('simple') and x.get('why_here') and x.get('remember') for x in items)
print(f"PASS: Critchley 1.1.5 source coverage, nine contextual cues, five closed "
      f"adjacent Source Depth records, six independent revision sections; "
      f"prose={c['prose']}, aids={c['aids']}, depth={c['depth']} words")
