"""Explicit fixed-page composition using browser-based measurement."""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright

from .css import base_css
from .themes import css_id


@dataclass
class ContentBlock:
    html: str
    region: str = "text"
    block_id: str | None = None
    is_splittable: bool = False


@dataclass
class SectionSpec:
    number: str
    title: str
    status_note: str
    theme: str
    layout: str
    background_url: str | None
    blocks: list[ContentBlock] = field(default_factory=list)


@dataclass
class Page:
    page_number: int
    template: str
    theme: str
    background_url: str | None
    layout_class: str
    section_number: str | None
    section_title: str | None
    is_continuation: bool
    blocks: list[ContentBlock] = field(default_factory=list)


MEASUREMENT_HTML = r"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<style>
__CSS__
</style>
<script>
function waitImages() {
  return Promise.all(Array.from(document.querySelectorAll('img')).map(img => {
    if (img.complete) {
      return img.decode ? img.decode().catch(() => {}) : Promise.resolve();
    }
    return new Promise((resolve) => { img.onload = resolve; img.onerror = resolve; });
  }));
}

function lastContentBottom(parent, safeTop) {
  if (!parent || !parent.lastElementChild) return 0;
  const last = parent.lastElementChild;
  const style = getComputedStyle(last);
  const mb = parseFloat(style.marginBottom) || 0;
  return (last.getBoundingClientRect().bottom + mb) - safeTop;
}

async function measureFill(args) {
  const { template, theme, backgroundUrl, layoutClass, blocks } = args;
  const pageEl = document.getElementById('measure');
  pageEl.className = `book-page template-${template} page-theme-${theme} ${layoutClass || ''}`.trim();
  const bg = pageEl.querySelector('.page-background');
  if (backgroundUrl) {
    bg.style.backgroundImage = `url("${backgroundUrl}")`;
    bg.style.backgroundColor = '';
  } else {
    bg.style.backgroundImage = 'none';
    bg.style.backgroundColor = 'var(--bg)';
  }
  const safe = pageEl.querySelector('.page-safe-area');
  if (template === 'toc') {
    safe.innerHTML = '<ul class="toc region-text"></ul><div class="region-art"></div>';
  } else if (template === 'gallery' || template === 'full-art') {
    safe.innerHTML = '';
  } else {
    safe.innerHTML = '<div class="region-text"></div><div class="region-art"></div>';
  }
  const textRegion = safe.querySelector('.region-text');
  const artRegion = safe.querySelector('.region-art');
  const maxH = safe.clientHeight;
  const safeTop = safe.getBoundingClientRect().top;
  let fitCount = 0;
  let overflowReason = null;
  for (let i = 0; i < blocks.length; i++) {
    const b = blocks[i];
    const wrap = document.createElement('div');
    wrap.innerHTML = b.html;
    let target;
    if (template === 'gallery' || template === 'full-art') {
      target = safe;
    } else if (b.region === 'art') {
      target = artRegion;
    } else {
      target = textRegion;
    }
    const added = [];
    while (wrap.firstChild) {
      const node = wrap.firstChild;
      target.appendChild(node);
      added.push(node);
    }
    await waitImages();
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    await new Promise(resolve => requestAnimationFrame(resolve));
    // force layout synchronisation
    void safe.clientHeight;
    let contentH;
    let textBottom = 0;
    let artBottom = 0;
    if (template === 'gallery' || template === 'full-art') {
      contentH = lastContentBottom(safe, safeTop);
    } else if (template === 'toc') {
      textBottom = lastContentBottom(textRegion, safeTop);
      contentH = textBottom;
    } else {
      textBottom = lastContentBottom(textRegion, safeTop);
      artBottom = lastContentBottom(artRegion, safeTop);
      contentH = Math.max(textBottom, artBottom);
    }
    if (contentH > maxH) {
      if (artBottom > maxH && b.region === 'art') overflowReason = 'art';
      else if (textBottom > maxH) overflowReason = 'text';
      else overflowReason = 'safe';
      added.forEach(n => { try { target.removeChild(n); } catch (e) {} });
      break;
    }
    fitCount++;
  }
  return { fitCount, overflowReason, safeScroll: safe.scrollHeight, safeMax: maxH };
}
</script>
</head><body>
<div id="measure" class="book-page">
  <div class="page-background"></div>
  <div class="page-safe-area"><div class="region-text"></div><div class="region-art"></div></div>
  <div class="page-number"></div>
