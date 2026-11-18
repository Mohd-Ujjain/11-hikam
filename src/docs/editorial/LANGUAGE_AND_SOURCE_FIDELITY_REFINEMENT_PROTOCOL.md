# Long-Run Editorial Refinement Protocol — Language, Source Fidelity, and Study Aids

**Project:** 11AM — Takhassus Hikam Dossier  
**Adopted:** 18 November 2026  
**Status:** Standing instructions for the reading-by-reading editorial refinement programme  
**Scope:** Existing and future bilingual Arabic/English dossiers in `MohdUjjain/11-hikam`  
**Governing rule:** **Make the source easier to understand, not smaller, different, or less complete. Preserve the book's established teaching and presentation system.**

> This protocol governs the present **editorial revision programme**, not a redesign, new-chapter template, philosophical critique, or authorization to modify the entire repository. It supplements — and does not supersede — the repository's [Design System](../design/DESIGN_SYSTEM.md), [Pagination System](../pagination/PAGINATION_SYSTEM.md), [source authoring instructions](../../README.md), and root [README](../../../README.md). Always inspect the current repository before editing; paths, counts, and conventions may change.

## 1. Purpose and scope

The established dossiers are substantial academic study notes, already supported by quotations, explanations, diagrams, tables, analogies, prompts, memory devices, checkpoints, and complete revision systems. The aim is **not to rebuild them**, replace their framework, change their visual language, or produce shortened summaries.

Three separate difficulties motivate this longer programme:

1. **Language and readability:** Arabic and English prose can be unnecessarily hard to follow. **This is the immediate editorial priority.**
2. **Coverage and fidelity to the actual reading:** a dossier may omit, compress, or misstate significant parts of its primary text. This requires a **separate, explicit source-comparison pass**.
3. **Intrinsic technical difficulty:** some source concepts are difficult even when the language is clear. A deeper concept-by-concept teaching/technical pass is a **distinct possible later phase**, not automatic permission to reframe the material.

Proceed **one reading/article at a time, in dossier order from the beginning**, using the primary material supplied for that reading. Each reading receives its own examination and revision; do not infer its contents from earlier chapters, a title, a generic treatment of the subject, or internet summaries.

### Priority and authority

- **Primary intellectual authority:** the actual main reading supplied for the dossier. It controls the author's ideas, thesis, terminology, distinctions, order of reasoning, evidence, quotations, examples, qualifications, objections/replies, level of certainty, and conclusions.
- **Arabic prose model:** the user's Arabic samples and `skill - language profiling.md`, when supplied or accessible. These control the requested *voice and linguistic habits* as far as compatible with readability, never the reading's intellectual conclusions.
- **Implementation authority:** the live repository and its real design, chapter, navigation, revision, print, and build conventions.
- **Editorial authorization:** the user's requested scope for the current reading and phase. Do not rewrite adjacent chapters or start a separate technical/design programme.

**Style is not substance.** The Arabic author's wording patterns do not license importing that writer's particular theological or philosophical claims into other authors' readings.

## 2. Non-negotiable source fidelity

Treat the dossier as an accurate teaching presentation of **what the source author says**, not a place for ChatGPT's independent philosophical opinions.

- Preserve every significant premise, inference, argument, objection, reply, distinction, definition, qualification, and conclusion present in the supplied source.
- Preserve the **strength and uncertainty** of the author's actual assertions: neither soften categorical claims nor turn tentative claims into certainties.
- Maintain a clear distinction among direct source statements, quoted third parties, historical reports, the author's interpretations, and our explanatory illustrations.
- Do not add unsolicited opposing opinions, artificial balancing, mainstream-consensus disclaimers, new objections, independent adjudication, or hedges such as “critics may argue” unless these come from the source or were explicitly requested.
- Do not silently “correct” a substantive claim or reassign an argument to another author. If a material discrepancy is identified, flag it as a separate editorial issue; preserve the supplied author's position in the dossier.
- Never invent quotations, citations, figures, examples purported to come from the source, or page references.
- Keep meaningful source quotations **verbatim** with their attribution and references; polish surrounding explanations, not the quoted text. If transcription is suspect, check the supplied original and flag discrepancies rather than guessing.
- When something is not covered or cannot be verified from the reading, identify it as such instead of filling it with unmarked general knowledge.
- Independent research may be carried out **only when requested** and must remain distinctly labelled from the reading's original content.

**Fidelity is not endorsement.** Present a controversial or strongly worded author's arguments faithfully without replacing them with the assistant's own stance.

