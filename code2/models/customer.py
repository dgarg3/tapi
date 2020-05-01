
from db import db
class CustModel(db.Model):
    __tablename__ = 'cust'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80))

    pos = db.relationship('PoModel',lazy = 'dynamic')


    def __init__(self,name):
        self.name = name


    def json_t(self):
        return {'name':self.name,'pos':[item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls,name):
        # conn = sqlite3.connect('tb.db')
        # cursor = conn.cursor()
        # query = "select * from items where name = ?"
        # results = cursor.execute(query, (name,))
        # row = results.fetchone()
        # conn.close()
        #
        # if row:
        #     return cls(*row)

        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def del_from_db(self):
        db.delete(self)
        db.session.commit()

    # def insert_item(self):
    #     # conn = sqlite3.connect('tb.db')
    #     # cursor = conn.cursor()
    #     # query = "insert into items values(?,?)"
    #     # cursor.execute(query, (self.name, self.price))
    #     # conn.commit()
    #     # conn.close()
    #     db.session.add(self)
    #     db.session.commit()
    #
    #
    # def update(self):
    #     conn = sqlite3.connect('tb.db')
    #     cursor = conn.cursor()
    #     query = "update items set price = ? where name = ?"
    #     cursor.execute(query, (self.name, self.price))
    #     conn.commit()
    #     conn.close()

