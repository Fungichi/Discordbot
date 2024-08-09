import sqlite3


conn = sqlite3.connect('stats.sql')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
num = 0
print("-"*20)
for num,table in enumerate(tables):
    print(f'[{num}] {table}')
print("-"*20)
try:
    input = int(input("index: "))
    table = tables[input][0]
    query = f'SELECT * FROM {table}'
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except(ValueError):
    print("Invalid input")
conn.close()
