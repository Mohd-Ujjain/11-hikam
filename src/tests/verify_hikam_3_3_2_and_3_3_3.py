#!/usr/bin/env python3
"""Verify the first two source-led dossiers in the 3.3 catalog."""
from pathlib import Path
from html.parser import HTMLParser
import json, re
R=Path(__file__).resolve().parents[2]
S=R/'src'
ids=['ch3-3-2','ch3-3-3']
def chapter(html,key):
    return re.search(rf'(?ms)^<section class="chapter(?: rtl)?" id="{key}"[^\n]*>.*?^</section>',html)[0]
main=(S/'main.html').read_text()
index=(S/'chapters/subtopic-3-3.html').read_text()
css=(S/'philosophy_notes.css').read_text()
current=json.loads((S/'reading_companions.json').read_text())['companions']
AIDS=set('box checkpoint comparison tbl-wrap section-objective golden-quote hierarchy analogy concept-rel'.split())
DEPTH=re.compile(r'<details class="hikam-source-depth-inline"[^>]*>[\s\S]*?</details>')
class Words(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.count=[0,0]
    def handle_starttag(self,tag,attrs):
        if tag not in {'br','hr','img','input'}:
            self.stack.append((tag,bool(AIDS&set(dict(attrs).get('class','').split()))))
    def handle_endtag(self,tag):
        for i in reversed(range(len(self.stack))):
            if self.stack[i][0]==tag:
                self.stack=self.stack[:i];break
    def handle_data(self,data):
        self.count[any(v for _,v in self.stack)]+=len(data.split())
for key,hue,author,prev,nxt in zip(ids,(268,288),('أحمد إبراهيم','علي آل محسن'),('ch3-2-8','ch3-3-2'),('ch3-3-3','ch3-3-4')):
    sec=chapter(index,key)
    assert sec.startswith(f'<section class="chapter rtl" id="{key}" lang="ar" style="--hue:{hue};">')
    assert sec.count('class="endh"')==6 and sec.count('class="examq-cat"')==5
    assert f'<strong>{author}</strong>' in sec
    assert f'@page {key}' in css and f'@page rev{key[2:]}' in css
    assert author in [line for line in main.splitlines() if f'href="#{key}"' in line][0]
    nav=sec.split('<nav class="chapter-endnav"',1)[1].split('</nav>',1)[0]
    assert f'href="#{nxt}"' in nav
    body=sec.split('<div class="chapter-body">',1)[1].split('<nav class="chapter-endnav"',1)[0]
    w=Words(); w.feed(DEPTH.sub('',body))
    a,b=w.count
    assert 650<=a<=850 and 850<=b<=1150 and 1500<=a+b<=2000,(key,w.count)
    entries=[c for c in current if c['chapter']==key]
    depths=list(DEPTH.finditer(body))
    assert len(entries)==len(depths)>0
    for c in entries:
        assert c['source']['author']==author
        supported=set(range(288,315)) if key==ids[0] else { *range(38,42), *range(44,49), *range(64,70), *range(72,75), *range(76,79), *range(80,83), *range(84,88) }
        assert set(c['source']['printedPages']) <= supported,(key,c['id'],c['source']['printedPages'])
        assert all(c.get(k) for k in ('simple','why_here','remember','sourceDepthId'))
        d=next(x for x in depths if c['sourceDepthId'] in x[0])
        assert ' open' not in d[0].split('>',1)[0]
        i=body.rfind('<p>',0,d.start())
        assert c['text'] in body[i:d.start()] and body[:d.start()].rstrip().endswith('</p>')
    print(f'PASS {key}: prose {a} + aids {b} = {a+b} visible words; {len(entries)} anchored Companions and closed Depth')
