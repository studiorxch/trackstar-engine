import os
from pathlib import Path
import numpy as np
import librosa
import soundfile as sf

# === Patch for deprecated np.complex in older librosa versions ===
if not hasattr(np, 'complex'):
    np.complex = complex

# === Config Paths ===
input_folder = Path("/Users/studio/playlist_generator/backend/audio")
output_folder = Path("/Users/studio/Public/home/assets/loops")
md_folder = Path("/Users/studio/Public/home/_tracks")

output_folder.mkdir(parents=True, exist_ok=True)

# === Load valid slugs from .md files ===
md_slugs = {f.stem.replace("_", "-") for f in md_folder.glob("*.md")}
print(f"📁 Found {len(md_slugs)} track slugs.")

# === Looping Parameters ===
loop_length = 16

# === Processing ===
for file in input_folder.iterdir():
    if file.suffix.lower() not in [".flac", ".wav", ".mp3"]:
        continue

    base_slug = file.stem.replace("_", "-")
    if base_slug not in md_slugs:
        print(f"❌ Skipped: {file.name} — no .md match")
        continue

    try:
        y, sr = librosa.load(str(file), sr=None)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

        if len(beats) < loop_length + 1:
            print(f"⚠️ Not enough beats in {file.name} — only {len(beats)} found")
            continue

        start = librosa.frames_to_samples(beats[0])
        end = librosa.frames_to_samples(beats[loop_length])
        loop_audio = y[start:end]

        output_path = output_folder / f"{base_slug}-loop.mp3"
        sf.write(str(output_path), loop_audio, sr, format="MP3")
        print(f"✅ Saved: {output_path.name}")

    except Exception as e:
        print(f"💥 Error processing {file.name}: {e}")
