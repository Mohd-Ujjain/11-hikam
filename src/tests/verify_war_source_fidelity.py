#!/usr/bin/env python3
"""Colin Bird's War, supplied 30-page second-edition extract: source-faithful 2.1.3."""
from __future__ import annotations
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
src = (ROOT/"src/chapters/subtopic-2-1.html").read_text(encoding="utf-8")
start = src.index('<section class="chapter" id="ch2-1-3"')
end = src.index('<section class="chapter" id="ch2-1-4"', start)
chapter = src[start:end]
body = chapter[chapter.index('<div class="chapter-body">'):chapter.index('<nav class="chapter-endnav"')]
revision = chapter[chapter.index('<div class="end-block">'):]

class LayerCounter(HTMLParser):
    aids = {"box","analogy","tbl-wrap","golden-quote","checkpoint",
            "section-objective","concept-rel","hierarchy","historical-timeline"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.n = {"prose":0,"aids":0,"depth":0}
    def handle_starttag(self,tag,attrs):
        names=set(dict(attrs).get("class","").split())
        self.stack.append((tag,"hikam-source-depth-inline" in names, bool(names & self.aids)))
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0] == tag:
                self.stack=self.stack[:i]
                return
    def handle_data(self,data):
        k="depth" if any(x[1] for x in self.stack) else ("aids" if any(x[2] for x in self.stack) else "prose")
        self.n[k]+=len(re.findall(r"[\w’'-]+",data))

layers=LayerCounter()
layers.feed(body)
n=layers.n
# Return to the adopted 18 November programme ranges without losing
# the original's indispensable propositions, counterarguments and replies.
assert 650 <= n["prose"] <= 850, n
assert 850 <= n["aids"] <= 1150, n
assert 1500 <= n["prose"]+n["aids"] <= 2000, n
assert 1300 <= n["depth"] <= 1800, n

assert 'id="ch2-1-3" style="--hue:348;"' in chapter
assert '<h1 class="chapter-title">War</h1>' in chapter
assert 'Original author: <strong>Colin Bird</strong>' in chapter
assert 'Chapter 11, “War,”' in chapter
assert '2nd ed.' in chapter and '2019' in chapter
assert '<em>An Introduction to Political Philosophy</em>' in chapter

