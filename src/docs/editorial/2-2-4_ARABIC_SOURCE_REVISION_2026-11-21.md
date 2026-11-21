# Dossier 2.2.4 — Arabic source-grounded editorial revision

**Scope:** Only chapter 2.2.4 within `src/chapters/subtopic-2-2.html`.

## Preservation
The complete prior 2.2.4 chapter was archived verbatim (except for an explanatory HTML comment outside the section) at `src/docs/editorial/archive/2-2-4-original-pre-revision.html` *before* replacement.

## Primary reading
User-supplied DOCX: `2.2.4 Source - مقدمة (أرسطوطاليس - الميتافيزيقا).docx`, paragraphs headed `مؤلفاته ومكانة كتاب «الميتافيزيقا»` and `نبذة عن كتاب الميتافيزيقا`. The uploaded Arabic writing samples and language profile informed editorial diction; they were not treated as substantive philosophical sources.

## Substantive changes
- Correctly distinguish the three-part Ross/Kerferd classification from the two-part classification adopted by the reading's author.
- Restore the five scientific groups and examples, the differences between published prose and evolving lecture notes, and the limits of the historic attribution estimates.
- Distinguish Aristotle's first philosophy from Andronicus' later organizational title.
- Restore the reading author's criticism of **later restriction** of philosophy by Aristotle's framework, without imputing that restriction to Aristotle himself.
- Reconstruct all fourteen books in a source-aligned table with stated chapter counts; preserve qualifications about book XI, the prominence of XII, and Ibn Rushd on XIII–XIV.
- Keep all six revision sections and five exam classes.
- Remove the original chapter's invented stand-in quotation and unsupported categorical language.
- Preserve RTL, `lang="ar"`, chapter ID, hue, navigation, and existing design classes.

## Validation status
Direct read-back from the fork confirms all six chapters 2.2.1–2.2.6 remain in the subtopic, chapter 2.2.4 occurs once, six revision headings and five exam categories remain, and the archive exists. **This is a source change only. The canonical build (`python src/build.py`), generated output hashes, browser accessibility tests, print pagination, offline checks, and CI have not yet been executed.** Do not merge or publish before those checks.

## Source traceability notes
The primary source provides no stable printed page references in the supplied DOCX, so no invented page citations or Source Depth records were added. Contextual Reading Companions were not added without a verified exact-anchor manifest and reader tests.

## Release gate
Run `python src/build.py`; verify and commit all generated outputs; run the repository's canonical structural, browser, print, PWA and design checks on this fork, then review before any upstream promotion.