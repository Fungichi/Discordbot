import sqlite3


conn = sqlite3.connect('stats.sql')
cursor = conn.cursor()
input = input("stats or transactions: ")

if input == "transactions":
    cursor.execute('SELECT * FROM transaction_logs')


    rows = cursor.fetchall()


    for row in rows:
        print(row)

elif input == "stats":
    cursor.execute('SELECT * FROM user_stats')


    rows = cursor.fetchall()


    for row in rows:
        print(row)
else:
    print("Invalid choice")

conn.close()
