#!/usr/bin/env python3
"""Editorial source integrity: Jonathan Wolff, The Place of Liberty.

Authority: user's 14-page Oxford PDF, original printed pp. 104–117.
Source concludes with the question whether a utilitarian legislator
should make only the law "Act to maximize happiness"; NO answer follows
within the assigned extract. Supporting study guides are not authority.
"""
from __future__ import annotations
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT/"src/chapters/subtopic-2-1.html").read_text(encoding="utf-8")
start = source.index('<section class="chapter" id="ch2-1-5"')
end = source.index('<section class="chapter" id="ch2-1-6"', start)
chapter = source[start:end]
body = chapter[chapter.index('<div class="chapter-body">'):chapter.index('<nav class="chapter-endnav"')]
revision = chapter[chapter.index('<div class="end-block">'):]

class LayerCounter(HTMLParser):
    aids = {"box", "analogy", "tbl-wrap", "golden-quote", "checkpoint",
            "section-objective", "concept-rel", "hierarchy", "historical-timeline"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]
        self.counts={"prose":0,"aids":0,"depth":0}
    def handle_starttag(self, tag, attrs):
        classes = set(dict(attrs).get("class","").split())
        self.stack.append((tag,"hikam-source-depth-inline" in classes,
                           bool(classes & self.aids)))
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                self.stack=self.stack[:i]
                return
    def handle_data(self,data):
        layer = "depth" if any(z[1] for z in self.stack) else (
            "aids" if any(z[2] for z in self.stack) else "prose")
        self.counts[layer]+=len(re.findall(r"[\w’'-]+",data))

counter=LayerCounter()
counter.feed(body)
n=counter.counts
# A dense 14-page original, covering several different source arguments,
# permits a documented density exception without hiding decisive claims.
assert 1200 <= n["prose"] <= 1450, n
assert 1100 <= n["aids"] <= 1380, n
assert 2350 <= n["prose"]+n["aids"] <= 2750, n
assert 1450 <= n["depth"] <= 1900, n

assert 'id="ch2-1-5" style="--hue:28;"' in chapter
assert '<h1 class="chapter-title">The Place of Liberty</h1>' in chapter
assert 'Original author: <strong>Jonathan Wolff</strong>' in chapter
assert '<em>An Introduction to Political Philosophy</em>' in chapter
assert 'Chapter 4, “The Place of Liberty,”' in chapter
assert 'Oxford University Press' in chapter and '2006' in chapter
assert 'pp. 104–117' in chapter

