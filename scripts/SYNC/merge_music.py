import pandas as pd
import sqlite3

# === 1. Load Notion CSV ===
notion_df = pd.read_csv("notion_export.csv")
notion_df.columns = [col.strip() for col in notion_df.columns]
notion_df = notion_df.rename(columns={
    "Title": "title",
    "Audio Filename": "filename",
    "album_artist": "album_artist"
})
notion_df['title_lower'] = notion_df['title'].str.lower()

# === 2. Load Mixxx SQLite DB ===
conn = sqlite3.connect("mixxxdb.sqlite")
query = """
SELECT
    id, title, artist, album, album_artist, genre, grouping, composer,
    bpm, key, duration, comment, rating, coverart_location, color
FROM library
"""
mixxx_df = pd.read_sql_query(query, conn)
conn.close()
mixxx_df['title_lower'] = mixxx_df['title'].str.lower()

# === 3. Merge ===
merged_df = pd.merge(mixxx_df, notion_df, on='title_lower', how='outer', suffixes=('_mixxx', '_notion'))
merged_df.drop(columns=['title_lower'], inplace=True)

# === 4. Save result ===
# Clean up duplicated fields
final_df = mixxx_df.copy()

# Overwrite or fill from Notion where available
for col in ['groove', 'rhythm density', 'phrase length', 'percussive shape', 'energy level',
            'Cover Art Filename', 'filename', 'Mood', 'grouping', 'rating']:
    if col in notion_df.columns:
        notion_col = notion_df.set_index('title_lower')[col]
        final_df[col] = final_df['title_lower'].map(notion_col)

# Save cleaned result
final_df.drop(columns=['title_lower'], inplace=True)
final_df.to_csv("music_catalog_cleaned.csv", index=False)
print("✅ Cleaned catalog saved to music_catalog_cleaned.csv")

