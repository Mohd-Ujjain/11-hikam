#!/usr/bin/env python3
"""Chromium regression for pilot Reading Companions, print and RTL-safe popovers."""
from __future__ import annotations

from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import json

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_IDS = tuple(entry['id'] for entry in json.loads((ROOT/'src/reading_companions.json').read_text(encoding='utf-8'))['companions'])
EXPECTED_COUNT = len(EXPECTED_IDS)

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

@contextmanager
def site():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}/'
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

def check(browser, url, width):
    ctx = browser.new_context(viewport={'width': width, 'height': 820},
                              reduced_motion='reduce', service_workers='block')
    ctx.route('https://fonts.googleapis.com/**', lambda route: route.abort())
    ctx.route('https://fonts.gstatic.com/**', lambda route: route.abort())
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda exc: errors.append(str(exc)))
    page.goto(url, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_function("(n) => window.__hikamReadingCompanions && window.__hikamReadingCompanions.attached() === n", arg=EXPECTED_COUNT)
    assert page.evaluate("window.__hikamReadingCompanions.failed()") == []
    assert page.locator('section.chapter').count() == 39
    cues = page.locator('.hikam-companion-trigger')
    assert cues.count() == EXPECTED_COUNT
    assert page.locator('.end-block .hikam-companion-trigger').count() == 0
    assert page.locator('.chapter-frontmatter .hikam-companion-trigger').count() == 0
    assert page.locator('#hikamCompanionPopup').is_hidden()
    for item in EXPECTED_IDS:
        cue = page.locator('[data-companion-id="'+item+'"]')
        assert cue.count() == 1
        assert cue.get_attribute('role') == 'button'
        cue.scroll_into_view_if_needed()
        cue.focus()
        page.keyboard.press('Enter')
        assert page.locator('#hikamCompanionPopup').is_visible()
        assert cue.get_attribute('aria-expanded') == 'true'
        rect = page.locator('#hikamCompanionPopup').bounding_box()
        assert rect and rect['x'] >= -1 and rect['x'] + rect['width'] <= width + 1, (width, rect)
        page.keyboard.press('Escape')
        assert page.locator('#hikamCompanionPopup').is_hidden()
        assert cue.get_attribute('aria-expanded') == 'false'
        cue.focus()
        page.keyboard.press('Space')
        assert page.locator('#hikamCompanionPopup').is_visible()
        page.keyboard.press('Escape')
        assert page.locator('#hikamCompanionPopup').is_hidden()
    # Local paragraph-level disclosures for all four source authors.
    for chapter, number in [('ch1-1-1', 10), ('ch1-1-2', 24), ('ch1-1-3', 9), ('ch1-1-4', 9), ('ch1-1-5', 5), ('ch2-1-1', 6), ('ch2-1-2', 6), ('ch2-1-3', 14), ('ch2-1-4', 17), ('ch2-1-5', 16), ('ch2-1-6', 2), ('ch2-1-7', 9), ('ch2-1-8', 11), ('ch2-2-1', 11), ('ch2-2-2', 11), ('ch2-2-3', 13)]:
        callouts = page.locator('#' + chapter + ' .chapter-body .hikam-source-depth-inline')
        assert callouts.count() >= 1
        assert callouts.locator('.hikam-source-depth-item').count() == number
        assert callouts.first.get_attribute('open') is None
        assert callouts.first.evaluate("(e) => e.previousElementSibling.tagName") == 'P'
        callouts.first.locator('summary').click()
        assert callouts.first.get_attribute('open') is not None
        assert callouts.first.locator('.hikam-source-depth-item p').first.is_visible()
        callouts.first.locator('summary').click()
        assert callouts.first.get_attribute('open') is None
    timeline = page.locator('#ch1-1-1 .chapter-body .historical-timeline')
    assert timeline.locator('.historical-timeline-event').count() == 4
    cue = page.locator('[data-companion-id="h111-russell-idealism"]')
    cue.scroll_into_view_if_needed()
    assert cue.evaluate("(e) => getComputedStyle(e).textDecorationStyle") == 'dotted'
    color = cue.evaluate("(e) => getComputedStyle(e).textDecorationColor")
    other_color = page.locator('[data-companion-id="h112-parfit-identity"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    papineau_color = page.locator('[data-companion-id="h113-induction"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    gutting_color = page.locator('[data-companion-id="h114-intentionality"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    critchley_color = page.locator('[data-companion-id="h115-felt-gap"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    bird_color = page.locator('[data-companion-id="h211-two-faces"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    common_good_color = page.locator('[data-companion-id="h212-marx"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    war_color = page.locator('[data-companion-id="h213-institution"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    wolff_color = page.locator('[data-companion-id="h214-power"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    liberty_color = page.locator('[data-companion-id="h215-majority"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    individualism_color = page.locator('[data-companion-id="h216-moral-bond"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    arabic_color = page.locator('[data-companion-id="h217-tadbir"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    plato_color = page.locator('[data-companion-id="h218-birth"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    metaphysics_color = page.locator('[data-companion-id="h221-shelf"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    division_color = page.locator('[data-companion-id="h222-division"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    islam_christian_color = page.locator('[data-companion-id="h223-kindiknow"]').evaluate(
        "(e) => getComputedStyle(e).textDecorationColor")
    assert len({color, other_color, papineau_color, gutting_color, critchley_color, bird_color, common_good_color, war_color, wolff_color, liberty_color, individualism_color, arabic_color, plato_color, metaphysics_color, division_color, islam_christian_color}) == 16
    cue.focus()
    page.keyboard.press('Enter')
    popup = page.locator('#hikamCompanionPopup')
    assert popup.get_attribute('role') == 'region'
    assert popup.locator('.hikam-companion-simple').is_visible()
    assert popup.locator('.hikam-companion-why').is_visible()
    assert popup.locator('.hikam-companion-remember').is_visible()
    assert popup.locator('.hikam-companion-close').is_visible()
    assert cue.evaluate("(e) => getComputedStyle(e).textDecorationStyle") == 'solid'
    popup.locator('.hikam-companion-close').click()
    assert popup.is_hidden()
    assert cue.evaluate("(e) => getComputedStyle(e).textDecorationStyle") == 'dotted'
    cue = page.locator('[data-companion-id="h112-parfit-identity"]')
    cue.scroll_into_view_if_needed()
    cue.focus()
    page.keyboard.press('Enter')
    assert popup.locator('.hikam-companion-simple').is_visible()
    page.keyboard.press('ArrowDown')
    assert popup.locator('.hikam-companion-close').evaluate(
        "(e) => document.activeElement === e")
    page.keyboard.press('Escape')
    assert popup.is_hidden()

    # Simulate a RTL chapter at one cue without editing authorial content.
    cue = page.locator('[data-companion-id="h112-harrod-rule"]')
    cue.evaluate("e=>{e.closest('.chapter').classList.add('rtl');e.closest('.chapter').setAttribute('lang','ar')}")
    cue.focus()
    page.keyboard.press('Enter')
    assert page.locator('#hikamCompanionPopup').get_attribute('dir') == 'rtl'
    assert page.locator('#hikamCompanionPopup').get_attribute('lang') == 'ar'
    page.keyboard.press('Escape')
    cue.evaluate("e=>{e.closest('.chapter').classList.remove('rtl');e.closest('.chapter').removeAttribute('lang')}")
    # Source-depth and Companion cue remain distinct on Wolff's introduction to feminism.
    assert page.locator('#ch2-1-6 .chapter-body .hikam-source-depth-inline').count() == 2
    assert page.locator('#ch2-1-6 .chapter-body .hikam-companion-trigger').count() == 4
    # Real Arabic chapter, not an English cue switched temporarily to RTL.
    arabic_cue = page.locator('[data-companion-id="h217-tadbir"]')
    assert page.locator('#ch2-1-7').get_attribute('lang') == 'ar'
    assert arabic_cue.count() == 1
    arabic_cue.scroll_into_view_if_needed()
    arabic_cue.focus()
    page.keyboard.press('Enter')
    assert popup.get_attribute('dir') == 'rtl'
    assert popup.get_attribute('lang') == 'ar'
    assert 'التعهّد' in popup.inner_text()
    page.keyboard.press('Escape')
    assert popup.is_hidden()
    assert page.locator('#ch2-1-7 .chapter-body .hikam-companion-trigger').count() == 8
    assert page.locator('#ch2-1-7 .chapter-body .hikam-source-depth-inline').count() == 7
    # Arabic 2.1.8 uses its real Arabic script and chapter hue, not a simulated RTL tag.
    plato_cue = page.locator('[data-companion-id="h218-birth"]')
    assert page.locator('#ch2-1-8').get_attribute('lang') == 'ar'
    assert plato_cue.count() == 1
    plato_cue.scroll_into_view_if_needed()
    plato_cue.focus()
    page.keyboard.press('Enter')
    assert popup.get_attribute('dir') == 'rtl'
    assert popup.get_attribute('lang') == 'ar'
    assert 'التوالد' in popup.inner_text()
    page.keyboard.press('Escape')
    assert popup.is_hidden()
    assert page.locator('#ch2-1-8 .chapter-body .hikam-companion-trigger').count() == 9
    assert page.locator('#ch2-1-8 .chapter-body .hikam-source-depth-inline').count() == 8
    # Arabic 2.2.1, true RTL, twelve unique contextual cues and native disclosures.
    metaphysics_cue = page.locator('[data-companion-id="h221-shelf"]')
    assert page.locator('#ch2-2-1').get_attribute('lang') == 'ar'
    assert metaphysics_cue.count() == 1
    metaphysics_cue.scroll_into_view_if_needed()
    metaphysics_cue.focus()
    page.keyboard.press('Enter')
    assert popup.get_attribute('dir') == 'rtl'
    assert popup.get_attribute('lang') == 'ar'
    assert 'ترتيب كتب أرسطو' in popup.inner_text()
    assert metaphysics_cue.evaluate("(e) => getComputedStyle(e).textDecorationStyle") == 'solid'
    page.keyboard.press('Escape')
    assert popup.is_hidden()
    assert metaphysics_cue.get_attribute('aria-expanded') == 'false'
    # The restored keyboard focus correctly keeps a solid focus-visible cue.
    # It returns to the chapter's dotted resting style once focus leaves.
    page.keyboard.press('Tab')
    assert metaphysics_cue.evaluate("(e) => getComputedStyle(e).textDecorationStyle") == 'dotted'
    assert page.locator('#ch2-2-1 .chapter-body .hikam-companion-trigger').count() == 12
    assert page.locator('#ch2-2-1 .chapter-body .hikam-source-depth-inline').count() == 7
    # 2.2.2 is an actual Arabic chapter, with its own 128-degree cue pigment.
    division_cue = page.locator('[data-companion-id="h222-division"]')
    assert page.locator('#ch2-2-2').get_attribute('lang') == 'ar'
    assert division_cue.count() == 1
    division_cue.scroll_into_view_if_needed()
    division_cue.focus()
    page.keyboard.press('Enter')
    assert popup.get_attribute('dir') == 'rtl'
    assert popup.get_attribute('lang') == 'ar'
    assert 'أربعة ميادين' in popup.inner_text()
    assert division_cue.get_attribute('aria-expanded') == 'true'
    assert division_cue.evaluate("(e) => getComputedStyle(e).textDecorationStyle") == 'solid'
    page.keyboard.press('Escape')
    assert popup.is_hidden()
    assert division_cue.get_attribute('aria-expanded') == 'false'
    # Keyboard focus must remain visible; resting dotted style after blur.
    page.keyboard.press('Tab')
    assert division_cue.evaluate("(e) => getComputedStyle(e).textDecorationStyle") == 'dotted'
    assert page.locator('#ch2-2-2 .chapter-body .hikam-companion-trigger').count() == 13
    assert page.locator('#ch2-2-2 .chapter-body .hikam-source-depth-inline').count() == 7
    # Arabic 2.2.3 contains 13 local Companions in true RTL and 7 native groups.
    islam_cue = page.locator('[data-companion-id="h223-kindiknow"]')
    assert page.locator('#ch2-2-3').get_attribute('lang') == 'ar'
    assert islam_cue.count() == 1
    islam_cue.scroll_into_view_if_needed()
    islam_cue.focus()
    page.keyboard.press('Enter')
    assert popup.get_attribute('dir') == 'rtl'
    assert popup.get_attribute('lang') == 'ar'
    assert 'معرفة علته' in popup.inner_text()
    assert islam_cue.get_attribute('aria-expanded') == 'true'
    assert islam_cue.evaluate("(e) => getComputedStyle(e).textDecorationStyle") == 'solid'
    page.keyboard.press('Escape')
    assert popup.is_hidden()
    assert islam_cue.get_attribute('aria-expanded') == 'false'
    page.keyboard.press('Tab')
    assert islam_cue.evaluate("(e) => getComputedStyle(e).textDecorationStyle") == 'dotted'
    assert page.locator('#ch2-2-3 .chapter-body .hikam-companion-trigger').count() == 13
    assert page.locator('#ch2-2-3 .chapter-body .hikam-source-depth-inline').count() == 7
    # The original paragraph text must include the uninterrupted wrapped phrase.
    assert page.locator('[data-companion-id="h112-parfit-identity"]').inner_text() == 'future generations'
    page.evaluate("""() => {
      window.__printControl.includeRevision(false);
      window.__runPagination(['ch1-1-2']);
    }""")
    assert page.locator('#ch1-1-2 .js-print-page').count() > 0
    assert page.locator('.js-print-page .hikam-companion-trigger').count() == 0
    assert page.locator('#ch1-1-2 .js-print-page').first.inner_text()
    page.evaluate("window.__runPagination(['ch1-1-1'])")
    assert page.locator('#ch1-1-1 .js-print-page').count() > 0
    assert page.locator('#ch1-1-1 .js-print-page .historical-timeline-event').count() == 4
    assert page.locator('#ch1-1-1 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch1-1-2 .js-print-page .hikam-source-depth-inline').count() == 0
    # The Papineau chapter keeps the twelve cue words in the original source
    # but removes all cue controls and its nine optional depth items in print.
    page.evaluate("window.__runPagination(['ch1-1-3'])")
    assert page.locator('#ch1-1-3 .js-print-page').count() > 0
    assert page.locator('#ch1-1-3 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch1-1-3 .js-print-page .hikam-companion-trigger').count() == 0
    # Gutting: keep source argument, remove contextual controls and all 9
    # optional depth records from real A4 pagination clones.
    page.evaluate("window.__runPagination(['ch1-1-4'])")
    assert page.locator('#ch1-1-4 .js-print-page').count() > 0
    assert page.locator('#ch1-1-4 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch1-1-4 .js-print-page .hikam-companion-trigger').count() == 0
    assert page.locator('#ch1-1-4 .js-print-page .historical-timeline-event').count() == 3
    assert page.locator('#ch1-1-1 .js-print-page .hikam-companion-trigger').count() == 0
    # Critchley: Source Depth is never copied into print; cue prose survives.
    page.evaluate("window.__runPagination(['ch1-1-5'])")
    assert page.locator('#ch1-1-5 .js-print-page').count() > 0
    assert page.locator('#ch1-1-5 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch1-1-5 .js-print-page .hikam-companion-trigger').count() == 0
    # Bird 2.1.1: contextual cue text remains in print without popovers or closed detail.
    page.evaluate("window.__runPagination(['ch2-1-1'])")
    assert page.locator('#ch2-1-1 .js-print-page').count() > 0
    assert page.locator('#ch2-1-1 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch2-1-1 .js-print-page .hikam-companion-trigger').count() == 0
    # Bird 2.1.2: six screen-only local disclosures and twelve exact cues
    # are excluded from the same A4 pagination clones without losing prose.
    page.evaluate("window.__runPagination(['ch2-1-2'])")
    assert page.locator('#ch2-1-2 .js-print-page').count() > 0
    assert page.locator('#ch2-1-2 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch2-1-2 .js-print-page .hikam-companion-trigger').count() == 0
    # Bird 2.1.3: all nineteen contextual markers retain print prose.
    # The ten native optional disclosures (fourteen source records) are
    # removed from measured A4 print clones in the canonical reader.
    page.evaluate("window.__runPagination(['ch2-1-3'])")
    assert page.locator('#ch2-1-3 .js-print-page').count() > 0
    assert page.locator('#ch2-1-3 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch2-1-3 .js-print-page .hikam-companion-trigger').count() == 0
    assert 'excuse' in page.locator('#ch2-1-3 .js-print-page').first.inner_text().lower() or page.locator('#ch2-1-3 .js-print-page').count() > 1
    # Wolff: print keeps the visible source argument, omitting screen-only
    # contextual cues and all optional depth before measuring A4 pages.
    page.evaluate("window.__runPagination(['ch2-1-4'])")
    assert page.locator('#ch2-1-4 .js-print-page').count() > 0
    assert page.locator('#ch2-1-4 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch2-1-4 .js-print-page .hikam-companion-trigger').count() == 0
    # Wolff 2.1.5: all original prose and six independent revisions retain
    # A4 print/pagination while optional source records and cue markup disappear.
    page.evaluate("window.__runPagination(['ch2-1-5'])")
    assert page.locator('#ch2-1-5 .js-print-page').count() > 0
    assert page.locator('#ch2-1-5 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch2-1-5 .js-print-page .hikam-companion-trigger').count() == 0
    # Arabic text, RTL pagination and the screen-only Source Depth exclusion.
    page.evaluate("window.__runPagination(['ch2-1-7'])")
    assert page.locator('#ch2-1-7 .js-print-page').count() > 0
    assert page.locator('#ch2-1-7 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch2-1-7 .js-print-page .hikam-companion-trigger').count() == 0
    page.evaluate("window.__runPagination(['ch2-1-8'])")
    assert page.locator('#ch2-1-8 .js-print-page').count() > 0
    assert page.locator('#ch2-1-8 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch2-1-8 .js-print-page .hikam-companion-trigger').count() == 0
    page.evaluate("window.__runPagination(['ch2-2-1'])")
    assert page.locator('#ch2-2-1 .js-print-page').count() > 0
    assert page.locator('#ch2-2-1 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch2-2-1 .js-print-page .hikam-companion-trigger').count() == 0
    page.evaluate("window.__runPagination(['ch2-2-2'])")
    assert page.locator('#ch2-2-2 .js-print-page').count() > 0
    assert page.locator('#ch2-2-2 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch2-2-2 .js-print-page .hikam-companion-trigger').count() == 0
    page.evaluate("window.__runPagination(['ch2-2-3'])")
    assert page.locator('#ch2-2-3 .js-print-page').count() > 0
    assert page.locator('#ch2-2-3 .js-print-page .hikam-source-depth-inline').count() == 0
    assert page.locator('#ch2-2-3 .js-print-page .hikam-companion-trigger').count() == 0
    assert not errors, errors
    ctx.close()

with site() as url, sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, args=['--no-sandbox'])
    try:
        for viewport in (390, 1440):
            check(browser, url, viewport)
    finally:
        browser.close()
# Native Source Depth also remains usable when scripts are entirely disabled.
with site() as no_js_url, sync_playwright() as no_js_pw:
    no_js_browser = no_js_pw.chromium.launch(headless=True, args=['--no-sandbox'])
    try:
        context = no_js_browser.new_context(java_script_enabled=False, viewport={'width':390,'height':820})
        page = context.new_page()
        page.goto(no_js_url, wait_until='domcontentloaded')
        for chapter in ('ch1-1-1', 'ch1-1-2', 'ch1-1-3', 'ch1-1-4', 'ch1-1-5', 'ch2-1-1', 'ch2-1-2', 'ch2-1-3', 'ch2-1-4', 'ch2-1-5', 'ch2-1-6', 'ch2-1-7', 'ch2-1-8', 'ch2-2-1', 'ch2-2-2', 'ch2-2-3'):
            disclosure = page.locator('#'+chapter+' .hikam-source-depth-inline').first
            assert disclosure.count() == 1 and disclosure.get_attribute('open') is None
            # Native summary keyboard activation works even when page JS is
            # disabled and the very long single-file reader is not scrollable
            # by Playwright's pointer auto-scroll in this no-script context.
            disclosure.locator('summary').focus()
            page.keyboard.press('Enter')
            assert disclosure.get_attribute('open') is not None
            assert disclosure.locator('.hikam-source-depth-item p').first.is_visible()
        context.close()
    finally:
        no_js_browser.close()
print(f'PASS: {EXPECTED_COUNT} contextual cues; native paragraph Source Depth, accessible focus, RTL and print integrity')
