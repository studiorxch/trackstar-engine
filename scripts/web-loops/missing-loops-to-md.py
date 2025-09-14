import os

# Adjust these paths to match your system
md_folder = "/Users/studio/Public/home/_tracks"  # folder with your .md files
mp3_folder = "/Users/studio/Public/home/assets/loops"  # folder with your .mp3 loop files

# Get list of expected filenames based on .md files
md_slugs = [os.path.splitext(f)[0] for f in os.listdir(md_folder) if f.endswith('.md')]
expected_mp3s = [f"{slug}-loop.mp3" for slug in md_slugs]

# Get actual .mp3 filenames
actual_mp3s = set(os.listdir(mp3_folder))

# Compare and find missing
missing = [f for f in expected_mp3s if f not in actual_mp3s]

print(f"🎧 Total .md files: {len(md_slugs)}")
print(f"🎵 Total .mp3 loops: {len(actual_mp3s)}")
print(f"❌ Missing ({len(missing)}):")
for m in missing:
    print(" -", m)
