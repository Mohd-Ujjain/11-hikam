# Pre-revamp original dossiers — historical archive

**Baseline:** 5 November 2026, Git commit [`aa601b2441f81ab1469b37e64514b5c2f117b273`](https://github.com/MohdUjjain/11-hikam/commit/aa601b2441f81ab1469b37e64514b5c2f117b273).
**Status:** Read-only by editorial policy and pinned integrity checks. This is not part of the live reader.

## What has been preserved

These are the **ten original dossier chapter sections** for 1.1.1–1.1.5 and 2.1.1–2.1.5, before the November 18–20 editorial redevelopment. Each archive file is the **exact, unmodified substring** from its opening `<section class="chapter" ... id="chN-N-N">` through its closing `</section>` in the source module at the pinned commit.

Each fragment preserves its original frontmatter, original title/credits as printed at that time, all original chapter prose, study aids and the **full six-part revision system**, including the five examination-question categories. The surrounding subtopic divider, chapter delimiter comments outside the section and unrelated chapters are not included. The `.html` files are historical **fragments**, not complete standalone HTML pages.

Original PDFs and privately supplied study syntheses are **not** archived here. These earlier dossiers may contain omissions, incorrect author credits or interpretations subsequently corrected; their preservation does **not** make them an authoritative source over the original reading or current revised dossier.

## Inventory and pinned Git object hashes

| Dossier | Original title | Archived fragment | Git blob SHA-1 |
| --- | --- | --- | --- |
| 1.1.1 | Towards an Assessment of Twentieth-Century Philosophy | [dossier-1.1.1.html](dossier-1.1.1.html) | `8519e267ca29786a5be2725b7406eab9e704a4df` |
| 1.1.2 | Twentieth-Century Moral Philosophy | [dossier-1.1.2.html](dossier-1.1.2.html) | `f2e04101842693e17a43f45a3bfc8252fec0c179` |
| 1.1.3 | Philosophy of Science | [dossier-1.1.3.html](dossier-1.1.3.html) | `c37214a498fd57803bedfaf946e0bfd7737722bf` |
| 1.1.4 | Sartre, Foucault and Derrida | [dossier-1.1.4.html](dossier-1.1.4.html) | `be8c2762c75c1eb0434d27456f665de26aeede42` |
| 1.1.5 | The Gap Between Knowledge and Wisdom | [dossier-1.1.5.html](dossier-1.1.5.html) | `4047bfa26f0e069732a8188676e7c3dd78d1f0f9` |
| 2.1.1 | Introduction to Political Philosophy | [dossier-2.1.1.html](dossier-2.1.1.html) | `a106165e4592f372291092321fe813ff2051c5ea` |
| 2.1.2 | The Common Good | [dossier-2.1.2.html](dossier-2.1.2.html) | `5efd59bbec39309978fed3cccd43a8ccbdf36c20` |
| 2.1.3 | War | [dossier-2.1.3.html](dossier-2.1.3.html) | `c367bf7903d68ac91b54f165827e531ed712113f` |
| 2.1.4 | Introduction & Who Should Rule? | [dossier-2.1.4.html](dossier-2.1.4.html) | `489ffd440712f27d6bca17cc244a9b7d616146a4` |
| 2.1.5 | The Place of Liberty | [dossier-2.1.5.html](dossier-2.1.5.html) | `a0b27efff6716d37af26ca489d5fe6809a2348c4` |

The [MANIFEST.json](MANIFEST.json) also records the original source module Git blob hashes, chapter IDs and baseline commit.

## Read-only preservation procedure

1. **Do not edit, reformat, summarize, reattribute or replace** these original fragments. They are deliberately duplicated chapter IDs outside the reader and must never be included in `src/main.html`, `src/chapters/` or the generated `index.html`.
2. Run `python src/tests/verify_dossier_archive.py`. The check uses independently pinned Git blob hashes (not only manifest values), verifies each chapter opening and closing, and checks the complete six-part revision scaffold. GitHub Actions runs this test on relevant pushes and PRs.
3. Compare or restore content by consulting these historical fragments and applying any **separately authorized, source-verified** change to the live canonical source file. Do not overwrite the archive with the revised edition.
4. Before a future dossier is replaced for the first time, preserve its complete pre-edit `<section>` as an additional separately dated snapshot with commit provenance and an integrity check. Never expand or modify this closed set of ten originals.
5. GitHub does **not** enforce individual path-level read-only permissions; this is a **no-edit policy backed by integrity testing**, not an unbreakable repository lock. Keep an offline ZIP or mirrored repository backup as an additional safeguard against deletion or rewritten history.

## Current editorial documentation

- [Standing language and source-fidelity protocol](../../docs/editorial/LANGUAGE_AND_SOURCE_FIDELITY_REFINEMENT_PROTOCOL.md)
- [Concise dossier/Reading Companion method](../../docs/editorial/CONCISE_DOSSIER_AND_READING_COMPANIONS.md)
- [Context-first Reading Companions and Source Depth](../../docs/editorial/CONTEXT_FIRST_COMPANIONS_AND_SOURCE_DEPTH.md)
- [Canonical chapter sources](../../chapters/)

**Reader isolation:** This directory is not assembled, searched, printed or cached as part of the published Hikam reader.
