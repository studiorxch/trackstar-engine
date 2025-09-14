import os
import re

# === Set your Mac path to the folder (e.g., covers or audio) ===
TARGET_FOLDER = "/Users/studio/TrackstarEngine/covers"

def convert_double_dashes_to_parentheses(name):
    # Replace --content-- with (content)
    return re.sub(r"--(.*?)--", r"(\1)", name)

def restore_filenames(folder):
    for filename in os.listdir(folder):
        if filename.startswith('.') or not os.path.isfile(os.path.join(folder, filename)):
            continue

        name, ext = os.path.splitext(filename)
        new_name = convert_double_dashes_to_parentheses(name)  # Replace -- -- with ( )
        new_name = new_name.replace("_", " ")                  # Replace _ with space

        new_filename = f"{new_name}{ext}"
        original_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_filename)

        if original_path != new_path:
            os.rename(original_path, new_path)
            print(f"🔄 Restored: {filename} → {new_filename}")

# Run the restorer
restore_filenames(TARGET_FOLDER)
