import sqlite3
from flask_restful import Resource,reqparse
class User:
    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password
    @classmethod
    def find_by_username(cls,username):
        conn = sqlite3.connect('tb.db')
        cursor = conn.cursor()
        sql = "select * from users where username = ? "
        result = cursor.execute(sql,(username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        conn.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        conn = sqlite3.connect('tb.db')
        cursor = conn.cursor()
        sql = "select * from users where id = ? "
        result = cursor.execute(sql, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        conn.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='mandatory',
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='mandatory',
                        )
    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            return {"message":"User already exists"},400

        conn = sqlite3.connect("tb.db")
        cursor = conn.cursor()
        query = "Insert into users values(Null,?,?)"
        cursor.execute(query, (data['username'], data['password']))
        conn.commit()
        conn.close()

        return {"message": "user created successfully"}, 201