</div>
</body></html>
"""


def build_measurement_html(css: str) -> str:
    # Theme classes are not required for measurement (colours do not affect box sizes).
    measurement_css = css.replace("__THEME_CLASSES__", "")
    return MEASUREMENT_HTML.replace("__CSS__", measurement_css)


def _split_block(block: ContentBlock) -> tuple[ContentBlock, ContentBlock] | None:
    """Split a paragraph block into two roughly equal halves."""
    m = re.match(r'^(<p[^>]*>)(.*?)(</p>)$', block.html, re.DOTALL)
    if not m:
        return None
    open_tag, text, close_tag = m.groups()
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    if len(sentences) >= 2:
        mid = max(1, len(sentences) // 2)
        first = ' '.join(sentences[:mid])
        second = ' '.join(sentences[mid:])
    else:
        words = text.split()
        mid = len(words) // 2
        if mid == 0:
            return None
        first = ' '.join(words[:mid])
        second = ' '.join(words[mid:])
    return (
        ContentBlock(html=f"{open_tag}{first}{close_tag}", region=block.region, is_splittable=True),
        ContentBlock(html=f"{open_tag}{second}{close_tag}", region=block.region, is_splittable=True),
    )


def _measure_page(page, template: str, theme: str, background_url: str | None, layout_class: str, blocks: list[ContentBlock]) -> tuple[list[ContentBlock], list[ContentBlock], dict[str, Any]]:
    args = {
        "template": css_id(template),
        "theme": css_id(theme),
        "backgroundUrl": background_url,
        "layoutClass": layout_class,
        "blocks": [{"html": b.html, "region": b.region} for b in blocks],
    }
    result = page.evaluate("async (args) => { return await measureFill(args); }", args)
    fit_count = int(result.get("fitCount", 0))
    if fit_count == 0 and blocks and blocks[0].is_splittable:
        split = _split_block(blocks[0])
        if split:
            new_remaining = [split[0], split[1]] + blocks[1:]
            return _measure_page(page, template, theme, background_url, layout_class, new_remaining)
    on_page = blocks[:fit_count]
    remaining = blocks[fit_count:]
    return on_page, remaining, result


def _choose_template(section: SectionSpec, is_first: bool, blocks: list[ContentBlock]) -> tuple[str, str]:
    """Return (template_name, layout_class) for the next page of a section."""
    if not is_first:
        return "continuation", ""
    layout = (section.layout or "text").lower()
    if layout in ("cover", "title", "toc"):
        return layout, ""
    if layout == "chapter-opener":
        return "chapter-opener", ""
    if layout in ("editorial-profile", "editorial_profile"):
        art_blocks = [b for b in blocks if b.region == "art"]
        if art_blocks:
            # Layout class is driven by the first art block's HTML data attribute if present.
            art_html = art_blocks[0].html
            if 'data-layout="bottom-wide"' in art_html:
                return "editorial-profile", "layout-bottom-wide"
            if 'data-layout="dominant"' in art_html:
                return "editorial-profile", "layout-dominant"
            return "editorial-profile", "layout-bottom-right"
    if layout in ("full_bleed_image", "full-art", "fullart"):
        return "full-art", ""
    if layout == "gallery":
        return "gallery", ""
    return "standard-prose", ""


def _paginate_section(page, section: SectionSpec, start_page: int, warnings: list[str]) -> tuple[list[Page], dict[str, int]]:
    """Paginate a single section, starting at start_page, returning pages and section start index."""
    pages: list[Page] = []
    remaining = list(section.blocks)
    is_first = True
    current_page = start_page
    while remaining:
        template, layout_class = _choose_template(section, is_first, remaining)
        # For editorial profile first page, keep art blocks on first page only.
        if template == "editorial-profile" and is_first:
            art_blocks = [b for b in remaining if b.region == "art"]
            text_blocks = [b for b in remaining if b.region != "art"]
            on_text, remaining_text, _ = _measure_page(page, template, section.theme, section.background_url, layout_class, text_blocks)
            on_page = on_text + art_blocks
            remaining = remaining_text
        else:
            on_page, remaining, result = _measure_page(page, template, section.theme, section.background_url, layout_class, remaining)
            if not on_page and remaining:
                # Force the first non-fitting block onto the page and warn.
                warnings.append(f"Section {section.number} forced overflow on page {current_page}: {result.get('overflowReason')}")
                on_page = [remaining[0]]
                remaining = remaining[1:]
        pages.append(Page(
            page_number=current_page,
            template=template,
            theme=section.theme,
            background_url=section.background_url,
            layout_class=layout_class,
            section_number=section.number,
            section_title=section.title,
            is_continuation=not is_first,
            blocks=on_page,
        ))
        is_first = False
        current_page += 1
    return pages


def _paginate_sections(page, sections: list[SectionSpec], start_page: int) -> tuple[list[Page], dict[str, int]]:
    """Paginate a list of sections sequentially."""
    all_pages: list[Page] = []
    section_start: dict[str, int] = {}
    warnings: list[str] = []
    current_page = start_page
    for section in sections:
        section_start[section.number] = len(all_pages)  # 0-based index within this result
        pages = _paginate_section(page, section, current_page, warnings)
        all_pages.extend(pages)
        current_page += len(pages)
    return all_pages, section_start


def _fill_toc(toc_section: SectionSpec, section_start: dict[str, int], front_count: int, body_sections: list[SectionSpec]) -> None:
    """Build TOC list items with section titles and computed page numbers."""
    items: list[str] = []
    for sec in body_sections:
        idx = section_start.get(sec.number, 0)
        page_num = front_count + 1 + idx
        status = sec.status_note.strip().rstrip('.')
        status_attr = f' <span class="status">{status}</span>' if status else ""
        items.append(f'<li><span class="title">{sec.number}. {sec.title}</span>{status_attr}<span class="page-ref">p. {page_num}</span></li>')
    toc_section.blocks = [ContentBlock(html=li, region="text") for li in items]


def _renumber_pages(pages: list[Page]) -> None:
    for i, p in enumerate(pages, start=1):
        p.page_number = i


def compose(
    front_sections: list[SectionSpec],
    body_sections: list[SectionSpec],
    back_sections: list[SectionSpec],
    css: str,
    output_dir: Path,
) -> tuple[list[Page], list[str]]:
    """Compose explicit physical pages with measurement-based pagination."""
    warnings: list[str] = []
    measurement_html = build_measurement_html(css)
    measure_path = output_dir / "_measure.html"
    measure_path.write_text(measurement_html, encoding="utf-8")
    measure_url = measure_path.as_uri()
    pages: list[Page] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(measure_url, wait_until="networkidle", timeout=120000)
        # Give fonts a moment to settle.
        time.sleep(0.2)

        front_count = len(front_sections)
        toc_section: SectionSpec | None = None
        for s in front_sections:
            if s.number == "toc":
                toc_section = s
                break

        for _ in range(5):
            # Body and back sections are laid out independently of absolute page numbers.
            body_and_back = body_sections + back_sections
            body_pages, section_start = _paginate_sections(page, body_and_back, front_count + 1)
            if toc_section is not None:
                _fill_toc(toc_section, section_start, front_count, body_sections)
            front_pages, _ = _paginate_sections(page, front_sections, 1)
            if len(front_pages) == front_count:
                pages = front_pages + body_pages
                break
            front_count = len(front_pages)
        else:
            warnings.append("TOC/front-matter pagination did not converge; using last attempt")
            body_pages, section_start = _paginate_sections(page, body_and_back, front_count + 1)
            if toc_section is not None:
                _fill_toc(toc_section, section_start, front_count, body_sections)
            front_pages, _ = _paginate_sections(page, front_sections, 1)
            pages = front_pages + body_pages

        _renumber_pages(pages)
        browser.close()
    measure_path.unlink(missing_ok=True)
    return pages, warnings
