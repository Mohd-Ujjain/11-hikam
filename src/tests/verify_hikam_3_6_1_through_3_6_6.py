#!/usr/bin/env python3
"""Verify edition pages, readable layers, local anchors and navigation for the 3.6 dossiers."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
import re,json
S=Path(__file__).resolve().parents[1]
src=(S/'chapters/subtopic-3-6.html').read_text()
main=(S/'main.html').read_text()
css=(S/'philosophy_notes.css').read_text()
manifest=json.loads((S/'reading_companions.json').read_text())['companions']
author={1:('سامي عامري',),2:('حسين أحمد الخشن',),3:('علي آل محسن',),4:('عبد الحسين خسروپناه',),5:('سلطان بن عبد الرحمن العميري',),6:('مركز المعارف للمناهج والمتون التعليمية',)}
hue={1:148,2:168,3:188,4:208,5:228,6:248}
pages={1:{*range(23,31),*range(45,63)},2:{*range(11,28),*range(85,125)},3:set(range(218,229)),4:set(range(109,135)),5:{*range(15,22),*range(317,343)},6:{*range(16,26),*range(68,75)}}
A=set('box checkpoint comparison tbl-wrap section-objective golden-quote hierarchy analogy concept-rel'.split())
V=set('area base br col embed hr img input link meta param source track wbr'.split())
DEPTH=re.compile(r'<details class="hikam-source-depth-inline"[^>]*>[\s\S]*?</details>')
class Count(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.n=[0,0]
 def handle_starttag(self,t,attrs):
  if t not in V:self.stack.append((t,bool(A&set(dict(attrs).get('class','').split()))))
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==t:del self.stack[i:];break
 def handle_data(self,x):self.n[any(v for _,v in self.stack)]+=len(x.split())
def plain(s):return ' '.join(unescape(re.sub(r'<[^>]+>','',s)).split())
def chapter(src,key):
 start=re.search(rf'<section class="chapter(?: rtl)?" id="{key}"',src).start()
 depth=0
 for tag in re.finditer(r'</?section\b[^>]*>',src[start:]):
  depth+=-1 if tag[0].startswith('</') else 1
  if depth==0:return src[start:start+tag.end()]
 raise AssertionError(key)
for n in range(1,7):
 key=f'ch3-6-{n}'
 sec=chapter(src,key)
 start=sec.split('>',1)[0]
 rtl=' rtl'
 assert f'class="chapter{rtl}"' in start and ('lang="ar"' in start)==bool(rtl)
 assert f'--hue:{hue[n]};' in start and f'@page {key}' in css and f'@page rev{key[2:]}' in css
 assert sec.count('class="endh"')==6 and sec.count('class="examq-cat"')==5
 assert all(a in plain(re.search(r'<div class="chapter-source"[^>]*>(.*?)</div>',sec,re.S)[1]) for a in author[n])
 assert all(a in [line for line in main.splitlines() if f'href="#{key}"' in line][0] for a in author[n])
 prev='ch3-5-4' if n==1 else f'ch3-6-{n-1}'
 nav=sec.split('<nav class="chapter-endnav"',1)[1].split('</nav>',1)[0]
 assert f'href="#{prev}"' in nav,(key,nav)
 if n<6:assert f'href="#ch3-6-{n+1}"' in nav,(key,nav)
 body=sec.split('<div class="chapter-body">',1)[1].split('<nav class="chapter-endnav"',1)[0]
 w=Count();w.feed(DEPTH.sub('',body));a,b=w.n
 assert 650<=a<=850 and 850<=b<=1150 and 1500<=a+b<=2000,(key,a,b)
 cues=[c for c in manifest if c['chapter']==key]; blocks=list(DEPTH.finditer(body))
 assert len(cues)==len(blocks)>0
 for c in cues:
  assert all(a in c['source']['author'] for a in author[n])
  assert all(c.get(k) for k in ('simple','why_here','remember','sourceDepthId'))
  assert c['source']['printedPages'] and set(c['source']['printedPages'])<=pages[n], (key,c['id'],c['source']['printedPages'])
  target=next(x for x in blocks if f'id="{c["sourceDepthId"]}"' in x[0])
  assert ' open' not in target[0].split('>',1)[0]
  previous=re.search(r'<p(?:\s[^>]*)?>((?:(?!</p>)[\s\S])*)</p>\s*$',body[:target.start()])
  assert previous and c['text'] in plain(previous[1]), (key,c['id'])
 print(f'PASS {key}: {a} prose + {b} aids = {a+b}; {len(cues)} exact linked Companions')
assert 'href="#ch3-6-7"' not in main and 'id="ch3-6-7"' not in src

for name in ('subtopic-3-4.html','subtopic-3-6.html'):
 html=(S/'chapters'/name).read_text()
 assert not any(ord(c)<32 and c not in '\t\r\n' for c in html), f'Unexpected control character in {name}'
 for label in re.findall(r'<nav class="chapter-endnav" aria-label="([^"]+)"',html):
  assert label.strip()
