from flask import Flask,jsonify,request,render_template

app = Flask(__name__)

stores = [
    {
        "name": "ABC",
        "items": [
            {
                "name": "test1",
                "price": "100"
            }

        ]
    },

{
        "name": "ABCD",
        "items": [
            {
                "name": "test1",
                "price": "100"
            }

        ]
    }
]



@app.route('/')  #'http://google.com/'
def home():
    return render_template('index.html')


@app.route('/store')
def get_stores():
    dict1 = {}
    x = []
    for i in stores:
        x.append(i["name"])
        dict1.update({"stores": x})
    return jsonify(dict1)

@app.route('/store',methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        "name" : request_data["name"],
        "items": []
    }
    stores.append(new_store)
    return jsonify(stores)

@app.route('/store/<string:name>')
def get_store(name):

    for i in stores:

        if i["name"] == name:
            return jsonify(i["items"])
    return jsonify("message:No Store found")

@app.route('/store/<string:name>/item',methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for i in stores:
        if i["name"] == name:
            new_item = {
                'name': request_data["name"],
                'price': request_data["price"]
            }
            i["items"].append(new_item)
            return jsonify(stores)


    return jsonify({'message':'Store not found'})







@app.route('/store/<string:name>/item')
def get_store_item(name):
    for i in stores:
        if i["name"] == name:
            return jsonify(stores['items'])
    return jsonify({'message' : 'store item not found'})







app.run(port=5000,debug = True)


