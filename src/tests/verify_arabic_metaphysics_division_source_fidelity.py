#!/usr/bin/env python3
"""Arabic 2.2.2 contract: all eight source pages, house density, 13 anchored Companions.

Primary DOCX, three Arabic syntheses, the language profile and private writing
samples remain outside the public repo. No verified source author name exists.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
chapter_file = (ROOT / "src/chapters/subtopic-2-2.html").read_text(encoding="utf-8")
start = chapter_file.index('<section class="chapter rtl" id="ch2-2-2"')
chapter = chapter_file[start:chapter_file.index("\n</section>", start) + len("\n</section>")]
body = chapter[chapter.index('<div class="chapter-body">'):chapter.index('<nav class="chapter-endnav"')]
revision = chapter[chapter.index('<div class="end-block">'):]

class Pools(HTMLParser):
    aids = {"golden-quote", "box", "section-objective", "hierarchy",
            "tbl-wrap", "checkpoint", "concept-rel", "analogy", "historical-timeline"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.words = {"prose": 0, "aids": 0, "depth": 0}
    def handle_starttag(self, tag, attrs):
        if tag in {"br", "hr", "img", "input", "meta", "link"}:
            return
        self.stack.append((tag, set(dict(attrs).get("class", "").split())))
    def handle_startendtag(self, tag, attrs):
        return
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
    def handle_data(self, content):
        classes = {cl for _, values in self.stack for cl in values}
        key = ("depth" if "hikam-source-depth-inline" in classes
               else "aids" if self.aids & classes else "prose")
        self.words[key] += len(content.split())

p = Pools()
p.feed(body)
assert 650 <= p.words["prose"] <= 850, p.words
assert 850 <= p.words["aids"] <= 1150, p.words
assert 1500 <= p.words["prose"] + p.words["aids"] <= 2000, p.words
assert p.words["depth"] >= 550
assert chapter.startswith('<section class="chapter rtl" id="ch2-2-2" lang="ar" style="--hue:128;"')
assert '<h1 class="chapter-title">التقسيم التقليدي للميتافيزيقا</h1>' in chapter
assert "لم يرد اسم المؤلف" in chapter
assert len(re.findall(r'<h2 class="sec">', body)) == 6
assert len(re.findall(r'<h2 class="endh">', revision)) == 6
assert len(re.findall(r'class="examq-cat"', revision)) == 5
assert all(t in revision for t in ("إجابة قصيرة", "إجابة مطوّلة", "مقارنة", "مفاهيمي", "تطبيقي"))
depths = list(re.finditer(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', body))
assert len(depths) == 7
assert body.count('class="hikam-source-depth-item"') == 11
assert sum(map(int, re.findall(r'data-depth-count="(\d+)"', body))) == 11
for d in depths:
    assert body[:d.start()].rstrip().endswith("</p>"), "Source Depth must be adjacent to ordinary prose"
    assert ' open' not in d.group(0).split(">", 1)[0]
    assert "hikam-source-depth-citation" in d.group(0)

visible = re.sub(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', "", body)
units = [
    ("Wolff and tentative identification", "ربما كان من أبرز من اهتموا"),
    ("four subjects", "تقسيم الميتافيزيقا إلى أربعة مباحث"),
    ("original list and exposition mismatch", "خلاف ترتيبهما في القائمة الافتتاحية"),
    ("Aristotle's being as being", "«الوجود بما هو وجود»"),
    ("ontology and epistemology", "الخصائص العامة للوجود"),
    ("Hegel unity of knowledge and being", "اتحد الوجود والمعرفة"),
    ("Heidegger Dasein", "«الوجود المتعين»"),
    ("Sartre in-itself", "«الوجود في ذاته»"),
    ("Sartre for-itself", "«الوجود لأجل ذاته»"),
    ("Sartre existence preceding essence", "أسبق من ماهيته"),
    ("facticity", "«الوجود الواقعي»"),
    ("soul spirit distinction", "الفرق بين النفس والروح"),
    ("Descartes interaction", "مشكلة التفاعل بين النفس والبدن"),
    ("immortality question", "أدلة خلودها"),
    ("free will theological", "مشكلة الجبر والاختيار"),
    ("free will law", "عمومية السببية والقانون"),
    ("modern evolutionary freedom", "حدث جديد في مجرى التطور"),
    ("cosmology time and space", "طبيعة الزمان والمكان"),
    ("life as substance", "جوهر مستقل"),
    ("life as functions", "التغذية والتنفس والإخراج والتمثل"),
    ("origin of life alternatives", "جاءت من كوكب آخر"),
    ("special/general creation kept undefined", "الخلق الخاص والخلق العام"),
    ("Hegel's cosmology", "العرضية والضرورة والأزل"),
    ("evil in Hegelian cosmology", "قوانين التغير وأصل الشر"),
    ("teleology problem", "مشكلة الغائية"),
    ("Stace", "ولتر ستيس"),
    ("three enumerated theologies", "ثلاث مجموعات"),
    ("theism", "التأليه"),
    ("deism", "«الطبيعيين الإلهيين»"),
    ("deist rejection of revelation", "ينكرون الوحي والرسل والكتب المقدسة"),
    ("atheism", "الإلحاد"),
    ("agnosticism", "تعليق الحكم"),
    ("problem of evil attributed to some", "كثيراً من الفلاسفة نفوا"),
    ("physical and moral evil", "الشر الفيزيقي"),
    ("religious experience", "التجربة الدينية"),
    ("fear as cited theory rather than narrator conclusion", "تفسير بعض المفكرين نشأة الدين بالخوف"),
    ("essential attributes", "صفات الذات"),
    ("action attributes", "صفات الفعل"),
    ("attributes relation to essence", "«إشكال الصفات»"),
    ("self-subsistence versus rationality", "القيومية أو العقلانية"),
    ("negative theology", "«ليس كمثله شيء»"),
    ("Kant critique", "«ميتافيزيقا دجماطيقية»"),
    ("examine faculties first", "قبل فحص إمكان معرفتها"),
    ("Hegel critical appreciation", "أيد أهمية النقد الكانطي"),
    ("Hegel system logic nature spirit", "مقولات المنطق وفلسفة الطبيعة وفلسفة الروح"),
    ("Hegel dialectical sequence", "سلسلة متصلة الحلقات")
]
for label, text in units:
    assert text in visible, f"Missing visible primary-source unit: {label}: {text}"
assert "ربما" in visible, "Wolff's tentative historical status must not be strengthened"
assert "ثلاث مجموعات" in visible and "بعد القسم الثالث" in visible
assert "على أنه رأياً" not in visible
manifest = json.loads((ROOT / "src/reading_companions.json").read_text(encoding="utf-8"))
items = [x for x in manifest["companions"] if x["chapter"] == "ch2-2-2"]
assert len(items) == 13
assert all(x["source"]["author"] == "المؤلف غير مذكور في النص المقرر" for x in items)
assert all(all(1 <= v <= 8 for v in x["source"]["printedPages"]) for x in items)
assert all(x.get("simple") and x.get("why_here") and x.get("remember") for x in items)
print("PASS: Arabic 2.2.2 full 8-page source: "
      f"{p.words['prose']} prose / {p.words['aids']} visible aids / {p.words['depth']} optional depth; "
      "13 Companions, eleven source records, six revision zones")
