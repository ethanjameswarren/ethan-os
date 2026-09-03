"""Reusable print CSS for the lore book."""
from __future__ import annotations


def base_css() -> str:
    return r"""
    :root {
      --bg: #0b0c0e;
      --fg: #d8dde6;
      --muted: #8a93a3;
      --cyan: #2dd4bf;
      --red: #ef4444;
      --purple: #a855f7;
      --silver: #c7cdd6;
      --line: #2a2d33;
    }
    __PAGE_RULES__
    __THEME_CLASSES__
    * { box-sizing: border-box; print-color-adjust: exact; -webkit-print-color-adjust: exact; }
    html, body {
      margin: 0;
      padding: 0;
      background: var(--bg);
      color: var(--fg);
      font-family: Georgia, "Times New Roman", serif;
      font-size: 11pt;
      line-height: 1.55;
    }
    h1, h2, h3, h4 {
      color: var(--silver);
      font-weight: 400;
      letter-spacing: 0.03em;
      margin-top: 0;
    }
    h1 { font-size: 28pt; text-transform: uppercase; margin-bottom: 6mm; }
    h2 { font-size: 18pt; border-bottom: 1px solid var(--line); padding-bottom: 2mm; margin-top: 10mm; break-after: avoid; }
    h3 { font-size: 13pt; color: var(--silver); margin-top: 8mm; break-after: avoid; }
    p { orphans: 2; widows: 2; }
    section { break-before: page; display: flow-root; }
    section.cover { break-before: auto; display: flex; }
    section.title-page, section.toc { break-before: page; }
    .lore-section { break-before: page; }
    .cover {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      min-height: 7.8in;
    }
    .cover h1 { font-size: 36pt; margin-bottom: 12mm; }
    .cover .subtitle { font-size: 14pt; color: var(--muted); margin-bottom: 8mm; }
    .cover .edition { font-size: 11pt; color: var(--cyan); text-transform: uppercase; letter-spacing: 0.15em; }
    .title-page { display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; min-height: 7.8in; }
    .title-page h1 { font-size: 32pt; margin-bottom: 10mm; }
    .toc ul { list-style: none; padding: 0; }
    .toc li { display: flex; justify-content: space-between; border-bottom: 1px dotted var(--line); padding: 2mm 0; }
    .toc .status { color: var(--muted); font-size: 9pt; }
    .tbd { color: var(--muted); font-style: italic; }
    .status { font-size: 9pt; color: var(--muted); }
    .visual-gaps { width: 100%; border-collapse: collapse; margin-top: 6mm; }
    .visual-gaps th, .visual-gaps td { border-bottom: 1px solid var(--line); padding: 2mm 1mm; text-align: left; }
    .visual-gaps th { color: var(--cyan); font-weight: 400; }
    .priority-required { color: var(--red); }
    .priority-recommended { color: var(--purple); }
    .priority-optional { color: var(--muted); }
    .provenance { font-size: 8pt; color: var(--muted); margin-top: 4mm; }
    .small-caps { font-variant: small-caps; }
    .media-asset { margin-top: 6mm; text-align: center; break-inside: avoid; }
    .media-asset img { max-width: 100%; max-height: 140mm; border: 1px solid var(--line); }
    .media-asset figcaption { font-size: 10pt; color: var(--silver); margin-top: 2mm; }
    figure.illustration { border: none; background: transparent; }
    figure.illustration img { width: 100%; height: auto; object-fit: contain; border: none; background: transparent; }
    figure.illustration figcaption, figure.illustration .provenance { display: none; }
    .dynasty-logo { display: block; max-width: 100%; height: auto; border: none; background: transparent; }
    .cover-heraldry { width: 1.8in; margin: 0.3in auto 0 auto; }

    /* editorial profiles: text wraps around a bottom-anchored illustration */
    .editorial-profile { display: flow-root; }
    .editorial-profile .profile-subtitle {
      font-size: 9pt;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-top: -4mm;
      margin-bottom: 4mm;
    }
    .editorial-profile figure.hero {
      float: right;
      clear: right;
      position: relative;
      margin: 0 0 0 0.3in;
      border: none;
      background: transparent;
      overflow: hidden;
    }
    .editorial-profile figure.hero img {
      position: absolute;
      bottom: 0;
      right: 0;
      width: 100%;
      height: auto;
      max-height: 45%;
      object-fit: contain;
      border: none;
      background: transparent;
    }
    .editorial-profile figure.hero.hero-standard { width: 2.1in; height: 5.6in; }
    .editorial-profile figure.hero.hero-dominant { width: 2.5in; height: 5.6in; }
    .editorial-profile figure.hero.hero-wide { width: 3.4in; height: 5.6in; }
    .layout-floating-bottom-right .hero { shape-outside: polygon(0% 60%, 100% 60%, 100% 100%, 0% 100%); }
    .layout-floating-bottom-wide .hero { float: left; margin: 0 0 0.2in 0; width: 100%; height: 5.6in; shape-outside: polygon(0% 60%, 100% 60%, 100% 100%, 0% 100%); }
    .layout-floating-bottom-wide .hero img { right: auto; left: 0; width: 100%; max-height: 40%; }

    /* chapter openers and full-art pages */
    .chapter-opener { break-before: right; }
    .chapter-opener .opener-art { break-inside: avoid; margin: 0.2in 0; text-align: center; }
    .chapter-opener .opener-art img { max-width: 100%; max-height: 60mm; }
    .full-art { display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 7.8in; }
    .full-art img { width: 100%; height: auto; object-fit: contain; }
    .facing-spread { break-before: left; page: spread; }
    @page spread { size: 6in 9in; margin: 0; }

    .pull-quote {
      float: left;
      clear: left;
      width: 2.0in;
      margin: 4mm 0.3in 4mm 0;
      padding: 4mm 4mm 4mm 3mm;
      border-left: 2pt solid var(--cyan);
      color: var(--silver);
      font-size: 12pt;
      font-style: italic;
      line-height: 1.35;
      break-inside: avoid;
    }
    .pull-quote .source { display: block; font-size: 7pt; color: var(--muted); font-style: normal; margin-top: 2mm; }
    .dossier {
      float: right;
      clear: right;
      width: 1.9in;
      margin: 4mm 0 4mm 0.3in;
      border: 1px solid var(--line);
      padding: 3mm;
      font-size: 8pt;
      break-inside: avoid;
    }
    .dossier dt { color: var(--cyan); text-transform: uppercase; font-size: 6.5pt; letter-spacing: 0.05em; margin-top: 2mm; }
    .dossier dd { margin: 0; color: var(--silver); }
    .lore-callout { border-left: 1pt solid var(--line); padding-left: 3mm; margin: 4mm 0; color: var(--muted); font-style: italic; }
    .detail-callout { break-inside: avoid; margin: 4mm 0; text-align: center; }
    .detail-callout img { max-width: 100%; max-height: 25mm; border: 1px solid var(--line); }

    .theme-cyan .pull-quote { border-left-color: var(--cyan); }
    .theme-cyan .dossier dt { color: var(--cyan); }
    .theme-cyan h2, .theme-cyan h3 { color: var(--cyan); }
    .theme-red .pull-quote { border-left-color: var(--red); }
    .theme-red .dossier dt { color: var(--red); }
    .theme-red h2, .theme-red h3 { color: var(--red); }
    .theme-purple .pull-quote { border-left-color: var(--purple); }
    .theme-purple .dossier dt { color: var(--purple); }
    .theme-purple h2, .theme-purple h3 { color: var(--purple); }
    @media (max-width: 600px) {
      .editorial-profile figure.hero, .pull-quote, .dossier { float: none; width: 80%; margin: 0.2in auto; }
    }
"""
