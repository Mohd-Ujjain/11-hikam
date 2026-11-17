#!/usr/bin/env python3
"""One-time integration prep for dossiers 3.4.5–3.4.9."""
from pathlib import Path
import re

root = Path(".")
part = root / "src/chapters/subtopic-3-4.html"
s = part.read_text(encoding="utf-8")
needle = '<a class="endnav-btn endnav-next endnav-end" href="#toc">↑ Back to Contents</a></nav>\n<div class="end-block"><span class="ekick">Revision Block · Dossier 3.4.4</span>'
replacement = '<a class="endnav-btn endnav-next" href="#ch3-4-5">Next Dossier — Liliputian Biology →</a></nav>\n<div class="end-block"><span class="ekick">Revision Block · Dossier 3.4.4</span>'
assert needle in s, "Existing 3.4.4 forward-navigation marker missing"
s = s.replace(needle, replacement, 1)
old = '<nav class="chapter-nav"><a href="#toc">↑ Back to Contents</a></nav>'
assert s.count(old) == 5, "Expected precisely five new chapter navigation placeholders"
names = ["A Black Box under the Microscope", "Liliputian Biology", "Questions about Design", "Ten Years Later", "The Nature and Scope of Evolution", "The Origin of Life"]
for n in range(5, 10):
    prev = names[n - 5]
    nav = f'<nav aria-label="Chapter navigation" class="chapter-endnav"><a class="endnav-btn" href="#ch3-4-{n-1}">← Previous Dossier — {prev}</a>'
    if n < 9:
        nav += f'<a class="endnav-btn endnav-next" href="#ch3-4-{n+1}">Next Dossier — {names[n-3]} →</a>'
    else:
        nav += '<a class="endnav-btn endnav-next endnav-end" href="#toc">↑ Back to Contents</a>'
    s = s.replace(old, nav + "</nav>", 1)
assert s.count(old) == 0
part.write_text(s, encoding="utf-8")

# Align metadata with the GitHub Pages project name.
for name in ("src/main.html", "sitemap.xml", "robots.txt", "README.md"):
    p = root / name
    data = p.read_text(encoding="utf-8")
    data = data.replace("https://mohdujjain.github.io/11am-hikam/", "https://mohdujjain.github.io/11-hikam/")
    if name == "README.md":
        data = re.sub(r"\b34\b", "39", data)
    p.write_text(data, encoding="utf-8")
p = root / "manifest.webmanifest"
p.write_text(p.read_text(encoding="utf-8").replace('"id": "/11am-hikam/"', '"id": "/11-hikam/"'), encoding="utf-8")

# The publication smoke test must follow the new Pages project path.
test = root / "src/tests/verify_publication.py"
test.write_text(test.read_text(encoding="utf-8")
    .replace("https://mohdujjain.github.io/11am-hikam/", "https://mohdujjain.github.io/11-hikam/")
    .replace("'/11am-hikam/'", "'/11-hikam/'"), encoding="utf-8")

# Scope the original 3.4.4 fidelity guard to its own chapter.
audit = root / "src/tests/verify_editorial_fidelity.py"
audit_text = audit.read_text(encoding="utf-8")
audit_text = "\n".join(
    line + ".split('</section>', 1)[0]" if line.strip().startswith("chapter_34 = text.split(")
    else line for line in audit_text.split("\n")
)
audit.write_text(audit_text, encoding="utf-8")

# Keep authored chapter counts and regression expectations consistent.
for p in (root / "src/tests").glob("*"):
    if p.suffix not in (".py", ".mjs"):
        continue
    data = p.read_text(encoding="utf-8")
    revised = re.sub(r"\b34\b", "39", data)
    if revised != data:
        p.write_text(revised, encoding="utf-8")

assert all(f'id="ch3-4-{n}"' in s for n in range(5, 10))
print("Prepared metadata, nav and checks for the 39-dossier edition")
