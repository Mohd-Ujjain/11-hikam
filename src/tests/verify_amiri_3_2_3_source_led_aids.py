#!/usr/bin/env python3
"""Source-faithful fine-tuning 3.2.3: semantics, archival Git blobs and exact Companions."""
from __future__ import annotations
from hashlib import sha1
from html.parser import HTMLParser
from pathlib import Path
import json
import re

SRC = Path(__file__).resolve().parents[1]
raw = (SRC / 'chapters/subtopic-3-2.html').read_text(encoding='utf-8')
start_tag = '<section class="chapter rtl" id="ch3-2-3" lang="ar" style="--hue:8;">'
assert raw.count(start_tag) == 1
start = raw.index(start_tag)
chapter = raw[start:raw.index('\n</section>', start) + len('\n</section>')]
front = chapter.split('<div class="chapter-body">',1)[0]
body = chapter.split('<div class="chapter-body">',1)[1].split('<nav class="chapter-endnav"',1)[0]
depth_regex = r'<details class="hikam-source-depth-inline"[^>]*>[\s\S]*?</details>'
visible = re.sub(depth_regex, '', body)
assert 'سامي عامري' in front and 'برهان الضبط الدقيق' in front
assert '--hue:8' in chapter and 'lang="ar"' in chapter
assert 'href="#ch3-2-4"' in chapter
assert chapter.count('class="sec"') == 5
assert chapter.count('class="endh"') == 6
assert chapter.count('class="examq-cat"') == 5
assert len(re.findall(depth_regex, body)) == 5
assert 'ص 441 و443–461' in front

def git_blob(path: Path) -> str:
    raw_bytes = path.read_bytes()
    return sha1(f'blob {len(raw_bytes)}\0'.encode()+raw_bytes).hexdigest()

archive = SRC / 'archive/pre-redevelopment-2026-11-21/dossier-3.2.3-before-2026-11-28-pedagogical-rework.html'
old_original = SRC / 'archive/pre-redevelopment-2026-11-21/dossier-3.2.3.html'
assert git_blob(archive) == '5b7dfde49d5a2c08518f37c73b6ff573a2f24d26'
assert git_blob(old_original) == 'fcedc9256c33f26c8034fc27fe3799063dec84d7'
archived = archive.read_text(encoding='utf-8')
assert archived.count('class="comparison"') == 6
assert archived.count('class="endh"') == 6
assert archived.count('class="examq-cat"') == 5
assert (SRC / 'docs/editorial/READING_3_2_3_AMERI_FINE_TUNING_SOURCE_AUDIT.md').exists()

AIDS=set('box checkpoint comparison tbl-wrap section-objective golden-quote hierarchy analogy concept-rel'.split())
class WordCount(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.count = [], [0, 0]
    def handle_starttag(self, tag, attrs):
        if tag not in {'br','hr','input','img','link','meta'}:
            self.stack.append((tag, bool(AIDS & set(dict(attrs).get('class','').split()))))
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                break
    def handle_data(self, text):
        self.count[int(any(is_aid for _,is_aid in self.stack))] += len(text.split())

word_count=WordCount()
word_count.feed(visible)
prose,aids=word_count.count
assert 650<=prose<=850, word_count.count
assert 850<=aids<=1150, word_count.count
assert 1500<=prose+aids<=2000, word_count.count
assert visible.count('class="comparison"') == 3
assert chapter.count('class="comparison"') == 4   # revision key table is independent
assert visible.count('scope="col"') == 9
assert visible.count('scope="row"') == 10
assert visible.count('class="hierarchy"') == 3
assert visible.count('class="box mistake"') == 1
assert visible.count('class="box memory"') == 2
assert visible.count('class="box definition"') == 1
assert visible.count('class="box tip"') == 1
assert visible.count('class="concept-rel"') == 1
assert visible.count('class="analogy"') == 1

for required in (
    'دليل العناية', 'الصيغة الرباعية', 'الضرورة المادية',
    'تفسيرًا', 'الصدفة', 'الحكمة', '١٩', '٣٧', '١٥٠',
    'القوة النووية الكبرى', 'القوة الكهرومغناطيسية',
    'مبدأ التكميم', 'الثابت الكوني',
    'بنروز', 'فن وايلن', 'هاوكنغ', 'مارتن ريس',
    'ستة', 'الماء', 'الكربون', 'هندرسون', 'دينتون'
):
    assert required in visible, (required, word_count.count)
assert 'مباحث الاعتراض' in chapter
for label in ('خلاصة الدرس','ورقة المراجعة المختصرة','التعريفات الأساسية',
              'الجدول الجامع','مفاتيح الاستذكار','أسئلة محتملة للامتحان'):
    assert label in chapter
assert 'الاستبعاد في حدود العادة' in chapter
assert 'الإنتروبيا' in chapter.split('<div class="end-block">')[1]

cues = [item for item in json.loads((SRC/'reading_companions.json').read_text(encoding='utf-8'))['companions']
        if item['chapter'] == 'ch3-2-3']
assert len(cues)==5
depths=re.findall(depth_regex,body)
for cue in cues:
    passage=cue['passage']
    assert body.count(passage) == 1, cue['id']
    assert cue['text'] in passage, cue['id']
    assert cue['source']['author'] == 'سامي عامري'
    assert all(p==441 or 443<=p<=461 for p in cue['source']['printedPages'])
    assert all(cue.get(k) for k in ('simple','why_here','remember','sourceDepthId'))
    matches=[x for x in depths if cue['sourceDepthId'] in x]
    assert len(matches)==1, cue['id']
    detail=matches[0]
    assert '<summary>' in detail and ' open' not in detail.split('>',1)[0]
    preceding=body[:body.index(detail)].rstrip()
    assert preceding.endswith('</p>'), cue['id']
    assert cue['text'] in preceding[preceding.rfind('<p>'):], cue['id']

print(f'PASS 3.2.3: {prose} prose + {aids} aids = {prose+aids}; 3 true comparisons, 3 hierarchies, 5 exact cues/Depth, immutable predecessor, all six revision sections',flush=True)
