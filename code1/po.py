from flask_jwt import jwt_required
from flask import Flask,request
from flask_restful import Resource,reqparse
import sqlite3


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
        item = self.find_by_name(name)
        if item:
            return item
        return {'message':'po not found'},404


       ## i = next((filter(lambda x:x["nbr"] == name,pos)),None)
        ##return i,200 if i else 404
    @classmethod
    def find_by_name(cls,name):
        conn = sqlite3.connect('tb.db')
        cursor = conn.cursor()
        query = "select * from items where name = ?"
        results = cursor.execute(query, (name,))
        row = results.fetchone()
        conn.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
    @classmethod
    def insert_item(cls,po):
        conn = sqlite3.connect('tb.db')
        cursor = conn.cursor()
        query = "insert into items values(?,?)"
        cursor.execute(query, (po["nbr"], po["price"]))
        conn.commit()
        conn.close()

    def post(self,name):
        data = Po.parser.parse_args()
        po = {'nbr': name, 'price': data['price']}
        if self.find_by_name(name):
            return {'message':'a po with number {} exists'.format(name)},400
        try:
            self.insert_item(po)
        except:
            return {"message":"An error occured inserting the item"},500

        return po,201

        # if next((filter(lambda x:x["nbr"] == name,pos)),None) is not None:
        #     return {'message':'a po with number {} exists'.format(name)},400
        #
        # data = Po.parser.parse_args()
        #
        # po = {'nbr': name,'price':data['price']}
        # pos.append(po)
        # return po,201

    def delete(self,name):
        if self.find_by_name(name):
            conn = sqlite3.connect('tb.db')
            curs = conn.cursor()
            query = "delete from items where name = ?"
            curs.execute(query,(name,))
            conn.commit()
            conn.close()
            return {"message":"Item {} is deleted".format(name)},200
        return {"message":"Item {} doesnt exist".format(name)}

        # global pos
        # pos = list(filter(lambda x:x["nbr"] != name, pos))
        # return {"message":'Attched item {} is deleted'.format(name)}



    def put(self,name):

        data = Po.parser.parse_args()
        item =  self.find_by_name(name)
        update_item = {"name":name,"price":data["price"]}
        if item is None:
            try:
                self.insert_item(update_item)
            except:
                return{"message":"An error occured"},500
        else:
            try:
                self.update(update_item)
            except:
                return {"message": "An error occured"}, 500
        return update_item

        # s = next((filter(lambda x:x["nbr"] == name,pos)),None)
        # if s is None:
        #     i = {"nbr":name,"price": data["price"]}
        #     pos.append(i)
        # else:
        #     s.update(data)
        # return s

    @classmethod
    def update(cls,item):
        conn = sqlite3.connect('tb.db')
        cursor = conn.cursor()
        query = "update items set price = ? where name = ?"
        cursor.execute(query,(item["price"],item["name"]))
        conn.commit()
        conn.close()



class Pos(Resource):
    def get(self):
        conn = sqlite3.connect("tb.db")
        cursor = conn.cursor()
        query = "select * from items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({"name":row[0],"price":row[1]})
        conn.commit()
        conn.close()

        return{"iems": items},200