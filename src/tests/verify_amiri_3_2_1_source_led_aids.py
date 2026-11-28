#!/usr/bin/env python3
"""3.2.1 Samy Ameri: source distinctions, true aids, density, anchors and immutable archives."""
from __future__ import annotations

from hashlib import sha1
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
module = (ROOT / 'chapters/subtopic-3-2.html').read_text(encoding='utf-8')
key = 'ch3-2-1'
start = module.index('<section class="chapter rtl" id="ch3-2-1" lang="ar" style="--hue:328;">')
chapter = module[start:module.index('\n</section>', start) + len('\n</section>')]
front = chapter.split('<div class="chapter-body">', 1)[0]
body = chapter.split('<div class="chapter-body">', 1)[1].split('<nav class="chapter-endnav"', 1)[0]
visible = re.sub(r'<details class="hikam-source-depth-inline"[^>]*>[\s\S]*?</details>', '', body)
original = ROOT / 'archive/pre-redevelopment-2026-11-21/dossier-3.2.1-before-2026-11-28-pedagogical-rework.html'
old = original.read_bytes()
blob = sha1(f'blob {len(old)}\0'.encode() + old).hexdigest()
assert blob == '8f1a4f6ee18ee5464104c73d35a80cb3b1f543ff', blob
assert old.decode('utf-8').count('class="comparison"') == 6
assert old.decode('utf-8').count('class="endh"') == 6
assert (ROOT / 'docs/editorial/READING_3_2_1_AMERI_FITRA_SOURCE_PEDAGOGY_AUDIT.md').exists()

assert 'سامي عامري' in front and '<h1 class="chapter-title">تمهيد — برهان النزوع الفطري</h1>' in front
assert chapter.count('class="sec"') == 5
assert chapter.count('class="endh"') == 6
assert chapter.count('class="examq-cat"') == 5
assert 'href="#ch3-2-2"' in chapter
assert chapter.count('class="hikam-source-depth-inline"') == 5

aids = {'box','checkpoint','comparison','tbl-wrap','section-objective','golden-quote','hierarchy','analogy','concept-rel'}
class WordPools(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.count = [0,0]
    def handle_starttag(self, tag, attrs):
        if tag not in {'br','hr','img','input','meta','link'}:
            classes=set(dict(attrs).get('class','').split())
            self.stack.append((tag,bool(classes & aids)))
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                break
    def handle_data(self, value):
        self.count[int(any(flag for _,flag in self.stack))] += len(value.split())

counter = WordPools()
counter.feed(visible)
prose, aids_words = counter.count
assert 650 <= prose <= 850, counter.count
assert 850 <= aids_words <= 1150, counter.count
assert 1500 <= prose + aids_words <= 2000, counter.count

assert visible.count('class="comparison"') == 2
assert chapter.count('class="comparison"') == 3  # includes unchanged revision key table
assert visible.count('scope="col"') == 6
assert visible.count('scope="row"') == 6
assert visible.count('class="hierarchy"') == 4
assert visible.count('class="box tip"') == 1
assert visible.count('class="box mistake"') == 1
assert visible.count('class="box memory"') == 1
assert visible.count('class="box definition"') == 1
assert visible.count('class="checkpoint"') == 2
assert visible.count('class="concept-rel"') == 2
assert visible.count('class="analogy"') == 1
assert 'مقارنة الأساس المعرفي: العلم الحضوري والحصولي' in visible
assert 'ما الفطرة وما الذي لا تعنيه؟' in visible
assert 'صياغة برهان الفطرة في سبع حلقات' in visible
for phrase in ('الشاهد التاريخي', 'التفسير المنافس', 'منزلة النزوع', 'أثر التشكيك',
               'لزوم التصديق', 'تطبيق اللزوم', 'نتيجة البرهان',
               'كولومبيا البريطانية سنة 2011', 'دراسة أحداث الحياة', 'سنة 2014',
               'باسكال', 'لويس', 'بلانتينجا', 'ساباتيه', 'هوكنج', 'الخير الأعظم', 'صور بسرعات متفاوتة'):
    assert phrase in visible, phrase
assert visible.count('class="h-node ') >= 12
assert 'الخير الأعظم هو اجتماع السعادة مع أداء الواجبات' in visible
assert 'يجب على الناس أن يسعوا' in visible
assert 'هنا ينتهي المصدر المقرر' in visible

cues = [x for x in json.loads((ROOT / 'reading_companions.json').read_text(encoding='utf-8'))['companions'] if x['chapter'] == key]
assert len(cues) == 5
evidence = next(cue for cue in cues if cue['id'] == 'h321-evidence')
assert 'عُرضت فيها صور بسرعات متفاوتة' in evidence['passage']
assert 'سرعة عرض الصور' in evidence['why_here']
assert 'جوابه السريع' not in evidence['explanation']
for cue in cues:
    assert cue['passage'] in body, cue['id']
    assert cue['text'] in cue['passage']
    source = cue['source']
    assert source['author'] == 'سامي عامري'
    assert all(165 <= n <= 185 for n in source['printedPages'])
    assert cue.get('simple') and cue.get('why_here') and cue.get('remember')
    depth = cue['sourceDepthId']
    details = next(d for d in re.findall(r'<details class="hikam-source-depth-inline"[\s\S]*?</details>', body) if depth in d)
    assert '<summary>' in details and ' open' not in details.split('>',1)[0]
print('PASS 3.2.1 Ameri:', counter.count, 'visible words; complete archives, 5 exact cues/depth, 2 real comparisons, 4 hierarchies, and full revisions')