blocks=list(re.finditer(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>',body))
assert len(blocks)==10, len(blocks)
assert body.count('class="hikam-source-depth-item"')==14
assert sum(int(x.group(1)) for b in blocks for x in re.finditer(r'data-depth-count="(\d+)"',b.group(0)))==14
for x in blocks:
    assert ' open' not in x.group(0).split('>',1)[0], "Optional source-detail opens by default"
    assert body[:x.start()].rstrip().endswith("</p>"), "Detail is detached from visible prose"
    assert "Colin Bird" in x.group(0)
    assert "hikam-source-depth-citation" in x.group(0)
    assert "supplied primary-source PDF" in x.group(0)
    assert "SOURCE DEPTH" in x.group(0) and "Optional source detail" in x.group(0)

visible=' '.join(unescape(re.sub(r'<[^>]+>',' ',re.sub(
    r'<details class="hikam-source-depth-inline"[\s\S]*?</details>','',body))).lower().split())
required=(
    # PDF pp. 1–5: institutional organisation and the three views
    "philosophers", "modern states", "mindless violence", "strateg", "professional",
    "courage", "1914 christmas truce", "institutional", "just war theorists",
    "pacifists", "realists", "gandhi", "hobbes", "blameless liberty",
    "disposition to fight",
    # PDF pp. 6–11: enmity, both kinds of justice and difficulty of application
    "cultivation of enmity", "morally coercive", "turning the other cheek",
    "jus ad bellum", "jus in bello", "legitimate public declaration",
    "just cause", "right intention", "proportionality", "prospects",
    "last resort", "noncombatant immunity", "2003 invasion of iraq",
    "elshtain", "catholic", "substantially clear guidance",
    # PDF pp. 12–13: independence, sliding scale, Walzer
    "independent", "nazi", "sliding scale", "walzer",
    "supreme emergency", "1942", "civilians",
    # PDF pp. 14–19: sovereignty and human rights, peace/enmity
    "vattel", "un charter article 2(4)", "mutual forbearance",
    "cosmopolitan", "darrel moellendorf", "aquinas", "grotius",
    "publicly acknowledging a just cause", "whether justice must outrank peace",
    # PDF pp. 20–22: kinds of pacifism and regulated force
    "radical pacifists", "just war pacifists", "nonviolent direct action",
    "martin luther king", "william penn", "force of the magistrate",
    # PDF pp. 23–30: self defence, innocents, scope, excuse/justification
    "combatants necessarily forfeit", "conscripts", "sleepwalking attacker",
    "one restraining member", "c. e. m. joad", "civilian deaths",
    "known attackers", "imminent danger", "border crossings",
    "attack planned next week", "excuse", "justification",
    "civilian officials who direct aggression", "london", "moscow",
)
for phrase in required:
    assert phrase in visible, f"2.1.3 original source point missing from visible reading: {phrase}"

# Attribution/epistemic gates: do not convert inquiries into endorsement
# of attacks on civilians, or assert that Bird finished his realist theory.
for phrase in (
    "bird accepts that unanimity is unrealistic",
    "bird replies",
    "sudden danger may",
    "bird leaves this unresolved",
    "a question rather than his completed verdict",
    "without justifying it",
    "some pacifists",
    "moellendorf replies",
    "walzer rejects",
    "yet considers a narrow",
):
    assert phrase in visible, phrase
assert "not a policy recommendation" in unescape(chapter).lower()
assert "bird accepts that unanimity is unrealistic, but insists" in visible
assert "not as a policy recommendation" not in visible  # limitation belongs in optional author-specific record
assert "Source Thought Experiment — The Sleepwalker" in body
assert "Thomas Hobbes" in body
assert "source-depth-h213-command" in body
assert "source-depth-h213-joad" in body

for typ in ("box concept","box definition","box mistake","box highyield",
            "box tip","box memory","tbl-wrap","comparison","concept-rel",
            "checkpoint","golden-quote","analogy"):
    assert f'class="{typ}"' in body, typ

heads=("Chapter Summary","One-Page Revision Sheet","Key Definitions",
       "Key Table","Memory Aids Collected","Possible Examination Questions")
positions=[revision.index(h) for h in heads]
assert positions == sorted(positions)
assert revision.count('<h2 class="endh">') == 6
assert '<table class="comparison">' in revision, "Revision table must be self-contained"
for category in ("Short Answer","Long Answer","Comparison","Conceptual","Application"):
    assert f'<div class="examq-cat">{category}</div>' in revision

manifest=json.loads((ROOT/"src/reading_companions.json").read_text(encoding="utf-8"))
cues=[x for x in manifest["companions"] if x["chapter"]=="ch2-1-3"]
assert len(cues)==19
assert len({x["id"] for x in cues})==19
for cue in cues:
    assert cue["source"]["author"]=="Colin Bird"
    assert "2019" in cue["source"]["work"]
    assert cue["simple"] and cue["why_here"] and cue["remember"]
    assert all(1<=pg<=30 for pg in cue["source"]["printedPages"])
    if cue.get("sourceDepthId"):
        assert body.count('id="'+cue["sourceDepthId"]+'"')==1

all_chapters="\n".join(f.read_text(encoding="utf-8") for f in sorted((ROOT/"src/chapters").glob("subtopic-*.html")))
assert len(re.findall(r'<section class="chapter(?: [^"]+)?" id="ch\d',all_chapters))==60
print(f"PASS Bird 2.1.3: 30-page authorial argument, 19 exact Companion cues, "
      f"10 local Depth disclosures, 14 source records, six independent revision sections, "
      f"60 chapters; prose={n['prose']}, aids={n['aids']}, depth={n['depth']}")
