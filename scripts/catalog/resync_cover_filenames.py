import os
import pandas as pd
import re

# === CONFIG ===
CATALOG_PATH = "/Users/studio/TrackstarEngine/catalog/track_catalog.csv"
COVERS_FOLDER = "/Users/studio/TrackstarEngine/covers"
OUTPUT_PATH = "/Users/studio/TrackstarEngine/catalog/track_catalog_resynced.csv"

# Load catalog
df = pd.read_csv(CATALOG_PATH)

# List existing cover images
cover_files = [f for f in os.listdir(COVERS_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

# Normalize for comparison
def normalize(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

cover_map = {normalize(os.path.splitext(f)[0]): f for f in cover_files}

# Update Cover Art Filename only if it exists
updated_cover_filenames = []
for _, row in df.iterrows():
    title = row.get("Title", "")
    normalized_title = normalize(title)
    cover_filename = cover_map.get(normalized_title, "")
    updated_cover_filenames.append(cover_filename)

df["Cover Art Filename"] = updated_cover_filenames
df.to_csv(OUTPUT_PATH, index=False)
print(f"✅ Cover filenames re-synced and saved to: {OUTPUT_PATH}")
