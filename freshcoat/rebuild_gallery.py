"""Rebuild the gallery/ folder from scratch: the user moved the old processed
files out to assets/ root (removing one duplicate) and dropped 18 brand-new
photos in alongside them. This script:
  1. Renames the 18 new photos to descriptive slugs
  2. Resizes + compresses ALL surviving/new originals into assets/gallery/
     (full + thumb, matching the original pipeline)
  3. Removes the old flat/raw copies from assets/ root
  4. Writes a fresh manifest.json
"""
from pathlib import Path
from PIL import Image
import json

ASSETS = Path(__file__).parent / "site" / "assets"
GALLERY_DIR = ASSETS / "gallery"
GALLERY_DIR.mkdir(exist_ok=True)

# ---- 1. New photos: raw filename -> (slug, category, alt) ----
NEW_MAPPING = [
    ("1000110831.jpg", "ceiling-vaulted-painted-finish", "Ceiling & Insulation", "Finished vaulted ceiling with painted exposed trusses"),
    ("1000110833.jpg", "ceiling-trusses-insulation-2", "Ceiling & Insulation", "Roof trusses with insulation before ceiling boards"),
    ("1000112353.jpg", "flooring-laminate-livingroom-1", "Flooring", "Laminate flooring in a finished living room"),
    ("1000112354.jpg", "flooring-laminate-hallway-1", "Flooring", "Laminate flooring installed in a hallway"),
    ("1000112355.jpg", "flooring-laminate-step-transition", "Flooring", "Laminate flooring across a raised step transition"),
    ("1000112357.jpg", "flooring-install-crew-1", "Flooring", "Installer fitting laminate flooring boards"),
    ("1000148424.jpg", "paving-installation-street", "Paving", "Paving brick installation along a driveway"),
    ("1000148591.jpg", "paving-finished-walkway", "Paving", "Finished herringbone paved walkway"),
    ("a70dd4a6-e059-4a62-b084-98eecf239614-1_all_254.jpg", "painting-mustard-room", "Painting", "Freshly painted mustard yellow room"),
    ("a70dd4a6-e059-4a62-b084-98eecf239614-1_all_255.jpg", "painting-burgundy-room-1", "Painting", "Freshly painted burgundy accent room"),
    ("a70dd4a6-e059-4a62-b084-98eecf239614-1_all_256.jpg", "painting-burgundy-room-2", "Painting", "Burgundy painted room with French doors"),
    ("a70dd4a6-e059-4a62-b084-98eecf239614-1_all_260.jpg", "ceiling-insulation-tiled-room", "Ceiling & Insulation", "Room mid-renovation with exposed ceiling insulation"),
    ("a70dd4a6-e059-4a62-b084-98eecf239614-1_all_261.jpg", "ceiling-pvc-finished", "Ceiling & Insulation", "Finished PVC ceiling with recessed lighting"),
    ("a70dd4a6-e059-4a62-b084-98eecf239614-1_all_1002.jpg", "flooring-laminate-finished-3", "Flooring", "Finished laminate flooring, bedroom view"),
    ("a70dd4a6-e059-4a62-b084-98eecf239614-1_all_1004.jpg", "flooring-laminate-finished-4", "Flooring", "Finished laminate flooring near window"),
    ("a70dd4a6-e059-4a62-b084-98eecf239614-1_all_1011.jpg", "flooring-install-crew-2", "Flooring", "Installer cutting laminate board with a circular saw"),
    ("a70dd4a6-e059-4a62-b084-98eecf239614-1_all_2610.jpg", "flooring-laminate-finished-5", "Flooring", "Finished light grey laminate flooring"),
    ("a70dd4a6-e059-4a62-b084-98eecf239614-1_all_2616.jpg", "flooring-laminate-edge-install", "Flooring", "Laminate flooring installation meeting existing tile"),
]

