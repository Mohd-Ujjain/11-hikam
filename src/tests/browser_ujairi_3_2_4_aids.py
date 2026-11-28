#!/usr/bin/env python3
"""Only 3.2.4: real Arabic reading, contextual access and complete A4 printing."""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
import json
import re
import unicodedata

from pypdf import PdfReader
from playwright.sync_api import sync_playwright
from browser_quality import ARTIFACTS, context, launch, load, no_errors, site

ID = 'ch3-2-4'
SRC = Path(__file__).resolve().parents[1]
CUES = [c for c in json.loads((SRC / 'reading_companions.json').read_text(encoding='utf-8'))['companions'] if c['chapter'] == ID]


def screen(browser, url):
    for width in (390, 1366):
        ctx = context(browser, width)
        page = load(ctx, url)
        chapter = page.locator('#'+ID)
        assert chapter.get_attribute('lang') == 'ar'
        assert chapter.get_attribute('style') == '--hue:28;'
        assert chapter.evaluate('(e)=>getComputedStyle(e).direction') == 'rtl'
        bad_fonts = chapter.evaluate(r'''(root) => [...root.querySelectorAll('*')]
          .filter(e=>[...e.childNodes].some(n=>n.nodeType===3 && /[\u0600-\u06ff]/.test(n.textContent)))
          .filter(e=>!/Amiri|Arabic/i.test(getComputedStyle(e).fontFamily))
          .map(e=>({tag:e.tagName,cls:e.className,font:getComputedStyle(e).fontFamily}))''')
        assert not bad_fonts, (width, bad_fonts)
        tables = chapter.locator(':scope > .chapter-body .tbl-wrap')
        assert tables.count() >= 2
        for i in range(tables.count()):
            wrap = tables.nth(i)
            table = wrap.locator('table.comparison')
            cols = table.locator('thead th[scope="col"]').count()
            assert 3 <= cols <= 4
            assert table.locator('tbody tr').count() == table.locator('tbody th[scope="row"]').count()
            assert wrap.evaluate('(e)=>getComputedStyle(e).overflowX') == 'auto'
            assert table.evaluate('(e)=>getComputedStyle(e).direction') == 'rtl'
            assert wrap.evaluate('(e)=>e.getBoundingClientRect().width <= e.closest(".chapter-body").getBoundingClientRect().width+2')
        details = chapter.locator(':scope > .chapter-body details.hikam-source-depth-inline')
        assert details.count() > 0
        assert all(details.nth(i).get_attribute('open') is None for i in range(details.count()))
        assert chapter.locator(':scope > .end-block .endh').count() == 6
        assert chapter.locator(':scope > .end-block .examq-cat').count() == 5
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+2'), width
        page.wait_for_function('(n)=>document.querySelectorAll("#ch3-2-4 .hikam-companion-trigger").length===n', arg=len(CUES))
        assert chapter.locator('.hikam-source-depth-inline .hikam-companion-trigger').count() == 0
        cue = chapter.locator('.hikam-companion-trigger').first
        cue.scroll_into_view_if_needed()
        cue.focus()
        page.keyboard.press('Enter')
        popup = page.locator('#hikamCompanionPopup')
        assert popup.is_visible() and popup.get_attribute('dir') == 'rtl'
        assert popup.get_attribute('lang') == 'ar' and popup.get_attribute('role') == 'region'
        assert cue.get_attribute('aria-expanded') == 'true'
        for selector in ('.hikam-companion-simple', '.hikam-companion-why', '.hikam-companion-remember'):
            assert popup.locator(selector).is_visible()
        rect = popup.bounding_box()
        assert rect and rect['x'] >= -1 and rect['x']+rect['width'] <= width+1, rect
        page.keyboard.press('Escape')
        assert popup.is_hidden() and cue.get_attribute('aria-expanded') == 'false'
        assert cue.evaluate('(e)=>document.activeElement===e')
        if width == 390:
            tables.first.scroll_into_view_if_needed()
            tables.first.screenshot(path=str(ARTIFACTS / 'ujairi-324-comparison-mobile-rtl.png'))
        else:
            chapter.locator('.hierarchy').first.screenshot(path=str(ARTIFACTS / 'ujairi-324-argument-desktop.png'))
        no_errors(page, f'3.2.4 RTL {width}px')
        ctx.close()
    print('PASS 3.2.4 mobile/desktop RTL, Arabic fonts, comparable tables and keyboard Companion access', flush=True)


