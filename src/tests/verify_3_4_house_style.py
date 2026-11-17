#!/usr/bin/env python3
"""Regression for Hikam's six-part, component-rich dossier architecture."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
HTML = (ROOT / "src/chapters/subtopic-3-4.html").read_text(encoding="utf-8")
CSS = (ROOT / "src/philosophy_notes.css").read_text(encoding="utf-8")
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
SUB = (ROOT / "src/philosophy_study_notes.html").read_text(encoding="utf-8")
SIX = [
    "Chapter Summary",
    "One-Page Revision Sheet",
    "Key Definitions",
    "Key Table",
    "Memory Aids Collected",
    "Possible Examination Questions",
]
FIVE = ["Short Answer", "Long Answer", "Comparison", "Conceptual", "Application"]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class ChapterStructure(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.children = {n: [] for n in range(5, 10)}
        self.current = None
        self.depth = None
        self.unexpected = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section" and a.get("id", "") in {f"ch3-4-{n}" for n in range(5, 10)}:
            assert self.current is None
            self.current = int(a["id"][-1])
            self.depth = len(self.stack) + 1
            assert (a.get("class") or "") == "chapter", (a, "English chapter incorrectly RTL")
            assert a.get("lang") is None
        if self.current is not None and len(self.stack) == self.depth and tag in {"div", "nav"}:
            self.children[self.current].append((tag, (a.get("class") or "").split()))
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        assert self.stack and self.stack[-1] == tag, ("bad or unbalanced HTML", self.stack[-5:], tag)
        if tag == "section" and self.current is not None and len(self.stack) == self.depth:
            self.current = None
            self.depth = None
        self.stack.pop()


def run():
    parser = ChapterStructure()
    parser.feed(HTML)
    assert not parser.stack, parser.stack
    for n in range(5, 10):
        id_ = f"ch3-4-{n}"
        prefix = f"<!-- CHAPTER 3.4.{n} -->"
        assert HTML.count(prefix) == 1
        chunk = HTML.split(prefix, 1)[1].split("</section>", 1)[0]
        assert len(chunk) >= 16000, (id_, "thin chapter", len(chunk))
        children = [cls[0] for tag, cls in parser.children[n] if cls and cls[0] in {
            "chapter-frontmatter", "chapter-body", "chapter-endnav", "end-block"}]
        assert children == ["chapter-frontmatter", "chapter-body", "chapter-endnav", "end-block"], (id_, children)
        assert chunk.count('<h2 class="sec">') >= 6, (id_, "section coverage")
        assert chunk.count('class="section-objective"') >= 6, id_
        assert chunk.count('class="tbl-wrap"') >= 2, (id_, "comparison tables")
        assert chunk.count('class="analogy"') >= 2, (id_, "memory devices")
        assert chunk.count('class="hierarchy"') >= 1, (id_, "concept hierarchy")
        assert chunk.count('class="checkpoint"') >= 1, (id_, "checkpoint")
        assert chunk.count('class="concept-rel"') >= 1, (id_, "concept relationships")
        assert chunk.count('class="box ') >= 5, (id_, "semantic callouts")
        assert chunk.count('class="revision-sheet"') == 1, id_
        assert chunk.count('class="rev-grid"') == 1, id_
        assert chunk.count('class="keydefs"') >= 3, (id_, "print-safe definition blocks")
        assert chunk.count('class="memlist"') == 1, id_
        assert chunk.count('class="examq"') == 1, id_
        block = chunk.split('<div class="end-block">', 1)[1]
        titles = re.findall(r'<h2 class="endh">([^<]+)</h2>', block)
        assert len(titles) == len(SIX), (id_, titles)
        assert titles[:3] == SIX[:3], (id_, titles)
        assert titles[3].startswith("Key Table"), (id_, titles)
        assert titles[4:] == SIX[4:], (id_, titles)
        assert re.findall(r'<div class="examq-cat">([^<]+)</div>', block) == FIVE, id_
        assert chunk.count('class="box concept"') == 1, id_
        assert f'@page ch3-4-{n}' in CSS, (id_, "missing light print template")
        assert f'@page rev3-4-{n}' in CSS, (id_, "missing dark print template")
        assert f'#ch3-4-{n} .chapter-body' in CSS, (id_, "missing print page assignment")
        assert f'#ch3-4-{n} .end-block' in CSS, (id_, "missing dark assignment")
        for rendered in [INDEX, SUB]:
            assert rendered.count(f'id="{id_}"') == 1, (id_, "missing or duplicate published chapter")
            assert f'<a class="toc-item" href="#{id_}">' in rendered, (id_, "missing TOC entry")
        assert f'<a class="endnav-btn" href="#ch3-4-{n-1}">' in chunk, (id_, "missing previous")
        if n < 9:
            assert f'href="#ch3-4-{n+1}"' in chunk, (id_, "missing next")
    print("PASS: five substantive, six-part, print-registered 3.4 dossiers; sibling print DOM and linked revisions verified.")


if __name__ == "__main__":
    run()
