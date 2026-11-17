#!/usr/bin/env python3
"""One-time restoration of 3.4.5–3.4.9 to the established Hikam dossier layout.

Canonical output is src/chapters/subtopic-3-4.html; draft chapter JSON files are
only build inputs to be removed from the repository after publication.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
PART = SRC / "chapters/subtopic-3-4.html"
DRAFTS = SRC / "tools/house_dossier_inputs"


def esc(value: str) -> str:
    return html.escape(value, quote=False)


def definition_groups(defs: list[list[str]]) -> str:
    groups = []
    for start in range(0, len(defs), 4):
        rows = "".join(
            f'<div class="keydef-item"><div class="kd-term">{esc(name)}</div>'
            f'<div class="kd-def">{esc(desc)}</div></div>'
            for name, desc in defs[start:start + 4]
        )
        flag = ' data-continuation="true"' if start else ''
        groups.append(f'<div class="keydefs"{flag}>{rows}</div>')
    return "\n".join(groups)


def render(d: dict) -> str:
    n = int(d["n"])
    assert 5 <= n <= 9
    title = esc(d["title"])
    kicker = esc(d["source"])
    hue = 148 + (n - 4) * 20
    road = "\n".join(f"<li>{esc(t)}</li>" for t in d["roadmap"])
    section_text = []
    for index, sec in enumerate(d["sections"]):
        numeral = ["I", "II", "III", "IV", "V", "VI", "VII"][index]
        section_text.append(
            f'<h2 class="sec"><span class="secnum">§{numeral}</span>{esc(sec["title"])}</h2>'
            f'\n<div class="section-objective"><b>This section answers: </b>{esc(sec["question"])}</div>\n'
            f'{sec["html"].strip()}'
        )
    summary = "".join(f"<p>{para}</p>" for para in d["summary"])
    sheet = "".join(
        f'<div class="rev-item"><b>{esc(name)}</b><span>{value}</span></div>'
        for name, value in d["sheet"]
    )
    memory = "".join(
        f'<li><b>{esc(name)}</b>{value}</li>' for name, value in d["memory"]
    )
    categories = ["Short Answer", "Long Answer", "Comparison", "Conceptual", "Application"]
    assert all(cat in d["questions"] and len(d["questions"][cat]) >= 3 for cat in categories)
    exam = "".join(
        f'<div class="examq-cat">{cat}</div><ol>'
        + "".join(f"<li>{esc(question)}</li>" for question in d["questions"][cat])
        + "</ol>"
        for cat in categories
    )
    previous = d["prev"]
    next_label = d.get("next")
    nav = (
        f'<nav aria-label="Chapter navigation" class="chapter-endnav">'
        f'<a class="endnav-btn" href="#ch3-4-{n-1}">← Previous Dossier — {esc(previous)}</a>'
        + (f'<a class="endnav-btn endnav-next" href="#ch3-4-{n+1}">Next Dossier — {esc(next_label)} →</a>'
           if next_label else '<a class="endnav-btn endnav-next endnav-end" href="#toc">↑ Back to Contents</a>')
        + "</nav>"
    )
    golden = "".join(
        f'<div class="golden-quote">{quote["text"]}<cite>— {esc(quote["cite"])}</cite></div>'
        for quote in d.get("opening_quotes", [])
    )
    return f"""
