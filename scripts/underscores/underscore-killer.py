import os

folder_path = "/Users/studio/Public/home/assets/loops"

for filename in os.listdir(folder_path):
    if "_" in filename:
        new_name = filename.replace("_", "-")
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"✅ Renamed: {filename} → {new_name}")
