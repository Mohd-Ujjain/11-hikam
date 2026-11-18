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
    page.wait_for_function("(n) => window.__hikamReadingCompanions && window.__hikamReadingCompanions.attached() === n", EXPECTED_COUNT)
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
    # Simulate a RTL chapter at one cue without editing authorial content.
    cue = page.locator('[data-companion-id="h112-harrod-rule"]')
    cue.evaluate("e=>{e.closest('.chapter').classList.add('rtl');e.closest('.chapter').setAttribute('lang','ar')}")
    cue.focus()
    page.keyboard.press('Enter')
    assert page.locator('#hikamCompanionPopup').get_attribute('dir') == 'rtl'
    assert page.locator('#hikamCompanionPopup').get_attribute('lang') == 'ar'
    page.keyboard.press('Escape')
    cue.evaluate("e=>{e.closest('.chapter').classList.remove('rtl');e.closest('.chapter').removeAttribute('lang')}")
    # The original paragraph text must include the uninterrupted wrapped phrase.
    assert page.locator('[data-companion-id="h112-parfit-identity"]').inner_text() == 'future generations'
    page.evaluate("""() => {
      window.__printControl.includeRevision(false);
      window.__runPagination(['ch1-1-2']);
    }""")
    assert page.locator('#ch1-1-2 .js-print-page').count() > 0
    assert page.locator('.js-print-page .hikam-companion-trigger').count() == 0
    assert page.locator('#ch1-1-2 .js-print-page').first.inner_text()
    assert not errors, errors
    ctx.close()

with site() as url, sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, args=['--no-sandbox'])
    try:
        for viewport in (390, 1440):
            check(browser, url, viewport)
    finally:
        browser.close()
print(f'PASS: {EXPECTED_COUNT} exact source cues; mobile/desktop, keyboard, RTL, source text and print-clone integrity')