blocks = list(re.finditer(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', body))
assert len(blocks)==8, len(blocks)
assert body.count('class="hikam-source-depth-item"')==16
assert sum(int(m.group(1)) for b in blocks for m in re.finditer(
    r'data-depth-count="(\d+)"', b.group(0)))==16
for disclosure in blocks:
    assert body[:disclosure.start()].rstrip().endswith('</p>'), "Depth not immediately after prose"
    assert ' open' not in disclosure.group(0).split('>',1)[0]
    assert 'SOURCE DEPTH' in disclosure.group(0)
    assert 'Optional source detail' in disclosure.group(0)
    assert 'Jonathan Wolff' in disclosure.group(0)
    assert 'hikam-source-depth-citation' in disclosure.group(0)

visible = re.sub(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', '', body)
plain = unescape(re.sub(r'<[^>]+>', ' ',visible)).lower()
# Complete units in original narrative order, not merely popup material.
source_units = (
    # 104–106: rationale and principle
    "tyranny of the majority", "representative government",
    "anarchists", "hobbes", "popular morality",
    "liberty principle", "harm principle", "paternalism", "drug addiction",
    # 106–107: original scope condition, NOT unsourced modern critique
    "maturity of their faculties", "free and equal discussion",
    "children", "barbarians",
    # 107–109: argument for debate and fallibility
    "freedom of thought and discussion", "true", "false",
    "partly true", "infallibility", "socrates", "jesus",
    "library of alexandria", "unreliable",
    # 109–110: objection, response, reservation (not independent adjudication)
    "rousseau", "arts and sciences", "nuclear weapons",
    "roman", "usefulness", "social peace",
    "wolff does not treat mill", "generally beneficial to happiness",
    # 110–112: active understanding, context-dependent speech
    "dead dogma", "evolutionary theory", "creationist",
    "corn-dealers", "excited mob",
    # 112–114: what counts as harm?
    "self-regarding actions", "other-regarding actions",
    "private worship", "brown shoes", "offence",
    "damage to interests", "competitive examination",
    "rights",
    # 114–116: rights problem, Bentham and natural-rights debate
    "rights-based interests", "natural rights", "bentham",
    "locke", "existing legal protections", "current laws",
    # 116–117: limited exposition of utility and exact terminal question
    "utility", "progressive beings", "utilitarian legislator",
    "maximise happiness", "not so obvious",
)
for phrase in source_units:
    assert phrase in plain, f"Source unit absent from visible reading: {phrase}"

# Distinguish Wolff's voice, source quotations and explicitly qualified reports.
assert "apparently a highly unreliable source" in unescape(body).lower()
assert "according to some accounts" in unescape(body).lower()
assert "wolff does not treat mill's answer as conclusive" in unescape(body).lower()
assert "injury to someone's interests is still not sufficient" in unescape(body).lower()
assert "wolff even leaves open whether damage to interests is always a necessary condition" in unescape(body).lower()
assert "does not include the subsequent demonstration" in plain
assert "the supplied extract stops there" in plain
# Prevent accidental promotion of the supporting syntheses' later demonstration
# into an accomplished conclusion within the source-extract scope.
assert 'the subsequent demonstration' in plain
assert 'the unfinished legislator' in unescape(chapter).lower()

# Pre-existing semantics and independent study/revision architecture.
for css in ("box concept","box definition","box mistake","box highyield",
            "box memory","box tip","golden-quote","analogy","tbl-wrap",
            "comparison","checkpoint","concept-rel","hierarchy"):
    assert f'class="{css}"' in body, css
headings=("Chapter Summary","One-Page Revision Sheet","Key Definitions",
          "Key Table","Memory Aids Collected","Possible Examination Questions")
positions=[revision.index(h) for h in headings]
assert positions==sorted(positions)
assert revision.count('<h2 class="endh">')==6
assert '<table class="comparison">' in revision
for cat in ("Short Answer","Long Answer","Comparison","Conceptual","Application"):
    assert f'<div class="examq-cat">{cat}</div>' in revision
assert 'class="chapter-endnav"' in chapter and 'href="#ch2-1-6"' in chapter

manifest=json.loads((ROOT/"src/reading_companions.json").read_text(encoding="utf-8"))
items=[item for item in manifest['companions'] if item['chapter']=='ch2-1-5']
assert len(items)==22 and len({x['id'] for x in items})==22
for item in items:
    assert item['source']['author']=="Jonathan Wolff"
    assert all(104 <= pg <= 117 for pg in item['source']['printedPages'])
    assert all(item.get(k) for k in ("simple","why_here","remember"))
    assert body.count('id="'+item['sourceDepthId']+'"')==1
all_files="\n".join(p.read_text(encoding='utf-8')
                    for p in sorted((ROOT/"src/chapters").glob("subtopic-*.html")))
assert len(re.findall(r'<section class="chapter(?: [^"]+)?" id="ch\d',all_files))==39
print(f"PASS Wolff 2.1.5: Oxford original pp104–117; qualified Alexandria/creationism, "
      f"Mill's and Wolff's separate arguments, exact utilitarian endpoint; "
      f"22 contextual cues, 8 local Depth disclosures, 16 records, "
      f"six independent revision sections, 39 dossiers; "
      f"prose={n['prose']}, aids={n['aids']}, depth={n['depth']}")
