import os
import pandas as pd
import re

# === CONFIG ===
CSV_PATH = "/Users/studio/TrackstarEngine/catalog/track_catalog.csv"
AUDIO_FOLDER = "/Users/studio/TrackstarEngine/audio"
COVERS_FOLDER = "/Users/studio/TrackstarEngine/covers"
OUTPUT_PATH = "/Users/studio/TrackstarEngine/catalog/track_catalog_with_filenames.csv"

# Load catalog
df = pd.read_csv(CSV_PATH)

def normalize(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

audio_files = [f for f in os.listdir(AUDIO_FOLDER) if f.lower().endswith((".flac", ".mp3"))]
cover_files = [f for f in os.listdir(COVERS_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

audio_map = {normalize(os.path.splitext(f)[0]): f for f in audio_files}
cover_map = {normalize(os.path.splitext(f)[0]): f for f in cover_files}

# Attempt to match audio/cover files by normalized Title
audio_filenames = []
cover_filenames = []

for _, row in df.iterrows():
    title = row.get("Title", "")
    title_key = normalize(title)

    audio_filename = audio_map.get(title_key, "")
    cover_filename = cover_map.get(title_key, "")

    audio_filenames.append(audio_filename)
    cover_filenames.append(cover_filename)

df["Audio Filename"] = audio_filenames
df["Cover Art Filename"] = cover_filenames

df.to_csv(OUTPUT_PATH, index=False)
print(f"✅ Output saved to: {OUTPUT_PATH}")
