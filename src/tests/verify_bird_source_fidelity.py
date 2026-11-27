#!/usr/bin/env python3
"""Dossier 2.1.1: Bird's supplied Introduction, source distinctions, layers and revision."""
from __future__ import annotations
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[2]
text=(ROOT/"src/chapters/subtopic-2-1.html").read_text(encoding="utf-8")
start=text.index('<section class="chapter" id="ch2-1-1"')
end=text.index('<section class="chapter" id="ch2-1-2"',start)
chapter=text[start:end]
body=chapter[chapter.index('<div class="chapter-body">'):chapter.index('<nav class="chapter-endnav"')]
revision=chapter[chapter.index('<div class="end-block">'):]

class Layers(HTMLParser):
    aids={"box","analogy","tbl-wrap","golden-quote","checkpoint",
          "section-objective","concept-rel","hierarchy","historical-timeline"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]
        self.n={"prose":0,"aids":0,"depth":0}
    def handle_starttag(self,tag,attrs):
        classes=set(dict(attrs).get("class","").split())
        self.stack.append((tag,"hikam-source-depth-inline" in classes,
                           bool(classes & self.aids)))
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                self.stack=self.stack[:i]
                break
    def handle_data(self,text):
        n=len(re.findall(r"[\w’'-]+",text))
        k="depth" if any(x[1] for x in self.stack) else (
          "aids" if any(x[2] for x in self.stack) else "prose")
        self.n[k]+=n

layers=Layers()
layers.feed(body)
n=layers.n
assert 650 <= n['prose'] <= 850,n
assert 850 <= n['aids'] <= 1150,n
assert 1500 <= n['prose']+n['aids'] <= 2000,n
assert n['depth'] >= 400,n
assert 'id="ch2-1-1" style="--hue:308;"' in chapter
assert '<h1 class="chapter-title">Introduction</h1>' in chapter
assert 'Original author: <strong>Colin Bird</strong>' in chapter
assert '<em>An Introduction to Political Philosophy</em>' in chapter
assert chapter.count('class="hikam-source-depth-inline"') == 6
assert chapter.count('class="hikam-source-depth-item"') == 6

depth=list(re.finditer(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>',body))
assert len(depth)==6
for item in depth:
    assert ' open' not in item.group(0).split('>',1)[0]
    assert body[:item.start()].rstrip().endswith('</p>'),"Source Depth must directly follow visible prose"
    assert 'Colin Bird' in item.group(0)
    assert 'supplied primary-source extract' in item.group(0)

visible=unescape(re.sub(r'<[^>]+>',' ',re.sub(
    r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', '', body))).lower()
for term in (
    "two contrasting faces", "jekyll-and-hyde", "passports", "wills",
    "surveillance", "hiroshima", "nagasaki", "tokyo",
    "dresden", "hamburg", "nazis", "cold war", "deterrence",
    "criminal punishment", "slavery", "child labour", "women",
    "religious intolerance", "racial and ethnic discrimination",
    "aristotle", "bees", "wildebeest", "democracy", "fascism",
    "aristocracies", "oligarchies", "monarchies", "theocracies",
    "choice", "strawberry", "global wealth", "innocent lives",
    "justice", "common good", "freedom", "equality", "authority",
    "representation", "rights", "property", "coercion", "sovereignty",
    "judge", "neighbour", "archaeologist", "theory", "practice",
    "oxfam", "nazi party", "vote", "of a piece",
    "trotsky", "passive voice", "socialization",
    "conscripts", "defensible beliefs",
):
    assert term in visible, f"Important Bird source unit missing from visible study: {term}"

for phrase in (
    "in some circumstances", "may conclude", "not as answers already established",
    "Sincerity is not the same thing as justification",
):
    assert phrase.lower() in visible, f"Qualification lost: {phrase}"
for klass in (
    "box concept","box definition","box highyield","box mistake",
    "box tip","box memory","analogy","tbl-wrap","comparison",
    "hierarchy","concept-rel","golden-quote","checkpoint",
):
    assert f'class="{klass}"' in body,f"Lost main-body teaching aid {klass}"
for exact in (
    "Colin Bird, adapting Leon Trotsky",
    "You may not be interested in politics, but politics is interested in you.",
):
    assert exact in unescape(body)
headings=("Chapter Summary","One-Page Revision Sheet","Key Definitions",
          "Key Table","Memory Aids Collected","Possible Examination Questions")
indexes=[revision.index(x) for x in headings]
assert indexes==sorted(indexes)
assert revision.count('<h2 class="endh">') == 6
assert '<table class="comparison">' in revision
for kind in ("Short Answer","Long Answer","Comparison","Conceptual","Application"):
    assert f'<div class="examq-cat">{kind}</div>' in revision

m=json.loads((ROOT/"src/reading_companions.json").read_text(encoding="utf-8"))
items=[x for x in m['companions'] if x['chapter']=="ch2-1-1"]
assert len(items)==11
assert all(x["source"]["author"]=="Colin Bird" for x in items)
assert all(all(1<=p<=11 for p in x["source"]["printedPages"]) for x in items)
assert all(x.get("simple") and x.get("why_here") and x.get("remember") for x in items)
all_sources="\n".join(p.read_text(encoding="utf-8") for p in
                     sorted((ROOT/"src/chapters").glob("subtopic-*.html")))
assert len(re.findall(r'<section class="chapter(?: [^"]+)?" id="ch\d',all_sources))==46
print(f"PASS Bird 2.1.1: author/title, qualified source argument, 11 cues, "
      f"6 adjacent source records, all six revision sections, 46 chapters; "
      f"prose={n['prose']}, aids={n['aids']}, optional depth={n['depth']}")
