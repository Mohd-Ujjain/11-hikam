#!/usr/bin/env python3
"""Verify source boundaries and established structure for dossiers 3.3.7 and 3.3.8."""
from pathlib import Path
from html.parser import HTMLParser
import html, json, re
R=Path(__file__).resolve().parents[2]
S=R/'src'
ids=['ch3-3-7','ch3-3-8']
pages=[set(range(75,98)),{*range(163,174),*range(207,211)}]
authors=['Alister E. McGrath and Joanna Collicutt McGrath','John C. Lennox']
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
for key,hue,prev,nxt in zip(ids,(8,28),('ch3-3-6','ch3-3-7'),('ch3-3-8','ch3-4-3')):
    sec=chapter(index,key)
    rtl=''
    lang=' lang="ar"' if rtl else ''
    assert sec.startswith(f'<section class="chapter{rtl}" id="{key}"{lang} style="--hue:{hue};">')
    author=authors[ids.index(key)]
    assert f'@page {key}' in css and f'@page rev{key[2:]}' in css
    assert sec.count('class="endh"')==6 and sec.count('class="examq-cat"')==5
    credit=re.search(r'<div class="chapter-source"[^>]*>(.*?)</div>',sec,re.S)[1]
    assert author in html.unescape(re.sub(r'<[^>]*>','',credit)),(key,credit,author)
    assert author in [line for line in main.splitlines() if f'href="#{key}"' in line][0]
    nav=sec.split('<nav class="chapter-endnav"',1)[1].split('</nav>',1)[0]
    assert f'href="#{nxt}"' in nav and f'href="#{prev}"' in nav
    body=sec.split('<div class="chapter-body">',1)[1].split('<nav class="chapter-endnav"',1)[0]
    w=Words(); w.feed(DEPTH.sub('',body))
    a,b=w.count
    assert 650<=a<=850 and 850<=b<=1150 and 1500<=a+b<=2000,(key,w.count)
    entries=[c for c in current if c['chapter']==key]
    depths=list(DEPTH.finditer(body))
    assert len(entries)==len(depths)>0
    for c in entries:
        assert c['source']['author']==author
        assert c['source']['printedPages'] and set(c['source']['printedPages'])<=pages[ids.index(key)], (key,c['id'],c['source']['printedPages'])
        assert all(c.get(k) for k in ('simple','why_here','remember','sourceDepthId'))
        d=next(x for x in depths if c['sourceDepthId'] in x[0])
        assert ' open' not in d[0].split('>',1)[0]
        i=body.rfind('<p>',0,d.start())
        assert c['text'] in body[i:d.start()] and body[:d.start()].rstrip().endswith('</p>')
    print(f'PASS {key}: prose {a} + aids {b} = {a+b} visible words; {len(entries)} anchored Companions and closed Depth')
