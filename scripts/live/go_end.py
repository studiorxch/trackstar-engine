# go_end.py — Shuts down Mixxx, OBS stream, and web server after scheduled stream

import subprocess
import time
import os
from obswebsocket import obsws, requests

# === CONFIG ===
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = "Oy05IW88uJ8yN7M6"
WEB_SERVER_PORT = "8080"

# === FUNCTIONS ===
def stop_obs_stream():
    try:
        ws = obsws(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD)
        ws.connect()
        ws.call(requests.StopStreaming())
        ws.disconnect()
        print("🛑 OBS stream stopped.")
    except Exception as e:
        print(f"⚠️ Failed to stop OBS stream: {e}")

def kill_process_by_name(name):
    subprocess.call(["pkill", "-f", name])
    print(f"❌ Killed process matching: {name}")

def shutdown_services():
    kill_process_by_name("Mixxx")
    kill_process_by_name("http.server")
    kill_process_by_name("mixxx_metadata_tracker_nowpatch.py")

if __name__ == "__main__":
    print("⏹ Ending StudioRich stream...")
    stop_obs_stream()
    time.sleep(2)
    shutdown_services()
    print("✅ Stream shutdown complete.")
