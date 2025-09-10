import sqlite3
import csv
import re
import os

# Folder containing logs
LOG_FOLDER = "logs"

# Connect to SQLite
conn = sqlite3.connect("logs.db")
cursor = conn.cursor()

# Drop old table (to avoid duplicates on rerun)
cursor.execute("DROP TABLE IF EXISTS logs")
cursor.execute("""
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    level TEXT,
    message TEXT,
    source_file TEXT
)
""")

# Regex for parsing
pattern = r"\[(.*?)\]\s+(INFO|ERROR|WARNING|DEBUG|CRITICAL):\s+(.*)"

# Process all log files in the folder
for filename in os.listdir(LOG_FOLDER):
    if filename.endswith(".log"):
        filepath = os.path.join(LOG_FOLDER, filename)
        with open(filepath, "r") as f:
            for line in f:
                match = re.match(pattern, line)
                if match:
                    timestamp, level, message = match.groups()
                    cursor.execute(
                        "INSERT INTO logs (timestamp, level, message, source_file) VALUES (?, ?, ?, ?)",
                        (timestamp, level, message, filename)
                    )

conn.commit()

# Export to CSV
cursor.execute("SELECT timestamp, level, message, source_file FROM logs")
rows = cursor.fetchall()

with open("logs.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "level", "message", "source_file"])
    writer.writerows(rows)

# Show counts
cursor.execute("SELECT level, COUNT(*) FROM logs GROUP BY level")
print("Log counts by level:", cursor.fetchall())

print("✅ Logs from all files in 'logs/' inserted into logs.db and exported to logs.csv")

conn.close()
