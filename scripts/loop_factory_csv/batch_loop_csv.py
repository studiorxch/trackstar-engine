
import os
import numpy as np
import librosa
import soundfile as sf
import pandas as pd

np.complex = complex  # Patch for librosa

csv_path = "track_loop_list.csv"
input_folder = "input_audio"
output_folder = "loop_exports"
os.makedirs(output_folder, exist_ok=True)

loop_length = 16
df = pd.read_csv(csv_path)

results = []

for index, row in df.iterrows():
    filename = row['filename']
    full_path = os.path.join(input_folder, filename)
    try:
        y, sr = librosa.load(full_path, sr=None)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        for i in range(0, min(len(beats) - loop_length, 32), loop_length):
            start = librosa.frames_to_samples(beats[i])
            end = librosa.frames_to_samples(beats[i + loop_length])
            loop = y[start:end]
            loop_name = f"{os.path.splitext(filename)[0]}_loop_{i//loop_length+1}.wav"
            loop_path = os.path.join(output_folder, loop_name)
            sf.write(loop_path, loop, sr)
            results.append({
                "filename": filename,
                "loop_file": loop_name,
                "status": "success"
            })
    except Exception as e:
        results.append({
            "filename": filename,
            "loop_file": "",
            "status": f"error: {str(e)}"
        })

# Save results
pd.DataFrame(results).to_csv("loop_results.csv", index=False)
print("Loop processing complete.")
