import os
import shutil
import re

# === PATHS ===
AUDIO_DIR = "/Users/studio/TrackstarEngine/audio"
COVERS_DIR = "/Users/studio/TrackstarEngine/covers"
LOG_PATH = "/Users/studio/TrackstarEngine/logs/cover_duplicate_log.csv"

# Normalize function
def normalize_base(name):
    return re.sub(r"--.*?--", "", name)

# Get list of covers (jpg, png, jpeg)
cover_files = {os.path.splitext(f)[0]: f for f in os.listdir(COVERS_DIR)
               if f.lower().endswith((".png", ".jpg", ".jpeg"))}

# Track results
log_rows = []

# Loop through audio files
for audio_file in os.listdir(AUDIO_DIR):
    if not audio_file.lower().endswith(".flac"):
        continue

    base_name = os.path.splitext(audio_file)[0]
    exact_cover = os.path.join(COVERS_DIR, f"{base_name}.png")

    if not os.path.exists(exact_cover):
        # Look for a fallback shared cover (by normalized base)
        shared_base = normalize_base(base_name)
        possible_match = next((f for f in cover_files if normalize_base(f) == shared_base), None)

        if possible_match:
            original_path = os.path.join(COVERS_DIR, cover_files[possible_match])
            new_cover_path = os.path.join(COVERS_DIR, f"{base_name}.png")
            try:
                shutil.copyfile(original_path, new_cover_path)
                print(f"🌀 Duplicated: {original_path} → {new_cover_path}")
                log_rows.append([audio_file, new_cover_path, "✅ Copied"])
            except Exception as e:
                print(f"❌ Error copying {original_path} to {new_cover_path}: {e}")
                log_rows.append([audio_file, "", f"❌ Error: {e}"])
        else:
            print(f"⚠️ No shared cover found for: {audio_file}")
            log_rows.append([audio_file, "", "⚠️ No shared cover found"])
    else:
        log_rows.append([audio_file, exact_cover, "✅ Already Exists"])

# Save log
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "w", encoding="utf-8", newline="") as f:
    import csv
    writer = csv.writer(f)
    writer.writerow(["Audio File", "Cover File Created", "Status"])
    writer.writerows(log_rows)

print(f"📄 Cover duplication log saved to: {LOG_PATH}")
