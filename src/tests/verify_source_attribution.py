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

print(f"Verified {len(READINGS)} primary-source titles and author credits in chapter frontmatter and TOC")
