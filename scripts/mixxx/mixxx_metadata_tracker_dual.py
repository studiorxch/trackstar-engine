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
LAST_COVER_PATH = "/Users/studio/Public/Ramen/last_art.jpg"
NOWPLAYING_JSON = "/Users/studio/Public/Ramen/nowplaying.json"
AUDIO_DIR = "/Users/studio/TrackstarEngine/audio"
DEFAULT_COVER = "/Users/studio/Public/Ramen/default_cover.jpg"

# === STATE ===
last_track_id = None
last_data = {"title": "", "artist": "", "album": "", "cover": ""}

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

def extract_cover(audio_path, save_path):
    try:
        if audio_path.lower().endswith(".flac"):
            audio = FLAC(audio_path)
            for pic in audio.pictures:
                Image.open(io.BytesIO(pic.data)).save(save_path)
                return True
        else:
            audio = MutagenFile(audio_path)
            if hasattr(audio, "tags") and isinstance(audio.tags, ID3):
                for tag in audio.tags.values():
                    if isinstance(tag, APIC):
                        Image.open(io.BytesIO(tag.data)).save(save_path)
                        return True
    except Exception as e:
        print(f"⚠️ Cover extract error: {e}")
    if os.path.exists(DEFAULT_COVER):
        Image.open(DEFAULT_COVER).save(save_path)
    return False

def get_dominant_color(image_path):
    try:
        img = Image.open(image_path).convert('RGB').resize((50, 50))
        pixels = list(img.getdata())
        most_common = Counter(pixels).most_common(1)[0][0]
        return list(most_common)
    except:
        return [255, 255, 255]

def write_nowplaying(now, now_cover, last, last_cover):
    data = {
        "now": {
            "title": now["title"],
            "artist": now["artist"],
            "album": now["album"],
            "cover": f"http://localhost:8080/{os.path.basename(now_cover)}",
            "color": get_dominant_color(now_cover)
        },
        "last": {
            "title": last["title"],
            "artist": last["artist"],
            "album": last["album"],
            "cover": f"http://localhost:8080/{os.path.basename(last_cover)}",
            "color": get_dominant_color(last_cover)
        }
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
                # move current to last
                extract_cover(os.path.join(AUDIO_DIR, os.path.basename(location)), OBS_COVER_PATH)
                last_data["title"] = last_data.get("title", "")
                last_data["artist"] = last_data.get("artist", "")
                last_data["album"] = last_data.get("album", "")
                if os.path.exists(OBS_COVER_PATH):
                    Image.open(OBS_COVER_PATH).save(LAST_COVER_PATH)

                now_data = {"title": title, "artist": artist, "album": album}
                write_nowplaying(now_data, OBS_COVER_PATH, last_data, LAST_COVER_PATH)
                last_data = now_data
                last_track_id = track_id
        time.sleep(5)
