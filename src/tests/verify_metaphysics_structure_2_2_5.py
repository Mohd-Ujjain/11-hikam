#!/usr/bin/env python3
"""Regress the source-faithful English 2.2.5 Aristotle Metaphysics critical introduction.

The user's original PDF is privately provided and deliberately not distributed in
the public repository. Source comparison is documented by printed PDF pages in:
src/docs/editorial/READING_2_2_5_METAPHYSICS_CRITICAL_INTRODUCTION_SOURCE_COVERAGE.md
"""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
SOURCE = (SRC / "chapters/subtopic-2-2.html").read_text(encoding="utf-8")
START = '<section class="chapter" id="ch2-2-5" style="--hue:188;">'
a = SOURCE.index(START)
b = SOURCE.index("\n</section>", a) + len("\n</section>")
chapter = SOURCE[a:b]
assert SOURCE.count('id="ch2-2-5"') == 1
assert '<h1 class="chapter-title">The Structure of Aristotle’s Metaphysics</h1>' in chapter
assert "By W. D. Ross" in chapter
assert "Clarendon Press, 1924" in chapter
assert "Introductory author not identified" not in chapter
assert "— W. D. Ross, Introduction I" in chapter
assert "The Ladder of Cognition" not in chapter
assert "all men by nature desire to know" not in chapter.lower()
assert chapter.count('class="end-block"') == 1
assert chapter.count('<h2 class="endh">') == 6
assert chapter.count('class="examq-cat"') == 5
assert all(t in chapter for t in (
    "two different orders to reconstruct",
    "continuity of thought",
    "four preliminary problems",
    "the formal element of sensible substances",
    "A–B–Γ–E",
    "Z–H–Θ",
    "M–N–I",
    "α (little alpha)",
    "Δ (Delta)",
    "K (Kappa)",
    "Λ (Lambda)",
    "Book B",
    "Jaeger",
    "Asclepius",
    "Andronicus",
    "Nicolaus of Damascus",
    "seven rolls containing two books each",
    "Socrates, Plato, and the Platonists",
)), "Missing a required original-source unit"

main = chapter[chapter.index('<div class="chapter-body">'):chapter.index('<nav class="chapter-endnav"')]
disclosures = list(re.finditer(
    r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', main
))
assert len(disclosures) == 4, "Expected four closed inline Source Depth groups"
assert [int(re.search(r'data-depth-count="(\d+)"', x.group()).group(1))
        for x in disclosures] == [1, 2, 2, 2]
assert main.count('class="hikam-source-depth-item"') == 7
for x in disclosures:
    assert main[:x.start()].rstrip().endswith("</p>"), "Source Depth must be paragraph adjacent"
    assert " open" not in x.group().split(">", 1)[0], "Source Depth must start closed"
    assert 'class="hikam-source-depth-citation"' in x.group()
    assert "PDF pp." in x.group() and "printed pp." in x.group()

manifest = json.loads((SRC / "reading_companions.json").read_text(encoding="utf-8"))
items = [x for x in manifest["companions"] if x["chapter"] == "ch2-2-5"]
assert len(items) == 10, "Ten exact 2.2.5 context-first Companions expected"
assert len(set(x["id"] for x in items)) == 10
assert all(x["source"]["author"] == "W. D. Ross"
           and x.get("simple") and x.get("why_here") and x.get("remember")
           and 1 <= x["source"]["printedPages"][0] <= 21
           for x in items)

# Main-body word allocation, as per the approved editorial distinction.
visible = re.sub(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>',
                 "", main)
AIDS = {"box", "section-objective", "tbl-wrap", "hierarchy", "checkpoint",
        "concept-rel", "analogy", "golden-quote"}

class CountWords(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.words = {"prose": 0, "aids": 0}

    def handle_starttag(self, tag, attrs):
        if tag in ("br", "hr", "img", "input", "meta", "link"):
            return
        classes = dict(attrs).get("class", "").split()
        self.stack.append((tag, bool(AIDS.intersection(classes))))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                return

    def handle_data(self, s):
        n = len(re.findall(r"[^\W_]+(?:['’\-][^\W_]+)*", s, re.UNICODE))
        bucket = "aids" if any(aid for _, aid in self.stack) else "prose"
        self.words[bucket] += n

counter = CountWords()
counter.feed(visible)
words = counter.words
assert 700 <= words["prose"] <= 1000, f"Unexpected 2.2.5 prose pool: {words}"
assert 800 <= words["aids"] <= 1250, f"Unexpected 2.2.5 aids pool: {words}"
assert 1500 <= sum(words.values()) <= 2200, f"Unexpected 2.2.5 visible total: {words}"
assert '<span class="tt">The Structure of Aristotle\'s Metaphysics</span>' in (
    SRC / "main.html"
).read_text(encoding="utf-8")

coverage = (SRC / "docs/editorial/READING_2_2_5_METAPHYSICS_CRITICAL_INTRODUCTION_SOURCE_COVERAGE.md").read_text(encoding="utf-8")
assert "xiii–xxxiii" in coverage
assert "The Structure of the Metaphysics" in coverage
assert "section II" in coverage

print(
    "PASS: 2.2.5 primary-source structure, textual uncertainty, 10 exact Companions, "
    f"seven optional source records, six revision sections, main={words['prose']}, "
    f"aids={words['aids']}, total={sum(words.values())}"
)
