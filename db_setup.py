import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('stats.sql')
cursor = conn.cursor()

# Create table for user balances
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_stats (
    username TEXT PRIMARY KEY,
    aura INTEGER NOT NULL DEFAULT 0,
    tokens INTEGER NOT NULL DEFAULT 500
)
''')

# Create table for transaction logs
cursor.execute('''
CREATE TABLE IF NOT EXISTS transaction_logs (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_name TEXT NOT NULL,
    receiver_name TEXT NOT NULL,
    amount INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    description TEXT
)
''')
print("ran the file")
conn.commit()
conn.close()