## 3. Phase separation: the standing workflow

### Phase 0 — Preparation and source anchoring (per reading)

1. Confirm the exact chapter/subtopic in the live TOC and its authored `src/chapters/subtopic-*.html` section.
2. Read the original supplied reading **in full**, including appendices, quoted extracts, footnotes, tables, and references where provided. Never pretend to have read unavailable pages or attachments.
3. Read the current dossier **in full**, including frontmatter, main body, all study aids, and the six-part revision block.
4. Read the applicable design and pagination documentation and at least two comparable completed chapters when preparing chapter edits.
5. Consult the user's Arabic samples and the **full** language-profile skill if the reading is Arabic; if those materials are not available in the working context, request/reopen them rather than approximate the author's personal voice.
6. Establish an internal correspondence between the reading and existing dossier sections, identifying ambiguous passages and source-language terminology. Preserve source identifiers and references where available.
7. Establish a per-reading baseline. Do not silently make whole-book style changes.

### Phase 1 — Language and readability (**current primary pass**)

Edit the existing explanation **in place** for immediately understandable Arabic or English. The goal is first-careful-reading comprehension without loss of argument or intellectual seriousness.

- Make each sentence communicate a clear logical step; untangle excessive clause nesting where it obscures meaning.
- Prefer familiar, precise terms and natural syntax over unnecessary jargon or ornamental difficulty, **but retain necessary technical terminology** and teach it in context.
- Explain technical terms at their first meaningful use, then use the original term consistently. Do not replace distinct technical concepts with one loose synonym.
- Repair unclear pronoun antecedents, referents, transitions, unexplained jumps, and poorly signposted distinctions.
- Keep the source's logical progression intact; help the reader see *why* one step leads to the next. Reorganization is limited to making that progression clearer, not constructing a different argument.
- Use helpful paragraphs, short explanatory sentences, examples already present, and the existing study aids **where their function genuinely helps**. Do not inflate passages with repetitive paraphrases or mechanical step-by-step scaffolding.
- Polish headings, callouts, captions, table cells, prompts, checkpoint wording, and revision sections just as carefully as continuous prose.
- Avoid making scholarly prose childish, casual, patronizing, or oversimplified. Easy language is compatible with rigorous scholarship.
- The **source-alignment check** operates throughout this phase: ensure every edit leaves the reading's substantive meaning and certainty intact. This is not a substitute for the later exhaustive coverage audit.

**Editing principle:** Rewrite difficult *language*, not difficult *thought*. Explain complex reasoning with enough space; do not omit it for brevity.

### Phase 2 — Full source-coverage and accuracy audit (**separate second pass**)

Compare the polished dossier against the complete original reading, in the source's own order. Track, for each substantial unit, whether its treatment is **accurately covered / partially covered / absent / misstated / not verifiable**.

Examine, as applicable:

- The thesis and complete sequence of arguments, reasons, premises, conclusions, and qualifications.
- Named thinkers, schools, dates, historical contexts, technical terminology, and primary references.
- Quotations, citations, examples, analogies, illustrative cases, empirical assertions, and methodological distinctions.
- Source-supplied criticisms, objections, responses, unresolved tensions, and limits.
- Connections that are substantive to the reading, including its own relations among sections.
- The accuracy and completeness of the **study aids** and the full revision block, not only the prose.

For gaps, restore and teach the missing **source-derived** material inside the chapter's existing patterns; for misstatements, revise against the source and report any unresolved discrepancy. Do not add outside content to make the dossier appear more “complete.”

**Completion criterion:** a diligent reader should recognize the original reading's important contents, order of reasoning, and authorial position when returning to the source.

### Later technical-concept pass (only if separately authorized)

A more intensive conceptual teaching pass may be commissioned for intrinsically difficult readings. Keep it distinct from language and coverage, and preserve the same source boundaries and repository architecture. Do not preemptively launch this pass or redesign the notes as a result of difficult subject matter.

## 4. Arabic and English language standards

### Arabic — authorial voice with accessible expression

Use the user's provided Arabic texts (including dissertation passages on رسائل إخوان الصفاء، ابن سينا، كتاب الشفاء، علم المنطق، and منهج البحث) as evidence of their preferred voice. Consult `skill - language profiling.md` in full, especially **Part IV (lexicon)**, **Part VII (AI failure modes)**, and **Part VIII (permanent writing instructions)**, rather than reconstructing these instructions from memory. **The profiling file and writing samples are user-supplied working materials, not assumed to be present in the GitHub repository.**