# ---- 2. Surviving originals from the first batch (already-good slugs) ----
SURVIVING_MAPPING = [
    ("tiling-marble-floor-1.jpg", "tiling-marble-floor-1", "Tiling", "Polished marble-look tile floor installation"),
    ("tiling-marble-floor-2.jpg", "tiling-marble-floor-2", "Tiling", "Marble-look tile floor, close-up finish"),
    ("tiling-plank-install-1.jpg", "tiling-plank-install-1", "Tiling", "Wood-look plank tile installation with spacers"),
    ("tiling-plank-finished-1.jpg", "tiling-plank-finished-1", "Tiling", "Finished wood-look plank tile flooring"),
    ("tiling-plank-finished-2.jpg", "tiling-plank-finished-2", "Tiling", "Wood-look plank tiling, room corner finish"),
    ("tiling-plank-finished-3.jpg", "tiling-plank-finished-3", "Tiling", "Wood-look plank tile flooring installation"),
    ("tiling-hall-project-1.jpg", "tiling-hall-project-1", "Tiling", "Large commercial hall tiling project"),
    ("tiling-hall-project-2.jpg", "tiling-hall-project-2", "Tiling", "Commercial hall tiling in progress"),
    ("tiling-commercial-floor.jpg", "tiling-commercial-floor", "Tiling", "Commercial building tile floor installation"),
    ("tiling-bathroom-marble-2.jpg", "tiling-bathroom-marble-2", "Tiling", "Marble bathroom tiling under thatched roof"),
    ("tiling-outdoor-patio.jpg", "tiling-outdoor-patio", "Tiling", "Outdoor patio and pool step tiling"),
    ("ceiling-roof-trusses.jpg", "ceiling-roof-trusses", "Ceiling & Insulation", "Roof truss and ceiling insulation installation"),
    ("ceiling-drywall-finish.jpg", "ceiling-drywall-finish", "Ceiling & Insulation", "Freshly installed drywall ceiling"),
    ("ceiling-repair-access.jpg", "ceiling-repair-access", "Ceiling & Insulation", "Ceiling access panel repair"),
    ("ceiling-grid-crew.jpg", "ceiling-grid-crew", "Ceiling & Insulation", "Crew installing suspended ceiling grid"),
    ("ceiling-lighting-finish-1.jpg", "ceiling-lighting-finish-1", "Ceiling & Insulation", "Finished ceiling with recessed LED lighting"),
    ("ceiling-lighting-finish-2.jpg", "ceiling-lighting-finish-2", "Ceiling & Insulation", "Modern ceiling installation with strip lighting"),
    ("flooring-vinyl-install.jpg", "flooring-vinyl-install", "Flooring", "Vinyl plank flooring installation"),
    ("flooring-staircase.jpg", "flooring-staircase", "Flooring", "Laminate flooring installed on staircase"),
    ("flooring-laminate-room-1.jpg", "flooring-laminate-room-1", "Flooring", "Laminate flooring installation, room view"),
    ("flooring-laminate-room-2.jpg", "flooring-laminate-room-2", "Flooring", "Laminate flooring near sliding door"),
    ("flooring-laminate-finished-1.jpg", "flooring-laminate-finished-1", "Flooring", "Finished laminate flooring, empty room"),
    ("flooring-laminate-finished-2.jpg", "flooring-laminate-finished-2", "Flooring", "Finished light grey laminate flooring"),
]

CATEGORY_ORDER = ["Painting", "Paving", "Tiling", "Flooring", "Ceiling & Insulation"]

manifest = []

def process(src_path: Path, slug: str, category: str, alt: str):
    im = Image.open(src_path)
    im = im.convert("RGB")

    full = im.copy()
    full.thumbnail((1600, 1600), Image.LANCZOS)
    full_path = GALLERY_DIR / f"{slug}.jpg"
    full.save(full_path, "JPEG", quality=78, optimize=True)

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
    print(f"  {src_path.name} -> {slug} ({full_path.stat().st_size//1024}KB / {thumb_path.stat().st_size//1024}KB)")


print("Processing new photos...")
for raw_name, slug, category, alt in NEW_MAPPING:
    src = ASSETS / raw_name
    if not src.exists():
        print(f"  MISSING new file: {raw_name}")
        continue
    process(src, slug, category, alt)

print("\nProcessing surviving originals...")
for raw_name, slug, category, alt in SURVIVING_MAPPING:
    src = ASSETS / raw_name
    if not src.exists():
        print(f"  MISSING surviving file: {raw_name}")
        continue
    process(src, slug, category, alt)

# Sort manifest by category order, then slug, for a stable/organized gallery
manifest.sort(key=lambda m: (CATEGORY_ORDER.index(m["category"]) if m["category"] in CATEGORY_ORDER else 99, m["slug"]))

(GALLERY_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

# ---- 3. Clean up: remove the flat raw copies now that gallery/ has processed versions ----
all_raw_names = [m[0] for m in NEW_MAPPING] + [m[0] for m in SURVIVING_MAPPING]
removed = 0
for raw_name in all_raw_names:
    p = ASSETS / raw_name
    if p.exists():
        p.unlink()
        removed += 1

print(f"\nDone. {len(manifest)} images in manifest, {removed} raw/flat originals cleaned up from assets/ root.")

# Print category counts
from collections import Counter
counts = Counter(m["category"] for m in manifest)
for cat in CATEGORY_ORDER:
    print(f"  {cat}: {counts.get(cat, 0)}")
