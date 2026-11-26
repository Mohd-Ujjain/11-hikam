#!/usr/bin/env python3
"""Focused structural, attribution and density guard for the two Arabic dossiers."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re

SRC=Path(__file__).resolve().parents[1]
module=(SRC/'chapters/subtopic-3-1.html').read_text(encoding='utf-8')
toc=(SRC/'main.html').read_text(encoding='utf-8')
companions=json.loads((SRC/'reading_companions.json').read_text(encoding='utf-8'))['companions']
coverage=(SRC/'docs/editorial/READINGS_3_1_4_3_1_5_ARABIC_SOURCE_COVERAGE.md').read_text(encoding='utf-8')
aids={'box','checkpoint','comparison','tbl-wrap','section-objective','golden-quote','hierarchy','analogy','concept-rel'}
class Pool(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]
        self.count=[0,0]
    def handle_starttag(self,tag,attrs):
        if tag not in {'br','hr','img','input','meta','link'}:
            classes=set(dict(attrs).get('class','').split())
            self.stack.append((tag,bool(classes&aids)))
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                self.stack=self.stack[:i]
                break
    def handle_data(self,text):
        words=len(re.findall(r'\S+',text))
        self.count[any(y for _,y in self.stack)]+=words

for n,hue,author,title,count,limits,terms in (
    (4,288,'سامر توفيق عجمي','نظريات حول نشوء الدين: دراسة تحليلية نقدية',5,(19,46),
     ('الخلط بين الدين المنزل وممارسة الناس له','فالعلاقة طولية','أن يلزم من هذه المقدمات','الاستضعاف')),
    (5,308,'سلطان بن عبد الرحمن العميري','الاعتراضات الإجمالية التي اعترض بها الناقدون على الأديان',6,(412,442),
     ('فقدان المسوغ الترابطي','حصر البواعث','عقدة أوديب','الطوطم','نتيجة عرضية في التطور البيولوجي')),
):
    key=f'ch3-1-{n}'
    start=f'<section class="chapter rtl" id="{key}" lang="ar" style="--hue:{hue};">'
    assert module.count(start)==1
    a=module.index(start)
    chapter=module[a:module.index('\n</section>',a)+len('\n</section>')]
    assert f'<h1 class="chapter-title">{title}</h1>' in chapter and author in chapter
    line=next(l for l in toc.splitlines() if f'href="#{key}"' in l and 'toc-item' in l)
    assert title in line and author in line
    assert chapter.count('class="endh"')==6 and chapter.count('class="examq-cat"')==5
    endnav='ch3-1-5' if n==4 else 'ch3-2-1'
    assert f'href="#{endnav}"' in chapter
    body=chapter.split('<div class="chapter-body">',1)[1].split('<nav class="chapter-endnav"',1)[0]
    d=r'<details class="hikam-source-depth-inline"[\s\S]*?</details>'
    details=re.findall(d,body)
    assert len(details)==count and all(' open' not in x.split('>',1)[0] and author in x for x in details)
    visible=re.sub(d,'',body)
    assert all(t in visible for t in terms)
    p=Pool();p.feed(visible)
    assert 650<=p.count[0]<=850 and 850<=p.count[1]<=1150 and 1500<=sum(p.count)<=2000,p.count
    cues=[x for x in companions if x['chapter']==key]
    assert len(cues)==count
    assert all(x['source']['author']==author and all(limits[0]<=v<=limits[1] for v in x['source']['printedPages']) for x in cues)
    assert author in coverage and title in coverage
    print(f'PASS: 3.1.{n} title and author, RTL/hue, {count} Companions and Depth entries, 6 revisions, visible words {p.count}')
