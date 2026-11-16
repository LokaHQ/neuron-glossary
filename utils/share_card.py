#!/usr/bin/env python3
"""Render the committed share card with Chrome or Chromium."""

import argparse
import base64
import html
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build import ASCII_ART, ROOT, SHARE_IMAGE, SHARE_SIZE


# Latin regular font files used by the glossary's existing Google Fonts stylesheet.
FONTS = {
    "PIXELFONT": "https://fonts.gstatic.com/s/silkscreen/v6/m8JXjfVPf62XiF7kO-i9YLNlaw.woff2",
    "MONOFONT": "https://fonts.gstatic.com/s/jetbrainsmono/v24/tDbY2o-flEEny0FZhsfKu5WU4zr3E_BX0PnT8RD8yKxTOlOV.woff2",
}


def render(chrome):
    """Render the source template and replace the committed PNG on success."""
    template = Path(__file__).with_name("share-card.html").read_text(encoding="utf-8")
    ascii_art = Path(ASCII_ART).read_text(encoding="ascii").rstrip()
    page = template.replace("%%ASCIIART%%", html.escape(ascii_art))
    for token, url in FONTS.items():
        with urlopen(url, timeout=15) as response:
            encoded = base64.b64encode(response.read()).decode("ascii")
        page = page.replace(f"%%{token}%%", f"data:font/woff2;base64,{encoded}")

    with TemporaryDirectory(prefix="neuron-share-card-") as directory:
        scratch = Path(directory)
        source = scratch / "card.html"
        source.write_text(page, encoding="utf-8")
        output = scratch / "card.png"
        width, height = SHARE_SIZE
        subprocess.run(
            [
                chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
                f"--user-data-dir={scratch / 'chrome'}", f"--window-size={width},{height}",
                f"--screenshot={output}", source.as_uri(),
            ],
            check=True, timeout=30,
        )
        shutil.copyfile(output, Path(ROOT) / SHARE_IMAGE)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chrome", default=shutil.which("google-chrome") or shutil.which("chromium"))
    args = parser.parse_args()
    if not args.chrome:
        parser.error("Chrome or Chromium is required")
    render(args.chrome)
