from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.user import UserRegister
from resources.po import Po,Pos
from resources.cust import Cust,Custlist
from security import authenticate,identity as identity_function

import os
import jsonify

app = Flask(__name__)
app.secret_key = os.environ["key"]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app,authenticate,identity_function)


api.add_resource(Po ,'/po/<string:name>')
api.add_resource(Pos ,'/pos')
api.add_resource(UserRegister,'/register')
api.add_resource(Cust ,'/cust/<string:name>')
api.add_resource(Custlist ,'/custlist')
if __name__=='__main__':
    from db import db
    db.init_app(app)
app.run(port = 5000,debug= True)