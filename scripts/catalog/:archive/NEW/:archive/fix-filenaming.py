import os
import re

AUDIO_FOLDER = "/Users/studio/TrackstarEngine/audio"

def title_case_name(filename):
    name, ext = os.path.splitext(filename)
    if name != name.title():  # Only change if needed
        # Replace underscores and double dashes before title-casing
        clean_name = re.sub(r"[_\-]+", " ", name)
        title_name = clean_name.title().replace(" ", "_")  # Underscores help keep structure
        return f"{title_name}{ext}"
    return None

def fix_lowercase_files(folder):
    for f in os.listdir(folder):
        if f.startswith('.') or f.endswith('.mp3') or '_mp3_quarantine' in f:
            continue
        path = os.path.join(folder, f)
        if os.path.isfile(path):
            new_name = title_case_name(f)
            if new_name and new_name != f:
                new_path = os.path.join(folder, new_name)
                os.rename(path, new_path)
                print(f"✅ Renamed: {f} → {new_name}")

fix_lowercase_files(AUDIO_FOLDER)
