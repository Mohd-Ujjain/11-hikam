#!/usr/bin/env python3
"""2.2.3: source-led Arabic philosophy dossier / complete eight-page DOCX audit.

The original DOCX, supplemental Arabic study drafts, language profile and
personal writing samples are private editorial materials, not repository files.
The supplied source's last sentence is incomplete. No completion is invented.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
content = (ROOT / "src/chapters/subtopic-2-2.html").read_text(encoding="utf8")
first = content.index('<section class="chapter rtl" id="ch2-2-3"')
last = content.index("\n</section>", first) + len("\n</section>")
chapter = content[first:last]
body = chapter[chapter.index('<div class="chapter-body">'):chapter.index('<nav class="chapter-endnav"')]
revision = chapter[chapter.index('<div class="end-block">'):]

class WordPools(HTMLParser):
    aids = {"golden-quote", "box", "section-objective", "hierarchy",
            "tbl-wrap", "checkpoint", "concept-rel", "analogy", "historical-timeline"}
    voids = {"br", "hr", "img", "input", "meta", "link"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.counts = {"prose": 0, "aids": 0, "depth": 0}
    def handle_starttag(self, tag, attrs):
        if tag not in self.voids:
            self.stack.append((tag, set(dict(attrs).get("class", "").split())))
    def handle_startendtag(self, tag, attrs):
        return
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
    def handle_data(self, value):
        classes = {cl for _, names in self.stack for cl in names}
        pool = ("depth" if "hikam-source-depth-inline" in classes else
                "aids" if classes & self.aids else "prose")
        self.counts[pool] += len(value.split())

p = WordPools()
p.feed(body)
assert 650 <= p.counts["prose"] <= 850, p.counts
assert 850 <= p.counts["aids"] <= 1150, p.counts
assert 1500 <= p.counts["prose"] + p.counts["aids"] <= 2000, p.counts
assert 650 <= p.counts["depth"] <= 1800, p.counts

assert chapter.startswith('<section class="chapter rtl" id="ch2-2-3" lang="ar" style="--hue:148;"')
assert '<h1 class="chapter-title">الميتافيزيقا عند فلاسفة الإسلام والمسيحية</h1>' in chapter
assert "اسم المؤلف غير مثبت" in chapter
assert "الفصل الأول" in chapter and "الفصل الثاني" in chapter
assert len(re.findall(r'<h2 class="sec">', body)) == 5
assert len(re.findall(r'<h2 class="endh">', revision)) == 6
assert len(re.findall(r'class="examq-cat"', revision)) == 5
assert all(k in revision for k in ("إجابة قصيرة", "إجابة مطوّلة", "مقارنة", "مفاهيمي", "تطبيقي"))
details = list(re.finditer(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', body))
assert len(details) == 7
assert body.count('class="hikam-source-depth-item"') == 13
assert sum(map(int, re.findall(r'data-depth-count="(\d+)"', body))) == 13
for d in details:
    assert body[:d.start()].rstrip().endswith("</p>"), "Source Depth must immediately follow an ordinary prose paragraph"
    assert ' open' not in d.group(0).split(">", 1)[0]
    assert "hikam-source-depth-citation" in d.group(0)

visible = re.sub(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', "", body)
visible_text = re.sub(r"\s+", " ", re.sub(r"<[^>]*>", " ", visible))
# Coverage gate below selects phrases wholly in a text node. It independently
# checks the intellectual home of each original unit in visible teaching.
units = {
    "author introduces four Islamic philosophers": "أربعة من فلاسفة الإسلام",
    "then Augustine as second chapter": "القديس أوغسطين",
    "source's Aristotle generalization": "بقيت في جملتها ضمن التصور الأرسطي",
    "al-Kindi named work and caliph": "رسالة إلى المعتصم بالله في الفلسفة الأولى",
    "al-Kindi polemical purpose": "إقامة الحجة على وجود الله الواحد الحق",
    "definition of philosophy human limits": "بحسب طاقة الإنسان",
    "epistemic purpose and practical act": "إصابة الحق",
    "superiority of knowing cause": "العلم بالعلة أشرف من العلم بالمعلول",
    "original rain example": "سبب سقوط المطر",
    "first cause": "العلة الأولى",
    "theology and divinity": "علم الربوبية",
    "al-Kindi material cause": "العلة المادية",
    "al-Kindi formal cause": "العلة الصورية",
    "al-Kindi efficient cause": "العلة الفاعلة",
    "al-Kindi final cause": "العلة المتممة",
    "al-Farabi existence subject": "الوجود بما هو وجود",
    "necessary vs possible": "واجب أو ممكن",
    "possible needs cause": "وكل ممكن يحتاج إلى علة",
    "no infinite regress": "تسلسل العلل إلى غير نهاية ممتنعاً",
    "necessary being no cause": "واجب الوجود الذي لا علة له",
    "self-standing one eternal intellect goodness": "عقل وخير وعاقل ومعقول",
    "no genus definition": "لا تركيب فيه ولا جنس له",
    "names as imperfect representation": "على سبيل التمثيل القاصر",
    "mathematics vs physical cognition": "معرفة الرياضيات",
    "strongest light metaphor": "أقوى الأنوار",
    "incapacity from embodiment": "المقيدة بالمادة",
    "Avicenna subject": "الموجود بما هو موجود",
    "Avicenna objects sought": "الأعراض الذاتية",
    "unity plurality causality": "الوحدة والكثرة والعلية",
    "necessary being one without peer": "واحد لا نظير له ولا جزء",
    "truth and pure good": "حق وخير محض",
    "self-intellection": "يعقل ذاته",
    "attributed author critique": "ينتقد عبارة أخرى لابن سينا",
    "the exact criticism": "خلط وتكرار لا معنى له",
    "Averroes vs al-Ghazali": "تكفير الغزالي للفلاسفة في ثلاث مسائل",
    "eternity first issue": "قِدم العالم",
    "divine knowledge second issue": "علم الله بالجزئيات",
    "bodily resurrection third issue": "بعث الأجساد",
    "sun and light contemporaneous": "كتلازم النور والشمس",
    "priority essence not chronology": "تقدم بالذات والرتبة لا بالزمان",
    "four proofs": "أربعة أدلة",
    "event from eternal": "امتناع صدور حادث عن قديم مطلقاً",
    "time prior to time": "أن يسبق الزمانَ زمانٌ",
    "eternity of possibility": "دوام إمكان العالم",
    "eternity of matter argument": "احتياج كل حادث إلى مادة سابقة",
    "al-Ghazali answered four and Averroes replied": "وقد رد الغزالي عليها",
    "Hood scripture": "وكان عرشه على الماء",
    "Ibrahim 48": "يوم تبدل الأرض غير الأرض والسماوات",
    "Fussilat 11": "وهي دخان",
    "Averroes pre-existence conclusion": "العدم المحض",
    "human knowledge caused by known": "علمنا معلول للمعلوم",
    "divine knowledge cause": "علم الله علة للمعلوم",
    "some philosophers' universals distinction": "قول بعض الفلاسفة بعلم الكليات دون الجزئيات",
    "sense and imagination": "الحس والخيال",
    "mistake of comparing two knowledges": "خطأ قياس العلم الإلهي",
    "bodily resurrection exemplary teaching": "صور المعاد الجسمانية بوصفها أمثلة للعامة",
    "al-Ghazali resurrection objection": "واعتراض الغزالي عليها",
    "limits of rational proof of afterlife": "أمور الآخرة لا يتناولها البرهان العقلي",
    "bodily metaphors are better for audience": "تمثيل المعاد بالأمور الجسمانية أنسب",
    "Augustine and evil": "مشكلة الشر سيطرت على تفكيره",
    "Augustine birthplace and birth": "طاجست سنة",
    "Augustine death Hippo": "هبون سنة",
    "mother Monica": "مونيكا مسيحية",
    "Confessions": "الاعترافات",
    "stolen pears despite better at home": "ثمار كمثرى",
    "lack of hunger": "من غير جوع",
    "contrition after conversion": "وعذابه النفسي بعد دخوله في المسيحية",
    "lying sometimes without reason": "كذبه المتكرر أحياناً بغير مبرر",
    "primary excerpt cut off": "ينتهي المصدر المرفق في أثناء الحديث عن مراهقته",
}
for label, phrase in units.items():
    assert phrase in visible, f"Missing visible source unit: {label} ({phrase})"
# The verbatim OCR/proofreading issue is not silently normalized.
assert "حرثات الأجرام السماوية" in body
assert "حركات الأجرام السماوية" in body
assert "مسألة نصية تحتاج مقابلة نسخة محققة" in body
# Recorded exact incomplete last line, without inventing the sequel.
assert "علاقاته بالنساء مركز" in body
assert "لم تُرفق بقية الجملة" in body
assert "لا تتمة متاحة" in revision
assert "لا يذكر المصدر إلا" not in visible, "Do not narrow an actual source claim"

manifest = json.loads((ROOT / "src/reading_companions.json").read_text(encoding="utf8"))
items = [x for x in manifest["companions"] if x["chapter"] == "ch2-2-3"]
assert len(items) == 13
assert all(x["source"]["author"] == "المؤلف غير مذكور في النص المقرر" for x in items)
assert all(all(1 <= page <= 8 for page in x["source"]["printedPages"]) for x in items)
assert all(all(x.get(key) for key in ("simple", "why_here", "remember")) for x in items)
assert len(set(x["id"] for x in items)) == 13
print(f"PASS: Arabic 2.2.3 full 8-page primary-source and truncation: "
      f"{p.counts['prose']} prose / {p.counts['aids']} aids / {p.counts['depth']} optional source depth; "
      "13 Companions, 13 source records, 7 disclosures, six revision sections")
