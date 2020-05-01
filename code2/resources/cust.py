from flask_jwt import jwt_required
from flask import Flask,request
from flask_restful import Resource,reqparse

from models.customer import CustModel
import json

class Cust(Resource):
    def get(self,name):
        cust = CustModel.find_by_name(name)
        if cust:
            return cust.json_t(),200
        else:
            return {"message":"resource is not found"},404
    def post(self,name):
        if CustModel.find_by_name(name):
            return {"message": "Store with name `{}` already there".format(name)}, 400
        else:
            cust1 = CustModel(name)
            try:
                cust1.save_to_db(),201
            except:
                return {"message":"couldnit create store '{}'".format(name)},500
        return cust1.json_t(),201



    def delete(self,name):
        cust = CustModel.find_by_name(name)
        if cust:
            cust.del_from_db()

        return{"message":"customer is deleted"}



class Custlist(Resource):
    def get(self):
        return{"store":list(map(lambda x:x.json_t,CustModel.query.all()))}