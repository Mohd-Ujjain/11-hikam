# Reading 1.1.5 — Simon Critchley, *The Gap between Knowledge and Wisdom*

**Editorial preparation:** 19 November 2026  
**Primary evidence:** user-supplied eight-page chapter extract, *Continental Philosophy*, chapter 1.  
**Secondary working aids:** three user-supplied teaching syntheses; claims were checked against the chapter, not adopted as separate source authority.  
**Scope:** dossier 1.1.5 only, `src/chapters/subtopic-1-1.html` and `src/reading_companions.json`.

## Source-to-dossier coverage register

| Primary source PDF page | Significant source unit | Revised treatment |
|---|---|---|
| 1 | Ancient philosophy as the love of wisdom; Socrates, Aristotle, Stoics; contemplation and happiness; formation, examination and polis | §I; definition, checkpoint and adjacent optional ancient-detail record |
| 2 | The party stranger, meaning of life; academic philosophy's embarrassment and “folk psychology” | §I, context-first Companion |
| 3 | Experimental science, faith/water comparison, theoros; epistemology, Locke and the Crystal Palace | §II, quote, terms and source detail |
| 4 | Value of science and technology, naturalistic ontology, appendix of wisdom, evolutionary epistemology, explanatory versus felt gap | §III, definition, Companion and source detail |
| 5 | Nihilism/affluence paradox, Brecht, invented neuroses, esotericism, religion and authoritarianism, scientism and obscurantism | §III–IV; comparisons, Source Depth where useful |
| 6 | John Stuart Mill's beasts/lunatics, ancient teleology and final causes, Descartes and Pascal | §IV; comparison and direct source quotations |
| 7 | Weber's disenchantment; re-enchantment dilemma; argument for existential engagement; opening Continental examples | §IV–V; definitions, Source Depth and table |
| 8 | Complete thinker list (including Freud and Levinas), Wittgenstein, and the necessary-versus-sufficient conclusion | §V, eight-row thinker table, Companion, Source Depth and independent revision |

## Source-fidelity corrections from the previous 1.1.5 edition

- Restores the author's **qualified** characterizations rather than converting his *I think*, *I would wager*, and *seems* into universal historical laws.
- Preserves the distinction between *not answering* and *at least tackling* the question of the meaning of life.
- Separates the success of science from Critchley's criticism of **scientism**.
- Explains evolutionary epistemology as a two-step reduction and the gap as **felt rather than explanatory**.
- Restores the roles of Freud and Levinas in Critchley's full set of Continental examples.
- Restores **Wittgenstein** and the exact concluding logical difference: bridging the gap is **not sufficient** to discriminate between traditions, but should be **necessary** for all philosophical activity.
- Replaces oversimplified labels that treated analytic and Continental philosophy as rigid or mutually exclusive types.
- Keeps illustrative car analogy identified as a **teaching analogy**, not author-supplied evidence.
- Preserves six revision sections and all five examination-question classes.

## Layer and interaction inventory

- Context-first Reading Companions: **9**. Each has a stable ID, a specified existing passage/phrase, a direct explanation, a local-purpose explanation, a recall line, and author/source PDF page attribution.
- Collapsed inline Source Depth disclosures: **5**, immediately after the connected ordinary prose paragraphs. All start closed; native `details/summary` should work without JavaScript.
- Existing semantic aids: core concept, definitions, high-yield, mistake, tip, comparisons, concept relationship, analogy, checkpoints and source quotations.
- The displayed argument is complete without opening a Companion or Source Depth.
- No unrelated chapter, shared design-system component or source PDF has been modified.

## Verification and release status

**Complete editorial review branch, NOT PUBLISHED.** The proposed source and Companion manifest were written to a dedicated GitHub branch; read-back confirmed nine entries, five native Source Depth elements, six revision headings, and preservation of the next-chapter link. No local canonical build or Chromium print / keyboard / touch / RTL / search / design-token / PWA tests have been executed in this environment because a complete runnable Git checkout and its assets are unavailable here. The generated `index.html`, `src/philosophy_study_notes.html` and `service-worker.js` have **not** been regenerated. The branch must remain unmerged until reproducible build and the repository's complete tests pass.

Required commands after checking out the review branch:

```bash
python src/build.py
python src/build.py --check
python src/tests/verify_publication.py
python src/tests/validate_structure.py
python src/tests/verify_sidebar.py
python src/tests/verify_reading_progress.py
python src/tests/browser_design_tokens.py
node src/tests/test_offline_cache.mjs
```

Also run the repository's actual Reading Companion browser and print/PDF test suites, and review the chapter at desktop and mobile widths. Run the prescribed secondary-account fork CI verification before promoting a tested edition to the publishing `main` branch.
