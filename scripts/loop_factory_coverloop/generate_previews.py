
import os
import subprocess
import pandas as pd

cover_folder = "/Users/studio/TrackstarEngine/covers"
loop_folder = "/Users/studio/TrackstarEngine/scripts/loop_factory_csv/loop_exports"
preview_folder = "cover_previews"
os.makedirs(preview_folder, exist_ok=True)

# Load loop metadata
df = pd.read_csv("loop_results.csv")

for _, row in df.iterrows():
    loop_file = row['loop_file']
    if not loop_file or "error" in row['status']:
        continue

    loop_path = os.path.join(loop_folder, loop_file)
    base_name = os.path.splitext(loop_file)[0]
    cover_guess = base_name.split("_loop")[0] + ".jpg"
    cover_path = os.path.join(cover_folder, cover_guess)

    if not os.path.exists(cover_path):
        print(f"Missing cover art: {cover_guess}")
        continue

    output_path = os.path.join(preview_folder, base_name + ".mp4")

    cmd = [
        "ffmpeg",
        "-loop", "1",
        "-i", cover_path,
        "-i", loop_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        print("Created:", output_path)
    except subprocess.CalledProcessError as e:
        print("Error creating preview for", loop_file, ":", e)
