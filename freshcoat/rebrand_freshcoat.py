"""Rebrand site: BL Renovations -> FreshCoat Painters (Montana, Pretoria).

Keeps the template layout. Swaps business details, services, copy, colours,
logo and structured data. Removes content that belonged to the previous
business (testimonials, social links/videos, non-painting gallery photos).

Run from anywhere:  python rebrand_freshcoat.py
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = Path(__file__).parent / "site"

NAME = "FreshCoat Painters"
PHONE = "065 313 8150"
PHONE_TEL = "+27653138150"
EMAIL = "abrahammupinga186@gmail.com"
AREA = "Montana, Pretoria"
TAGLINE = "Bringing Walls to Life with Color"
DOMAIN = "https://freshcoatpainters.co.za"  # placeholder until a real domain is confirmed
FORMSPREE_ID = "mvkgzzaq"  # FreshCoat's own Formspree form
WHATSAPP_URL = "https://wa.me/27653138150"
WHATSAPP_SVG = ('<svg viewBox="0 0 24 24" width="38" height="38" fill="currentColor" aria-hidden="true">'
                '<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.71.306 1.263.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>')
MAPS_URL = "https://www.google.com/maps/place/Montana,+Pretoria"
MAPS_EMBED = "https://maps.google.com/maps?q=Montana%2C%20Pretoria&t=&z=13&ie=UTF8&iwloc=&output=embed"

SERVICES = [
    ("Interior & Exterior Painting",
     "Clean, even finishes inside and out, from single rooms to full exteriors.",
     "assets/stock/svc-interior-exterior-thumb.jpg"),
    ("Roof Painting & Coating",
     "Restore faded roofs and protect them from sun and rain with durable coatings.",
     "assets/stock/svc-roof-coating-thumb.jpg"),
    ("Waterproofing & Damp Proofing",
     "Stop leaks and rising damp before they damage your walls and paintwork.",
     "assets/stock/svc-waterproofing-thumb.jpg"),
    ("Custom Colors & Design Touch-Up",
     "Feature walls, colour advice, and detailed touch-ups that finish a space.",
     "assets/stock/svc-custom-colors-thumb.jpg"),
]
# Stock media (Unsplash photos / Mixkit videos, free commercial licences).
# Replace with FreshCoat's own job photos when available.
HERO_VIDEO = "assets/hero-painting.mp4"
HERO_POSTER = "assets/hero-painting-poster.jpg"
SHOWREEL_VIDEO = "assets/showreel-painting.mp4"
SHOWREEL_POSTER = "assets/showreel-painting-poster.jpg"
FONTS_URL = ("https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800"
             "&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&display=swap")
PAGE_HERO_IMAGES = {  # page -> stock photo behind the page title
    "about": "painter-white-wall", "services": "roller-white-wall",
    "contact": "colour-swatches",
}
FOOTER_SERVICES = ["Interior & Exterior Painting", "Roof Painting & Coating",
                   "Waterproofing & Damp Proofing", "Custom Colors & Touch-Ups"]
FORM_OPTIONS = ["Interior Painting", "Exterior Painting", "Roof Painting & Coating",
                "Waterproofing & Damp Proofing", "Custom Colors & Touch-Ups",
                "Multiple Services", "Other"]
# (file in assets/stock, alt text, gallery category)
GALLERY = [
    ("exterior-purple-house", "Painters on ladders finishing a lilac house exterior", "Exterior"),
    ("interior-green-bedroom", "Bedroom with deep green painted walls", "Interior"),
    ("exterior-two-tone-house", "Two-tone painted house with white trim", "Exterior"),
    ("interior-navy-bedroom", "Bedroom with navy blue painted walls", "Interior"),
    ("painter-exterior-wall", "Painter rolling a fresh coat onto an exterior wall", "Exterior"),
    ("interior-feature-wall", "Living room with a painted feature wall", "Interior"),
    ("exterior-blue-house", "Blue painted house with white trim", "Exterior"),
    ("svc-roof-coating", "Roof coating being sprayed onto a flat roof", "Roofs & Waterproofing"),
    ("painter-blue-facade", "Painter on a ladder painting a blue facade", "Exterior"),
    ("svc-waterproofing", "Waterproofing coating applied to a roof", "Roofs & Waterproofing"),
]
HOME_GALLERY = ["exterior-purple-house", "interior-green-bedroom", "exterior-two-tone-house"]

COLOR_MAP = {
    "#f59e0b": "#FBA01B",   # accent (gold -> brand orange)
    "#001b3d": "#0A243D",   # primary navy
    "#001229": "#061A2E",   # primary hover
    "#1a3a66": "#163A5C",
    "#f4f4f4": "#F5F4F5",   # off-white
    "#f5f5f5": "#F5F4F5",
    "#b91c1c": "#F1212D",   # error red -> brand red
    "#161a1e": "#0F2D4A",   # dark cards -> lifted navy
    "rgba(0,27,61,": "rgba(10,36,61,",
    "rgba(0, 27, 61,": "rgba(10, 36, 61,",
    "rgba(0,10,26,": "rgba(6,26,46,",
}

# Ordered: specific phrases first, generic fallbacks last. Applied to text
# nodes and to meta/alt/title/aria-label attributes.
TEXT_SWAPS = [
    # --- titles / meta
    ("BL Renovations | Pretoria, South Africa Roofing, Gutters & Siding",
     f"{NAME} | Painting & Waterproofing in {AREA}"),
    ("BL Renovations, Pretoria, South Africa's trusted roofing, gutter, and siding contractor. Quality craftsmanship, free inspections, and financing available.",
     f"{NAME}: professional interior & exterior painting, roof painting & coating, and waterproofing in {AREA} and surrounding areas. Affordable rates, quality guaranteed."),
    ("Painting, waterproofing, rhinolite skimming, paving, tiling, laminate/vinyl flooring, plumbing, and ceiling & insulation in Pretoria, South Africa.",
     f"Interior & exterior painting, roof painting & coating, waterproofing & damp proofing, and custom colour work in {AREA}."),
    ("About BL Renovations | Pretoria, South Africa Roofing Contractor",
     f"About {NAME} | Painting Contractor in {AREA}"),
    ("BL Renovations is a Pretoria, South Africa roofing, siding, and gutter contractor built on honest communication, fair pricing, and a job done right the first time.",
     f"{NAME} is a professional, reliable painting team in {AREA}, built on honest communication, premium paints, and a job done right the first time."),
    ("Contact BL Renovations | Free Roof Inspections in Pretoria",
     f"Contact {NAME} | Free Painting Quotes in {AREA}"),
    ("Get in touch with BL Renovations. Free inspections, fast quotes, and friendly service for roofing, gutters, and siding in Pretoria, South Africa and surrounding areas. Call +27 74 415 7569.",
     f"Get in touch with {NAME} for a free quote on painting, roof coating and waterproofing in {AREA} and surrounding areas. Call {PHONE}."),
    ("Flexible financing options for your renovation project in Pretoria, South Africa.",
     f"Flexible payment options for your painting project in {AREA}."),

    # --- CTAs
    ("Schedule Free Inspection", "Get a Free Quote"),
    ("Get a Free Inspection", "Get a Free Quote"),
    ("Free Inspections", "Free Quotes"),
    ("Free Inspection", "Free Quote"),
    ("inspection scheduled", "quote scheduled"),

    # --- home
    ("Full-Service Renovations", "Premium Paints"),
    ("Precision. Every Shingle. Every Time.", "Clean Lines. Even Coats. Every Time."),
    ("Watch how our crew transforms your roof from the ground up — with military precision and craftsmanship that speaks for itself.",
     "Watch how our painters transform tired walls and roofs, with careful prep, premium paints, and a finish that lasts."),
    ("Why Pretoria Homeowners Choose BL Renovations", f"Why Montana Homeowners Choose {NAME}"),
    ("GAF Certified Contractor", "Quality Guaranteed"),
    ("Every project is completed with precision, using only premium materials and proven techniques that stand the test of time.",
     "Every job gets thorough prep, clean lines, and premium paints for long-lasting results."),
    ("Complimentary roof inspections to identify issues before they become costly problems. No pressure, no obligation.",
     "We come out, look at the job, and give you a clear, affordable quote. No pressure, no obligation."),
    ("Local Expertise", "Local & Reliable"),
    ("Born and raised in Pretoria. We understand South Africa weather, local building codes, and what your home needs to stay protected all year.",
     "Based in Montana, Pretoria. We know what the Highveld sun, storms and damp do to walls and roofs, and which coatings hold up."),
    ("We offer a full range of renovation and finishing services, including painting, waterproofing and damp proofing, rhinolite skimming, paving installation, tiling, laminate and vinyl flooring, plumbing, and ceiling and insulation work.",
     "We offer interior and exterior painting, roof painting and coating, waterproofing and damp proofing, and custom colours and design touch-ups."),
    ("across Pretoria and the surrounding areas", f"across {AREA} and the surrounding areas"),
    ("a full flooring or waterproofing job", "a full exterior or roof coating job"),
    ("Ready to Protect Your Home?", "Ready for a Fresh Coat?"),
    ("Whether you need a full roof replacement, storm damage repair, or just a free inspection, the BL Renovations team is ready to help. Get a no-obligation quote today.",
     f"Whether it's a single room, a full exterior, or a leaking roof, the {NAME} team is ready to help. Get a free, no-obligation quote today."),
    ("Built to Last. Built by Hugo.", TAGLINE),

    # --- services page
    ("Professional renovation and finishing services throughout Pretoria and surrounding areas.",
     f"Professional painting and waterproofing services throughout {AREA} and surrounding areas."),
    ("Everything Your Space Needs", "Everything Your Walls & Roof Need"),
    ("One trusted team for every stage of your renovation — inside and out.",
     "One trusted team for every coat, inside and out."),
    ("A look at real jobs completed by the BL Renovations team.", "A look at recent painting work."),

    # --- about page
    ("Pretoria, South Africa's trusted contractor for roofing, siding, and gutter services. Built on honesty, quality, and a commitment to protecting your home.",
     f"Professional and reliable painters in {AREA}. {TAGLINE}, and protecting it for years to come."),
    ("Pretoria, South Africa's Trusted Exterior Contractor", f"Professional & Reliable Painters in {AREA}"),
    ("At BL Renovations, we are a Pretoria, South Africa–based exterior construction company proudly serving both residential and commercial clients throughout Pretoria, South Africa. We specialize in roofing, siding, and gutter systems, delivering dependable solutions that protect, restore, and enhance properties of all sizes.",
     f"At {NAME}, we are a {AREA}–based painting company proudly serving both residential and commercial clients in Montana and the surrounding areas. We specialise in interior and exterior painting, roof painting and coating, and waterproofing and damp proofing, delivering finishes that protect, restore, and add value to your property."),
    ("Whether it's a full residential roof replacement, commercial flat roofing system, new siding installation, or seamless gutter upgrade, our team is committed to quality craftsmanship and professional execution. We use trusted materials, proven installation methods, and maintain clear communication from start to finish.",
     "Whether it's a single feature wall, a full interior repaint, a faded exterior, or a roof that needs recoating, our team is committed to careful preparation and professional execution. We use premium paints, proven application methods, and keep clear communication from start to finish."),
    ("For homeowners, we focus on protecting your investment and improving curb appeal. For business owners and property managers, we provide reliable, efficient service that minimizes downtime and ensures long-term performance.",
     "For homeowners, we help transform your space and add value to your home. For business owners and property managers, we provide reliable, efficient service that keeps disruption to a minimum and looks sharp for years."),
    ("Financing Options Available", "Affordable Rates"),
    ("We offer flexible financing options for all credit types, and if qualified, 0% financing for 22 months — making your project affordable and stress-free.",
     "Fair, transparent pricing with quality guaranteed. Premium results without the premium price tag."),
    ("Roofs Completed", "Quality Guaranteed"),
    ("Years Experience", "No-Obligation Quotes"),
    ("Customer Rating", "Long-Lasting Paints"),
    ("We assess your roof's condition with a thorough, no-obligation inspection. Honest findings, no pressure.",
     "We visit, look at the surfaces, and talk through colours and finishes. Honest advice, no pressure."),
    ("Expert Installation", "Prep & Paint"),
    ("Our professional crew handles every detail using premium materials and proven techniques.",
     "We clean, repair, and prime properly, then apply premium paints with clean lines and even coats."),
    ("Schedule your free roof inspection today. No obligation, no pressure — just an honest assessment from a team you can trust.",
     "Book your free quote today. No obligation, no pressure, just honest advice from a team you can trust."),

    # --- financing page
    ("Whether you're investing in painting, flooring, tiling, or a full home renovation,",
     "Whether you're investing in interior painting, a new exterior, or a roof coating,"),

    # --- contact page
    ("Ready to protect your home? Reach out for a free, no obligation inspection.",
     "Ready for a fresh coat? Reach out for a free, no-obligation quote."),
    ("Proudly serving homeowners and businesses across Pretoria.",
     f"Proudly serving homeowners and businesses across {AREA} and surrounding areas."),

    ("(614) 555-1234", "082 123 4567"),
    ("Monday to Saturday: 9 AM to 7 PM", "Monday to Friday: 8 AM to 5 PM"),
    ("Sunday: 12 PM to 7 PM", "Saturday & Sunday: 10 AM to 2 PM"),

    # --- generic fallbacks
    ("BL Renovations", NAME),
    ("BL RENOVATIONS", NAME.upper()),
    ("Pretoria, South Africa", AREA),
    ("+27 74 415 7569", PHONE),
    ("+27744157569", PHONE_TEL),
    ("Renovationsbl6@gmail.com", EMAIL),
]
STAT_VALUES = {"500+": "100%", "15+": "Free", "5★": "Premium"}

ATTRS = ("content", "alt", "title", "aria-label", "placeholder")


def swap(text: str, used: set[int]) -> str:
    for i, (old, new) in enumerate(TEXT_SWAPS):
        if old in text:
            text = text.replace(old, new)
            used.add(i)
    return text


def swap_colors(text: str) -> str:
    for old, new in COLOR_MAP.items():
        text = re.sub(re.escape(old), new, text, flags=re.IGNORECASE)
    return text


def schema(desc: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "HousePainter",
        "@id": f"{DOMAIN}#business",
        "name": NAME,
        "description": desc,
        "slogan": TAGLINE,
        "url": DOMAIN,
        "logo": f"{DOMAIN}/assets/freshcoat-logo.png",
        "image": f"{DOMAIN}/assets/freshcoat-logo.png",
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": "Montana",
                    "addressRegion": "Gauteng", "addressCountry": "ZA"},
        "areaServed": [{"@type": "Place", "name": AREA}],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[0]}}
                       for s in SERVICES],
    }
    return json.dumps(data, ensure_ascii=False)


def arrow(soup, cid):
    svg = soup.new_tag("svg", attrs={"fill": "none", "height": "16", "stroke": "currentColor",
                                     "stroke-width": "2", "viewbox": "0 0 24 24", "width": "16",
                                     "data-astro-cid-j7pv25f6": ""})
    svg.append(soup.new_tag("path", attrs={"d": "M5 12h14M12 5l7 7-7 7"}))
    return svg


def rebuild_home_services(soup):
    grid = soup.select_one("section#services .services__grid")
    if not grid:
        return
    cid = {"data-astro-cid-j7pv25f6": ""}
    grid.clear()
    for i, (title, desc, img) in enumerate(SERVICES):
        a = soup.new_tag("a", attrs={"class": "service-card", "data-stagger": str(i),
                                     "href": "services/index.html", **cid})
        wrap = soup.new_tag("div", attrs={"class": "service-card__image-wrap", **cid})
        if img:
            wrap.append(soup.new_tag("img", attrs={"alt": title, "class": "service-card__image",
                                                   "loading": "lazy", "src": img, **cid}))
        else:
            wrap["class"] = "service-card__image-wrap service-card__image-wrap--placeholder"
            lbl = soup.new_tag("span", attrs={"class": "service-card__placeholder-label"})
            lbl.string = title
            wrap.append(lbl)
        body = soup.new_tag("div", attrs={"class": "service-card__body", **cid})
        h = soup.new_tag("h3", attrs={"class": "service-card__title", **cid}); h.string = title
        p = soup.new_tag("p", attrs={"class": "service-card__desc", **cid}); p.string = desc
        link = soup.new_tag("span", attrs={"class": "service-card__link", **cid})
        link.append("Learn More ")
        link.append(arrow(soup, cid))
        body.extend([h, p, link])
        a.extend([wrap, body])
        grid.append(a)
    grid["class"] = grid.get("class", []) + ["services__grid--four"]


def rebuild_services_page(soup):
    grid = soup.select_one(".services-grid")
    if grid:
        grid.clear()
        for i, (title, desc, _) in enumerate(SERVICES, 1):
            card = soup.new_tag("div", attrs={"class": "service-card"})
            icon = soup.new_tag("div", attrs={"class": "service-card__icon"}); icon.string = f"{i:02d}"
            h = soup.new_tag("h3", attrs={"class": "service-card__title"}); h.string = title
            p = soup.new_tag("p", attrs={"class": "service-card__desc"}); p.string = desc
            card.extend([icon, h, p])
            grid.append(card)
    filters = soup.select_one(".gallery-filters")
    if filters:
        filters.clear()
        cats = ["all"] + list(dict.fromkeys(c for _, _, c in GALLERY))
        for c in cats:
            btn = soup.new_tag("button", attrs={"class": "gallery-filter" + (" active" if c == "all" else ""),
                                                "data-filter": c})
            btn.string = "All" if c == "all" else c
            filters.append(btn)
    g = soup.select_one("#gallery-grid")
    if g:
        sec = g.find_parent("section")
        if sec:
            sec["id"] = "projects"
        g.clear()
        for slug, alt, cat_name in GALLERY:
            item = soup.new_tag("div", attrs={"class": "gallery-item", "data-category": cat_name})
            item.append(soup.new_tag("img", attrs={"alt": alt, "data-full": f"../assets/stock/{slug}.jpg",
                                                   "loading": "lazy", "src": f"../assets/stock/{slug}-thumb.jpg"}))
            cat = soup.new_tag("span", attrs={"class": "gallery-item__cat"}); cat.string = cat_name
            item.append(cat)
            g.append(item)


def rebuild_home(soup):
    rebuild_home_services(soup)

    # Hero wordmark (swap for the real logo image once supplied)
    hero = soup.select_one(".hero__content .bl-hero-name")
    if hero:
        hero.clear()
        hero["class"] = ["hero__logo", "fc-hero-name"]
        top = soup.new_tag("span", attrs={"class": "fc-hero-name__main"}); top.string = "FreshCoat"
        sub = soup.new_tag("span", attrs={"class": "fc-hero-name__sub"}); sub.string = "Painters"
        tag = soup.new_tag("span", attrs={"class": "fc-hero-name__tagline"}); tag.string = TAGLINE
        hero.extend([top, sub, tag])

    # Gallery: painting photos only, one row of three
    grid = soup.select_one("section.gallery .gallery__grid")
    if grid:
        grid.clear()
        alts = {s: a for s, a, _ in GALLERY}
        for i, slug in enumerate(HOME_GALLERY):
            alt = alts[slug]
            item = soup.new_tag("div", attrs={"class": "gallery__item", "data-stagger": str(i),
                                              "data-astro-cid-j7pv25f6": ""})
            item.append(soup.new_tag("img", attrs={"alt": alt, "class": "gallery__image", "loading": "lazy",
                                                   "src": f"assets/stock/{slug}-thumb.jpg",
                                                   "data-astro-cid-j7pv25f6": ""}))
            grid.append(item)

    # Trust bar: drop the empty badge slot (and its divider) so the items centre
    bar = soup.select_one(".trust-bar__inner")
    if bar:
        for item in bar.select(".trust-bar__item"):
            if not item.get_text(strip=True):
                prev = item.find_previous_sibling(class_="trust-bar__divider")
                if prev:
                    prev.decompose()
                item.decompose()

    # No financing offer: drop the FAQ entry
    for item in soup.select(".faq__item"):
        if "financing" in item.get_text().lower():
            item.decompose()

    # Stock videos
    hv = soup.select_one("video#heroVideo")
    if hv:
        hv["src"] = HERO_VIDEO
        hv["poster"] = HERO_POSTER
    sv = soup.select_one("video#showreelVideo")
    if sv:
        sv["src"] = SHOWREEL_VIDEO
        sv["poster"] = SHOWREEL_POSTER

    # Previous business's reviews and social videos don't belong to FreshCoat
    for sel in ("section.testimonials", "section.follow-us"):
        el = soup.select_one(sel)
        if el:
            el.decompose()


def common(soup, prefix, page):
    logo = f"{prefix}assets/freshcoat-logo.png"
    for img in soup.select("img.header__logo-img, img.footer__logo-img"):
        img["src"] = logo
        img["alt"] = NAME
    for a in soup.select("a.header__logo"):
        a["aria-label"] = f"{NAME} Home"

    # Social links pointed at the previous business's accounts
    for el in soup.select(".header__socials, .footer__socials, .mobile-menu__socials"):
        el.decompose()
    for a in soup.find_all("a", href=re.compile(r"facebook\.com/profile\.php\?id=61584933921950|instagram\.com/blrenovations")):
        a.decompose()

    for a in soup.find_all("a", href=re.compile(r"financing/index\.html$")):
        if re.search(r"quote|estimate|inspection", a.get_text(), re.I):
            a["href"] = f"{prefix}contact/index.html"

    # Financing page removed: drop every link to it
    for a in soup.find_all("a", href=re.compile(r"financing/index\.html$")):
        li = a.find_parent("li")
        (li or a).decompose()

    # Balance the header: 2 links either side of the logo ("Projects" jumps to the gallery)
    right = soup.select_one("nav.header__nav--right")
    if right and not right.select_one("a[data-fc-projects]"):
        contact = right.find("a", href=re.compile(r"contact/index\.html$"), class_="header__link")
        if contact:
            proj = soup.new_tag("a", attrs={"class": "header__link", "href": f"{prefix}services/index.html#projects",
                                            "data-fc-projects": ""})
            proj.string = "Projects"
            contact.insert_before(proj)
    mm = soup.select_one("a.mobile-menu__link[href$='contact/index.html']")
    if mm and not soup.select_one("a.mobile-menu__link[data-fc-projects]"):
        mp = soup.new_tag("a", attrs={"class": "mobile-menu__link", "href": f"{prefix}services/index.html#projects",
                                      "data-fc-projects": ""})
        mp.string = "Projects"
        mm.insert_before(mp)

    # Floating WhatsApp button (bottom right) — rebuilt each run so the icon stays current
    for old in soup.select("a.fc-whatsapp"):
        old.decompose()
    if soup.body:
        wa = BeautifulSoup(
            f'<a class="fc-whatsapp" href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer" '
            f'aria-label="Chat with {NAME} on WhatsApp" title="Chat on WhatsApp">{WHATSAPP_SVG}</a>',
            "html.parser")
        soup.body.append(wa)

    # Header CTA -> contact form
    for a in soup.select("a.btn--cta, a.hero__cta-ghost"):
        a["href"] = f"{prefix}contact/index.html"

    # Footer service list
    for heading in soup.select("h4.footer__heading"):
        if heading.get_text(strip=True) == "Services":
            ul = heading.find_next_sibling("ul")
            if ul:
                ul.clear()
                for s in FOOTER_SERVICES:
                    li = soup.new_tag("li")
                    a = soup.new_tag("a", attrs={"class": "footer__link", "href": f"{prefix}services/index.html"})
                    a.string = s
                    li.append(a)
                    ul.append(li)

    # Contact form service options
    for sel in soup.select("select#service"):
        for opt in sel.find_all("option"):
            if opt.get("value"):
                opt.decompose()
        for o in FORM_OPTIONS:
            opt = soup.new_tag("option", attrs={"value": o, "data-astro-cid-svshx33u": ""})
            opt.string = o
            sel.append(opt)

    # Links
    for a in soup.find_all("a", href=True):
        h = a["href"]
        if h.startswith("tel:"):
            a["href"] = f"tel:{PHONE_TEL}"
        elif h.startswith("mailto:"):
            a["href"] = f"mailto:{EMAIL}"
        elif "google.com/maps" in h:
            a["href"] = MAPS_URL
    for f in soup.find_all("iframe", src=True):
        if "maps.google" in f["src"]:
            f["src"] = MAPS_EMBED
            f["title"] = f"Map of {AREA}"

    # Meta
    for m in soup.find_all("meta"):
        prop = m.get("property", "")
        if prop == "og:url":
            m["content"] = DOMAIN + "/"
        elif prop in ("og:image",) or m.get("name") == "twitter:image":
            m["content"] = f"{DOMAIN}/assets/freshcoat-logo.png"
        elif prop == "og:locale":
            m["content"] = "en_ZA"

    # Brand fonts: Poppins (headings) + DM Sans (body)
    for link in soup.find_all("link", href=re.compile(r"fonts\.googleapis\.com/css2")):
        link["href"] = FONTS_URL

    # Photo behind the page title on inner pages
    hero = soup.select_one("section.page-hero")
    if hero and page in PAGE_HERO_IMAGES:
        hero["style"] = f"--fc-hero-img:url('{prefix}assets/stock/{PAGE_HERO_IMAGES[page]}.jpg')"
        if "fc-page-hero" not in hero.get("class", []):
            hero["class"] = hero.get("class", []) + ["fc-page-hero"]

    # Stat values on About
    for span in soup.select(".stat-item__value"):
        v = span.get_text(strip=True)
        if v in STAT_VALUES:
            span.string = STAT_VALUES[v]


all_used: set[int] = set()
for html_path in sorted(ROOT.rglob("*.html")):
    rel = html_path.relative_to(ROOT)
    prefix = "../" * (len(rel.parts) - 1)
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")

    common(soup, prefix, rel.parts[0] if len(rel.parts) > 1 else None)
    if rel.as_posix() == "index.html":
        rebuild_home(soup)
    elif rel.as_posix() == "services/index.html":
        rebuild_services_page(soup)

    # Text nodes (skip scripts/styles/comments)
    for node in soup.find_all(string=True):
        if isinstance(node, Comment) or node.parent.name in ("script", "style"):
            continue
        new = swap(str(node), all_used)
        if new != str(node):
            node.replace_with(NavigableString(new))
    for tag in soup.find_all(True):
        for attr in ATTRS:
            if isinstance(tag.get(attr), str):
                tag[attr] = swap(tag[attr], all_used)

    # Structured data
    desc_meta = soup.find("meta", attrs={"name": "description"})
    for s in soup.find_all("script", attrs={"type": "application/ld+json"}):
        s.string = schema(desc_meta["content"] if desc_meta else NAME)

    out = swap_colors(str(soup))
    # Inline JS strings (form messages etc.)
    for old, new in (("BL Renovations", NAME), ("+27 74 415 7569", PHONE), ("mbdqggey", FORMSPREE_ID),
                     ("+27744157569", PHONE_TEL), ("Renovationsbl6@gmail.com", EMAIL)):
        out = out.replace(old, new)
    html_path.write_text(out, encoding="utf-8")
    print(f"rebranded {rel}")

for css in ROOT.rglob("*.css"):
    t = css.read_text(encoding="utf-8", errors="ignore")
    new = swap_colors(t)
    if new != t:
        css.write_text(new, encoding="utf-8")
        print(f"colours {css.relative_to(ROOT)}")

unused = [TEXT_SWAPS[i][0][:70] for i in range(len(TEXT_SWAPS)) if i not in all_used]
if unused:
    print("\nUNMATCHED swaps:")
    for u in unused:
        print("  -", u)