def no_javascript(browser, url):
    ctx = browser.new_context(viewport={'width': 390, 'height': 844}, java_script_enabled=False, service_workers='block')
    ctx.route('https://fonts.googleapis.com/**', lambda route: route.abort())
    ctx.route('https://fonts.gstatic.com/**', lambda route: route.abort())
    page = ctx.new_page()
    page.goto(url, wait_until='domcontentloaded', timeout=60000)
    detail = page.locator('#'+ID+' > .chapter-body details.hikam-source-depth-inline').first
    assert detail.get_attribute('open') is None
    detail.locator('summary').click()
    assert detail.get_attribute('open') is not None
    assert detail.locator('.hikam-source-depth-item p').first.is_visible()
    detail.locator('summary').click()
    assert detail.get_attribute('open') is None
    assert page.locator('#'+ID+' > .end-block .endh').count() == 6
    ctx.close()
    print('PASS 3.2.4 native Source Depth remains accessible without JavaScript', flush=True)


def arabic_tokens(text):
    text = ''.join(c for c in unicodedata.normalize('NFKC', text) if not unicodedata.combining(c) and c != 'ـ')
    tokens = set(re.findall(r'[\u0621-\u064a]+', text))
    return tokens | {t[::-1] for t in tokens}


def print_a4(browser, url):
    ctx = context(browser, 1024)
    page = load(ctx, url)
    original_ids = page.evaluate('Array.from(document.querySelectorAll("section.chapter")).map(e=>e.id)')
    revision_headings = page.locator('#'+ID+' > .end-block .endh').all_text_contents()
    page.evaluate('''() => {
      window.__printControl.setFilter(['ch3-2-4']);
      window.__printControl.includeRevision(true);
      window.dispatchEvent(new Event('beforeprint'));
    }''')
    page.emulate_media(media='print')
    pdf = page.pdf(print_background=True, prefer_css_page_size=True)
    (ARTIFACTS / 'ujairi-324-creation-a4.pdf').write_bytes(pdf)
    pages = page.locator('#'+ID+' > .js-print-page')
    count = pages.count()
    assert count >= 3
    geometry = pages.evaluate_all('''nodes=>nodes.map(e=>{
      const content=e.querySelector('.js-page-content');
      const footer=e.querySelector('.js-page-footer').getBoundingClientRect();
      const bottom=Math.max(content.getBoundingClientRect().top,...[...content.children].map(c=>c.getBoundingClientRect().bottom));
      return {overflow:content.scrollWidth-content.clientWidth,clearance:footer.top-bottom,dark:e.classList.contains('js-dark')};
    })''')
    assert all(g['overflow'] <= 3 and g['clearance'] >= -1 for g in geometry), geometry
    assert any(g['dark'] for g in geometry) and any(not g['dark'] for g in geometry)
    assert pages.locator('.hikam-source-depth-inline, .hikam-companion-trigger').count() == 0
    assert pages.locator('.endh').count() == 6
    reader = PdfReader(BytesIO(pdf))
    assert len(reader.pages) == count+1, ('A4 must contain the frontmatter and every generated page', len(reader.pages), count)
    assert all(abs(float(p.mediabox.width)-595.28) < 2 and abs(float(p.mediabox.height)-841.89) < 2 for p in reader.pages)
    # Check dark revision material actually reached the PDF, including all six headings.
    revision_text = '\n'.join(reader.pages[i+1].extract_text() or '' for i,g in enumerate(geometry) if g['dark'])
    tokens = arabic_tokens(revision_text)
    for heading in revision_headings:
        assert all(t in tokens or t[::-1] in tokens for t in re.findall(r'[\u0621-\u064a]+', heading)), ('Missing PDF revision heading', heading)
    page.evaluate('window.dispatchEvent(new Event("afterprint"))')
    assert page.locator('.js-print-page').count() == 0
    assert page.evaluate('Array.from(document.querySelectorAll("section.chapter")).map(e=>e.id)') == original_ids
    no_errors(page, '3.2.4 A4 print and restoration')
    ctx.close()
    print(f'PASS 3.2.4 actual A4 PDF: {len(reader.pages)} pages, six revision headings, no overflow, optional depth omitted, original DOM restored', flush=True)


def main():
    with site() as url, sync_playwright() as playwright:
        browser = launch(playwright)
        try:
            screen(browser, url)
            no_javascript(browser, url)
            print_a4(browser, url)
        finally:
            browser.close()


if __name__ == '__main__':
    main()
