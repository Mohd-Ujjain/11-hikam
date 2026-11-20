# Compact Re-pass of Political Dossiers 2.1.3–2.1.5

**Editorial decision and authority:** Adopted 18 November 2026 in [Concise Dossiers and Source-Grounded Reading Companions](CONCISE_DOSSIER_AND_READING_COMPANIONS.md) and affirmed by [Context-First Companions and Source Depth](CONTEXT_FIRST_COMPANIONS_AND_SOURCE_DEPTH.md): aim for **650–850 immediately readable explanatory words**, **850–1,150 meaningful existing study-aid words**, and **1,500–2,000 immediately visible words** per dossier. Source fidelity overrides mechanical cutting. Frontmatter, optional Companions/Source Depth and all six end-of-chapter revision sections are separately counted.

**Scope and archive safeguard:** This three-reading pass starts from original authoritative `main` commit `35507f88fc4c4df2e4877fe04784ce921f49f843`, including the user's one-commit 21 November addition of the `src/archive/pre-revamp-2026-11-05/` snapshot and `src/tests/verify_dossier_archive.py`. None of the archive files, user README changes or original archive workflow changes are edited or displaced. This re-pass edits the **live** `ch2-1-3`, `ch2-1-4`, `ch2-1-5` source sections and their cue paragraph matches, not the historical archive.

## Before and after, using the existing Python HTMLParser word-layer model

| Dossier | Original source | Previous prose | Concise prose | Previous aids | Concise aids | Previous visible | Concise visible |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **2.1.3 — War** | Colin Bird, *An Introduction to Political Philosophy*, 2nd ed. (2019), chapter 11, 30-page PDF | 1,234 | **780** | 1,184 | **1,117** | 2,418 | **1,897** |
| **2.1.4 — Introduction & Who Should Rule?** | Jonathan Wolff, *An Introduction to Political Philosophy*, revised 2006 ed., Introduction pp. 1–5 and Chapter 3 pp. 62–77 (21 pages) | 1,430 | **729** | 1,247 | **1,131** | 2,677 | **1,860** |
| **2.1.5 — The Place of Liberty** | Jonathan Wolff, Chapter 4, pp. 104–117 (14 pages) | 1,331 | **715** | 1,202 | **1,113** | 2,533 | **1,828** |
| **Total** | 65 pages of original supplied academic reading | **3,995** | **2,224** | **3,633** | **3,361** | **7,628** | **5,585** |

**Result:** All three fit the agreed **individual prose, aid and combined visible bands**; visible reading drops **2,043 words** while preserving the original source argument sequence and the existing revision system. Counts are direct word-layer measurements of the source HTML, not estimated page numbers or total DOM text. Rerun the three dedicated source-fidelity scripts before release for definitive CI confirmation.

| Unchanged optional and revision material | 2.1.3 | 2.1.4 | 2.1.5 |
| --- | ---: | ---: | ---: |
| Optional Source Depth words | 1,457 | 1,682 | 1,653 |
| Paragraph-adjacent, closed source disclosures | 10 | 9 | 8 |
| Source-cited items | 14 | 17 | 16 |
| Existing source-grounded Reading Companions | 19 | 23 | 22 |
| Independent end-of-chapter revision areas | 6 | 6 | 6 |

All **64** contextual Companion records retain their original authors, intellectual content, page numbers, identifiers, exact trigger terms, distinct `simple`, `why_here`, `remember`, and `sourceDepthId` references. Their **`passage` selectors alone** have been refreshed to the newly condensed, uniquely identifiable visible paragraphs. The optional Source Depth prose and citations have not been rewritten to achieve the count. The whole reader contains **154** Companion records.

## Source-to-visible spine after compression

### 2.1.3 — Bird, “War” (original PDF pages 1–30)

| Pages | Indispensable argument and qualification retained visibly | New owner |
| --- | --- | --- |
| 1–5 | War's institutional planning and codes; Bird's sombre 1914 truce; just war, pacifism and realism; Hobbes's blameless liberty and disposition to fight | §I–II prose, original comparison and Hobbes quotation |
| 6–11 | Cultivated enmity, Walzer's morally coercive aggression; differences between `jus ad bellum` and `jus in bello`, all seven criteria in a stand-alone table; divergent 2003 Iraq applications and Bird's demand for useful guidance rather than universal consensus | §III–IV prose; unchanged criteria table and misunderstanding aid |
| 12–19 | Independent war-conduct standards; Walzer against the sliding scale yet acknowledging a narrowly conditional supreme emergency; Vattel/statist restraint versus Moellendorf/cosmopolitan justice; Bird's danger of symbolic hostility before an attack | §V–VI prose, conceptual map, original cited local records |
| 20–26 | Radical and just-war pacifism, King and Penn's different forms of coercion; innocent soldiers, Moellendorf's self-defence cases, Joad, civilian targeting and unintended harm | §VII–VIII prose; distinct comparison, analogy and qualification aids |
| 27–30 | Actual imminence and alternatives versus past wrongs, excuse versus justification, civilian commanders versus protected noncombatants, London/Moscow and Bird's **open transition** toward realism | §IX prose; retained Exam Tip, revision and separate source records |

