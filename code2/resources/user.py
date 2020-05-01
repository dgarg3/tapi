import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='wat',
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='mandatory',
                        )
    def post(self):
        data = UserRegister.parser.parse_args()
        print(data)
        if UserModel.find_by_username(data['username']):
            return {"message":"User already exists"},400

        # conn = sqlite3.connect("tb.db")
        # cursor = conn.cursor()
        # query = "Insert into users values(Null,?,?)"
        # cursor.execute(query, (data['username'], data['password']))
        # conn.commit()
        # conn.close()
        user = UserModel(**data)
        user.save_to_db()

        return user.json_t(), 201


