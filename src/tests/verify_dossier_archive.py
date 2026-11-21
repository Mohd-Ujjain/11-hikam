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
    # Subsequent dossiers use separately dated snapshots; the closed ten-file set
    # above must never be enlarged or rewritten.
    later = ROOT / "src/archive/pre-redevelopment-2026-11-21/dossier-2.1.6.html"
    original = later.read_bytes()
    assert blob_sha(original) == "eb45bb6ac0de1827cbf812bcc0f223c20ce3ed81", (
        "2.1.6 pre-redevelopment snapshot changed"
    )
    html = original.decode("utf-8")
    assert html.startswith('<section class="chapter" id="ch2-1-6"')
    assert html.rstrip().endswith("</section>")
    assert html.count('class="end-block"') == 1
    assert all(title in html for title in REVISION_HEADINGS)
    assert html.count('class="examq-cat"') >= 5
    assert "pre-redevelopment-2026-11-21" not in (
        ROOT / "src/main.html"
    ).read_text(encoding="utf-8")
    original_217 = ROOT / "src/archive/pre-redevelopment-2026-11-21/dossier-2.1.7.html"
    archived_217 = original_217.read_bytes()
    assert blob_sha(archived_217) == "10d7b05acc14bcd58eb130abedead2b1930c2f55", (
        "2.1.7 original Arabic dossier snapshot changed"
    )
    old_217 = archived_217.decode("utf-8")
    assert old_217.startswith('<section class="chapter rtl" id="ch2-1-7" lang="ar"')
    assert old_217.endswith("</section>")
    assert old_217.count('class="end-block"') == 1
    assert old_217.count('class="examq-cat"') == 5
    assert old_217.count('class="endh"') == 6
    assert "pre-redevelopment-2026-11-21" not in (
        ROOT / "src/main.html"
    ).read_text(encoding="utf-8")
    original_218 = ROOT / "src/archive/pre-redevelopment-2026-11-21/dossier-2.1.8.html"
    archived_218 = original_218.read_bytes()
    assert blob_sha(archived_218) == "375b0d2733a27470c713bce7ef8554a9ae30dfd1", (
        "2.1.8 original Arabic Plato dossier snapshot changed"
    )
    old_218 = archived_218.decode("utf-8")
    assert old_218.startswith('<section class="chapter rtl" id="ch2-1-8" lang="ar"')
    assert old_218.endswith("</section>")
    assert old_218.count('class="end-block"') == 1
    assert old_218.count('class="examq-cat"') == 5
    assert old_218.count('class="endh"') == 6
    original_221 = ROOT / "src/archive/pre-redevelopment-2026-11-21/dossier-2.2.1.html"
    archived_221 = original_221.read_bytes()
    assert blob_sha(archived_221) == "7db0c56b5cb7ff363c7fa95f8b43517f7acc9c8d", (
        "Original Arabic metaphysics dossier 2.2.1 changed"
    )
    old_221 = archived_221.decode("utf-8")
    assert old_221.startswith('<section class="chapter rtl" id="ch2-2-1" lang="ar"')
    assert old_221.endswith("</section>")
    assert old_221.count('class="end-block"') == 1
    assert old_221.count('class="endh"') == 6
    assert old_221.count('class="examq-cat"') == 5
    assert "pre-redevelopment-2026-11-21" not in (ROOT / "src/main.html").read_text(encoding="utf-8")
    original_222 = ROOT / "src/archive/pre-redevelopment-2026-11-21/dossier-2.2.2.html"
    archived_222 = original_222.read_bytes()
    assert blob_sha(archived_222) == "7378c12e696cfa253328f9d44669fe046e62b135", (
        "Arabic metaphysics 2.2.2 original snapshot changed"
    )
    old_222 = archived_222.decode("utf-8")
    assert old_222.startswith('<section class="chapter rtl" id="ch2-2-2" lang="ar" style="--hue:128;"')
    assert old_222.endswith("</section>")
    assert old_222.count('class="end-block"') == 1
    assert old_222.count('class="endh"') == 6
    assert old_222.count('class="examq-cat"') == 5
    assert "pre-redevelopment-2026-11-21" not in (ROOT / "src/main.html").read_text(encoding="utf-8")
    original_223 = ROOT / "src/archive/pre-redevelopment-2026-11-21/dossier-2.2.3.html"
    archived_223 = original_223.read_bytes()
    assert blob_sha(archived_223) == "6d9a061553530b847235215d99f579fcf2740285", (
        "Original 2.2.3 Arabic Islam/Christian metaphysics snapshot changed"
    )
    old_223 = archived_223.decode("utf-8")
    assert old_223.startswith('<section class="chapter rtl" id="ch2-2-3" lang="ar" style="--hue:148;"')
    assert old_223.endswith("</section>")
    assert old_223.count('class="end-block"') == 1
    assert old_223.count('class="endh"') == 6
    assert old_223.count('class="examq-cat"') == 5
    assert "pre-redevelopment-2026-11-21" not in (ROOT / "src/main.html").read_text(encoding="utf-8")
    print("PASS: ten originals plus all protected 2.1.6–2.1.8 and 2.2.1–2.2.3 complete editions")


if __name__ == "__main__":
    verify()
