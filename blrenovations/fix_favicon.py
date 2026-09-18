"""Replace the old Hugo Builders favicon links with the real BL Renovations logo."""
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent / "site"
OLD_ICON = "FA8B98E4-382D-411C-ACAA-11436CCCEE20-removebg-preview_7a1032c1.png"

for html_path in ROOT.rglob("*.html"):
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    if OLD_ICON not in text:
        continue

    soup = BeautifulSoup(text, "html.parser")
    depth = len(html_path.relative_to(ROOT).parts) - 1
    prefix = "../" * depth

    for link in soup.find_all("link", href=True):
        if OLD_ICON not in link["href"]:
            continue
        rel = link.get("rel", [])
        if "shortcut icon" in rel or rel == ["shortcut", "icon"]:
            link["href"] = f"{prefix}assets/favicon-32x32.png"
        elif "apple-touch-icon" in rel:
            link["href"] = f"{prefix}assets/apple-touch-icon.png"
        elif "icon" in rel:
            link["href"] = f"{prefix}assets/favicon-32x32.png"

    html_path.write_text(str(soup), encoding="utf-8")
    print(f"fixed {html_path.relative_to(ROOT)}")

print("done")
