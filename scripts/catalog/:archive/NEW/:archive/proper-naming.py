import os
import re
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

AUDIO_FOLDER = "/Users/studio/TrackstarEngine/audio"

def clean_filename(name):
    name = name.lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"\((.*?)\)", r"--\1--", name)
    name = re.sub(r"[^a-z0-9_\-\.]", "", name)
    name = re.sub(r"__+", "_", name)
    return name.strip("_")

def format_title(name):
    name = name.replace("_", " ")

    # Convert EACH --section-- into (Section), preserving dashes
    def replace_double_dashes(match):
        inner = match.group(1).strip()
        return f"({inner.title()})"

    # Apply globally for all --...-- sections
    name = re.sub(r"--(.*?)--", replace_double_dashes, name)

    return name.strip().title()


def preserve_title_and_rename(folder):
    for filename in os.listdir(folder):
        if filename.startswith('.') or not filename.lower().endswith(('.mp3', '.wav', '.flac')):
            continue
        print(f"🔍 Found file: {filename}")

        filepath = os.path.join(folder, filename)
        raw_name = os.path.splitext(filename)[0]
        original_name = raw_name.replace("_", " ")  # cleaned for title
        title_tag = format_title(original_name)
        safe_name = clean_filename(raw_name)        # cleaned for filename
        ext = os.path.splitext(filename)[1].lower()
        new_path = os.path.join(folder, f"{safe_name}{ext}")

        try:
            if ext == '.mp3':
                audio = MP3(filepath, ID3=EasyID3)
                audio['title'] = title_tag
                audio.save()
            elif ext == '.flac':
                audio = FLAC(filepath)
                audio['title'] = title_tag
                audio.save()

            if filepath != new_path:
                os.rename(filepath, new_path)
                print(f"✅ Renamed: {filename} → {safe_name}{ext} (Title: {title_tag})")

        except Exception as e:
            print(f"❌ Failed to tag {filename}: {e}")

preserve_title_and_rename(AUDIO_FOLDER)
