#!/usr/bin/env python3
"""Real Chromium audit: Amiri 3.2.1 RTL comparisons, mobile layout, A4 print."""
from __future__ import annotations
from io import BytesIO

from pypdf import PdfReader
from playwright.sync_api import sync_playwright
from browser_quality import ARTIFACTS, context, launch, load, no_errors, site

CHAPTER = 'ch3-2-1'

def screen(browser, url):
    for width in (390, 1366):
        ctx = context(browser, width)
        page = load(ctx, url)
        chap = page.locator('#' + CHAPTER)
        assert chap.count() == 1
        assert chap.get_attribute('lang') == 'ar'
        assert chap.evaluate('(e) => getComputedStyle(e).direction') == 'rtl'
        assert chap.get_attribute('style').find('--hue:328') != -1
        tables = chap.locator(':scope > .chapter-body .tbl-wrap')
        assert tables.count() == 2, (width, tables.count())
        for i in range(2):
            wrap = tables.nth(i)
            table = wrap.locator('table.comparison')
            assert table.locator('thead th[scope="col"]').count() == 3
            assert table.locator('tbody th[scope="row"]').count() == 3
            assert wrap.evaluate('(e) => getComputedStyle(e).overflowX') == 'auto'
            assert table.evaluate('(e) => getComputedStyle(e).direction') == 'rtl'
        for selector, count in (
            ('.hierarchy',4),('.box.tip',1),('.box.mistake',1),
            ('.box.memory',1),('.analogy',1),('.concept-rel',2),
        ):
            assert chap.locator(':scope > .chapter-body ' + selector).count() == count, (selector,width)
        assert chap.locator(':scope > .end-block .examq-cat').count() == 5
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+2'), (
            'horizontal page overflow',width)
        if width == 390:
            tables.last.scroll_into_view_if_needed()
            tables.last.screenshot(path=str(ARTIFACTS / 'amiri-321-fitra-comparison-mobile.png'))
        no_errors(page, f'Amiri 3.2.1 RTL {width}px')
        ctx.close()
    print('PASS Amiri 3.2.1 mobile & desktop RTL comparisons and semantic aids',flush=True)

def print_a4(browser,url):
    ctx = context(browser,1024)
    page = load(ctx,url)
    before = page.evaluate(
        "Array.from(document.querySelectorAll('section.chapter')).map(e => e.id)")
    page.evaluate("""() => {
       window.__printControl.setFilter(['ch3-2-1']);
       window.__printControl.includeRevision(true);
       window.dispatchEvent(new Event('beforeprint'));
    }""")
    page.emulate_media(media='print')
    printed = page.locator('#ch3-2-1 > .js-print-page')
    n = printed.count()
    assert n >= 4, n
    over = page.evaluate("""() =>
       [...document.querySelectorAll('#ch3-2-1 > .js-print-page .js-page-content')]
          .map(e => e.scrollWidth - e.clientWidth)""")
    assert len(over)==n and max(over)<=3, ('A4 horizontal overflow',over)
    assert page.locator('#ch3-2-1 .js-print-page .end-block').count() >= 1
    assert page.locator('#ch3-2-1 .js-print-page .hikam-source-depth-inline').count() == 0
    pdf=page.pdf(print_background=True,prefer_css_page_size=True)
    assert pdf.startswith(b'%PDF') and len(pdf)>10000
    pages=PdfReader(BytesIO(pdf)).pages
    assert len(pages)>=n,(len(pages),n)
    (ARTIFACTS/'amiri-321-rtl-a4.pdf').write_bytes(pdf)
    page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    assert page.locator('.js-print-page').count()==0
    assert page.evaluate("Array.from(document.querySelectorAll('section.chapter')).map(e => e.id)")==before
    no_errors(page,'Amiri 3.2.1 A4')
    ctx.close()
    print(f'PASS Amiri 3.2.1 real RTL A4 PDF, {len(pages)} pages, no overflow, clean restore',flush=True)

def main():
    with site() as url,sync_playwright() as playwright:
        browser=launch(playwright)
        try:
            screen(browser,url)
            print_a4(browser,url)
        finally:
            browser.close()

if __name__=='__main__':
    main()
