import os
import time
import sqlite3
import json
import io
from mutagen.flac import FLAC
from mutagen.id3 import ID3, APIC
from mutagen import File as MutagenFile
from PIL import Image
from collections import Counter

# === CONFIG ===
DB_PATH = "/Users/studio/Library/Containers/org.mixxx.mixxx/Data/Library/Application Support/Mixxx/mixxxdb.sqlite"
OBS_COVER_PATH = "/Users/studio/Public/Ramen/current_art.jpg"
NOWPLAYING_JSON = "/Users/studio/Public/Ramen/nowplaying.json"
AUDIO_DIR = "/Users/studio/TrackstarEngine/audio"
DEFAULT_COVER = "/Users/studio/Public/Ramen/default_cover.jpg"

# === STATE ===
last_track_id = None

# === FUNCTIONS ===

def get_last_played_track():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT library.id, track_locations.location, library.title, library.artist, library.album
            FROM library
            JOIN track_locations ON library.location = track_locations.id
            WHERE library.title IS NOT NULL
            ORDER BY library.last_played_at DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        conn.close()
        return result if result else None
    except Exception as e:
        print(f"❌ DB error: {e}")
        return None

def extract_cover(audio_path):
    try:
        if audio_path.lower().endswith(".flac"):
            audio = FLAC(audio_path)
            for pic in audio.pictures:
                Image.open(io.BytesIO(pic.data)).save(OBS_COVER_PATH)
                return True
        else:
            audio = MutagenFile(audio_path)
            if hasattr(audio, "tags") and isinstance(audio.tags, ID3):
                for tag in audio.tags.values():
                    if isinstance(tag, APIC):
                        Image.open(io.BytesIO(tag.data)).save(OBS_COVER_PATH)
                        return True
    except Exception as e:
        print(f"⚠️ Cover extract error: {e}")
    if os.path.exists(DEFAULT_COVER):
        Image.open(DEFAULT_COVER).save(OBS_COVER_PATH)
    return False

def get_dominant_color(image_path):
    try:
        img = Image.open(image_path).convert('RGB').resize((50, 50))
        pixels = list(img.getdata())
        most_common = Counter(pixels).most_common(1)[0][0]
        return list(most_common)
    except:
        return [255, 255, 255]

def write_nowplaying(title, artist, album):
    color = get_dominant_color(OBS_COVER_PATH)
    data = {
        "title": title,
        "artist": artist,
        "album": album,
        "cover": f"http://localhost:8080/{os.path.basename(OBS_COVER_PATH)}",
        "color": color
    }
    with open(NOWPLAYING_JSON, "w") as f:
        json.dump(data, f, indent=2)
    print("📝 nowplaying.json updated.")

# === MAIN LOOP ===
if __name__ == "__main__":
    print("🔄 Mixxx metadata tracker started...")
    while True:
        current = get_last_played_track()
        if current:
            track_id, location, title, artist, album = current
            if track_id != last_track_id:
                print(f"🎶 Now Playing: {artist} – {title}")
                last_track_id = track_id
                audio_path = os.path.join(AUDIO_DIR, os.path.basename(location))
                if extract_cover(audio_path):
                    print("🖼️ Cover art updated.")
                else:
                    print("⚠️ No embedded cover found. Using fallback.")
                write_nowplaying(title, artist, album)
        time.sleep(5)
