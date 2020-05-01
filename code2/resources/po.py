from flask_jwt import jwt_required
from flask import Flask,request
from flask_restful import Resource,reqparse

from models.po import PoModel
import json


class Po(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',

                        required=True)
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='mandatory',
                        )
    parser.add_argument('cust_id',
                        type=int,
                        required=True,
                        help='customer id',
                        )

    @jwt_required()
    def get(self,name):
        item = PoModel.find_by_name(name)
        if item:
            #return json.dumps(item.__dict__)
            return item.json_t()
        return {'message':'po not found'},404






    def post(self,name):
        if PoModel.find_by_name(name):
            return {'message':'a po with number {} exists'.format(name)},400
        data = Po.parser.parse_args()
        po1 = PoModel( **data)
        try:
            po1.save_to_db()
        except:
            return {"message":"An error occured inserting the item"},500
        print(type(po1))

        print({"message":"here is the {}".format(name)})
        #return json.dumps(po1.__dict__),201
        return {"message":"here is the {}".format(name)}, 201





    def delete(self,name):
        po = PoModel.find_by_name(name)
        if po:
            po.del_frm_db()
        # if PoModel.find_by_name(name):
        #     conn = sqlite3.connect('tb.db')
        #     curs = conn.cursor()
        #     query = "delete from items where name = ?"
        #     curs.execute(query,(name,))
        #     conn.commit()
        #     conn.close()
            return {"message":"Item {} is deleted".format(name)},200
        return {"message":"Item {} doesnt exist".format(name)}

        # global pos
        # pos = list(filter(lambda x:x["nbr"] != name, pos))
        # return {"message":'Attched item {} is deleted'.format(name)}



    def put(self,name):

        data = Po.parser.parse_args()
        item = PoModel.find_by_name(name)
        # update_item = PoModel(name, data['price'])
        if item is None:
            try:
                item = PoModel(name, data['price'],data['cust_id'])
            except:
                return{"message":"An error occured"},500
        else:
            try:
                item.price = data['price']



                # update_item.update()

            except:
                return {"message": "An error occured"}, 500
        item.save_to_db()
        return item.json_t()







class Pos(Resource):
    def get(self):
        x = PoModel.query.all()
        # conn = sqlite3.connect("tb.db")
        # cursor = conn.cursor()
        # query = "select * from items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({"name":row[0],"price":row[1]})
        # conn.commit()
        # conn.close()

        #return {"items":[item.json_t() for item in PoModel.query.all()]},200
        return{"items":list(map(lambda x:x.json_t(),PoModel.query.all()))}