The voice's useful governing traits are documentary primacy, evidence-led development, precise distinctions between testimony and inference, carefully calibrated inference vocabulary (where *the source* warrants inference), purposeful connectives, coherent paragraph progression, and unforced scholarly restraint.

- Retain the signature scholarly diction and connective choices where they work naturally and improve precision; do **not** imitate the samples' densest dissertation syntax if it makes a study explanation hard to understand.
- Keep the prose fluent, readable, orderly, and suitable for teaching; an idāfah-heavy or nominal construction is not required when a simpler accurate construction communicates better.
- The **source's epistemic degree prevails** over any stylistic preference for tentative language. Do not turn the source's categorical claims into `يظهر`/`يمكن أن` merely because such verbs occur in the Arabic profile.
- Do not use the profile's source-specific worldview, evidentiary hierarchy, or religious premises to rewrite unrelated authors' positions.
- Distinguish original technical terms from everyday explanatory words; use accessible Arabic without converting the text into a literal translation from English.
- Preserve correct Arabic quotations, honorifics, references, names, and the existing `lang="ar"`, RTL, typography, and `<bdi>` conventions.

### English — plain, precise academic explanation

Prefer direct, readable scholarly English. Replace avoidable syntactic density with clear relationships between claims; define difficult vocabulary without diluting it; preserve the source's actual distinctions and degrees of certainty. Avoid inflated academic jargon, formulaic hedging, conversational oversimplification, and unsupported interpretations. Neither language is a word-for-word translation template for the other.

### Shared readability test

After revision, ask: **Can a conscientious learner explain the idea in ordinary language, then return to the dossier and recover the source's full technical meaning and argument without a contradiction or missing step?**

## 5. Every existing study aid retains equal editorial standing

**All established aids matter equally as parts of the dossier's teaching architecture.** Their functions differ; do not give one privileged status, demand identical numbers of each, or add an aid merely for decorative consistency. Preserve, polish, and source-check **every type actually present in the reading**.

Use the real component semantics from [DESIGN_SYSTEM.md](../design/DESIGN_SYSTEM.md). The relevant system includes:

| Main-body aid | Existing component | Editorial responsibility |
| --- | --- | --- |
| Chapter roadmap | `.in-this-chapter` | Accurate orientation to the actual chapter |
| Central concept | `.box.concept` | State the reading's governing idea without overstatement |
| Definitions | `.box.definition` | Keep technical distinctions accurate and learnable |
| Examination tips | `.box.tip` | Clarify examination use without inventing source claims |
| Common misunderstandings | `.box.mistake` | Correct real interpretive confusions fairly |
| Memory supports | `.box.memory` | Preserve useful recall and simplification |
| High-yield material | `.box.highyield` | Make especially important points clear |
| Important source quotations | `.golden-quote` | Protect exact quotation and attribution |
| Section objectives | `.section-objective` | Express the genuine question each section answers |
| Hierarchies / logical structures | `.hierarchy` | Represent actual ranked or nested relations |
| Intermediate checkpoints | `.checkpoint` | Test understanding of material already taught |
| Concept relationships | `.concept-rel` | Express genuine source-grounded links |
| Analogies / accessible illustrations | `.analogy` | Explain without changing the concept |
| Tables and comparisons | `.tbl-wrap`, `.comparison` | Preserve all relevant distinctions; make cells readable |

Keep any existing timelines, lists, examples, quotation treatments, and other legitimate chapter-specific teaching structures as well. Do not assume this descriptive table is permission to replace the actual repository's component glossary.

### EL10 / ELI10 has a specific, limited role

**Explain Like I'm 10 is a clarifying technique for intrinsically difficult concepts — not a separate phase, not a general language standard, not a universal requirement, and not more important than other aids.**

- Use it decisively when a concept remains hard despite lucid scholarly prose.
- Supply a concise, plain-language bridge (and, where genuinely apt, an everyday analogy) through existing `.analogy`, `.box.memory`, or other already appropriate structures.
- Explicitly reconnect the simple explanation to the source's real technical term and argument.
- Keep explanatory illustrations distinguishable from examples or evidence **provided by the source**.
- Never let an analogy replace the full explanation, distort the concept, introduce an unsupported premise, or patronize the learner.
- Do not insert EL10 everywhere or turn the whole language pass into an EL10 rewrite.

**All aids — tables, timelines, quotes, checkpoints, tips, roadmaps, revision elements, and EL10 where applicable — receive the same editorial care.**

## 6. Revision-block preservation

