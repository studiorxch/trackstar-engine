import sqlite3

DB_PATH = "/Users/studio/Library/Containers/org.mixxx.mixxx/Data/Library/Application Support/Mixxx/mixxxdb.sqlite"

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()

    if tables:
        print("📋 Tables found in Mixxx DB:")
        for t in tables:
            print(" -", t[0])
    else:
        print("⚠️ No tables found. The database may not be initialized yet.")

except Exception as e:
    print(f"❌ Failed to read database: {e}")
