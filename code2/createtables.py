import sqlite3
conn = sqlite3.connect("tb.db")
query = ["create table if not exists users(id INTEGER PRIMARY KEY,username text,password text)",
         "create table if not exists items(name text,price real)", "insert into items values('test',208)"]
cursor = conn.cursor()
for i in query:
    cursor.execute(i)
    conn.commit()
conn.close()
