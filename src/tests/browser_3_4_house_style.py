#!/usr/bin/env python3
"""Real Chromium audit of 3.4.5–3.4.9 screen, dark revisions and A4 pagination."""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
from pypdf import PdfReader
from playwright.sync_api import sync_playwright

from browser_quality import context, launch, load, no_errors, site

ROOT = Path(__file__).resolve().parents[2]
IDS = [f"ch3-4-{n}" for n in range(5, 10)]


def screen_check(browser, url: str) -> None:
    for width in [390, 1366]:
        ctx = context(browser, width)
        page = load(ctx, url)
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), ("horizontal overflow", width)
        for ident in IDS:
            ch = page.locator(f"#{ident}")
            for selector in (
                "> .chapter-frontmatter", "> .chapter-body",
                "> .chapter-endnav", "> .end-block",
                "> .end-block .revision-sheet",
                "> .end-block .memlist", "> .end-block .examq",
            ):
                assert ch.locator(f":scope {selector}").count() == 1, (ident, selector)
            assert ch.locator("> .chapter-body .tbl-wrap").count() >= 2, ident
            assert ch.locator("> .chapter-body .analogy").count() >= 2, ident
            assert ch.locator("> .chapter-body .checkpoint").count() >= 1, ident
            assert ch.locator("> .end-block .examq-cat").count() == 5, ident
            assert ch.locator("> .end-block .rev-item").count() >= 10, ident
            assert ch.locator("> .end-block .keydef-item").count() >= 12, ident
            assert ch.locator("> .end-block").evaluate("(e) => getComputedStyle(e).backgroundImage !== 'none'"), ident
            assert not ch.evaluate("(e) => e.classList.contains('rtl')"), ident
        no_errors(page, f"3.4 dossiers screen {width}px")
        ctx.close()
    print("PASS 5 dossier screen layouts, dark revision surfaces and 390/1366px overflow", flush=True)


def print_check(browser, url: str) -> None:
    ctx = context(browser, 1024)
    page = load(ctx, url)
    original = page.evaluate("Array.from(document.querySelectorAll('section.chapter')).map(x => x.id)")
    page.evaluate("(ids) => { window.__printControl.setFilter(ids); window.__printControl.includeRevision(true); window.dispatchEvent(new Event('beforeprint')); }", IDS)
    page.emulate_media(media="print")
    pages = page.evaluate("""(ids) => {
        let out = {};
        for (let id of ids) {
            const chapter = document.getElementById(id);
            const nodes = [...chapter.querySelectorAll(':scope > .js-print-page')];
            const light = nodes.filter(n=>n.classList.contains('js-light'));
            const dark = nodes.filter(n=>n.classList.contains('js-dark'));
            const gaps = [];
            const widths = [];
            for (const p of nodes) {
                const c = p.querySelector('.js-page-content');
                const foot = p.querySelector('.js-page-footer');
                const last = c?.lastElementChild;
                if (last && foot) gaps.push(foot.getBoundingClientRect().top - last.getBoundingClientRect().bottom);
                widths.push((c?.scrollWidth ?? 0) - (c?.clientWidth ?? 0));
            }
            out[id] = {
                count:nodes.length,
                light:light.length,
                dark:dark.length,
                minGap:Math.min(...gaps),
                maxWidthOverflow:Math.max(...widths),
                headerPresent:nodes.every(p=>p.querySelector('.js-page-header') && p.querySelector('.js-page-footer')),
                tabId: chapter.querySelector('.chapter-tabnum')?.textContent.trim()
            };
        }
        return out;
    }""", IDS)
    print(f'PRINT GEOMETRY SAMPLE: {pages}', flush=True)
    for ident, info in pages.items():
        assert info["light"] >= 2, (ident, info)
        assert info["dark"] >= 2, (ident, "revision section not paginated")
        assert info["headerPresent"], ident
        assert info["minGap"] >= 4, (ident, "content overlaps print footer", info)
        assert info["maxWidthOverflow"] <= 5, (ident, "printed content exceeds available width", info)
        assert ident.replace("ch", "").replace("-", ".") in info["tabId"], (ident, info)
    print(f"PASS JS pagination across all five dossiers: {pages}", flush=True)
    # Verify one representative long chapter as an actual PDF, not merely DOM pages.
    page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    page.evaluate("(ids) => { window.__printControl.setFilter(ids); window.__printControl.includeRevision(true); window.dispatchEvent(new Event('beforeprint')); }", [IDS[-1]])
    expected_pages = page.locator(f"#{IDS[-1]} > .js-print-page").count()
    assert expected_pages >= 12, ("missing generated revision pages", expected_pages)
    pdf = page.pdf(print_background=True, prefer_css_page_size=True)
    assert pdf.startswith(b"%PDF")
    reader = PdfReader(BytesIO(pdf))
    pdf_text = "\\n".join(p.extract_text() or "" for p in reader.pages)
    print(f'PDF AUDIT: expected_generated={expected_pages}, actual_pdf={len(reader.pages)}, '
          f'post_pdf_generated={page.locator(f"#{IDS[-1]} > .js-print-page").count()}, '
          f'has_revision={"Revision Block" in pdf_text}, '
          f'has_examination={"Possible Examination Questions" in pdf_text}', flush=True)
    assert len(reader.pages) >= expected_pages, ("PDF dropped generated pages", expected_pages, len(reader.pages))
    assert "Possible Examination Questions" in pdf_text, "The dark revision material did not print"
    page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    assert page.locator(".js-print-page").count() == 0
    assert page.evaluate("Array.from(document.querySelectorAll('section.chapter')).map(x => x.id)") == original
    no_errors(page, "3.4 print")
    ctx.close()
    print(f"PASS representative 3.4.9 A4 PDF ({len(reader.pages)} pages), non-destructive print restore", flush=True)


def main() -> None:
    with site() as url, sync_playwright() as playwright:
        browser = launch(playwright)
        try:
            screen_check(browser, url)
            print_check(browser, url)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
