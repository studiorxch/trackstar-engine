#!/bin/bash

################################################################################
# convert_covers_to_webp.sh
#
# Description:
#   This script converts all JPG and JPEG album cover images from your
#   playlist_generator/backend/covers folder into optimized WebP format for use
#   on the StudioRich Jekyll site.
#
#   It saves the output to: /Users/studio/Public/home/assets/covers
#
# Usage:
#   1. Place this file anywhere (e.g., inside playlist_generator).
#   2. Run once anytime new covers are added:
#        chmod +x convert_covers_to_webp.sh
#        ./convert_covers_to_webp.sh
#
# Requirements:
#   - ffmpeg must be installed and accessible from your terminal
#
# Notes:
#   - Output filenames keep the original name (e.g., chill-wave.jpg → chill-wave.webp)
#   - Add slugifying if needed later to match _tracks/ format
################################################################################

SOURCE_DIR="/Users/studio/playlist_generator/backend/covers"
DEST_DIR="/Users/studio/Public/home/assets/covers"

mkdir -p "$DEST_DIR"

for file in "$SOURCE_DIR"/*.{jpg,jpeg,JPG,JPEG}; do
  [ -e "$file" ] || continue
  base=$(basename "$file")
  name="${base%.*}"
  # Replace underscores with hyphens for web-safe output
  hyphen_name="${name//_/-}"
  ffmpeg -i "$file" -qscale 90 "$DEST_DIR/$hyphen_name.webp"
done

echo "✅ WebP conversion complete. Files saved to: $DEST_DIR"
