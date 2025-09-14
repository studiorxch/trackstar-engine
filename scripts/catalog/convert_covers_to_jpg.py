import os
from PIL import Image

# === PATH ===
COVERS_DIR = "/Users/studio/TrackstarEngine/covers"
LOG_PATH = "/Users/studio/TrackstarEngine/logs/cover_conversion_log.csv"

# Track changes
log_rows = []

# Loop through files
for file in os.listdir(COVERS_DIR):
    src_path = os.path.join(COVERS_DIR, file)
    name, ext = os.path.splitext(file)
    ext = ext.lower()

    if ext not in [".png", ".jpeg"]:
        continue

    jpg_path = os.path.join(COVERS_DIR, f"{name}.jpg")

    try:
        img = Image.open(src_path).convert("RGB")
        img.save(jpg_path, "JPEG", quality=95)
        os.remove(src_path)
        print(f"🧼 Converted and deleted: {file} → {name}.jpg")
        log_rows.append([file, f"{name}.jpg", "✅ Converted + Deleted"])
    except Exception as e:
        print(f"❌ Failed to convert: {file} ({e})")
        log_rows.append([file, "", f"❌ Error: {e}"])

# Save log
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
with open(LOG_PATH, "w", encoding="utf-8", newline="") as f:
    import csv
    writer = csv.writer(f)
    writer.writerow(["Original File", "New JPG File", "Status"])
    writer.writerows(log_rows)

print(f"📄 Conversion log saved to: {LOG_PATH}")
