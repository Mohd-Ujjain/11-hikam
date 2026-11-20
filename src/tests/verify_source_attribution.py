#!/usr/bin/env python3
"""Verify original titles and source-author attribution for primary-verified dossiers.

Add a dossier here only after its author and title have been checked against
the user's actual original reading, not a derivative study guide.
"""
from __future__ import annotations
from html import unescape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
CHAPTERS = (ROOT / "src/chapters/subtopic-1-1.html").read_text(encoding="utf-8")
MAIN = (ROOT / "src/main.html").read_text(encoding="utf-8")
READINGS = {
    "ch1-1-1": ("Towards an Assessment of Twentieth-Century Philosophy", "Dermot Moran"),
    "ch1-1-2": ("Twentieth-Century Moral Philosophy", "Rowland Stout"),
}

def plain(html: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", html)).strip()

for chapter_id, (title, author) in READINGS.items():
    start = CHAPTERS.find(f'<section class="chapter" id="{chapter_id}"')
    assert start >= 0, f"Missing chapter {chapter_id}"
    end = CHAPTERS.find("</section>", start)
    assert end > start, f"Unclosed chapter {chapter_id}"
    chapter = CHAPTERS[start:end]
    title_match = re.search(r'<h1 class="chapter-title">([\s\S]*?)</h1>', chapter)
    assert title_match and plain(title_match.group(1)) == title, f"Incorrect original title: {chapter_id}"
    attribution = re.search(r'<div class="chapter-source">([\s\S]*?)</div>', chapter)
    assert attribution and author in plain(attribution.group(1)), f"Missing source author in frontmatter: {chapter_id}"
    toc = re.search(rf'<a class="toc-item" href="#{chapter_id}">([\s\S]*?)</a>', MAIN)
    assert toc, f"Missing TOC entry: {chapter_id}"
    toc_title = re.search(r'<span class="tt">([\s\S]*?)</span>', toc.group(1))
    toc_source = re.search(r'<span class="ts">([\s\S]*?)</span>', toc.group(1))
    assert toc_title and plain(toc_title.group(1)) == title, f"Incorrect TOC title: {chapter_id}"
    assert toc_source and author in plain(toc_source.group(1)), f"Missing TOC author: {chapter_id}"

# The next source-verified reading resides in another canonical subtopic module.
bird_html = (ROOT / "src/chapters/subtopic-2-1.html").read_text(encoding="utf-8")
bird_start = bird_html.index('<section class="chapter" id="ch2-1-1"')
bird_end = bird_html.index('<nav class="chapter-endnav"',bird_start)
bird = bird_html[bird_start:bird_end]
assert '<h1 class="chapter-title">Introduction</h1>' in bird
assert 'Original author: <strong>Colin Bird</strong>' in bird
assert '<em>An Introduction to Political Philosophy</em>' in bird
bird_toc = re.search(r'<a class="toc-item" href="#ch2-1-1">([\s\S]*?)</a>', MAIN)
assert bird_toc
assert '<span class="tt">Introduction</span>' in bird_toc.group(1)
assert '<span class="ts">Colin Bird · Cambridge</span>' in bird_toc.group(1)

# Bird chapter 2: verify the original source title and credit independently
# from the previous Introduction, preserving both contents entries.
common_start = bird_html.index('<section class="chapter" id="ch2-1-2"')
common_end = bird_html.index('<nav class="chapter-endnav"',common_start)
common = bird_html[common_start:common_end]
assert '<h1 class="chapter-title">The Common Good</h1>' in common
assert 'Original author: <strong>Colin Bird</strong>' in common
assert 'Chapter 2, “The Common Good,”' in common
assert '<em>An Introduction to Political Philosophy</em>' in common
common_toc = re.search(r'<a class="toc-item" href="#ch2-1-2">([\s\S]*?)</a>', MAIN)
assert common_toc
assert '<span class="tt">The Common Good</span>' in common_toc.group(1)
assert '<span class="ts">Colin Bird · Cambridge</span>' in common_toc.group(1)

# 2.1.3 belongs to the second edition (2019): it is chapter 11, not
# chapter 10 as in the distinct 2006 first edition.
war_start = bird_html.index('<section class="chapter" id="ch2-1-3"')
war_end = bird_html.index('<nav class="chapter-endnav"', war_start)
war = bird_html[war_start:war_end]
assert '<h1 class="chapter-title">War</h1>' in war
assert 'Original author: <strong>Colin Bird</strong>' in war
assert 'Chapter 11, “War,”' in war and '2nd ed.' in war and '2019' in war
assert '<em>An Introduction to Political Philosophy</em>' in war
war_toc = re.search(r'<a class="toc-item" href="#ch2-1-3">([\s\S]*?)</a>', MAIN)
assert war_toc
assert '<span class="tt">War</span>' in war_toc.group(1)
assert '<span class="ts">Colin Bird · Cambridge</span>' in war_toc.group(1)

# Wolff 2.1.4 combines the Oxford Introduction and opening Who Should Rule?
wolff_start = bird_html.index('<section class="chapter" id="ch2-1-4"')
wolff_end = bird_html.index('<nav class="chapter-endnav"', wolff_start)
wolff = bird_html[wolff_start:wolff_end]
assert '<h1 class="chapter-title">Introduction &amp; Who Should Rule?</h1>' in wolff
assert 'Original author: <strong>Jonathan Wolff</strong>' in wolff
assert '<em>An Introduction to Political Philosophy</em>' in wolff
assert 'pp. 1–5' in wolff and 'pp. 62–77' in wolff
assert 'Oxford University Press' in wolff and '2006' in wolff
wolff_toc = re.search(r'<a class="toc-item" href="#ch2-1-4">([\s\S]*?)</a>', MAIN)
assert wolff_toc
assert '<span class="tt">Introduction &amp; Who Should Rule?</span>' in wolff_toc.group(1)
assert '<span class="ts">Jonathan Wolff · Oxford</span>' in wolff_toc.group(1)
print(f"Verified {len(READINGS)+4} primary-source titles and author credits in chapter frontmatter and TOC")
