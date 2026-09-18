"""Fix root-relative asset/link paths across every page.

Root cause: the original mirror script wrote paths relative to the SITE
ROOT (e.g. "assets/style.css", "about/index.html") into every page,
without adjusting for how deep that page sits in the folder tree. That
works fine for the top-level index.html, but on any nested page
(about/, contact/, financing/, services/) those same paths resolve to
the WRONG location (e.g. /about/assets/style.css, which 404s) — causing
missing CSS/JS and broken internal links.

Fix: for every HTML file, normalize each href/src (and data-full/
data-src) attribute by stripping any existing "../" prefix to recover
the intended site-root-relative path, then re-prepend the correct
number of "../" for that file's actual depth.
"""
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent / "site"

ATTR_TAGS = [
    ("link", "href"),
    ("script", "src"),
    ("img", "src"),
    ("img", "data-full"),
    ("img", "data-src"),
    ("a", "href"),
    ("form", "action"),
    ("source", "src"),
    ("video", "src"),
    ("video", "poster"),
]

SKIP_PREFIXES = ("http://", "https://", "//", "mailto:", "tel:", "javascript:", "data:", "#")


def normalize_and_fix(value: str, depth: int) -> str | None:
    if not value or value.startswith(SKIP_PREFIXES):
        return None
    # strip any existing leading "../" segments to recover the root-relative path
    root_relative = value
    while root_relative.startswith("../"):
        root_relative = root_relative[3:]
    # also handle a bare "./"
    if root_relative.startswith("./"):
        root_relative = root_relative[2:]
    fixed = ("../" * depth) + root_relative
    if fixed == value:
        return None
    return fixed


changed_files = 0
changed_attrs = 0

for html_path in ROOT.rglob("*.html"):
    depth = len(html_path.relative_to(ROOT).parts) - 1
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(text, "html.parser")
    file_changed = False

    for tag_name, attr in ATTR_TAGS:
        for tag in soup.find_all(tag_name):
            if not tag.has_attr(attr):
                continue
            new_val = normalize_and_fix(tag[attr], depth)
            if new_val is not None:
                tag[attr] = new_val
                file_changed = True
                changed_attrs += 1

    # also fix srcset-style attributes (comma-separated "url descriptor" pairs)
    for tag in soup.find_all(["img", "source"]):
        for attr in ("srcset", "data-srcset"):
            if not tag.has_attr(attr):
                continue
            parts = []
            any_changed = False
            for chunk in tag[attr].split(","):
                chunk = chunk.strip()
                if not chunk:
                    continue
                bits = chunk.split(None, 1)
                url = bits[0]
                rest = (" " + bits[1]) if len(bits) > 1 else ""
                new_url = normalize_and_fix(url, depth)
                if new_url is not None:
                    any_changed = True
                    parts.append(new_url + rest)
                else:
                    parts.append(chunk)
            if any_changed:
                tag[attr] = ", ".join(parts)
                file_changed = True
                changed_attrs += 1

    if file_changed:
        html_path.write_text(str(soup), encoding="utf-8")
        changed_files += 1
        print(f"fixed {html_path.relative_to(ROOT)} (depth {depth})")

print(f"\nDone. {changed_files} files changed, {changed_attrs} attributes fixed.")
