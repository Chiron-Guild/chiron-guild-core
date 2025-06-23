import sqlite3
DB_PATH = "pwl_ledger.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
for row in cursor.execute("SELECT * FROM events ORDER BY timestamp DESC LIMIT 10"):
    print(row)
conn.close()