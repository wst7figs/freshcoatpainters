"""Mirror a site the user owns to a local static folder.

Downloads HTML pages linked from the homepage (same origin only), plus every
referenced asset (img/css/js/font/video), and rewrites URLs to relative paths
so the copy can be hosted anywhere.
"""
from __future__ import annotations

import os
import re
import sys
import hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag, unquote

import requests
from bs4 import BeautifulSoup

START = "https://hugobuildersllc.com/"
OUT = Path(__file__).parent / "site"
OUT.mkdir(exist_ok=True)
(OUT / "assets").mkdir(exist_ok=True)

ORIGIN = urlparse(START).netloc
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

session = requests.Session()
session.headers.update(UA)

page_queue: list[str] = []
seen_pages: set[str] = set()
asset_map: dict[str, str] = {}  # abs_url -> local relative path from OUT root
page_map: dict[str, str] = {}   # abs_url -> local filename


def norm_url(base: str, ref: str) -> str | None:
    if not ref:
        return None
    ref = ref.strip()
    if ref.startswith(("data:", "mailto:", "tel:", "javascript:", "#")):
        return None
    absu, _ = urldefrag(urljoin(base, ref))
    return absu


def is_same_origin(u: str) -> bool:
    return urlparse(u).netloc == ORIGIN


def page_filename(u: str) -> str:
    p = urlparse(u)
    path = p.path
    if path in ("", "/"):
        return "index.html"
    path = path.strip("/")
    if path.endswith("/"):
        path += "index.html"
    elif not re.search(r"\.[a-zA-Z0-9]{2,5}$", path):
        path += "/index.html"
    if p.query:
        path += "__" + hashlib.md5(p.query.encode()).hexdigest()[:6] + ".html"
    return path


def asset_filename(u: str) -> str:
    p = urlparse(u)
    name = os.path.basename(unquote(p.path)) or "asset"
    stem, ext = os.path.splitext(name)
    if not ext:
        ext = ".bin"
    h = hashlib.md5((u).encode()).hexdigest()[:8]
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", stem)[:60]
    return f"assets/{safe}_{h}{ext}"


def fetch(u: str) -> requests.Response | None:
    try:
        r = session.get(u, timeout=30, allow_redirects=True)
        if r.status_code >= 400:
            print(f"  [{r.status_code}] {u}")
            return None
        return r
    except Exception as e:
        print(f"  [ERR] {u}: {e}")
        return None


def save_asset(abs_url: str) -> str | None:
    if not abs_url or abs_url.startswith("data:"):
        return None
    if abs_url in asset_map:
        return asset_map[abs_url]
    r = fetch(abs_url)
    if not r:
        return None
    rel = asset_filename(abs_url)
    out_path = OUT / rel
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(r.content)
    asset_map[abs_url] = rel
    print(f"  asset -> {rel}  ({len(r.content)} B)")
    # If CSS, rewrite url() inside it and re-fetch its refs
    ctype = r.headers.get("content-type", "").lower()
    if rel.endswith(".css") or "text/css" in ctype:
        rewrite_css(out_path, abs_url)
    return rel


CSS_URL_RE = re.compile(r"""url\(\s*(?:'([^']*)'|"([^"]*)"|([^)\s]+))\s*\)""")
CSS_IMPORT_RE = re.compile(r"""@import\s+(?:url\()?\s*(?:'([^']*)'|"([^"]*)"|([^)\s;]+))\s*\)?""")


def rewrite_css(path: Path, base_url: str) -> None:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return

    # css lives in assets/, so relative paths back to other assets are just filenames within assets/
    def repl_url(m: re.Match) -> str:
        ref = m.group(1) or m.group(2) or m.group(3)
        absu = norm_url(base_url, ref)
        if not absu or absu.startswith("data:"):
            return m.group(0)
        local = save_asset(absu)
        if not local:
            return m.group(0)
        # Path from the css file (inside assets/) to the asset (also inside assets/)
        rel_from_css = os.path.relpath(str(OUT / local), start=str(path.parent)).replace("\\", "/")
        return f"url('{rel_from_css}')"

    def repl_import(m: re.Match) -> str:
        ref = m.group(1) or m.group(2) or m.group(3)
        absu = norm_url(base_url, ref)
        if not absu:
            return m.group(0)
        local = save_asset(absu)
        if not local:
            return m.group(0)
        rel_from_css = os.path.relpath(str(OUT / local), start=str(path.parent)).replace("\\", "/")
        return f"@import url('{rel_from_css}')"

    text = CSS_URL_RE.sub(repl_url, text)
    text = CSS_IMPORT_RE.sub(repl_import, text)
    path.write_text(text, encoding="utf-8")


