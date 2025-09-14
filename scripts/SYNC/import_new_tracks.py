import pandas as pd
from pathlib import Path

CSV_PATH = "music_catalog.csv"
AUDIO_FOLDER = Path("audio")  # adjust if your audio lives elsewhere
SUPPORTED_EXTS = [".mp3", ".wav", ".flac"]

# Load existing catalog
df = pd.read_csv(CSV_PATH)
df.columns = [col.strip() for col in df.columns]
existing_files = set(df["Filename"].astype(str).str.strip())

# Function to format a readable title from filename
def format_title(name):
    name = name.replace("_", " ").replace("-", " ")
    name = name.strip(" .")
    return name.title()

# Discover new audio files
new_rows = []
for file in AUDIO_FOLDER.glob("*"):
    if file.suffix.lower() not in SUPPORTED_EXTS:
        continue
    if file.name in existing_files:
        continue
    title = format_title(file.stem)
    new_rows.append({
        "Title": title,
        "Filename": file.name,
        "Mood": "",
        "Energy Level": "",
        "Genre": ""
    })

# Append to catalog
if new_rows:
    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)
    print(f"✅ Imported {len(new_rows)} new tracks into {CSV_PATH}")
else:
    print("📂 No new tracks found.")
