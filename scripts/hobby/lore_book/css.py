"""Print CSS for explicit 6in x 9in physical pages."""
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
    __THEME_CLASSES__
    * { box-sizing: border-box; print-color-adjust: exact; -webkit-print-color-adjust: exact; }
    @page { size: 6in 9in; margin: 0; }
    html, body {
      margin: 0;
      padding: 0;
      background: var(--bg);
      color: var(--fg);
      font-family: Georgia, "Times New Roman", serif;
      font-size: 11pt;
      line-height: 1.55;
    }

    .book-page {
      width: 6in;
      height: 9in;
      position: relative;
      overflow: hidden;
      background: var(--bg);
    }
    .page-background {
      position: absolute;
      inset: 0;
      z-index: 0;
      background-color: var(--bg);
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
    }
    .page-safe-area {
      position: absolute;
      top: 0.6in;
      right: 0.5in;
      bottom: 0.6in;
      left: 0.5in;
      z-index: 1;
      overflow: hidden;
    }
    .page-number {
      position: absolute;
      bottom: 0.3in;
      left: 0;
      right: 0;
      text-align: center;
      z-index: 2;
      font-size: 7pt;
      color: var(--muted);
    }

    .template-cover .page-safe-area,
    .template-title .page-safe-area {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
    }
    .template-cover h1 { font-size: 36pt; margin-bottom: 12mm; text-transform: uppercase; }
    .template-cover .subtitle { font-size: 14pt; color: var(--muted); margin-bottom: 8mm; }
    .template-cover .edition { font-size: 11pt; color: var(--cyan); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 6mm; }
    .template-cover .status { font-size: 9pt; color: var(--muted); }
    .template-cover .cover-heraldry,
    .template-title .cover-heraldry { width: 1.8in; max-height: 2in; margin: 0.3in auto 0 auto; }
    .template-cover .dynasty-logo,
    .template-title .dynasty-logo { display: block; width: 100%; height: 100%; object-fit: contain; border: none; background: transparent; }

    .template-title h1 { font-size: 32pt; margin-bottom: 10mm; text-transform: uppercase; }
    .template-title .subtitle { font-size: 14pt; color: var(--muted); margin-bottom: 8mm; }
    .template-title .edition { font-size: 11pt; color: var(--cyan); text-transform: uppercase; letter-spacing: 0.15em; }
    .template-title .status { font-size: 9pt; color: var(--muted); }

    h1, h2, h3, h4 {
      color: var(--silver);
      font-weight: 400;
      letter-spacing: 0.03em;
      margin-top: 0;
    }
    h1 { font-size: 28pt; text-transform: uppercase; margin-bottom: 6mm; }
    h2 { font-size: 18pt; border-bottom: 1px solid var(--line); padding-bottom: 2mm; margin-bottom: 4mm; }
    h3 { font-size: 13pt; color: var(--silver); margin-bottom: 3mm; margin-top: 6mm; }
    p { margin: 0 0 0.25in 0; orphans: 2; widows: 2; }
    .tbd { color: var(--muted); font-style: italic; }
    .status { font-size: 9pt; color: var(--muted); margin-bottom: 4mm; }
    .provenance { font-size: 8pt; color: var(--muted); margin-top: 2mm; }
    .toc ul { list-style: none; padding: 0; margin: 0; }
    .toc li { display: flex; justify-content: space-between; border-bottom: 1px dotted var(--line); padding: 2mm 0; }
    .toc a { text-decoration: none; color: var(--fg); }
    .toc .page-ref { color: var(--muted); font-size: 9pt; }
    .visual-gaps { width: 100%; border-collapse: collapse; margin-top: 6mm; }
    .visual-gaps th, .visual-gaps td { border-bottom: 1px solid var(--line); padding: 2mm 1mm; text-align: left; }
    .visual-gaps th { color: var(--cyan); font-weight: 400; }
    .priority-required { color: var(--red); }
    .priority-recommended { color: var(--purple); }
    .priority-optional { color: var(--muted); }

    /* continuation header */
    .continuation h2 { border-bottom: none; }
    .continued { font-size: 10pt; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 2mm; }

    /* chapter opener */
    .template-chapter-opener .opener-art { margin-bottom: 6mm; text-align: center; }
    .template-chapter-opener .opener-art img { max-width: 100%; max-height: 45mm; object-fit: contain; border: none; }
    .template-chapter-opener .status { margin-bottom: 6mm; }

    /* full art */
    .template-full-art .page-safe-area { display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .template-full-art figure { width: 100%; text-align: center; }
    .template-full-art img { max-width: 100%; max-height: 6.5in; object-fit: contain; border: none; }

    /* gallery */
    .template-gallery .page-safe-area { display: grid; grid-template-columns: repeat(2, 1fr); grid-auto-rows: auto; gap: 0.15in; }
    .template-gallery figure { margin: 0; text-align: center; }
    .template-gallery img { max-width: 100%; max-height: 2.8in; object-fit: contain; border: 1px solid var(--line); }
    .template-gallery figcaption { font-size: 9pt; color: var(--silver); margin-top: 1mm; }

    /* editorial profile grid */
    .template-editorial-profile .page-safe-area {
      display: grid;
      grid-template-columns: 1fr 2.2in;
      grid-template-rows: 1fr minmax(0, 3in);
      gap: 0.2in;
    }
    .template-editorial-profile .region-text { grid-column: 1; grid-row: 1 / 3; overflow: hidden; }
    .template-editorial-profile .region-art {
      grid-column: 2; grid-row: 2;
      display: flex; align-items: flex-end; justify-content: center;
      padding-bottom: 20px; overflow: hidden;
    }
    .template-editorial-profile .region-art .hero-art { margin: 0; height: 100%; width: 100%; display: flex; align-items: flex-end; justify-content: center; }
    .template-editorial-profile .region-art .hero-art img { width: 100%; height: 100%; object-fit: contain; border: none; background: transparent; }
    .template-editorial-profile .region-art .hero-art figcaption,
    .template-editorial-profile .region-art .hero-art .provenance { display: none; }
    .template-editorial-profile.layout-bottom-wide .page-safe-area {
      grid-template-columns: 1fr;
      grid-template-rows: 1fr minmax(0, 2.5in);
    }
    .template-editorial-profile.layout-bottom-wide .region-text { grid-column: 1; grid-row: 1; }
    .template-editorial-profile.layout-bottom-wide .region-art { grid-column: 1; grid-row: 2; }
    .template-editorial-profile.layout-dominant .page-safe-area {
      grid-template-columns: 1fr;
      grid-template-rows: auto 1fr;
    }
    .template-editorial-profile.layout-dominant .region-text { grid-column: 1; grid-row: 1; overflow: hidden; }
    .template-editorial-profile.layout-dominant .region-art { grid-column: 1; grid-row: 2; align-items: center; justify-content: center; padding-bottom: 0; }

    .profile-subtitle {
      font-size: 9pt; color: var(--muted); text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 4mm;
    }
    .dossier {
      border: 1px solid var(--line); padding: 3mm; font-size: 8pt; margin-bottom: 4mm; break-inside: avoid;
    }
    .dossier dt { color: var(--cyan); text-transform: uppercase; font-size: 6.5pt; letter-spacing: 0.05em; margin-top: 2mm; }
    .dossier dd { margin: 0; color: var(--silver); }
    .pull-quote {
      border-left: 2pt solid var(--cyan); padding: 3mm 3mm 3mm 3mm;
      color: var(--silver); font-size: 12pt; font-style: italic; line-height: 1.35;
      margin: 4mm 0 4mm 0; break-inside: avoid;
    }
    .pull-quote .source { display: block; font-size: 7pt; color: var(--muted); font-style: normal; margin-top: 2mm; }

    .unit-card {
      border-bottom: 1px solid var(--line); padding: 2mm 0; margin-bottom: 2mm;
    }
    .unit-card .unit-name { font-weight: bold; color: var(--silver); }
    .unit-card .unit-meta { font-size: 8pt; color: var(--muted); }

    .media-asset { margin: 4mm 0 4mm 0; text-align: center; break-inside: avoid; }
    .media-asset img { display: block; max-width: 100%; max-height: 4.5in; height: auto; object-fit: contain; border: 1px solid var(--line); margin: 0 auto; }
    .media-asset figcaption { font-size: 9pt; color: var(--silver); margin-top: 1mm; }
    .media-asset .provenance { font-size: 8pt; color: var(--muted); margin-top: 1mm; }

    .theme-cyan .pull-quote { border-left-color: var(--cyan); }
    .theme-cyan .dossier dt { color: var(--cyan); }
    .theme-cyan h2, .theme-cyan h3 { color: var(--cyan); }
    .theme-red .pull-quote { border-left-color: var(--red); }
    .theme-red .dossier dt { color: var(--red); }
    .theme-red h2, .theme-red h3 { color: var(--red); }
    .theme-purple .pull-quote { border-left-color: var(--purple); }
    .theme-purple .dossier dt { color: var(--purple); }
    .theme-purple h2, .theme-purple h3 { color: var(--purple); }
    .theme-cover .page-background { background-color: #050608; }
    .theme-neutral .page-background { background-color: var(--bg); }

    @media (max-width: 600px) {
      .book-page { width: 100%; height: auto; min-height: 9in; }
      .page-safe-area { position: relative; top: auto; right: auto; bottom: auto; left: auto; padding: 0.5in; height: auto; }
      .page-background { position: relative; height: 9in; }
    }
    """
