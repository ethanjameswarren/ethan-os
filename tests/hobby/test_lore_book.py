"""Tests for the modular lore-book publication system."""
from __future__ import annotations

import shutil
import struct
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "hobby"))

from lore_book.css import base_css
from lore_book.html_renderer import render_html
from lore_book.publication import (
    Chapter,
    TrimConfig,
    _extract_outline_sections,
    assemble_book,
    load_project,
)
from lore_book.themes import build_page_rules, build_theme_classes, css_id
from lore_book.validator import validate


class TestThemes(unittest.TestCase):
    def test_named_page_rules_and_classes(self):
        config = TrimConfig(width=6.0, height=9.0, margins=[0.6, 0.5, 0.6, 0.5], bleed=0.0)
        css = build_page_rules({"cyan", "red"}, {"cyan": None, "red": "assets/red-bg.png"}, config)
        self.assertIn("@page cyan", css)
        self.assertIn("@page red", css)
        self.assertIn("background-image: none", css)
        self.assertIn("background-image: url(assets/red-bg.png)", css)
        classes = build_theme_classes({"cyan", "red"})
        self.assertIn(".page-theme-cyan { page: cyan; }", classes)
        self.assertIn(".page-theme-red { page: red; }", classes)

    def test_css_id_sanitizes(self):
        self.assertEqual(css_id("red-13!"), "red-13-")


class TestHtmlRenderer(unittest.TestCase):
    def _make_book(self, chapters):
        return type("Book", (), {
            "title": "Test Book",
            "subtitle": "",
            "edition_year": 2026,
            "status": "draft",
            "generated_date": "2026-09-04",
            "config": TrimConfig(),
            "heraldry_src": None,
            "visual_gaps": [],
            "front_matter": ["cover", "title", "toc", "body"],
            "chapters": chapters,
            "assets_dir": Path("assets"),
            "project_dir": Path("."),
            "default_theme": "cyan",
            "theme_backgrounds": {"cyan": None, "red": "assets/red-bg.png"},
        })

    def test_named_pages_via_classes(self):
        ch = Chapter(
            number="13",
            title="Destroyer Curse",
            status_note="developing",
            theme="red",
            layout="editorial-profile",
            lore_entries=[{"id": "lore-1", "title": "Destroyer Lore", "content": "Red eyes glow."}],
            presentation_media=[],
            other_media=[],
            background_url="assets/red-bg.png",
        )
        book = self._make_book([ch])
        html, _ = render_html(book)
        self.assertNotIn('style="page:', html)
        self.assertIn('class="lore-section page-theme-red theme-red layout-editorial-profile', html)
        self.assertIn("@page red", html)
        self.assertIn("background-image: url(assets/red-bg.png)", html)

    def test_front_matter_deduplication(self):
        ch = Chapter(
            number="5",
            title="Body Section",
            status_note="ok",
            theme="cyan",
            layout="text",
            lore_entries=[{"id": "lore-1", "title": "T", "content": "C"}],
            presentation_media=[],
            other_media=[],
            background_url=None,
        )
        book = self._make_book([ch])
        html, _ = render_html(book)
        self.assertIn('<section class="cover', html)
        self.assertIn('<section class="title-page', html)
        self.assertIn('<section class="toc', html)
        self.assertIn('<section class="lore-section', html)
        # cover/title/toc should not also appear as numbered lore sections
        self.assertNotRegex(html, r'<h2>\s*1\.\s*Cover</h2>')
        self.assertNotRegex(html, r'<h2>\s*2\.\s*Title')


class TestValidator(unittest.TestCase):
    def _write_fake_png(self, path: Path, width: int, height: int) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")
            f.write(b"\x00\x00\x00\x0dIHDR")
            f.write(struct.pack(">II", width, height))
            f.write(b"\x08\x02\x00\x00\x00")  # bit depth, color type, etc.
            f.write(b"\x00\x00\x00\x00")  # placeholder CRC

    def test_aspect_ratio_mismatch(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            assets_dir = tmp / "test_assets"
            self._write_fake_png(assets_dir / "bad-bg.png", 1000, 1000)
            book = type("Book", (), {
                "config": TrimConfig(),
                "assets_dir": assets_dir,
                "project_dir": Path("."),
                "theme_backgrounds": {"red": "assets/bad-bg.png"},
                "chapters": [],
            })
            errors = validate(book)
            self.assertTrue(any("aspect ratio" in e for e in errors))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestPublication(unittest.TestCase):
    def test_outline_extraction(self):
        text = "  5. Origins — developing.  6. History — TBD."
        items = _extract_outline_sections(text)
        self.assertEqual(items, [("5", "Origins", "developing."), ("6", "History", "TBD.")])

    def test_life_data_loads_and_assembles(self):
        life = ROOT.parent / "ethan-life"
        if not life.exists():
            self.skipTest("ethan-life not present")
        edition, outline, lore, media, section_map = load_project(life, edition_year=2026)
        self.assertEqual(edition.get("default_visual_theme"), "cyan")
        self.assertIn("red", edition.get("visual_themes", {}))
        book = assemble_book(
            edition, outline, lore, media, section_map,
            life / "domains" / "hobby" / "warhammer-40k-necron-dynasty",
            life / "reports" / "hobby" / "warhammer-40k-necron-dynasty" / "lore-book" / "2026" / "assets",
        )
        numbers = [ch.number for ch in book.chapters]
        self.assertNotIn("1", numbers)
        self.assertNotIn("2", numbers)
        self.assertNotIn("3", numbers)
        self.assertNotIn("4", numbers)
        self.assertIn("13", numbers)
        red = next((ch for ch in book.chapters if ch.number == "13"), None)
        self.assertIsNotNone(red)
        self.assertEqual(red.theme, "red")


if __name__ == "__main__":
    unittest.main()
