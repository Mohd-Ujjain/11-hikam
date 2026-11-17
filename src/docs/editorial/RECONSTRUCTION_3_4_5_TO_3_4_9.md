# Editorial Reconstruction — Dossiers 3.4.5–3.4.9

## Source boundary

The only substantive inputs for these five dossiers were the **five study briefs supplied in the conversation**: *Liliputian Biology*, *Questions about Design*, *Ten Years Later*, *The Nature and Scope of Evolution*, and *The Origin of Life*. The original PDFs were not available as repository files during this reconstruction. The chapter arguments follow those briefs; they have not been supplemented by external research, opposing arguments, bibliographic inventions, or editorial opinions. Figures, models, scholars and source-specific conclusions remain tied to the briefs from which they came.

The reconstructed dossiers preserve the source positions while using the house's direct explanatory voice. Provenance appears where the author is quoted or a controversial probability/model is invoked; it does not intrude into every paragraph.

## Canonical integration

Only the five **English LTR** sections `ch3-4-5` through `ch3-4-9` of `src/chapters/subtopic-3-4.html` were rewritten. Dossiers 3.4.3 and 3.4.4 remain byte-identical within that fragment. Each revised chapter now has direct chapter children, in exactly this order:

1. `.chapter-frontmatter` (banner and numbered argument map)
2. `.chapter-body` (golden quote, thesis, sections, teaching components, synthesis)
3. `.chapter-endnav` (contextual previous/next links)
4. `.end-block` (dark, independently paginated revision material)

This repairs the initial incorrect nesting of the navigation and revision block *inside* `.chapter-body`. That nesting bypassed the JS print engine's independent dark flow and broke the entire point of the revisions.

All five revisions use the six named house sections, in the established order: **Chapter Summary → One-Page Revision Sheet → Key Definitions → Key Table → Memory Aids Collected → Possible Examination Questions**. The question bank is divided into **Short Answer, Long Answer, Comparison, Conceptual, Application**, with source-specific prompts in each category.

## Per-dossier fidelity map

| Dossier | Source argument preserved | Teaching apparatus |
|---|---|---|
| **3.4.5 — Liliputian Biology** | Chain of biological black boxes; Hippocrates through Harvey and cell theory; Kendrew, Watson and Crick; molecular machines; micro/macro ditch-versus-canyon; six-step phototransduction; Haeckel and the imagined simple cell | Historical chronology table, cell-machine hierarchy, visual cascade map and parts table, nested-boxes/factory/bridge/light-gate/cardboard-box memory aids |
| **3.4.6 — Questions about Design** | Simplicity barrier; Paley's mechanical arrangement versus incidental details; Hume's analogy critique and best explanation; Dawkins' WEASEL and combination lock; Miller's blind spot, pseudogenes, vestiges and panda's thumb; coexistence with common descent | Invention and watch tables, Hume matrix, WEASEL/lock comparison, imperfect-structure comparison, inference hierarchy and copier analogy |
| **3.4.7 — Ten Years Later** | Genomes, multi-protein teams, microRNAs and machinery; exact IC definition; Pennock/Miller/Orr critiques and replies; the positive engineering inference; cilia, flagella/TTSS, immunity and clotting as literature challenges; burden of proof | Genomic-decade table, IC scope matrix, three-critic comparison, engineering hierarchy, four-system comparison, motor-factory/mousetrap/stone-route/statue/catalogue analogies |
| **3.4.8 — The Nature and Scope of Evolution** | Five meanings of evolution; Patterson's logic and selection as a weeder; malaria and CCC statistical edge; fossil stasis, Cambrian diversification and intermediate/transitional distinction; punctuated equilibrium; common design, Smith's wheat and Logos | Five-category taxonomy, selection syllogism, CCC progression, fossil matrix, descent/design comparison, five-drawers/judge/lottery/film/Smith analogies |
| **3.4.9 — The Origin of Life** | Cell versus crystal, flagellum and IC, Miller–Urey/atmosphere/chirality/thermodynamics, 100-residue sequence probabilities, Hoyle's 747 and Cicero's gold letters, self-organization versus specified information | Cellular hierarchy, flagellum/trap, chemical obstacles, probability hierarchy, order/information table, factory/gloves/letters/clock-program analogies |

## Numerical and source-sensitive anchors

- **3.4.5**: Harvey's estimated **540 pounds/hour** and the visual chain **11-cis-retinal → rhodopsin/metarhodopsin II → transducin/GDP–GTP → phosphodiesterase → cGMP → ion channels**.
- **3.4.7**: The IC definition is explicitly **system-level**. The critique does not purport to rule out all conceivable indirect paths.
- **3.4.8**: The **1 in 10²⁰** figure is retained as the **CCC-model claim**; it is not applied to every mutation.
- **3.4.9**: The chirality illustration is **(1/2)¹⁰⁰ ≈ 1 in 10³⁰**; the one-specified-protein illustration is **(1/20)¹⁰⁰ ≈ 1 in 10¹³⁰**. Their different assumptions are kept separate.

## Regression and printing

- `src/tests/verify_3_4_house_style.py` now asserts separate chapter direct children, six-part revision sections, five exam categories, source-appropriate component variety, TOC and navigation integrity, and all named print templates.
- `src/tests/browser_3_4_house_style.py` exercises actual Chromium rendering, 390/1366px viewports, independent light/dark page flows, footer clearance and a sampled A4 PDF.
- Five named `ch3-4-N` and `rev3-4-N` templates and their CSS assignments have been added. JS auto-discovers the new chapters without changing chapter-selection logic.

The existing 34 earlier dossier texts were not revised by this chapter reconstruction.
