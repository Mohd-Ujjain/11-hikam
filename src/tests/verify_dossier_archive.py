#!/usr/bin/env python3
"""Guard the ten historical pre-revamp dossier fragments against accidental edits."""

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "src/archive/pre-revamp-2026-11-05"
BASELINE = "aa601b2441f81ab1469b37e64514b5c2f117b273"

# Independently pinned: changing MANIFEST.json and the archived HTML together
# cannot silently approve a replacement of the original edition.
PINNED_BLOBS = {
    "1.1.1": "8519e267ca29786a5be2725b7406eab9e704a4df",
    "1.1.2": "f2e04101842693e17a43f45a3bfc8252fec0c179",
    "1.1.3": "c37214a498fd57803bedfaf946e0bfd7737722bf",
    "1.1.4": "be8c2762c75c1eb0434d27456f665de26aeede42",
    "1.1.5": "4047bfa26f0e069732a8188676e7c3dd78d1f0f9",
    "2.1.1": "a106165e4592f372291092321fe813ff2051c5ea",
    "2.1.2": "5efd59bbec39309978fed3cccd43a8ccbdf36c20",
    "2.1.3": "c367bf7903d68ac91b54f165827e531ed712113f",
    "2.1.4": "489ffd440712f27d6bca17cc244a9b7d616146a4",
    "2.1.5": "a0b27efff6716d37af26ca489d5fe6809a2348c4",
}
REVISION_HEADINGS = (
    "Chapter Summary",
    "One-Page Revision Sheet",
    "Key Definitions",
    "Key Table",
    "Memory Aids Collected",
    "Possible Examination Questions",
)


def blob_sha(contents: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(contents)).encode("ascii") + b"\0" + contents
    ).hexdigest()


def verify() -> None:
    manifest = json.loads((ARCHIVE / "MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["source_commit"] == BASELINE, "Historical source commit changed"
    entries = manifest["entries"]
    assert len(entries) == 10, "Archive must contain exactly ten entries"
    assert {entry["dossier"] for entry in entries} == set(PINNED_BLOBS), "Inventory mismatch"
    assert {p.name for p in ARCHIVE.glob("*.html")} == {
        f"dossier-{n}.html" for n in PINNED_BLOBS
    }, "Missing or unexpected archive file"

    for entry in entries:
        number = entry["dossier"]
        chapter_id = "ch" + number.replace(".", "-")
        path = ARCHIVE / f"dossier-{number}.html"
        contents = path.read_bytes()
        checksum = blob_sha(contents)
        assert checksum == PINNED_BLOBS[number], (
            f"{number}: archive changed (found Git blob {checksum})"
        )
        assert entry["archive_git_blob_sha"] == checksum, f"{number}: manifest hash mismatch"
        assert entry["archive_path"] == path.relative_to(ROOT).as_posix(), (
            f"{number}: manifest path mismatch"
        )
        assert entry["section_id"] == chapter_id, f"{number}: chapter ID mismatch"
        assert entry["original_module"] == (
            f"src/chapters/subtopic-{number[0]}-1.html"
        ), f"{number}: original module mismatch"

        html = contents.decode("utf-8")
        assert re.match(r'<section\b[^>]*\bid="' + re.escape(chapter_id) + r'"', html), (
            f"{number}: original opening section missing"
        )
        assert html.endswith("</section>"), f"{number}: section closing tag missing"
        assert len(re.findall(r"<section\b", html)) == 1, (
            f"{number}: duplicate/nested chapter section"
        )
        assert html.count("</section>") == 1, f"{number}: section imbalance"
        assert 'class="chapter-frontmatter"' in html, f"{number}: frontmatter missing"
        assert html.count('class="end-block"') == 1, (
            f"{number}: revision system missing or duplicated"
        )
        for heading in REVISION_HEADINGS:
            assert heading in html, f"{number}: revision section missing: {heading}"
        assert html.count('class="examq-cat"') >= 5, (
            f"{number}: missing examination question categories"
        )

    assert "pre-revamp-2026-11-05" not in (
        ROOT / "src/main.html"
    ).read_text(encoding="utf-8"), "Archive must not enter the current book spine"
    print("PASS: ten original dossiers match pinned Git blobs, with full revision systems")


if __name__ == "__main__":
    verify()
