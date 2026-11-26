#!/usr/bin/env python3
"""Focused checks for the source-led final pair in Unit 3.2."""
from html.parser import HTMLParser
from hashlib import sha1
import json
import re
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
MODULE = (SRC / "chapters/subtopic-3-2.html").read_text()
TOC = (SRC / "main.html").read_text()
CUES = json.loads((SRC / "reading_companions.json").read_text())["companions"]
ARCHIVE = SRC / "archive/pre-redevelopment-2026-11-21"
SPEC = {
    7: (88, "مركز المعارف للمناهج والمتون التعليمية", {27, *range(29,35)}, "73f14ee2f736f39c708853245bf3d86a42d00680", ("عدم وجدان الدليل وعدم وجود المدلول", "شاهدًا يؤيد الاستدلال لا دليلًا مستقلًا", "افتقار الشيء إلى الغير في أصل وجوده", "الكافي")),
    8: (108, "Karen Armstrong", set(range(1,11)), "6b28ab108990f8c49026c96eca85dacda96f847e", ("complementary ways of knowing", "trained self-forgetfulness", "more representative traditions", "does not treat it as internally uniform")),
}
AIDS = set("box checkpoint comparison tbl-wrap section-objective golden-quote hierarchy analogy concept-rel".split())
DEPTH = re.compile(r'<details class="hikam-source-depth-inline"[^>]*>[\s\S]*?</details>')

class Words(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.count = [], [0, 0]

    def handle_starttag(self, tag, attrs):
        if tag not in {"br", "hr", "img", "input"}:
            self.stack.append((tag, bool(AIDS & set(dict(attrs).get("class", "").split()))))

    def handle_endtag(self, tag):
        for i in reversed(range(len(self.stack))):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                break

    def handle_data(self, data):
        self.count[any(flag for _, flag in self.stack)] += len(data.split())

for n, (hue, author, pages, pinned, anchors) in SPEC.items():
    key = f"ch3-2-{n}"
    shape = ' rtl' if n == 7 else ''
    lang = ' lang="ar"' if n == 7 else ''
    opening = f'<section class="chapter{shape}" id="{key}"{lang} style="--hue:{hue};">'
    assert MODULE.count(opening) == 1
    chap = MODULE[MODULE.index(opening):].split("\n</section>", 1)[0]
    old = (ARCHIVE / f"dossier-3.2.{n}.html").read_bytes()
    assert sha1(f"blob {len(old)}\0".encode() + old).hexdigest() == pinned
    assert author in chap and re.search(r'<strong>' + author + r'</strong>', chap)
    assert author in next(line for line in TOC.splitlines() if f'href="#{key}"' in line)
    assert chap.count('class="endh"') == 6 and chap.count('class="examq-cat"') == 5
    assert ('href="#ch3-2-8"' if n == 7 else 'href="#ch3-3-2"') in chap
    assert 'class="chapter-source" style="color:var(--parchment)"' in chap
    body = chap.split('<div class="chapter-body">', 1)[1].split('<nav class="chapter-endnav"', 1)[0]
    visible = DEPTH.sub("", body)
    assert all(anchor in visible for anchor in anchors)
    for c in re.findall(r'class="((?:box |hierarchy|analogy|golden-quote|concept-rel|checkpoint)[^"]*)"', old.decode().split('<nav class="chapter-endnav"')[0]):
        assert f'class="{c}"' in visible, (key, c)
    w = Words()
    w.feed(visible)
    p, a = w.count
    assert 650 <= p <= 850 and 850 <= a <= 1150 and 1500 <= p+a <= 2000, (key, w.count)
    cues = [c for c in CUES if c["chapter"] == key]
    records = list(DEPTH.finditer(body))
    assert len(cues) == len(records) == 5
    for c in cues:
        assert all(c.get(k) for k in ("simple", "why_here", "remember", "sourceDepthId"))
        assert c["source"]["author"] == author and set(c["source"]["printedPages"]) <= pages
        if n == 8:
            assert c["source"]["paginationBasis"].startswith("Assigned PDF leaves")
        r = next(x for x in records if c["sourceDepthId"] in x[0])
        assert " open" not in r[0].split(">", 1)[0] and author in r[0]
        pstart = body.rfind("<p>", 0, r.start())
        assert c["text"] in body[pstart:r.start()] and body[:r.start()].rstrip().endswith("</p>")
    print(f"PASS {key}: scoped content, correct language and hue, {len(cues)} Companions/Depth, 6 revisions, 5 exam classes; {w.count} visible words")
