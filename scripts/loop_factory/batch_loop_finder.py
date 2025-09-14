import os
import numpy as np
import librosa
import soundfile as sf

np.complex = complex  # Patch for librosa

input_folder = "/Users/studio/TrackstarEngine/scripts/loop_factory/input_audio"
output_folder = "/Users/studio/Public/home/assets/loops/"
os.makedirs(output_folder, exist_ok=True)

loop_length = 16
for file in os.listdir(input_folder):
    if file.endswith((".wav", ".flac", ".mp3")):
        y, sr = librosa.load(os.path.join(input_folder, file), sr=None)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        for i in range(0, min(len(beats) - loop_length, 32), loop_length):
            start = librosa.frames_to_samples(beats[i])
            end = librosa.frames_to_samples(beats[i + loop_length])
            loop = y[start:end]
            out_file = f"{os.path.splitext(file)[0]}_loop_{i//loop_length+1}.wav"
            sf.write(os.path.join(output_folder, out_file), loop, sr)
            print("Saved:", out_file)
