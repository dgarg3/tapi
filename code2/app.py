from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate,identity as identity_function
from resources.user import UserRegister
from resources.po import Po,Pos
import os
import jsonify

app = Flask(__name__)
app.secret_key = os.environ["key"]
api = Api(app)
jwt = JWT(app,authenticate,identity_function)





api.add_resource(Po ,'/po/<string:name>')
api.add_resource(Pos ,'/pos')
api.add_resource(UserRegister,'/register')

app.run(port = 5000,debug= True)