The shorter prose keeps the author's objections and replies in view; the existing labelled tables and study aids teach their criteria, distinctions and case comparisons without reiterating whole prose paragraphs. The nonprinting Source Depth gives the detailed primary-source circumstances, chronology, qualifications and named authorities, **never an indispensable premise missing from the main visible reading**.

### 2.1.4 — Wolff, Introduction and “Who Should Rule?” (printed 1–5 and 62–77)

| Pages | Indispensable source progression | New owner |
| --- | --- | --- |
| 1–5 | Distribution of rights/goods versus coercive authority, Locke's qualified account, anarchism/authoritarianism, normative versus descriptive method, the impossibility of political nonparticipation | §I–II prose, comparison and definition |
| 62–66 | Democratic “of/by/for”; 51% versus minority rights, Tocqueville, Mill and Madison; direct/representative democracy, selection and franchise disputes | §III–IV prose; labelled tables and restored Hierarchy Recognition |
| 66–71 | Plato's navigation and medicine craft analogies, guardian education, unchecked authority/corruption, why an expert's fallibility and defects in guardianship **do not prove democracy** | §V–VI prose; ship-role table and existing mistaken-inference aid |
| 71–75 | Competing interests, Hume, opinion polls, the student-house smoking vote's mixed motives, and both **conditional** requirements for Condorcet's result | §VII–VIII prose, case table and conditional theorem aid |
| 76–77 | Intrinsic versus instrumental democratic value, craft/training-voyage examples, freedom/equality, Rousseau's question of obeying oneself under joint rule | §IX prose and analogy; no general-will solution imported |

The source ends part-way through the next section's epigraph. The main text and independent revision explicitly preserve this cutoff. The existing 23 contextual cues now point to shorter main paragraphs; no full argument was moved exclusively to Companion/Depth.

### 2.1.5 — Wolff, “The Place of Liberty” (printed 104–117)

| Pages | Indispensable source progression | New owner |
| --- | --- | --- |
| 104–107 | Majority tyranny, anarchy and absolute state power, the Harm Principle's distinction from paternalism and Mill's explicitly limited applicability | §I–II prose, independently useful definitions and misconception box |
| 107–110 | True, false and partly true opinions, infallibility, Socrates and Jesus, **Alexandria as an unreliable historical report**, Rousseau's challenge to the benefit of truth, Mill's reply **and Wolff's remaining reservation** | §III–IV prose, three-case hierarchy, objection/reply table |
| 110–112 | “Dead dogma,” evolutionary controversy **according to some accounts**, and printed criticism of corn dealers versus incitement at an excited crowd | §V prose, mnemonic analogy, harm-context distinction |
| 112–116 | Self/other-regarding acts, private worship and indirect impacts; offence, harmed interests and morally permissible competitive losses; natural-rights scepticism, Bentham, Locke and conventional legal limitations | §VI–VII prose, comparisons, rights definitions and original case-specific Source Depth |
| 116–117 | Utility in the largest sense, progressive interests and quality of pleasures, socially defensible rights, the <em>utilitarian legislator</em>'s question | §VIII prose and revision; **no answer beyond the final “not so obvious” sentence** |

The new version preserves all six revision areas and the independently meaningful table contrasting possible interference. The distinction between source reports, quoted authors, and Wolff's own reservations remains explicit.

## Editorial operations and controlled test obligations

- **Concise prose:** Rewrote **15 / 16 / 16 existing ordinary explanatory paragraphs** into simpler, shorter source-connected sentences, retaining the original chapter sequence and section numbers.
- **Instructional aids:** Shortened duplicated orientation, “mistake,” memory and explanatory analogy boxes; did **not** remove or relabel any existing aid component class or change what it means. All retained comparison tables and all six revision components are still independently examinable.
- **Optional layers:** Unchanged 27 native closed Source Depth disclosures (47 independent citations), plus original 64 user-initiated, context-first Companion answers. These layers are not extra compulsory pages or substitutes for the argument.
- **Structural boundaries:** The 39-chapter book, chapter IDs, TOC attribution, original quotes, color `--hue` values, CSS/JS implementation, search and single-file offline reader remain unchanged.
- **Tests:** The three existing author-specific source-integrity scripts now enforce **650–850 / 850–1,150 / 1,500–2,000** and retain checks covering source units, terms, author's uncertainty, objection/reply, citations, A4 exclusions and six revision areas. A few literal old-phrase assertions have been aligned with semantically equivalent shortened wording without removing source requirements.
- **Archive protection:** This test branch comes from the user's newer original `main` with its new archive and archive verification workflow. Include `verify_dossier_archive.py` in the fork, and verify the original PR diff to make sure no archive path changes.

**Release policy:** This file is a **fork candidate audit**, not a claim of publication. Do not transfer the academic or generated reader files to the original repository before the full fork Python, accessible Chromium, real A4 print/PDF and offline PWA suites pass. Then compare every transferred file's Git blob hash, require original PR verification, confirm post-merge checks and the authoritative GitHub Pages deployment. Update the README and the three previous release audits with the new measured counts only after an independently verified merge. Do not publish user-supplied source PDFs or supporting texts.
