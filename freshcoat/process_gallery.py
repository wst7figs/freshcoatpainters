"""Rename + optimize the 24 WhatsApp business photos, then build a gallery/index.json
that the HTML generator uses.
"""
from pathlib import Path
from PIL import Image
import json

ASSETS = Path(__file__).parent / "site" / "assets"
GALLERY_DIR = ASSETS / "gallery"
GALLERY_DIR.mkdir(exist_ok=True)

# Ordered mapping: original filename -> (new slug, category, alt text)
MAPPING = [
    ("WhatsApp Image 2026-09-06 at 10.44.57.jpeg", "tiling-marble-floor-1", "Tiling", "Polished marble-look tile floor installation"),
    ("WhatsApp Image 2026-09-06 at 10.44.58.jpeg", "tiling-marble-floor-2", "Tiling", "Marble-look tile floor, close-up finish"),
    ("WhatsApp Image 2026-09-06 at 10.44.59.jpeg", "tiling-plank-install-1", "Tiling", "Wood-look plank tile installation with spacers"),
    ("WhatsApp Image 2026-09-06 at 10.44.59 (1).jpeg", "tiling-plank-finished-1", "Tiling", "Finished wood-look plank tile flooring"),
    ("WhatsApp Image 2026-09-06 at 10.45.00.jpeg", "tiling-plank-finished-2", "Tiling", "Wood-look plank tiling, room corner finish"),
    ("WhatsApp Image 2026-09-06 at 10.45.01.jpeg", "tiling-plank-finished-3", "Tiling", "Wood-look plank tile flooring installation"),
    ("WhatsApp Image 2026-09-06 at 10.45.01 (1).jpeg", "tiling-hall-project-1", "Tiling", "Large commercial hall tiling project"),
    ("WhatsApp Image 2026-09-06 at 10.45.03.jpeg", "tiling-hall-project-2", "Tiling", "Commercial hall tiling in progress"),
    ("WhatsApp Image 2026-09-06 at 10.45.04.jpeg", "tiling-commercial-floor", "Tiling", "Commercial building tile floor installation"),
    ("WhatsApp Image 2026-09-06 at 10.45.04 (1).jpeg", "tiling-bathroom-marble-1", "Tiling", "Luxury marble bathroom tiling with double vanity"),
    ("WhatsApp Image 2026-09-06 at 10.45.04 (2).jpeg", "tiling-bathroom-marble-2", "Tiling", "Marble bathroom tiling under thatched roof"),
    ("WhatsApp Image 2026-09-06 at 10.45.05.jpeg", "tiling-outdoor-patio", "Tiling", "Outdoor patio and pool step tiling"),
    ("WhatsApp Image 2026-09-06 at 10.45.43.jpeg", "ceiling-roof-trusses", "Ceiling & Insulation", "Roof truss and ceiling insulation installation"),
    ("WhatsApp Image 2026-09-06 at 10.45.43 (1).jpeg", "ceiling-drywall-finish", "Ceiling & Insulation", "Freshly installed drywall ceiling"),
    ("WhatsApp Image 2026-09-06 at 10.45.44.jpeg", "ceiling-repair-access", "Ceiling & Insulation", "Ceiling access panel repair"),
    ("WhatsApp Image 2026-09-06 at 10.45.44 (1).jpeg", "ceiling-grid-crew", "Ceiling & Insulation", "Crew installing suspended ceiling grid"),
    ("WhatsApp Image 2026-09-06 at 10.45.44 (2).jpeg", "ceiling-lighting-finish-1", "Ceiling & Insulation", "Finished ceiling with recessed LED lighting"),
    ("WhatsApp Image 2026-09-06 at 10.45.44 (3).jpeg", "ceiling-lighting-finish-2", "Ceiling & Insulation", "Modern ceiling installation with strip lighting"),
    ("WhatsApp Image 2026-09-06 at 10.47.40.jpeg", "flooring-vinyl-install", "Flooring", "Vinyl plank flooring installation"),
    ("WhatsApp Image 2026-09-06 at 10.47.41.jpeg", "flooring-staircase", "Flooring", "Laminate flooring installed on staircase"),
    ("WhatsApp Image 2026-09-06 at 10.47.41 a.jpeg", "flooring-laminate-room-1", "Flooring", "Laminate flooring installation, room view"),
    ("WhatsApp Image 2026-09-06 at 10.47.41 b.jpeg", "flooring-laminate-room-2", "Flooring", "Laminate flooring near sliding door"),
    ("WhatsApp Image 2026-09-06 at 10.47.41 c.jpeg", "flooring-laminate-finished-1", "Flooring", "Finished laminate flooring, empty room"),
    ("WhatsApp Image 2026-09-06 at 10.47.42.jpeg", "flooring-laminate-finished-2", "Flooring", "Finished light grey laminate flooring"),
]

manifest = []

for orig_name, slug, category, alt in MAPPING:
    src = ASSETS / orig_name
    if not src.exists():
        print(f"MISSING: {orig_name}")
        continue
    im = Image.open(src)
    im = im.convert("RGB")

    # Full-size (capped) version
    full = im.copy()
    full.thumbnail((1600, 1600), Image.LANCZOS)
    full_path = GALLERY_DIR / f"{slug}.jpg"
    full.save(full_path, "JPEG", quality=78, optimize=True)

    # Thumbnail version for grid
    thumb = im.copy()
    thumb.thumbnail((640, 640), Image.LANCZOS)
    thumb_path = GALLERY_DIR / f"{slug}-thumb.jpg"
    thumb.save(thumb_path, "JPEG", quality=72, optimize=True)

    manifest.append({
        "slug": slug,
        "category": category,
        "alt": alt,
        "full": f"assets/gallery/{slug}.jpg",
        "thumb": f"assets/gallery/{slug}-thumb.jpg",
    })
    print(f"processed {orig_name} -> {slug} ({full_path.stat().st_size//1024}KB / {thumb_path.stat().st_size//1024}KB)")

(GALLERY_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

# Remove the original heavy WhatsApp files now that optimized copies exist
for orig_name, *_ in MAPPING:
    src = ASSETS / orig_name
    if src.exists():
        src.unlink()

print(f"\nDone. {len(manifest)} images processed into {GALLERY_DIR}")
