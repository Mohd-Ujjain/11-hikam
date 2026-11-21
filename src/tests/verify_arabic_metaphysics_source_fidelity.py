#!/usr/bin/env python3
"""Arabic source-fidelity and density contract for the 16-page 2.2.1 source.

The primary DOCX, private writing samples and three supplementary syntheses
are editorial inputs only; they are intentionally absent from the repository.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
text = (ROOT / "src/chapters/subtopic-2-2.html").read_text(encoding="utf-8")
start = text.index('<section class="chapter rtl" id="ch2-2-1"')
chapter = text[start:text.index("\n</section>", start) + len("\n</section>")]
body = chapter[chapter.index('<div class="chapter-body">'):chapter.index('<nav class="chapter-endnav"')]
revision = chapter[chapter.index('<div class="end-block">'):]

class WordPools(HTMLParser):
    aids = {"golden-quote", "box", "hierarchy", "analogy",
            "section-objective", "tbl-wrap", "checkpoint",
            "concept-rel", "historical-timeline"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.words = {"prose": 0, "aids": 0, "depth": 0}
    def handle_starttag(self, tag, attrs):
        if tag in {"hr", "img", "br", "input", "meta", "link", "source"}:
            return
        self.stack.append((tag, set(dict(attrs).get("class", "").split())))
    def handle_startendtag(self, tag, attrs):
        return
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
    def handle_data(self, text):
        classes = {name for _, names in self.stack for name in names}
        target = ("depth" if "hikam-source-depth-inline" in classes
                  else "aids" if self.aids & classes else "prose")
        self.words[target] += len(text.split())

pools = WordPools()
pools.feed(body)
assert 650 <= pools.words["prose"] <= 850, pools.words
assert 850 <= pools.words["aids"] <= 1150, pools.words
assert 1500 <= pools.words["prose"] + pools.words["aids"] <= 2000, pools.words
assert pools.words["depth"] >= 500, pools.words
assert chapter.startswith('<section class="chapter rtl" id="ch2-2-1" lang="ar" style="--hue:108;"')
assert '<h1 class="chapter-title">ما الميتافيزيقا...؟</h1>' in chapter
assert "اسم المؤلف غير مذكور" in chapter
assert len(re.findall(r'<h2 class="sec">', body)) == 6
assert len(re.findall(r'<h2 class="endh">', revision)) == 6
assert len(re.findall(r'class="examq-cat"', revision)) == 5
assert all(x in revision for x in ("إجابة قصيرة","إجابة مطوّلة","مقارنة","مفاهيمي","تطبيقي"))
depths = re.findall(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', body)
assert len(depths) == 7, len(depths)
assert sum(map(int, re.findall(r'data-depth-count="(\d+)"', body))) == 11
assert body.count('class="hikam-source-depth-item"') == 11
assert all('hikam-source-depth-citation' in d for d in depths)
for m in re.finditer(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', body):
    assert body[:m.start()].rstrip().endswith("</p>"), "Source Depth must immediately follow ordinary prose paragraph"
    assert ' open' not in m.group(0).split(">",1)[0], "Source Depth disclosure opens by default"

# These source units must remain immediately visible and not be moved entirely
# into optional material, Companions or the six end-of-chapter revision zones.
visible = re.sub(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', "", body)
units = [
    ("historical Greek terminology", "العصر الهليني"),
    ("Andronicus role", "أندرونيقوس الرودسي"),
    ("shelf-label origin", "ترتيبية عرضية"),
    ("first philosophy", "«الفلسفة الأولى»"),
    ("Aristotle's first cause", "العلة الأولى"),
    ("Aphrodisias' tentative precedence", "ربما"),
    ("being as being", "«الوجود بما هو وجود»"),
    ("Collingwood systematic science", "كولنجوود"),
    ("two definitional obstacles", "سببين رئيسيين"),
    ("James's critique", "وليم جيمس"),
    ("D'Alembert critique", "دالمبير"),
    ("Voltaire critique", "فولتير"),
    ("Condillac division", "كوندياك"),
    ("Engels critique", "إنجلز"),
    ("Christian Wolff", "كريستيان فولف"),
    ("Kant's Mendelssohn letter", "مندلسون"),
    ("Hegel defence", "«قدس الأقداس»"),
    ("Bradley", "برادلي"),
    ("Schopenhauer", "شوبنهاور"),
    ("A. E. Taylor's simple questions", "ألفرد إدوارد تايلور"),
    ("categories", "المقولات"),
    ("ordinary category example", "«هذه السيارة الفخمة بيضاء»"),
    ("time question and Zeno to Einstein", "زينون إلى أينشتاين"),
    ("logic analogy", "المنطق"),
    ("appearance/reality", "الظاهر والحقيقة"),
    ("a-priori analysis", "التفكير القبلي"),
    ("intuition/natural light", "«نور العقل الطبيعي»"),
    ("epistemology", "الإبستمولوجيا"),
    ("modern epistemological thinkers", "هوبز وباركلي ولوك وديكارت وهيوم وكانط"),
    ("historical vs logical sequence", "تاريخياً"),
    ("Kant's conceptual tool", "أداة المعرفة"),
    ("logical presuppositions", "«الافتراضات السابقة»"),
    ("logical not temporal priority", "لا في الزمن"),
    ("being to existence", "Existence"),
    ("being-in-world", "«الوجود في العالم»"),
    ("Pascal", "بسكال"),
    ("Omar Khayyam", "عمر الخيام"),
    ("Jaspers limit situations", "«المواقف الحدية»"),
    ("facticity", "«وقائعية الوجود»"),
    ("suicide interpretation explicitly attributed", "يقرر مؤلف الفصل"),
    ("death universal and singular", "عام لكل الناس"),
    ("death certain, time unknown", "مجهول الموعد"),
    ("immortality inquiry", "الخلود"),
    ("Christian Adam-Paulinian death and freedom", "خطيئة آدم"),
    ("Hegel on intrinsic finitude", "الفناء كامناً في الموجود"),
    ("death perceived in mature personality", "بنضج الشخصية"),
    ("fear/anxiety distinction", "الخوف"),
    ("classical mind and body", "النفس والبدن"),
    ("God proofs", "وجود الله وأدلته"),
    ("substance matter causality universals particulars", "الكليات والجزئيات"),
    ("personal identity", "الهوية الشخصية"),
]
for label, term in units:
    assert term in visible, f"Missing source unit from visible edition: {label}: {term}"
assert "يقرر مؤلف الفصل" in visible, "Do not endorse author's suicide interpretation as a general fact"
assert "في تفسير مسيحي" in visible, "Do not attribute Christian doctrine universally"
assert "ربما" in visible, "Do not turn Aphrodisias' tentative chronological priority into certainty"
assert "تاريخياً" in visible and "منطقياً" in visible, "Preserve historical/logical distinction"
manifest = json.loads((ROOT / "src/reading_companions.json").read_text(encoding="utf-8"))
items = [c for c in manifest["companions"] if c["chapter"] == "ch2-2-1"]
assert len(items) == 12
assert all(x["source"]["author"] == "المؤلف غير مذكور في النص المقرر" for x in items)
assert all(all(1 <= pg <= 16 for pg in x["source"]["printedPages"]) for x in items)
assert all(x.get("simple") and x.get("why_here") and x.get("remember") for x in items)
print(f"PASS: Arabic 2.2.1 source: {pools.words['prose']} prose / "
      f"{pools.words['aids']} visible aids / {pools.words['depth']} optional source words, "
      "12 Companions, 11 sourced records and six revision zones")
