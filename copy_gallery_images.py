import os
import shutil
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "billing_app" / "assets"
GALLERY_DIR = BASE_DIR / "billing_app" / "static" / "billing_app" / "images" / "gallery"

# 1. Ensure target gallery directory exists
GALLERY_DIR.mkdir(parents=True, exist_ok=True)
print(f"[OK] Ensured gallery directory exists: {GALLERY_DIR}")

# 2. Mapping of source images from assets to target gallery names
# Based on user assets and requested alt descriptions:
# - delivery_1.jpg : "Happy customer taking delivery" -> 7.jpeg
# - showroom_1.jpg : "Komaki scooters displayed in showroom" -> 3.jpeg
# - delivery_2.jpg : "Happy customer taking delivery" -> 13.jpeg
# - showroom_2.jpg : "Inside N.P. Motors Showroom" -> 4.jpeg
IMAGE_MAPPING = {
    "delivery_1.jpg": "7.jpeg",
    "showroom_1.jpg": "3.jpeg",
    "delivery_2.jpg": "13.jpeg",
    "showroom_2.jpg": "4.jpeg",
}

# Also support finding original WhatsApp filenames if present
WHATSAPP_FALLBACKS = {
    "delivery_1.jpg": ["*15.21.43 (1)*", "*delivery_1*"],
    "showroom_1.jpg": ["*15.21.45*", "*showroom_1*"],
    "delivery_2.jpg": ["*15.21.43*", "*delivery_2*"],
    "showroom_2.jpg": ["*15.21.45 (1)*", "*showroom_2*"],
}

copied_files = []

for target_name, source_filename in IMAGE_MAPPING.items():
    source_path = ASSETS_DIR / source_filename
    target_path = GALLERY_DIR / target_name
    
    # Check if primary mapped file exists in assets
    if source_path.exists():
        shutil.copy2(source_path, target_path)
        copied_files.append((source_path.name, target_name))
        print(f"[COPIED] {source_path.name} -> {target_path.name}")
    else:
        # Try finding using fallbacks
        found = False
        for pattern in WHATSAPP_FALLBACKS.get(target_name, []):
            matches = list(ASSETS_DIR.glob(pattern))
            if matches:
                shutil.copy2(matches[0], target_path)
                copied_files.append((matches[0].name, target_name))
                print(f"[COPIED] {matches[0].name} -> {target_path.name}")
                found = True
                break
        if not found:
            print(f"[WARNING] Could not find source image for {target_name}")

print(f"\nSuccessfully copied {len(copied_files)} images to {GALLERY_DIR}:")
for src, dst in copied_files:
    print(f"  - {dst} (from {src})")
