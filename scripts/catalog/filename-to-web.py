import os
import re

# === Set your Mac path to the folder (e.g., covers or audio) ===
TARGET_FOLDER = "/Users/studio/TrackstarEngine/audio"

def convert_parentheses_to_dashes(name):
    # Replace (content) with --content--
    return re.sub(r"\((.*?)\)", r"--\1--", name)

def rename_files(folder):
    for filename in os.listdir(folder):
        if filename.startswith('.') or not os.path.isfile(os.path.join(folder, filename)):
            continue

        name, ext = os.path.splitext(filename)
        new_name = name.replace(" ", "_")                   # Replace spaces
        new_name = convert_parentheses_to_dashes(new_name)  # Replace ( ) with -- --

        new_filename = f"{new_name}{ext}"
        original_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_filename)

        if original_path != new_path:
            os.rename(original_path, new_path)
            print(f"✅ Renamed: {filename} → {new_filename}")

# Run the renamer
rename_files(TARGET_FOLDER)
