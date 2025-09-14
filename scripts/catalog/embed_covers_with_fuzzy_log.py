import os
import re
import csv
import mimetypes
import difflib
from mutagen.flac import FLAC, Picture

# === PATHS ===
FLAC_DIR = "/Users/studio/TrackstarEngine/audio"
COVER_DIR = "/Users/studio/TrackstarEngine/covers"
LOG_PATH = "/Users/studio/TrackstarEngine/logs/cover_embedding_log.csv"

# Normalize keys: strip symbols, lowercase, unify dashes/underscores
def normalize_key(name):
    name = re.sub(r"--.*?--", "", name)  # remove double dash markers
    name = re.sub(r'[^a-z0-9]', '', name.lower())  # keep only alphanumeric
    return name

# Embed cover art
def embed_cover(flac_file, cover_file):
    audio = FLAC(flac_file)
    picture = Picture()
    picture.type = 3  # front cover
    picture.mime = mimetypes.guess_type(cover_file)[0] or "image/jpeg"
    with open(cover_file, "rb") as img:
        picture.data = img.read()
    audio.clear_pictures()
    audio.add_picture(picture)
    audio.save()

# Build cover map
cover_map = {}
normalized_keys = []
for f in os.listdir(COVER_DIR):
    name, ext = os.path.splitext(f)
    if ext.lower() in [".jpg", ".jpeg", ".png"]:
        norm_key = normalize_key(name)
        cover_map[norm_key] = os.path.join(COVER_DIR, f)
        normalized_keys.append(norm_key)

# Process audio files
log_rows = []
for fname in os.listdir(FLAC_DIR):
    if not fname.lower().endswith(".flac"):
        continue

    flac_path = os.path.join(FLAC_DIR, fname)
    base_key = normalize_key(os.path.splitext(fname)[0])

    cover_path = cover_map.get(base_key)

    # Fuzzy match fallback
    if not cover_path:
        close_matches = difflib.get_close_matches(base_key, normalized_keys, n=1, cutoff=0.8)
        if close_matches:
            cover_path = cover_map[close_matches[0]]

    if cover_path:
        try:
            embed_cover(flac_path, cover_path)
            print(f"✅ Embedded: {os.path.basename(cover_path)} → {fname}")
            log_rows.append([fname, cover_path, "✅ Embedded"])
        except Exception as e:
            print(f"❌ Failed to embed: {fname} ({e})")
            log_rows.append([fname, cover_path, f"❌ Error: {e}"])
    else:
        print(f"⚠️ No matching cover for: {fname}")
        log_rows.append([fname, "", "⚠️ No matching cover"])

# Save log
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "w", newline="", encoding="utf-8") as logfile:
    writer = csv.writer(logfile)
    writer.writerow(["Audio File", "Cover File", "Status"])
    writer.writerows(log_rows)

print(f"📄 Log saved to: {LOG_PATH}")