<!-- CHAPTER 3.4.{n} -->
<section class="chapter" id="ch3-4-{n}" style="--hue:{hue};">
<div class="chapter-frontmatter">
<div class="chapter-banner">
<div class="chapter-tabnum"><span>DOSSIER 3.4.{n}</span></div>
<div class="chapter-stamp"><span>{esc(d["stamp"])}</span></div>
<div class="chapter-banner-inner">
<div class="chapter-kicker">3.4 · <span class="ar" lang="ar">التصميم والتطور</span> · Design &amp; Evolution<span class="dot"></span>Source: {kicker}<a class="toc-back" href="#toc">↑ Contents</a></div>
<h1 class="chapter-title">{title}</h1>
<div class="chapter-source">{esc(d["subtitle"])}</div>
</div></div>
<div class="chapter-map-pad"><div class="in-this-chapter"><h3>In This Chapter — The Argument Map</h3><ol>
{road}
</ol></div></div>
</div><!-- /chapter-frontmatter -->
<div class="chapter-body">
{golden}
<div class="box concept"><div class="box-label"><span class="ico">C</span>Central Thesis — {esc(d["thesis_label"])}</div><p>{d["thesis"]}</p></div>
{"".join(section_text)}
{d["closing"].strip()}
</div><!-- /chapter-body -->
{nav}
<div class="end-block"><span class="ekick">Revision Block · Dossier 3.4.{n}</span>
<h2 class="endh">Chapter Summary</h2>
{summary}
<h2 class="endh">One-Page Revision Sheet</h2>
<div class="revision-sheet"><div class="rev-grid">{sheet}</div></div>
<h2 class="endh">Key Definitions</h2>
{definition_groups(d["defs"])}
<h2 class="endh">Key Table — {esc(d["table_title"])}</h2>
<p class="keytable-note">{d["table_note"]}</p>
<h2 class="endh">Memory Aids Collected</h2>
<ul class="memlist">{memory}</ul>
<h2 class="endh">Possible Examination Questions</h2>
<div class="examq">{exam}</div>
</div><!-- /end-block -->
</section>
"""


def inject_css(css: str, docs: list[dict]) -> str:
    if "@page ch3-4-5" not in css:
        needle = '  @page ch3-4-4{ @top-left{content:"3.4 · Design & Evolution";} @top-right{content:"3.4.4 · A Black Box under the Microscope";} }'
        assert css.count(needle) == 1, "Unexpected print light-page anchor"
        additions = "".join(
            f'\n  @page ch3-4-{d["n"]}{{ @top-left{{content:"3.4 · Design & Evolution";}} @top-right{{content:"3.4.{d["n"]} · {d["short_print_title"]}";}} }}'
            for d in docs
        )
        css = css.replace(needle, needle + additions, 1)
    if "@page rev3-4-5" not in css:
        begin = css.index("  @page rev3-4-4{")
        depth = 0
        end = None
        for i in range(css.index("{", begin), len(css)):
            if css[i] == "{":
                depth += 1
            if css[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        assert end is not None
        exemplar = css[begin:end]
        additions = "".join(
            "\n" + exemplar.replace("rev3-4-4", f'rev3-4-{d["n"]}')
                          .replace("Revision · 3.4.4", f'Revision · 3.4.{d["n"]}')
            for d in docs
        )
        css = css[:end] + additions + css[end:]
    assign = '  #ch3-4-4 .chapter-body, #ch3-4-4 .chapter-endnav{ page:ch3-4-4; } #ch3-4-4 .end-block{ page:rev3-4-4; }'
    assert css.count(assign) == 1
    if '#ch3-4-5 .chapter-body' not in css:
        next_lines = "".join(
            f'\n  #ch3-4-{d["n"]} .chapter-body, #ch3-4-{d["n"]} .chapter-endnav{{ page:ch3-4-{d["n"]}; }} #ch3-4-{d["n"]} .end-block{{ page:rev3-4-{d["n"]}; }}'
            for d in docs
        )
        css = css.replace(assign, assign + next_lines, 1)
    return css


def main() -> None:
    docs = [
        json.loads((DRAFTS / f"3.4.{n}.json").read_text(encoding="utf-8"))
        for n in range(5, 10)
    ]
    assert [int(d["n"]) for d in docs] == list(range(5, 10))
    s = PART.read_text(encoding="utf-8")
    anchor = "<!-- CHAPTER 3.4.5 -->"
    assert s.count(anchor) == 1
    s = s[:s.index(anchor)] + "\n".join(render(d) for d in docs)
    PART.write_text(s, encoding="utf-8")

    css = SRC / "philosophy_notes.css"
    css.write_text(inject_css(css.read_text(encoding="utf-8"), docs), encoding="utf-8")
    print("Restored five complete source-aligned house-style dossiers and print rules")


if __name__ == "__main__":
    main()
