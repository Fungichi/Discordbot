import sqlite3

conn = sqlite3.connect('stats.sql')
cursor = conn.cursor()


cursor.execute('UPDATE user_stats SET tokens = 500')
conn.commit()
conn.close()

print("All tokens are now set to 500")