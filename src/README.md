# Hikam — source code and editorial workspace

`src/main.html` and `src/chapters/subtopic-*.html` are the canonical book source. Build the website with `python src/build.py` **from the repository root**. No build framework or package installation is required.

**Arabic 2.1.7:** The current source-aligned edition uses the [16-page Arabic source and language-fidelity register](docs/editorial/READING_2_1_7_ARABIC_SOURCE_COVERAGE.md); its original full HTML section was [archived before replacement](archive/pre-redevelopment-2026-11-21/README.md). The three teaching syntheses, original DOCX and personal Arabic voice samples remain outside GitHub. Verify with `python src/tests/verify_arabic_politics_source_fidelity.py` in addition to all established checks.

**Arabic 2.1.8:** The source-complete Plato chapter uses the [12-page Arabic source-to-dossier register](docs/editorial/READING_2_1_8_ARABIC_PLATO_SOURCE_COVERAGE.md) and the [pinned full historical section](archive/pre-redevelopment-2026-11-21/README.md). The original DOCX, three Arabic syntheses and personal language samples stay outside the repository. Run `python src/tests/verify_arabic_plato_source_fidelity.py` along with the established Arabic/print/reader tests.

**Arabic 2.2.1:** The complete original [16-page Arabic source](docs/editorial/READING_2_2_1_ARABIC_METAPHYSICS_SOURCE_COVERAGE.md) governs the reworked metaphysics chapter; [its prior full 2.2.1 edition is immutable](archive/pre-redevelopment-2026-11-21/README.md). Source DOCX, three syntheses, language profile and personal writing samples are private editorial references, not published. Run `python src/tests/verify_arabic_metaphysics_source_fidelity.py` alongside all existing reader/RTL/PDF/offline checks.

**Arabic 2.2.2:** The original eight-page Arabic reading controls the revised traditional-division dossier. The [full original source-to-section coverage record](docs/editorial/READING_2_2_2_ARABIC_METAPHYSICS_DIVISION_SOURCE_COVERAGE.md) preserves the source's distinct introductory and exposition orderings and all author-attributed positions. The [complete former dossier](archive/pre-redevelopment-2026-11-21/README.md) is stored with a protected Git hash. Source DOCX, Arabic syntheses, writing samples and profile remain private. Verify via `python src/tests/verify_arabic_metaphysics_division_source_fidelity.py` and all existing reader, print and offline gates.

## Subsequent dossier snapshots

Dossier 2.1.6 was archived in full before its first replacement on 21 November 2026: [pre-redevelopment snapshot](archive/pre-redevelopment-2026-11-21/README.md). It is separately pinned and never a build input. The fixed original ten-dossier baseline below remains unchanged.

## Preserved pre-revamp originals

The [dated original-dossier archive](archive/pre-revamp-2026-11-05/README.md) holds the **full unmodified HTML chapter sections** for 1.1.1–1.1.5 and 2.1.1–2.1.5 from the 5 November 2026 baseline, including every original study aid and revision block. These are **not build inputs**. Do not edit or incorporate them into the live reader. Verify the pinned content with `python src/tests/verify_dossier_archive.py`; follow the standing editorial protocol to preserve future pre-edit snapshots.

## Authoring sequence

1. Edit or add a `src/chapters/subtopic-*.html` fragment.
2. Update `src/main.html`: TOC links/placeholders, sub-topic divider, Topic divider, cover description, and chapter count. Keep the user-established 3.2.5 vs. 3.3 distinction.
3. Extend `src/philosophy_notes.css` only as needed for new print page templates; never break the existing six semantic box colors, RTL conventions, or print isolation.
4. Update the relevant living documentation in `src/docs/design` or `src/docs/pagination` when architecture changes.
5. Run `python src/build.py`, then all checks in root README. Commit the newly generated `index.html` and `service-worker.js` together with their source.

`src/philosophy_study_notes.html` is a generated non-inlined HTML export kept next to its CSS and JavaScript; `index.html` is the public, offline self-contained reader. Do not hand-edit either generated file.

The `src/source_materials/` extracts remain publicly visible to anyone browsing this public repository; the directory move is organizational only, not access control.

## Contents and printing

The accessible Topic → Sub-topic → Chapter → Section sidebar supports live search, explicit branch control, a chapter-only ordered print selector, and optional revision pages. See [SIDEBAR_GUIDE.md](docs/hosting/SIDEBAR_GUIDE.md). Validate with `python src/tests/verify_sidebar.py`.

## Screen-only reading location

The sticky progress rail, circular chapter gauge, sidebar's active § link,
and optional locally saved Resume Reading prompt are implemented in
`src/main.html`, `src/philosophy_notes.css`, and the **same existing**
`wireScrollSpy()` in `src/philosophy_notes.js`. See
[`docs/hosting/READING_POSITION.md`](docs/hosting/READING_POSITION.md).
Do not add a second scroll tracker or save print-transformed positions.

## On-screen revision visibility

The Tools tab has **Show chapter Revision Blocks** (default: on). Turning it off
hides every chapter's complete `.end-block` from the screen, with preference
stored under `11am-hikam-show-revisions-v1` in device `localStorage`.
The main book and every revision block remain in the HTML. The print dialog
has an **independent** Include chapter revision pages option; hiding a block
on screen never excludes it from a PDF unless that print option is unchecked.
Search still indexes the entire book and reveals Revision Blocks when a
reader deliberately selects a result inside a hidden block.
