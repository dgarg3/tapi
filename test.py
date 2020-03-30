import sqlite3

conn = sqlite3.connect('dt.db')

cursor = conn.cursor()

create_table = "create table users (id int, username text, passd text)"

cursor.execute(create_table)

user = ( 1,'ab','ab')

users = [
( 1,'bob','asdf'),
( 2,'bob1','asdf'),
( 3,'abcd','abcd')
]
insert_query = "insert into users values(?,?,?)"
cursor.executemany(insert_query,users)
select_query = "select * from users"

for row in cursor.execute(select_query):
    print(row)

conn.commit()

conn.close()


