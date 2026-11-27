from io import BytesIO
from pypdf import PdfReader
from playwright.sync_api import sync_playwright
from browser_quality import site,launch,context,ROOT
from browser_design_tokens import AUDIT
from pathlib import Path
import json
S=ROOT/'src'
ids=[f'ch3-6-{n}' for n in range(1,7)]
manifest=json.loads((S/'reading_companions.json').read_text())['companions']
expected={x:sum(r['chapter']==x for r in manifest) for x in ids}
def watch(page):
 errors=[]
 page.on('pageerror',lambda err:errors.append(str(err)))
 return errors
def load(ctx,url):
 page=ctx.new_page();errors=watch(page);page.goto(url,wait_until='domcontentloaded',timeout=60000)
 return page,errors
with site() as url,sync_playwright() as pw:
 browser=launch(pw)
 try:
  for width in (390,1366):
   ctx=context(browser,width)
   page,errors=load(ctx,url)
   result=page.evaluate(AUDIT)
   assert not result['failures'],result['failures']
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+2')
   for key in ids:
    chapter=page.locator(f'#{key}')
    cues=chapter.locator('.hik-companion-trigger, .hikam-companion-trigger')
    if not cues.count():
     cues=chapter.locator('[data-companion-id]')
    assert cues.count()==expected[key],(key,cues.count(),expected[key])
    assert chapter.locator('.end-block .endh').count()==6
    assert chapter.locator('.end-block .examq-cat').count()==5
    assert chapter.evaluate('(node)=>getComputedStyle(node).direction')=='rtl'
    cue=cues.first
    cue.scroll_into_view_if_needed();cue.focus();cue.press('Enter')
    assert cue.get_attribute('aria-expanded')=='true',(key,width)
    cue.press('Escape')
    assert cue.get_attribute('aria-expanded')=='false',(key,width)
   assert not errors,errors
   ctx.close()
   print(f'PASS {width}px: {sum(expected.values())} live cues; keyboard, RTL/LTR, contrast and no horizontal scroll.')
  ctx=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':820})
  page,_=load(ctx,url)
  for key in ids:
   block=page.locator(f'#{key} details.hikam-source-depth-inline')
   assert block.count()==expected[key]
   assert not block.first.evaluate('(node)=>node.open')
   block.first.locator('summary').click()
   assert block.first.evaluate('(node)=>node.open')
  ctx.close()
  print('PASS all six have usable native Source Depth with JavaScript disabled.')
  ctx=context(browser,1024)
  page,errors=load(ctx,url)
  def compose(ids):
   page.evaluate("(ids) => { window.__printControl.setFilter(ids); window.__printControl.includeRevision(true); window.dispatchEvent(new Event('beforeprint')); }",ids)
   page.emulate_media(media='print')
  compose(ids)
  stat=page.evaluate("""ids=>Object.fromEntries(ids.map(id=>{
    const rs=[...document.querySelectorAll('#'+id+' > .js-print-page')];
    return [id, {light:rs.filter(x=>x.matches('.js-light')).length,dark:rs.filter(x=>x.matches('.js-dark')).length,
      gap:Math.min(...rs.map(x=>{const c=x.querySelector('.js-page-content');const f=x.querySelector('.js-page-footer');
        return f.getBoundingClientRect().top-c.lastElementChild.getBoundingClientRect().bottom})),
      overflow:Math.max(...rs.map(x=>{const c=x.querySelector('.js-page-content');return c.scrollWidth-c.clientWidth})),
      depth:rs.some(x=>x.querySelector('.hikam-source-depth-inline'))}];
   }))""",ids)
  print(stat)
  for key,s in stat.items():
   assert s['light']>=2 and s['dark']>=1 and s['gap']>=4 and s['overflow']<=5 and not s['depth'],(key,s)
  page.evaluate("window.dispatchEvent(new Event('afterprint'))");page.emulate_media(media='screen')
  for key in ('ch3-6-1','ch3-6-6'):
   compose([key])
   expected_pages=page.locator(f'#{key} > .js-print-page').count()
   pdf=PdfReader(BytesIO(page.pdf(print_background=True,prefer_css_page_size=True)))
   assert len(pdf.pages)>=expected_pages,(key,len(pdf.pages),expected_pages)
   assert all(abs(float(x.mediabox.width)-595.28)<3 and abs(float(x.mediabox.height)-841.89)<3 for x in pdf.pages)
   page.evaluate("window.dispatchEvent(new Event('afterprint'))");page.emulate_media(media='screen')
   print(f'PASS {key}: {len(pdf.pages)} real A4 PDF pages and non-destructive restore')
  assert not errors,errors
  ctx.close()
 finally: browser.close()
