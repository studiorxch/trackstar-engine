# 🎛️ Trackstar Engine

Welcome to the StudioRich Trackstar Engine — your modular music identity and drop system. This structure supports the full lifecycle of a track, from cataloging and cover art to social media presence, bundles, and Twitch streaming.

## Folder Breakdown

### `/catalog/`
Your central `track_catalog.csv` lives here. It contains metadata like track name, mood, cover file, theme, and download status.

### `/covers/`
Square album art for each track (1024x1024 recommended). Used in posts, OBS, and store listings.

### `/audio/`
Final FLAC/MP3 audio files for cataloged tracks.

### `/bundles/`
ZIP bundles of tracks + art + extras. For Gumroad, Ko-fi, etc.

### `/social_posts/`
Auto-generated social media content (text/image pairs) for IG, Pinterest, Threads.

### `/scripts/`
Python/Node scripts to auto-generate bundles, update OBS, sync with Notion or Twitch, etc.

---

This system is built for automation, presence, and style.
