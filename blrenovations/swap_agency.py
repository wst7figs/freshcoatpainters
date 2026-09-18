"""Swap SiteRabbits → JI Media in every page (footer credit, links, mark image)."""
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent / "site"

JI_URL = "https://jimedia.co.za"  # placeholder — swap if user gives real URL

for html_path in ROOT.rglob("*.html"):
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(text, "html.parser")

    # Remove the siterabbits mark image entirely
    for img in soup.find_all("img"):
        if "siterabbits" in (img.get("src", "") + img.get("alt", "")).lower():
            img.decompose()

    # Rewrite any anchor pointing to siterabbits.com
    for a in soup.find_all("a", href=True):
        if "siterabbits.com" in a["href"].lower():
            a["href"] = JI_URL
            if a.string and "siterabbits" in a.string.lower():
                a.string.replace_with("JI Media")

    out = str(soup)

    # Case-insensitive text swap for any remaining loose references
    out = out.replace("SiteRabbits", "JI Media")
    out = out.replace("siterabbits", "jimedia")
    out = out.replace("SITERABBITS", "JI MEDIA")

    html_path.write_text(out, encoding="utf-8")
    print(f"swapped {html_path.relative_to(ROOT)}")

print("done")
