import os
import pandas as pd
import re
import difflib

# === CONFIG ===
CSV_PATH = "/Users/studio/TrackstarEngine/catalog/track_catalog.csv"
AUDIO_FOLDER = "/Users/studio/TrackstarEngine/audio"
COVERS_FOLDER = "/Users/studio/TrackstarEngine/covers"
OUTPUT_PATH = "/Users/studio/TrackstarEngine/catalog/track_catalog_with_filenames.csv"

# Load catalog
df = pd.read_csv(CSV_PATH)

def normalize(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

# Scan files
audio_files = [f for f in os.listdir(AUDIO_FOLDER) if f.lower().endswith((".flac", ".mp3"))]
cover_files = [f for f in os.listdir(COVERS_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

# Normalize and build maps
audio_keys = {normalize(os.path.splitext(f)[0]): f for f in audio_files}
cover_keys = {normalize(os.path.splitext(f)[0]): f for f in cover_files}
audio_keys_list = list(audio_keys.keys())
cover_keys_list = list(cover_keys.keys())

# Matching logic
audio_filenames = []
cover_filenames = []

for _, row in df.iterrows():
    title = row.get("Title", "")
    title_key = normalize(title)

    # Try direct match first
    audio_filename = audio_keys.get(title_key, "")
    cover_filename = cover_keys.get(title_key, "")

    # If not found, try fuzzy match
    if not audio_filename:
        matches = difflib.get_close_matches(title_key, audio_keys_list, n=1, cutoff=0.8)
        if matches:
            audio_filename = audio_keys[matches[0]]

    if not cover_filename:
        matches = difflib.get_close_matches(title_key, cover_keys_list, n=1, cutoff=0.8)
        if matches:
            cover_filename = cover_keys[matches[0]]

    audio_filenames.append(audio_filename)
    cover_filenames.append(cover_filename)

df["Audio Filename"] = audio_filenames
df["Cover Art Filename"] = cover_filenames

df.to_csv(OUTPUT_PATH, index=False)
print(f"✅ Output saved to: {OUTPUT_PATH}")
