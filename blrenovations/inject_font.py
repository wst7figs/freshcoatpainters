"""Inject the font-override stylesheet + Google Fonts link into every mirrored HTML page."""
from pathlib import Path
import re

ROOT = Path(__file__).parent / "site"

GOOGLE = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">'

for html_path in ROOT.rglob("*.html"):
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    # depth from this file to site root
    depth = len(html_path.relative_to(ROOT).parts) - 1
    prefix = "../" * depth
    override = f'<link rel="stylesheet" href="{prefix}assets/font-override.css">'
    tag = GOOGLE + override

    if "font-override.css" in text:
        continue

    if "</head>" in text:
        text = text.replace("</head>", tag + "</head>", 1)
    else:
        text = tag + text
    html_path.write_text(text, encoding="utf-8")
    print(f"patched {html_path.relative_to(ROOT)}")

print("done")
