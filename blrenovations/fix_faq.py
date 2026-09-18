"""Replace the roofing-specific FAQ (visible HTML + JSON-LD schema) on the
homepage with FAQs that actually match BL Renovations' 8 real services."""
import json
import re
from pathlib import Path

PATH = Path(__file__).parent / "site" / "index.html"
text = PATH.read_text(encoding="utf-8")

NEW_FAQS = [
    (
        "What services does BL Renovations offer?",
        "We offer a full range of renovation and finishing services, including painting, "
        "waterproofing and damp proofing, rhinolite skimming, paving installation, tiling, "
        "laminate and vinyl flooring, plumbing, and ceiling and insulation work."
    ),
    (
        "Do you offer free quotes?",
        "Yes! We provide free, no-obligation quotes for every project. Our team will assess "
        "the work required and give you an honest, transparent price before anything begins."
    ),
    (
        "What areas do you service?",
        "We proudly serve homeowners and businesses across Pretoria and the surrounding areas."
    ),
    (
        "How long does a typical project take?",
        "Timelines depend on the size and scope of the work — a single room repaint looks "
        "very different from a full flooring or waterproofing job. We'll give you a realistic "
        "timeframe as part of your free quote."
    ),
    (
        "Do you handle both residential and commercial projects?",
        "Yes, we take on both residential and commercial work, from single rooms to larger "
        "multi-room and commercial spaces."
    ),
    (
        "Do you offer financing options?",
        "Yes, we offer flexible financing options to help make your project more affordable. "
        "Contact us to learn more about what's available."
    ),
]

# ---- 1. Rebuild the visible FAQ HTML block ----
items_html = []
for i, (question, answer) in enumerate(NEW_FAQS):
    items_html.append(f'''<div class="faq__item" data-astro-cid-j7pv25f6=""> <button aria-controls="faq-answer-{i}" aria-expanded="false" class="faq__trigger" data-astro-cid-j7pv25f6=""> <span class="faq__question" data-astro-cid-j7pv25f6="">{question}</span> <span aria-hidden="true" class="faq__icon" data-astro-cid-j7pv25f6=""> <svg class="faq__plus" data-astro-cid-j7pv25f6="" fill="none" height="20" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="20"><line data-astro-cid-j7pv25f6="" x1="12" x2="12" y1="5" y2="19"></line><line data-astro-cid-j7pv25f6="" x1="5" x2="19" y1="12" y2="12"></line></svg> <svg class="faq__minus" data-astro-cid-j7pv25f6="" fill="none" height="20" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="20"><line data-astro-cid-j7pv25f6="" x1="5" x2="19" y1="12" y2="12"></line></svg> </span> </button> <div class="faq__answer" data-astro-cid-j7pv25f6="" id="faq-answer-{i}" role="region"> <div class="faq__answer-inner" data-astro-cid-j7pv25f6=""> <p data-astro-cid-j7pv25f6="">{answer}</p> </div> </div> </div>''')

new_faq_list = '<div class="faq__list" data-astro-cid-j7pv25f6="">' + ''.join(items_html) + ' </div>'

pattern = re.compile(r'<div class="faq__list"[^>]*>.*?</div>\s*</div>\s*</div>\s*</section>', re.S)
m = pattern.search(text)
if not m:
    raise SystemExit("Could not find faq__list block")

replacement = new_faq_list + ' </div> </div> </section>'
text = text[:m.start()] + replacement + text[m.end():]

# ---- 2. Rebuild the JSON-LD FAQPage schema ----
faq_schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in NEW_FAQS
    ],
}
faq_json = json.dumps(faq_schema, separators=(",", ":"))

schema_pattern = re.compile(r'\{"@context":"https://schema\.org","@type":"FAQPage".*?\}\]\}')
m2 = schema_pattern.search(text)
if not m2:
    raise SystemExit("Could not find FAQPage JSON-LD block")
text = text[:m2.start()] + faq_json + text[m2.end():]

PATH.write_text(text, encoding="utf-8")
print(f"Replaced {len(NEW_FAQS)} FAQ items (HTML + JSON-LD).")
