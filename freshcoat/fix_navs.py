"""Update nav/footer in all HTML pages to match the new site structure.

Only touches nav dropdowns, footer service lists, and mobile menu accordion.
Body copy is left alone.
"""
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent / "site"

for html_path in ROOT.rglob("*.html"):
    if html_path.name != "index.html" and not html_path.parent.name:
        continue
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(text, "html.parser")

    # depth-adjusted path prefix
    depth = len(html_path.relative_to(ROOT).parts) - 1
    prefix = "../" * depth

    # 1) Header nav: replace .header__dropdown (Services dropdown) with a plain link
    for dropdown in soup.select(".header__dropdown"):
        link = soup.new_tag("a", **{"class": "header__link", "href": f"{prefix}services/index.html"})
        link.string = "Services"
        dropdown.replace_with(link)

    # 2) Mobile menu accordion for services -> plain link
    for accordion in soup.select(".mobile-menu__accordion"):
        link = soup.new_tag("a", **{"class": "mobile-menu__link", "href": f"{prefix}services/index.html"})
        link.string = "Services"
        accordion.replace_with(link)

    # 3) Footer "Services" column: rewrite the list to the 8 new services (all pointing to /services/)
    for footer_col in soup.select(".footer__col"):
        heading = footer_col.find("h4")
        if not heading or "service" not in heading.get_text(strip=True).lower():
            continue
        if "quick" in heading.get_text(strip=True).lower():
            continue
        ul = footer_col.find("ul")
        if not ul:
            continue
        ul.clear()
        for name in [
            "Painting",
            "Waterproofing",
            "Rhinolite Skimming",
            "Paving",
            "Tiling",
            "Flooring",
            "Plumbing",
            "Ceiling & Insulation",
        ]:
            li = soup.new_tag("li")
            a = soup.new_tag("a", **{"class": "footer__link", "href": f"{prefix}services/index.html"})
            a.string = name
            li.append(a)
            ul.append(li)

    # 4) Remove any remaining service-area links (in footer or elsewhere)
    for a in soup.find_all("a", href=True):
        if "service-area" in a["href"]:
            (a.find_parent("li") or a).decompose()

    # 5) Point any stray old service subpage links to /services/
    for a in soup.find_all("a", href=True):
        h = a["href"]
        if "services/roofing" in h or "services/gutters" in h or "services/siding" in h:
            a["href"] = f"{prefix}services/index.html"

    html_path.write_text(str(soup), encoding="utf-8")
    print(f"patched {html_path.relative_to(ROOT)}")

print("done")
