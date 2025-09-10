import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Connect to SQLite and load logs into Pandas
conn = sqlite3.connect("logs.db")
df = pd.read_sql_query("SELECT * FROM logs", conn)

# ✅ Count logs by level
counts = df["level"].value_counts()

# --- Bar Chart ---
plt.bar(counts.index, counts.values, color="skyblue")
plt.title("Log Counts by Level")
plt.xlabel("Log Level")
plt.ylabel("Count")
plt.savefig("log_levels_bar.png")  # Save chart as image
plt.show()

conn.close()
