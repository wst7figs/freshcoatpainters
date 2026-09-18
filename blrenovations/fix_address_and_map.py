"""Remove the leftover fake Ohio address (2524 Billingsley Rd) sitewide,
fix the duplicate 'Serving Pretoria & Pretoria' heading on the contact page,
and replace the broken map iframe with a real Google Maps embed of Pretoria.
"""
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent / "site"

PRETORIA_MAPS_EMBED = "https://maps.google.com/maps?q=Pretoria%2C%20South%20Africa&t=&z=11&ie=UTF8&iwloc=&output=embed"
PRETORIA_MAPS_LINK = "https://www.google.com/maps/place/Pretoria,+South+Africa"

for html_path in ROOT.rglob("*.html"):
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    if "Billingsley" not in text and "maps_9dcb4c1d.bin" not in text and "Serving Pretoria &amp; Pretoria" not in text:
        continue

    soup = BeautifulSoup(text, "html.parser")

    # 1) Footer address block: drop the fake street, keep just the city line
    for a in soup.select("a.footer__address"):
        a.clear()
        a.append("Pretoria, South Africa")
        a["href"] = PRETORIA_MAPS_LINK

    # 2) JSON-LD schema: strip the fake street/region/country (leave city only)
    for script in soup.find_all("script", type="application/ld+json"):
        if script.string and "Billingsley" in script.string:
            new_text = script.string.replace(
                '"streetAddress":"2524 Billingsley Rd"', '"streetAddress":""'
            ).replace(
                '"addressRegion":"OH"', '"addressRegion":"Gauteng"'
            ).replace(
                '"addressCountry":"US"', '"addressCountry":"ZA"'
            )
            script.string.replace_with(new_text)

    # 3) Contact page: fix heading + subtitle + map iframe
    for h2 in soup.find_all("h2"):
        if h2.get_text(strip=True) == "Serving Pretoria & Pretoria, South Africa":
            h2.string = "Serving Pretoria, South Africa"

    for p in soup.find_all("p", class_="section__subtitle"):
        if "Billingsley" in p.get_text():
            p.string = "Proudly serving homeowners and businesses across Pretoria."

    for iframe in soup.find_all("iframe"):
        if "maps_9dcb4c1d.bin" in iframe.get("src", ""):
            iframe["src"] = PRETORIA_MAPS_EMBED

    html_path.write_text(str(soup), encoding="utf-8")
    print(f"fixed {html_path.relative_to(ROOT)}")

print("done")
