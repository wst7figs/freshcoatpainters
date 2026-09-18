"""Rebrand mirrored site: Hugo Builders -> BL Renovations.

Rules:
- Do not change layout structures.
- Swap red accent colors -> #001B3D across every CSS/HTML file.
- Swap business name in text nodes, titles, meta, alt.
- Remove GAF/BBB badge images.
- Remove /service-area/ nav link (whole section pages removed separately).
- Replace hero logo <img> with text 'BL RENOVATIONS' styled to match.
- Update location references Columbus, Ohio -> Pretoria, South Africa.
"""
from __future__ import annotations
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).parent / "site"

# Color swaps: original reds -> navy
COLOR_MAP = {
    "#c8102e": "#001B3D",
    "#C8102E": "#001B3D",
    "#a00d24": "#001229",
    "#A00D24": "#001229",
    "#b71c1c": "#001229",
    "#B71C1C": "#001229",
    "#ef5350": "#1a3a66",
    "#EF5350": "#1a3a66",
}

# Text swaps (business + location)
TEXT_SWAPS = [
    ("Hugo Builders LLC", "BL Renovations"),
    ("Hugo Builders", "BL Renovations"),
    ("HUGO BUILDERS", "BL RENOVATIONS"),
    ("hugobuildersllc.com", "blrenovations.co.za"),
    ("hugobuilders", "blrenovations"),
    ("Columbus, Ohio", "Pretoria, South Africa"),
    ("Columbus Ohio", "Pretoria, South Africa"),
    ("Columbus, OH", "Pretoria, South Africa"),
    ("Central Ohio", "Pretoria, South Africa"),
    ("Columbus", "Pretoria"),
    ("Ohio", "South Africa"),
    ("Roofing, Gutters & Siding", "Painting, Waterproofing, Tiling & More"),
    ("Roofing, Siding & Gutters", "Painting, Waterproofing, Tiling & More"),
    ("Roofing • Siding • Gutters", "Renovations • Painting • Waterproofing"),
]

# --- CSS pass ---
def swap_colors_in_text(text: str) -> str:
    for old, new in COLOR_MAP.items():
        text = text.replace(old, new)
    return text

for css in ROOT.rglob("*.css"):
    t = css.read_text(encoding="utf-8", errors="ignore")
    new = swap_colors_in_text(t)
    if new != t:
        css.write_text(new, encoding="utf-8")
        print(f"css swapped: {css.relative_to(ROOT)}")

# --- HTML pass ---
def swap_text_in_html(html: str) -> str:
    # Handle style attributes / <style> blocks
    html = swap_colors_in_text(html)
    for old, new in TEXT_SWAPS:
        html = html.replace(old, new)
    return html

BADGE_HINTS = ("gaf-certified", "black-seal", "bbb", "GAF", "Better Business Bureau")

for html_path in ROOT.rglob("*.html"):
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(text, "html.parser")

    # Remove badge images by src/alt hint
    for img in soup.find_all("img"):
        s = (img.get("src", "") + " " + img.get("alt", "")).lower()
        if any(h.lower() in s for h in BADGE_HINTS):
            # Remove nearest parent that looks like a badge wrapper (li, div, a)
            parent = img.find_parent(["li", "figure", "a"]) or img
            parent.decompose()

    # Remove service-area nav links
    for a in soup.find_all("a", href=True):
        if "service-area" in a["href"]:
            li = a.find_parent("li")
            (li or a).decompose()

    # Hero: replace HUGO BUILDERS logo image with text
    for img in soup.find_all("img"):
        alt = (img.get("alt", "") + " " + img.get("src", "")).lower()
        if "hugo" in alt and img.get("src", "").endswith((".png", ".svg", ".jpg", ".jpeg", ".webp")):
            # Only for the large hero logo (heuristic: alt contains hugo builders)
            if "removebg" in img.get("src", "") or "logo" in alt or "hugo builders" in alt:
                span = soup.new_tag("span")
                span["class"] = img.get("class", []) + ["bl-hero-name"]
                span.string = "BL RENOVATIONS"
                img.replace_with(span)

    # Serialize + text swaps as raw
    out = str(soup)
    out = swap_text_in_html(out)
    html_path.write_text(out, encoding="utf-8")
    print(f"html rebranded: {html_path.relative_to(ROOT)}")

# Append hero styling to the font override CSS
override = ROOT / "assets" / "font-override.css"
extra = """
/* BL Renovations rebrand */
.bl-hero-name {
  display: inline-block;
  font-family: "Barlow Condensed", sans-serif !important;
  font-weight: 800;
  font-size: clamp(3rem, 8vw, 6rem);
  letter-spacing: 0.02em;
  color: #FFFFFF;
  text-transform: uppercase;
  line-height: 1;
  text-shadow: 0 4px 24px rgba(0,0,0,0.35);
}
"""
if "bl-hero-name" not in override.read_text(encoding="utf-8"):
    with override.open("a", encoding="utf-8") as f:
        f.write(extra)
    print("appended hero styles to font-override.css")

print("done")
