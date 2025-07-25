# init_db.py
import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()

# Create table (drop if already exists)
c.execute("DROP TABLE IF EXISTS checkins")

# Recreate with full schema
c.execute("""
    CREATE TABLE checkins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place_id TEXT,
        wait_minutes INTEGER,
        timestamp TEXT,
        temp_c REAL,
        condition TEXT,
        is_day INTEGER
    )
""")

conn.commit()
conn.close()
print("✅ checkins table created successfully.")
