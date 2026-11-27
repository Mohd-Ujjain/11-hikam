#!/usr/bin/env python3
"""Verify edition pages, readable layers, local anchors and navigation for the 3.4 revisions."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
import re,json
S=Path(__file__).resolve().parents[1]
src=(S/'chapters/subtopic-3-4.html').read_text()
main=(S/'main.html').read_text()
css=(S/'philosophy_notes.css').read_text()
manifest=json.loads((S/'reading_companions.json').read_text())['companions']
author={2:'سامي عامري',3:'علي آل محسن',4:'Michael J. Behe',5:'Michael J. Behe',6:'Michael J. Behe',7:'Michael J. Behe',8:'John C. Lennox',9:'John C. Lennox'}
hue={2:48,3:128,4:148,5:168,6:188,7:208,8:228,9:248}
ranges={2:(491,564),3:(282,296),4:(1,21),5:(3,25),6:(209,231),7:(255,271),8:(100,121),9:(122,134)}
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
for n in range(2,10):
 key=f'ch3-4-{n}'
 sec=chapter(src,key)
 start=sec.split('>',1)[0]
 rtl=' rtl' if n in {2,3} else ''
 assert f'class="chapter{rtl}"' in start and ('lang="ar"' in start)==bool(rtl)
 assert f'--hue:{hue[n]};' in start and f'@page {key}' in css and f'@page rev{key[2:]}' in css
 assert sec.count('class="endh"')==6 and sec.count('class="examq-cat"')==5
 assert author[n] in plain(re.search(r'<div class="chapter-source"[^>]*>(.*?)</div>',sec,re.S)[1])
 assert author[n] in [line for line in main.splitlines() if f'href="#{key}"' in line][0]
 prev='ch3-3-8' if n==2 else f'ch3-4-{n-1}'
 nav=sec.split('<nav class="chapter-endnav"',1)[1].split('</nav>',1)[0]
 assert f'href="#{prev}"' in nav,(key,nav)
 if n<9:assert f'href="#ch3-4-{n+1}"' in nav,(key,nav)
 body=sec.split('<div class="chapter-body">',1)[1].split('<nav class="chapter-endnav"',1)[0]
 w=Count();w.feed(DEPTH.sub('',body));a,b=w.n
 assert 650<=a<=850 and 850<=b<=1150 and 1500<=a+b<=2000,(key,a,b)
 cues=[c for c in manifest if c['chapter']==key]; blocks=list(DEPTH.finditer(body))
 assert len(cues)==len(blocks)>0
 for c in cues:
  assert c['source']['author']==author[n]
  assert all(c.get(k) for k in ('simple','why_here','remember','sourceDepthId'))
  lo,hi=ranges[n]; assert c['source']['printedPages'] and all(lo<=p<=hi for p in c['source']['printedPages'])
  target=next(x for x in blocks if f'id="{c["sourceDepthId"]}"' in x[0])
  assert ' open' not in target[0].split('>',1)[0]
  previous=re.search(r'<p(?:\s[^>]*)?>((?:(?!</p>)[\s\S])*)</p>\s*$',body[:target.start()])
  assert previous and c['text'] in plain(previous[1]), (key,c['id'])
 print(f'PASS {key}: {a} prose + {b} aids = {a+b}; {len(cues)} exact linked Companions')
assert 'href="#ch3-4-1"' not in main and 'id="ch3-4-1"' not in src
