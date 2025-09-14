import librosa
import soundfile as sf
import os

INPUT_FILE = "input_audio/Broadcast-Error-Loop.wav"
OUTPUT_FOLDER = "loops"

# Load track
y, sr = librosa.load(INPUT_FILE, sr=None)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

# 4-bar loop = 16 beats
loop_length = 16
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for i in range(0, len(beats) - loop_length, loop_length):
    start_sample = librosa.frames_to_samples(beats[i])
    end_sample = librosa.frames_to_samples(beats[i + loop_length])
    loop_audio = y[start_sample:end_sample]
    
    loop_file = os.path.join(OUTPUT_FOLDER, f"loop_{i//loop_length+1}.wav")
    sf.write(loop_file, loop_audio, sr)
    print(f"Saved: {loop_file}")
