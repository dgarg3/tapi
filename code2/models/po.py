import sqlite3
class PoModel:
    def __init__(self,name,price):
        self.name = name
        self.price = price

    def json(self):
        return {'name':'self.name','price':'self.price'}

    @classmethod
    def find_by_name(cls,name):
        conn = sqlite3.connect('tb.db')
        cursor = conn.cursor()
        query = "select * from items where name = ?"
        results = cursor.execute(query, (name,))
        row = results.fetchone()
        conn.close()

        if row:
            return cls(*row)


    def insert_item(self):
        conn = sqlite3.connect('tb.db')
        cursor = conn.cursor()
        query = "insert into items values(?,?)"
        cursor.execute(query, (self.name, self.price))
        conn.commit()
        conn.close()


    def update(self):
        conn = sqlite3.connect('tb.db')
        cursor = conn.cursor()
        query = "update items set price = ? where name = ?"
        cursor.execute(query, (self.name, self.price))
        conn.commit()
        conn.close()