Maintain the established `.end-block` and its **complete sequence**, for every revised chapter:

1. Chapter Summary.
2. One-Page Revision Sheet.
3. Key Definitions.
4. Key Table.
5. Memory Aids Collected.
6. Possible Examination Questions.

Preserve the five examination-question classes in order: **Short Answer, Long Answer, Comparison, Conceptual, Application**.

Revision material must be rechecked against the improved main body and the original source. It must not retain confusing old phrasing, omit restored source material, or introduce unsupported facts. Do not shorten, delete, or redesign the revision system during a language pass.

## 7. Technical and presentation boundaries

This programme is **editorial, not architectural**.

- Retain the existing chapter frontmatter, sections, headings, navigation, banners, labels, quotation treatments, semantic box colors, tables, diagrams, timelines, aids, and dark concluding revision blocks.
- Keep all corresponding authored HTML structure and meaning. Amend text in canonical `src/chapters/subtopic-*.html` fragments; do not edit generated `index.html`, `service-worker.js`, or `src/philosophy_study_notes.html` by hand.
- Preserve Arabic `class="chapter rtl"`, `lang="ar"`, existing Amiri/RTL conventions, and print-specific behavior.
- Do not opportunistically refactor the stylesheet, JS reader, navigation, printing, PWA, or other chapters.
- If an editorial content change truly requires a structural change, first verify that the existing documented components cannot accommodate it, then limit the change strictly to what is necessary.
- Do not upload unpublished, restricted, or user-supplied full reading texts/style samples to GitHub unless explicitly authorized; their use as editorial references does **not** authorize publication.

## 8. Repeatable quality checklist and handoff

For **each reading**, maintain a compact record (in the task report, and in repository editorial notes when requested) with the following:

| Check | What must be demonstrated |
| --- | --- |
| Exact reading | Main text accessible and reviewed; edition/pages noted where available |
| Exact dossier | Correct current section located in canonical repository |
| Voice | Arabic sample/profile consulted if applicable; English/Arabic fluent and accessible |
| Language | Sentences, terms, transitions, and all aid text made clearer without trivialization |
| Source fidelity | Thesis, reasoning, conclusions, certainty, quotation and attribution unchanged in substance |
| Coverage | Original-to-dossier comparison performed in Phase 2; omissions and misstatements addressed or explicitly flagged |
| Study aids | Every preexisting aid type and chapter-specific structure reviewed; EL10 used only where useful |
| Revision | All six end-block components and five question categories retained and aligned |
| Scope | No unrelated chapter, design-system, or reader change |
| Implementation | Changes made to canonical files, generated outputs rebuilt, links/RTL/print inspected as applicable |
| Verification | Exact commands/tests performed and their results reported; unresolved issues listed |

For source-to-dossier coverage, a brief traceability matrix may use: **source unit / dossier location / status (covered, partial, absent, inaccurate, unverifiable) / required editorial action / resolved?** Do not substitute the matrix for actual close reading.

When making **chapter content changes**, follow the repository's current canonical build and verification procedure (from repository root), as available:

```bash
python src/build.py
python src/build.py --check
python src/tests/verify_publication.py
python src/tests/validate_structure.py
python src/tests/verify_sidebar.py
python src/tests/verify_reading_progress.py
node src/tests/test_offline_cache.mjs
```

Also inspect relevant browser reading, Arabic typography/RTL, and print output when applicable. **Documentation-only changes to this protocol do not themselves imply a content rebuild or a deployment.** Do not claim tests, builds, commits, or publication checks passed unless actually observed.

## 9. Operating instruction for every subsequent session

Before undertaking a reading's language or fidelity pass:

1. Reopen **this protocol** from the current repository.
2. Reopen the latest [Design System](../design/DESIGN_SYSTEM.md), [Pagination System](../pagination/PAGINATION_SYSTEM.md), the relevant canonical chapter, and comparable chapters.
3. Read the full user-supplied main reading; for Arabic, also reopen the actual language-profile file and available Arabic samples. Ask for missing reading materials only if genuinely necessary; do not invent their content.
4. Confirm the requested phase and proceed only within its scope, using the source as intellectual authority and the repository as implementation authority.
5. Preserve all study aids without ranking them; use EL10 **only** where it serves concept comprehension.
6. Report the actual files changed, source coverage reviewed, tests performed, and remaining limitations.

**Final standard:** **Source fidelity + full intellectual coverage + accessible scholarly language + equal care for every established study aid + unchanged dossier architecture.** The result should be much easier to read but no poorer in content.
