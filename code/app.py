from flask import Flask,request
from flask_restful import Resource, Api,reqparse
from flask_jwt import JWT,jwt_required
from security import authenticate,identity
import os

app = Flask(__name__)
app.secret_key = os.environ["key"]
api = Api(app)
jwt = JWT(app,authenticate,identity)
pos = []


class Po(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='mandatory',
                        )
    parser.add_argument('timepass',
                        required=True)
    @jwt_required()
    def get(self,name):
        i = next((filter(lambda x:x["nbr"] == name,pos)),None)
        return i,200 if i else 404


    def post(self,name):
        if next((filter(lambda x:x["nbr"] == name,pos)),None) is not None:
            return {'message':'a po with number {} exists'.format(name)},400

        data = Po.parser.parse_args()

        po = {'nbr': name,'price':data['price']}
        pos.append(po)
        return po,201
    def delete(self,name):
        global pos
        pos = list(filter(lambda x:x["nbr"] != name, pos))
        return {"message":'Attched item {} is deleted'.format(name)}
    def put(self,name):

        data = Po.parser.parse_args()
        s = next((filter(lambda x:x["nbr"] == name,pos)),None)
        if s is None:
            i = {"nbr":name,"price": data["price"]}
            pos.append(i)
        else:
            s.update(data)
        return s


class Pos(Resource):
    def get(self):
        return{"pos": pos},200




api.add_resource(Po ,'/po/<string:name>')
api.add_resource(Pos ,'/pos')

app.run(port = 5000,debug= True)