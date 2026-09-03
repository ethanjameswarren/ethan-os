"""Paged.js PDF renderer wrapper."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PAGEDJS_CLI_VERSION = "0.4.3"


def render_pdf(html_path: Path, pdf_path: Path, timeout: int = 600) -> None:
    """Render HTML to a print-ready PDF using the pinned Paged.js CLI."""
    html_uri = html_path.resolve().as_uri()
    npx_args = [
        "npx",
        "-y",
        f"pagedjs-cli@{PAGEDJS_CLI_VERSION}",
        "--inputs",
        html_uri,
        "--output",
        str(pdf_path),
    ]
    if shutil.which("npx") is None:
        raise RuntimeError("npx is not available. Install Node.js and npm.")
    # On Windows, .CMD files must be launched through the command interpreter
    # so we use `cmd /c` while keeping subprocess shell=False.
    if sys.platform == "win32":
        cmd = ["cmd", "/c", *npx_args]
    else:
        cmd = npx_args
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        msg = (result.stderr or result.stdout or "unknown error").strip()
        raise RuntimeError(f"PDF render failed: {msg}")
    print(f"PDF rendered: {pdf_path}")
