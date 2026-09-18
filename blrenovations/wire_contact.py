"""Wire in the user's confirmed brand assets: logo image, phone, email.

Only touches:
  - <a class="header__logo"> content -> logo <img>
  - <a class="footer__logo-link"> content -> logo <img>
  - tel: links -> new phone
  - email links (Cloudflare-obfuscated span or plain mailto:) -> new email
  - visible phone/email text nodes matching known old values

Body copy is not touched.
"""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import re

ROOT = Path(__file__).parent / "site"

PHONE_NEW = "+27 74 415 7569"
PHONE_TEL = "+27744157569"
EMAIL_NEW = "Renovationsbl6@gmail.com"

OLD_PHONE_PATTERNS = [
    re.compile(r"\(614\)\s*673-4649"),
    re.compile(r"tel:\+16146734649"),
    re.compile(r"6146734649"),
]

for html_path in ROOT.rglob("*.html"):
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(text, "html.parser")

    depth = len(html_path.relative_to(ROOT).parts) - 1
    prefix = "../" * depth
    logo_src = f"{prefix}assets/bl-logo.png"

    # 1) Header logo: replace inner content with <img>
    for a in soup.select("a.header__logo"):
        a.clear()
        img = soup.new_tag("img", src=logo_src, alt="BL Renovations")
        img["class"] = ["header__logo-img"]
        img["style"] = "height:48px;width:auto;display:block"
        a.append(img)

    # 2) Footer brand logo: replace inner content with <img>
    for a in soup.select("a.footer__logo-link"):
        a.clear()
        img = soup.new_tag("img", src=logo_src, alt="BL Renovations")
        img["class"] = ["footer__logo-img"]
        img["style"] = "height:56px;width:auto;display:block"
        a.append(img)

    # 3) Phone: rewrite tel: hrefs and visible number
    for a in soup.find_all("a", href=True):
        if a["href"].startswith("tel:"):
            a["href"] = f"tel:{PHONE_TEL}"
            # replace visible text if it looks like a phone
            if a.string and re.search(r"\d", a.string):
                a.string.replace_with(PHONE_NEW)

    # 4) Email: replace Cloudflare-obfuscated spans and mailto:
    for span in soup.select("span.__cf_email__"):
        # Replace the span (and remove data-cfemail attribute) with plain text
        parent_a = span.find_parent("a")
        span.string = EMAIL_NEW
        if "data-cfemail" in span.attrs:
            del span.attrs["data-cfemail"]
        if parent_a is not None:
            parent_a["href"] = f"mailto:{EMAIL_NEW}"
    for a in soup.find_all("a", href=True):
        if a["href"].startswith("mailto:"):
            a["href"] = f"mailto:{EMAIL_NEW}"
        # Some obfuscated emails linked to cdn-cgi/l/email-protection
        if "email-protection" in a["href"]:
            a["href"] = f"mailto:{EMAIL_NEW}"

    # 5) Text-level cleanups for any raw old phone strings left in HTML text nodes
    out = str(soup)
    for pat in OLD_PHONE_PATTERNS:
        out = pat.sub(PHONE_NEW if "tel" not in pat.pattern else f"tel:{PHONE_TEL}", out)

    html_path.write_text(out, encoding="utf-8")
    print(f"wired {html_path.relative_to(ROOT)}")

print("done")
