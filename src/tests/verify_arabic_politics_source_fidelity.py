#!/usr/bin/env python3
"""Scope-bound structural/source-regression checks for Arabic Dossier 2.1.7.

The full supplied DOCX remains outside the public repository. This is an
edition-contract check; the separately documented source coverage was
editorially verified from the 16-page supplied original.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
chapter_file = (ROOT / "src/chapters/subtopic-2-1.html").read_text(encoding="utf-8")
start = chapter_file.index('<section class="chapter rtl" id="ch2-1-7"')
end = chapter_file.index('<section class="chapter rtl" id="ch2-1-8"', start)
chapter = chapter_file[start:end]
body = chapter[chapter.index('<div class="chapter-body">'):chapter.index('<nav class="chapter-endnav"')]
revision = chapter[chapter.index('<div class="end-block">'):]

class TextPools(HTMLParser):
    aids = {"golden-quote", "box", "hierarchy", "analogy",
            "section-objective", "tbl-wrap", "checkpoint",
            "concept-rel", "historical-timeline"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.counts = {"prose": 0, "aids": 0, "depth": 0}
    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "").split()
        self.stack.append((tag, set(classes)))
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        for idx in range(len(self.stack)-1, -1, -1):
            if self.stack[idx][0] == tag:
                del self.stack[idx:]
                break
    def handle_data(self, data):
        parents = [cls for _, group in self.stack for cls in group]
        target = ("depth" if "hikam-source-depth-inline" in parents
                  else "aids" if any(cls in self.aids for cls in parents)
                  else "prose")
        self.counts[target] += len(data.split())

pools = TextPools()
pools.feed(body)
assert 650 <= pools.counts["prose"] <= 850, pools.counts
assert 850 <= pools.counts["aids"] <= 1150, pools.counts
assert 1500 <= pools.counts["prose"] + pools.counts["aids"] <= 2000
assert pools.counts["depth"] > 500

assert chapter.startswith('<section class="chapter rtl" id="ch2-1-7" lang="ar"')
assert chapter.count('<h1 class="chapter-title">تطور علم السياسة</h1>') == 1
assert 'المصدر: «الفصل الأول: تطور علم السياسة»' in chapter
assert 'اسم المؤلف غير مذكور في الملف' in chapter
assert len(re.findall(r'<h2 class="sec">', body)) == 7
assert len(re.findall(r'<h2 class="endh">', revision)) == 6
assert len(re.findall(r'class="examq-cat"', revision)) == 5

# Each substantive unit in the supplied reading must remain visible in the
# explanatory prose or the independently readable instructional aids.
source_units = [
    ("linguistic origin", "المقريزي"),
    ("Mawardi care and prophetic authority", "الماوردي"),
    ("Ibn Qayyim on text-versus-conformity", "النص الجزئي"),
    ("al-Bahr and masalih", "عبد الوهاب خلاف"),
    ("Zaydan legal-positivist division", "عبد الكريم زيدان"),
    ("De Grazia administration", "دي جريشيا"),
    ("Blom power conflict", "وليام بلوم"),
    ("science methodology", "التجربة المعملية"),
    ("three science difficulties", "التحيز"),
    ("Confucian education", "كونفوشيوس"),
    ("Greek polis", "أرسطو"),
    ("Islamic law", "الأحكام السلطانية"),
    ("Christian ecclesiastical tradition", "أوغسطين"),
    ("Renaissance legal approach", "جان بودان"),
    ("three traditional schools", "المؤسسية"),
    ("six behavioural precepts", "المبادئ الستة"),
    ("Easton three-part system", "ديفيد إيستون"),
    ("postbehavioural five objections", "خمسة اعتراضات"),
    ("return to classical philosophy", "ليو ستراوس"),
    ("university history", "كولومبيا"),
    ("French legal influence", "القانونية الفرنسية"),
]
for label, term in source_units:
    assert term in body, f"Missing essential unit in visible body: {label}"

assert '«ثم رسمت بأنها القانون الموضوع لرعاية الآداب والمصالح وانتظام الأحوال»' in body
assert '«ما كان به الناس أقرب إلى الصلاح، وأبعد عن الفساد»' in body
assert '«العمليات الاجتماعية المتميزة بالصراع والتعاون في ممارسة القوة»' in body
assert '«حيوان سياسي بطبعه»' in body
assert 'النتائج والتغذية الراجعة' not in body or 'المعطيات' in body
assert 'أربعة عناصر' not in body, "Easton enumerates exactly three elements in source"
visible_body = re.sub(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', "", body)
assert "التقصير في معرفة الشريعة ومعرفة الواقع" in visible_body
assert "العمل السياسي الجاري تاريخ معاصر" in visible_body

manifest = json.loads((ROOT / "src/reading_companions.json").read_text(encoding="utf-8"))
items = [x for x in manifest["companions"] if x["chapter"] == "ch2-1-7"]
assert len(items) == 8
assert all(x["source"]["author"] == "المؤلف غير مذكور في النص المقرر" for x in items)
details = re.findall(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', body)
assert len(details) == 7
assert body.count('class="hikam-source-depth-item"') == 9
assert sum(map(int, re.findall(r'data-depth-count="(\d+)"', body))) == 9
for x in details:
    assert ' open' not in x.split('>', 1)[0]
    assert "hikam-source-depth-citation" in x
    assert 1 <= len(re.findall(r'class="hikam-source-depth-item"', x)) <= 2

print(f"PASS: Arabic 2.1.7 source spine and six-part revision, "
      f"{pools.counts['prose']} prose + {pools.counts['aids']} study-aid words, "
      f"{len(items)} Companions, 9 cited records")
