#!/usr/bin/env python3
"""Source-fidelity and language-density gates for Jonathan Wolff 2.1.4.

Primary: supplied 21-page extract of 2006 Oxford revised edition:
Introduction printed pp. 1–5; Who Should Rule? printed pp. 62–77.
The file ends *within the opening epigraph* of Rousseau's next subsection.
"""
from __future__ import annotations
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT/"src/chapters/subtopic-2-1.html").read_text(encoding="utf-8")
start = source.index('<section class="chapter" id="ch2-1-4"')
end = source.index('<section class="chapter" id="ch2-1-5"',start)
chapter = source[start:end]
body = chapter[chapter.index('<div class="chapter-body">'):chapter.index('<nav class="chapter-endnav"')]
revision = chapter[chapter.index('<div class="end-block">'):]

class LayerCounter(HTMLParser):
    aids = {"box","analogy","tbl-wrap","golden-quote","checkpoint",
            "section-objective","concept-rel","hierarchy","historical-timeline"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.counts = {"prose":0,"aids":0,"depth":0}
    def handle_starttag(self,tag,attrs):
        classes=set(dict(attrs).get("class","").split())
        self.stack.append((tag,"hikam-source-depth-inline" in classes,bool(classes & self.aids)))
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0] == tag:
                self.stack=self.stack[:i]
                return
    def handle_data(self,data):
        k="depth" if any(x[1] for x in self.stack) else ("aids" if any(x[2] for x in self.stack) else "prose")
        self.counts[k]+=len(re.findall(r"[\w’'-]+",data))

counter=LayerCounter()
counter.feed(body)
n=counter.counts
# Normal policy ranges restored: complete source argument remains in
# concise connected prose and purpose-built visible study aids.
assert 650<=n["prose"]<=850, n
assert 850<=n["aids"]<=1150, n
assert 1500<=n["prose"]+n["aids"]<=2000, n
assert 1550<=n["depth"]<=1900, n

assert 'id="ch2-1-4" style="--hue:8;"' in chapter
assert '<h1 class="chapter-title">Introduction &amp; Who Should Rule?</h1>' in chapter
assert 'Original author: <strong>Jonathan Wolff</strong>' in chapter
assert '<em>An Introduction to Political Philosophy</em>' in chapter
assert 'Oxford University Press' in chapter and '2006' in chapter
assert 'pp. 1–5' in chapter and 'pp. 62–77' in chapter

blocks=list(re.finditer(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', body))
assert len(blocks)==9, len(blocks)
assert body.count('class="hikam-source-depth-item"')==17
assert sum(int(m.group(1)) for b in blocks for m in re.finditer(r'data-depth-count="(\d+)"',b.group(0)))==17
for block in blocks:
    assert body[:block.start()].rstrip().endswith('</p>'), 'Source Depth must follow ordinary prose'
    assert ' open' not in block.group(0).split('>',1)[0], 'Source Depth must start closed'
    assert 'Jonathan Wolff' in block.group(0)
    assert 'hikam-source-depth-citation' in block.group(0)
    assert 'Optional source detail' in block.group(0)
    assert 'SOURCE DEPTH' in block.group(0)

plain = unescape(re.sub(r'<[^>]+>', ' ', re.sub(
    r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', '', body))).lower()
# Main visible reading must contain every decisive source step in order.
units = (
    # Introduction (printed 1–5): distribution, power, methodology, no withdrawal
    "who gets what", "says who", "john locke", "right to command",
    "anarchist", "authoritarian", "autonomy", "normative",
    "descriptive", "altruism", "political agnosticism", "feminist",
    # Who Should Rule? (62–66): triad and two foundational tensions
    "for the people", "by the people", "of the people",
    "benevolent", "term of praise", "51%", "tocqueville", "mill",
    "madisonian", "direct democracy", "representative democracy",
    "lottery", "enfranchised", "proportional representation",
    # Plato (66–68): allegory, craft and long guardian training
    "plato", "demos", "craft analogy", "true navigator", "doctor",
    "sophists", "philosopher-guardians", "thirty", "fifteen years",
    # Guardianship objections and limits (68–71)
    "who guards the guardians", "private property", "reluctant turns governing",
    "public scrutiny", "appointed experts", "not yet a triumphant",
    "qualified doctor can err", "fallible",
    # Interests, voting and the epistemic test (71–75)
    "road", "competing interests", "hume", "opinion polling",
    "student-house smoking", "mixed-motivation", "ballot therefore reveals neither",
    "condorcet", "two conditions", "better than chance", "common good",
    "condorcet himself doubts",
    # Values and exact limit (76–77)
    "instrumental", "intrinsic", "making one\'s own table", "training voyage",
    "freedom and equality", "rousseau", "obey himself alone",
    "extract stops", "opening epigraph",
)
for phrase in units:
    assert phrase in plain, f"Original Wolff source unit absent from visible chapter: {phrase}"

# Do not silently replace Wolff's qualified claims with dogma or syntheses.
for phrase in (
    "possibly exaggerated",
    "not yet a triumphant defence of democracy",
    "Wolff explicitly",
    "Condorcet himself doubts",
    "the explanatory account of the general will is",
):
    assert phrase.lower() in unescape(chapter).lower(), phrase
assert "the supplied extract stops" in plain
assert "rousseau and the general will" in chapter.lower()
assert "source-depth-h214-rousseau" in chapter
for css in ("box concept","box definition","box mistake","box highyield",
            "box memory","box tip","golden-quote","analogy","tbl-wrap",
            "comparison","checkpoint","concept-rel"):
    assert f'class="{css}"' in body, css

headings = ("Chapter Summary","One-Page Revision Sheet","Key Definitions",
            "Key Table","Memory Aids Collected","Possible Examination Questions")
indices=[revision.index(h) for h in headings]
assert indices==sorted(indices)
assert revision.count('<h2 class="endh">')==6
assert '<table class="comparison">' in revision, 'Independent revision table missing'
for cat in ("Short Answer","Long Answer","Comparison","Conceptual","Application"):
    assert f'<div class="examq-cat">{cat}</div>' in revision

manifest=json.loads((ROOT/"src/reading_companions.json").read_text(encoding="utf-8"))
cues=[x for x in manifest["companions"] if x["chapter"]=="ch2-1-4"]
assert len(cues)==23
assert len({x["id"] for x in cues})==23
for cue in cues:
    assert cue["source"]["author"]=="Jonathan Wolff"
    assert all((1<=p<=5) or (62<=p<=77) for p in cue["source"]["printedPages"])
    assert cue.get("simple") and cue.get("why_here") and cue.get("remember")
    if cue.get("sourceDepthId"):
        assert body.count('id="'+cue["sourceDepthId"]+'"')==1
all_files="\n".join(p.read_text(encoding="utf-8") for p in sorted((ROOT/"src/chapters").glob("subtopic-*.html")))
assert len(re.findall(r'<section class="chapter(?: [^"]+)?" id="ch\d',all_files))==51
print(f"PASS Wolff 2.1.4: 21 printed-page source units through exact Rousseau boundary, "
      f"23 context-first cues, 9 adjacent Depth disclosures, 17 source records, "
      f"six independent revision blocks, 51 dossiers; "
      f"prose={n['prose']}, aids={n['aids']}, depth={n['depth']}")
