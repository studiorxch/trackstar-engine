import os
import pandas as pd
import re

# === CONFIG ===
CATALOG_PATH = "/Users/studio/TrackstarEngine/catalog/track_catalog.csv"
AUDIO_FOLDER = "/Users/studio/TrackstarEngine/audio"
OUTPUT_PATH = "/Users/studio/TrackstarEngine/catalog/track_catalog_updated.csv"

# Load existing catalog
df = pd.read_csv(CATALOG_PATH)
existing_files = set(df["Audio Filename"].dropna().tolist())

# Normalize title from filename
def normalize_title(name):
    base = os.path.splitext(name)[0]
    return base.replace("_", " ").replace("--", "–").strip().title()

# List all audio files
audio_files = [f for f in os.listdir(AUDIO_FOLDER) if f.lower().endswith((".flac", ".mp3"))]

# Detect new files
new_entries = []
for file in audio_files:
    if file not in existing_files:
        title = normalize_title(file)
        cover = os.path.splitext(file)[0] + ".jpg"
        new_entries.append({
            "Title": title,
            "Audio Filename": file,
            "Cover Art Filename": cover,
            "Mood": "",
            "album_artist": "",
            "grouping": ""
        })

# Append new entries and save
if new_entries:
    df = pd.concat([df, pd.DataFrame(new_entries)], ignore_index=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Added {len(new_entries)} new songs. Updated catalog saved to: {OUTPUT_PATH}")
else:
    print("✅ No new audio files detected.")