ASSET_ATTRS = {
    "img": ["src", "data-src", "data-lazy-src", "srcset", "data-srcset"],
    "source": ["src", "srcset"],
    "video": ["src", "poster"],
    "audio": ["src"],
    "script": ["src"],
    "link": ["href"],
    "iframe": ["src"],
    "embed": ["src"],
    "object": ["data"],
    "use": ["href", "xlink:href"],
}


def process_srcset(value: str, base: str) -> str:
    parts = []
    for chunk in value.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        bits = chunk.split(None, 1)
        u = bits[0]
        rest = " " + bits[1] if len(bits) > 1 else ""
        absu = norm_url(base, u)
        if absu:
            local = save_asset(absu)
            if local:
                parts.append(local + rest)
                continue
        parts.append(chunk)
    return ", ".join(parts)


def process_page(url: str) -> None:
    if url in seen_pages:
        return
    seen_pages.add(url)
    print(f"PAGE {url}")
    r = fetch(url)
    if not r or "text/html" not in r.headers.get("content-type", "").lower():
        return

    soup = BeautifulSoup(r.text, "html.parser")

    # Assets
    for tag_name, attrs in ASSET_ATTRS.items():
        for tag in soup.find_all(tag_name):
            for attr in attrs:
                if not tag.has_attr(attr):
                    continue
                val = tag[attr]
                if attr in ("srcset", "data-srcset"):
                    tag[attr] = process_srcset(val, url)
                    continue
                absu = norm_url(url, val)
                if not absu:
                    continue
                # link[rel=stylesheet], scripts, images, fonts, icons -> download
                rel_types = tag.get("rel", []) if tag_name == "link" else []
                is_style = tag_name == "link" and any(x in ("stylesheet",) for x in rel_types)
                is_icon = tag_name == "link" and any("icon" in x for x in rel_types)
                is_preload = tag_name == "link" and "preload" in rel_types
                if tag_name in ("img", "script", "source", "video", "audio", "iframe", "embed", "object", "use") or is_style or is_icon or is_preload:
                    local = save_asset(absu)
                    if local:
                        tag[attr] = local
                elif tag_name == "link":
                    # canonical, alternate etc -> just leave or rewrite if internal page
                    if is_same_origin(absu) and tag.get("rel") and any(x in ("canonical",) for x in tag.get("rel", [])):
                        tag[attr] = page_filename(absu)

    # inline style url()
    for tag in soup.find_all(style=True):
        style_val = tag["style"]

        def repl(m: re.Match) -> str:
            ref = m.group(1) or m.group(2) or m.group(3)
            absu = norm_url(url, ref)
            if not absu or absu.startswith("data:"):
                return m.group(0)
            local = save_asset(absu)
            return f"url('{local}')" if local else m.group(0)

        tag["style"] = CSS_URL_RE.sub(repl, style_val)

    # <style> blocks
    for style in soup.find_all("style"):
        if not style.string:
            continue
        css = style.string

        def repl(m: re.Match) -> str:
            ref = m.group(1) or m.group(2) or m.group(3)
            absu = norm_url(url, ref)
            if not absu or absu.startswith("data:"):
                return m.group(0)
            local = save_asset(absu)
            return f"url('{local}')" if local else m.group(0)

        style.string.replace_with(CSS_URL_RE.sub(repl, css))

    # Rewrite internal anchor links to local page files and enqueue them
    for a in soup.find_all("a", href=True):
        absu = norm_url(url, a["href"])
        if not absu:
            continue
        if is_same_origin(absu):
            # Skip file assets that happened to be hrefs (pdf, jpg, etc.)
            path = urlparse(absu).path.lower()
            if re.search(r"\.(pdf|jpg|jpeg|png|gif|webp|svg|mp4|mp3|zip|doc|docx)$", path):
                local = save_asset(absu)
                if local:
                    a["href"] = local
                continue
            fname = page_filename(absu)
            page_map[absu] = fname
            a["href"] = fname
            if absu not in seen_pages and absu not in page_queue:
                page_queue.append(absu)

    # <form action=...> — leave external, rewrite internal
    for form in soup.find_all("form", action=True):
        absu = norm_url(url, form["action"])
        if absu and is_same_origin(absu):
            form["action"] = page_filename(absu)

    out_name = page_map.get(url) or page_filename(url)
    page_map[url] = out_name
    out_path = OUT / out_name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(str(soup), encoding="utf-8")
    print(f"  -> {out_name}")


def main() -> None:
    page_queue.append(START)
    while page_queue:
        u = page_queue.pop(0)
        process_page(u)
    print(f"\nDone. {len(seen_pages)} pages, {len(asset_map)} assets saved into {OUT}")


if __name__ == "__main__":
    main()
