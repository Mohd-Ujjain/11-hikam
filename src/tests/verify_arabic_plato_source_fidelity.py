#!/usr/bin/env python3
"""Source and Arabic edition contract for the 12-page Plato reading 2.1.8.

The private supplied source and user's Arabic profile remain outside the
public repository. Source units were checked against the full original DOCX.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
chapter_html = (ROOT / "src/chapters/subtopic-2-1.html").read_text(encoding="utf-8")
start = chapter_html.index('<section class="chapter rtl" id="ch2-1-8"')
chapter = chapter_html[start:]  # final 2.1 module chapter; nested source sections are not chapter boundaries
body = chapter[chapter.index('<div class="chapter-body">'):chapter.index('<nav class="chapter-endnav"')]
rev = chapter[chapter.index('<div class="end-block">'):]

class TextPools(HTMLParser):
    aid_classes = {"golden-quote", "box", "hierarchy", "analogy",
                   "section-objective", "tbl-wrap", "checkpoint",
                   "concept-rel", "historical-timeline"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.counts = {"prose": 0, "aids": 0, "depth": 0}
    def handle_starttag(self, tag, attrs):
        if tag in {"br", "hr", "img", "meta", "input", "link", "source"}:
            return
        self.stack.append((tag, set(dict(attrs).get("class", "").split())))
    def handle_startendtag(self, tag, attrs):
        return
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return
    def handle_data(self, text):
        parents = [cls for _, group in self.stack for cls in group]
        target = ("depth" if "hikam-source-depth-inline" in parents
                  else "aids" if any(x in self.aid_classes for x in parents)
                  else "prose")
        self.counts[target] += len(text.split())

pools = TextPools()
pools.feed(body)
assert 650 <= pools.counts["prose"] <= 850, pools.counts
assert 850 <= pools.counts["aids"] <= 1150, pools.counts
assert 1500 <= pools.counts["prose"] + pools.counts["aids"] <= 2000, pools.counts
assert pools.counts["depth"] >= 500, pools.counts
assert chapter.startswith('<section class="chapter rtl" id="ch2-1-8" lang="ar"')
assert 'style="--hue:88;"' in chapter
assert '<h1 class="chapter-title">أفلاطون: المدينة الفاضلة</h1>' in chapter
assert 'اسم المؤلف غير مذكور في الملف' in chapter
assert len(re.findall(r'<h2 class="sec">', body)) == 6
assert len(re.findall(r'<h2 class="endh">', rev)) == 6
assert len(re.findall(r'class="examq-cat"', rev)) == 5

# The important original-source units must be in the visible study reading,
# not hidden in optional depth or accessible only through the JS companions.
visible = re.sub(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', '', body)
units = [
    ("historical context", "سقراط"),
    ("rulers' disputes", "بالخلاف بين أفراد السلطة الحاكمة"),
    ("breeding rule", "أوقات التوالد"),
    ("timocracy", "التيموقراطية"),
    ("wealth and oligarchy", "الأوليجاركية"),
    ("poor revolt", "يثور الفقراء"),
    ("democracy and tyranny", "الطاغوتية"),
    ("education in common", "تربية جماعية"),
    ("philosopher-king age stages", "٣٠–٣٥"),
    ("arrival and union terminology", "«الوصول» و«الحلول»"),
    ("monarchy and aristocracy", "أريستقراطي"),
    ("justice as functional non-equality", "اللامساواة الوظيفية"),
    ("three soul faculties", "الشهوانية"),
    ("three classes", "طبقة عامة الشعب"),
    ("exclusion of people from ruler training", "لا يدخل طبقة عامة الشعب"),
    ("elite collective family and property", "الحكام والحراس"),
    ("Plato / Marx contrast", "كارل ماركس"),
    ("body/finger example", "الإصبع"),
    ("early personal wisdom / late codification", "القانون الجامد"),
    ("Karam's tentative observation", "يوسف كرم"),
    ("Saunders's comparison", "تريفور سوندرز"),
    ("wealth ranks behind soul and body", "بعد الروح والجسد"),
    ("universal citizen vote but no mandatory democracy", "دون أن يجعل الديمقراطية نظاماً لازماً"),
    ("moderate Persian-Athenian mix", "الفارسي المستبد"),
    ("institutional executive / legislative powers", "التنفيذي والتشريعي"),
    ("Abu Rayan's metaphysical continuity", "محمد علي أبو ريان"),
    ("Taha Husayn on textual difficulty", "طه حسين"),
    ("al-Farabi's ideal-city inheritance", "الفارابي"),
    ("legal school legacy", "المدرسة القانونية"),
    ("behavioral / positivist conflict", "الفلسفة الوضعية"),
    ("revival figures", "محسن مهدي"),
]
for label, term in units:
    assert term in visible, f"Source unit missing from visible notes: {label} / {term}"
assert '«العدالة إنما هي أن يمتلك المرء ما ينتمي فعلاً إليه، ويؤدي الوظيفة الخاصة به»' in body
assert 'أفلاطون (٤٢٧–٣٤٧ ق.م)' in body
assert 'ربما' in visible and 'يبدو' in visible, "Do not turn source's qualified law-transition interpretation into certainty"
assert "دون أن يجعل الديمقراطية نظاماً لازماً للحكم" in visible
assert 'حق التصويت لكل المواطنين' in visible
assert 'حاكم معصوم' not in visible, "No unsourced philosophical infallibility claim"
manifest = json.loads((ROOT / "src/reading_companions.json").read_text(encoding="utf-8"))
companions = [x for x in manifest["companions"] if x["chapter"] == "ch2-1-8"]
assert len(companions) == 9
assert all(x["source"]["author"] == "المؤلف غير مذكور في النص المقرر" for x in companions)
depths = re.findall(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', body)
assert len(depths) == 8 and body.count('class="hikam-source-depth-item"') == 11
assert sum(map(int, re.findall(r'data-depth-count="(\d+)"', body))) == 11
assert all("hikam-source-depth-citation" in d for d in depths)
print(f"PASS: Plato Arabic 2.1.8: {pools.counts['prose']} prose, "
      f"{pools.counts['aids']} aids, {pools.counts['depth']} depth words, "
      f"9 Companions, 11 cited optional records, six-part revision")
