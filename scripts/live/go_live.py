# go_live.py — Automates Twitch stream startup (adds web server for widget display)

import subprocess
import time
import requests as http
import json
import sqlite3
import os
from obswebsocket import obsws, requests

# === CONFIG ===
M3U_PLAYLIST = "/Users/studio/TrackstarEngine/playlists/lofi_morning_monday.m3u"
MIDIXX_PATH = "/Applications/Mixxx.app/Contents/MacOS/mixxx"
MIXXX_ARGS = [MIDIXX_PATH]
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = "Oy05IW88uJ8yN7M6"
OBS_SCENE = "Start"
MIXXX_DB = "/Users/studio/Library/Containers/org.mixxx.mixxx/Data/Library/Application Support/Mixxx/mixxxdb.sqlite"
AUTODJ_TRIGGER_SCRIPT = "/Users/studio/TrackstarEngine/scripts/auto_dj_trigger.applescript"
WEB_SERVER_DIR = "/Users/studio/Public/Ramen"
WEB_SERVER_PORT = "8080"

# === TWITCH AUTH ===
TWITCH_CLIENT_ID = "gp762nuuoqcoxypju8c569th9wz7q5"
TWITCH_OAUTH_TOKEN = "hoy4u4fzm2orbb3wb6dqx3x35yzz3k"
TWITCH_CHANNEL_ID = 652015218  

# === STREAM INFO ===
STREAM_TITLE = "☕ Lo-Fi Stranger Vibes - Live from StudioRich"
STREAM_CATEGORY = "Music"
STREAM_TAGS = ["Lofi", "Chillhop", "Relax", "Radio", "Music", "Study", "DJ", "Sleep", "StrangerVibes", "Evening" ]

# === FUNCTIONS ===
def load_playlist_into_autodj():
    if not os.path.exists(M3U_PLAYLIST):
        print(f"❌ Playlist file not found: {M3U_PLAYLIST}")
        return

    conn = sqlite3.connect(MIXXX_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Playlists WHERE name='Auto DJ'")
    result = cursor.fetchone()
    if not result:
        print("❌ 'Auto DJ' playlist not found in Mixxx DB.")
        conn.close()
        return
    playlist_id = result[0]
    cursor.execute("DELETE FROM PlaylistTracks WHERE playlist_id=?", (playlist_id,))

    with open(M3U_PLAYLIST, "r") as f:
        tracks = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    position = 0
    for track_path in tracks:
        basename = os.path.basename(track_path)
        cursor.execute("SELECT id FROM track_locations WHERE location LIKE ?", (f"%{basename}",))
        track_row = cursor.fetchone()
        if track_row:
            track_id = track_row[0]
            cursor.execute("INSERT INTO PlaylistTracks (playlist_id, track_id, position) VALUES (?, ?, ?)", (playlist_id, track_id, position))
            position += 1
        else:
            print(f"⚠️ Track not found in Mixxx library: {basename}")

    conn.commit()
    conn.close()
    print("🎶 Playlist injected into Auto DJ queue.")

def start_mixxx():
    print("🎧 Launching Mixxx...")
    subprocess.Popen(MIXXX_ARGS)
    time.sleep(10)
    trigger_autodj_play()

def trigger_autodj_play():
    if os.path.exists(AUTODJ_TRIGGER_SCRIPT):
        print("▶️ Triggering Auto DJ via AppleScript...")
        subprocess.Popen(["osascript", AUTODJ_TRIGGER_SCRIPT])
    else:
        print("⚠️ Auto DJ trigger script not found.")

def start_web_server():
    print(f"🌐 Starting web server in {WEB_SERVER_DIR} on port {WEB_SERVER_PORT}...")
    subprocess.Popen(
        ["python3", "-m", "http.server", WEB_SERVER_PORT],
        cwd=WEB_SERVER_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def switch_obs_scene_and_stream():
    try:
        ws = obsws(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD)
        ws.connect()
        ws.call(requests.SetCurrentScene(sceneName=OBS_SCENE))
        ws.call(requests.StartStreaming())
        ws.disconnect()
        print(f"🎬 OBS scene switched and stream started: {OBS_SCENE}")
    except Exception as e:
        print(f"⚠️ OBS scene or stream start failed: {e}")

def start_metadata_tracker():
    print("📡 Starting metadata tracker...")
    subprocess.Popen(["python3", "/Users/studio/TrackstarEngine/scripts/mixxx_metadata_tracker_nowpatch.py"])

def update_twitch_stream():
    headers = {
        "Authorization": f"Bearer {TWITCH_OAUTH_TOKEN}",
        "Client-Id": TWITCH_CLIENT_ID,
        "Content-Type": "application/json"
    }
    body = {
        "title": STREAM_TITLE,
        "game_id": get_music_category_id(headers)
    }
    url = f"https://api.twitch.tv/helix/channels?broadcaster_id={TWITCH_CHANNEL_ID}"
    response = http.patch(url, headers=headers, json=body)
    if response.status_code == 204:
        print("📝 Twitch stream title/category updated.")
    else:
        print("❌ Failed to update Twitch stream info:", response.text)

def get_music_category_id(headers):
    response = http.get("https://api.twitch.tv/helix/games?name=Music", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            return data["data"][0]["id"]
    return ""

if __name__ == "__main__":
    print("🚀 Starting StudioRich Go-Live Protocol")
    start_mixxx()
    time.sleep(7)
    load_playlist_into_autodj()
    start_web_server()
    switch_obs_scene_and_stream()
    start_metadata_tracker()
    update_twitch_stream()
    print("✅ Go-live complete. Stream is rolling!")
