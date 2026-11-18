# Reading Companion Pilot — Dossiers 1.1.1 and 1.1.2

**Date:** 18 November 2026  
**Scope:** Reader mechanism and a three-entry, source-verified pilot; **no prose or study-aid compression** in this commit.  
**Editorial authority:** [Concise Dossiers & Reading Companions](CONCISE_DOSSIER_AND_READING_COMPANIONS.md) and [Standing Language & Source-Fidelity Protocol](LANGUAGE_AND_SOURCE_FIDELITY_REFINEMENT_PROTOCOL.md).

## Source and redundancy audit

The originals were directly consulted, not inferred from derivative notes:
- Dermot Moran, *Towards an Assessment of Twentieth-Century Philosophy*, supplied PDF `1.1.1 Source - Introduction - Towards an Assessment of Twentieth-Century Philosophy (Routledge Companion).pdf`.
- Rowland Stout, *Twentieth-Century Moral Philosophy*, supplied PDF `1.1.2 Source - Twentieth-Century Moral Philosophy (Routledge Companion).pdf`.

These source PDFs are **not** committed into the public repository. The manifest contains the editors' brief, sourced paraphrases and only references the original printed pages.

| Companion ID | Current phrase / added intellectual value | Original source page | What the visible notes already cover / why the popup does not duplicate it |
| --- | --- | --- | --- |
| `h111-russell-idealism` | “Russell initially described analysis” — Moran contrasts an empiricist story of Russell with Hylton’s evidence of Bradley and McTaggart’s idealist influence. | Moran, 28–29 | The prose covers Russell's logical analysis and philosophical system-building but not the particular disagreement among historians about his intellectual ancestry. |
| `h112-parfit-identity` | “future generations” — Stout connects moral concern for future people to Parfit's less rigid view of the identity of one's own future self. | Stout, 874 | The prose and utility table introduce future persons; they do not explain the identity argument connecting future self-concern to wider future interests. |
| `h112-harrod-rule` | “generalization principle” — Stout distinguishes Harrod’s Kantian justification for general principles from utility's role in selecting among principles. | Stout, 876 | The visible text compares act and rule utility but does not explain this distinct Kantian contribution to rule-utilitarianism. |

All three items add specific material from the primary reading without changing its author's position or level of confidence. Other possible annotations were not added just to increase the count. No original passage content was edited or removed.

## Implementation contract

- Canonical content: unchanged `src/chapters/subtopic-1-1.html`.
- Canonical pilot records: `src/reading_companions.json`. Each item has an ID, chapter, identifying passage, exact trigger phrase, short kind/title/explanation, source author/work/page and added-value rationale.
- Renderer: `src/reading_companions.js`. Locates **one** unique paragraph matching the assigned passage and **one** exact text-node occurrence inside it. Ambiguous or missing matches fail closed. It never rewrites the source chapter HTML.
- Presentation: appended restrained CSS in `src/philosophy_notes.css`, chapter hue, flowing multiword underline, viewport-bound noninteractive tooltip, keyboard Enter/Space/Escape, click/tap, optional desktop hover, dismissal on navigation/print and RTL/Amiri handling.
- Offline: `src/build.py` embeds the validated manifest into `src/main.html` at the authored marker, then inlines the controller alongside the existing CSS/JS. No Companion network request is required.
- Printing: the existing `src/philosophy_notes.js` clones the chapter body; the new narrow guard unwraps cues into their identical source text **inside that private clone before pagination**. Revision content, source chapter, TOC, reading progress and navigation remain untouched.
- Regression: `src/tests/verify_reading_companions.py` verifies source anchors and publication integration. `src/tests/browser_reading_companions.py` checks mobile/desktop behavior, keyboard/RTL and print clones. The normal build, publication, search, page-count, progress, offline and PWA regression tests remain mandatory.

## Pilot boundaries and next editorial phase

**This release introduces the mechanism and three optional local companions, not a condensed 1.1.1 or 1.1.2.** The present expanded dossiers remain readable without any Companion. Both require a separate source-to-layer coverage matrix and compression pass **before** moving towards the adopted **1,500–2,000 visible-word range** (650–850 prose / 850–1,150 aid words according to source length). No semantic aid category, revision section or scholarly quotation has been removed.

Additional companions may be considered only after the six editorial acceptance checks against each complete primary source. A short pilot with three source-verified entries is more useful than dozens of redundant popovers.
