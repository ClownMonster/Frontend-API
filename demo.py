from flask import Flask,request
from flask import jsonify
import firebase_admin
from firebase_admin import credentials,firestore

import json
app = Flask(__name__)

cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
product_ref = db.collection('products')

@app.route('/')
def index():
    return "Hello World"

@app.route('/addProduct',methods=['POST'])
def postProduct():
    productDetails = request.json
    try:
        id = productDetails['productId']
        product_ref.document(id).set(productDetails)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/updateProduct',methods=['PUT'])
def updateProduct():
    productDetails = request.json
    try:
        id = productDetails['productId']
        product_ref.document(id).update(productDetails)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/deleteProduct',methods=['DELETE'])
def deleteProduct():
    deleteId = request.json['id']
    try:
        product_ref.document(deleteId).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/getProduct',methods=['GET'])
def getProduct():
    productId = request.json['id']
    try:
        ans = product_ref.document(productId).get()
        return jsonify(ans.to_dict()), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/getAllProducts',methods=['GET'])
def getAllProducts():
    try:
        all_products = [product.to_dict() for product in product_ref.stream()]
        return jsonify(all_products),200
    except Exception as e:
        return f"An Error Occured: {e}"


from flask import Flask,request
from flask import jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/aboutMe')
def home():

    ans = {
        "name":"raghav",
        "age":20,
        "hobbies":["travelling","coding"],
        "education":[
            {
                "education":"HACS",
                "year":2015
            },
            {
                "education":"DDPS",
                "year":2017
            },
            {
                "education":"MSRIT",
                "year":2021
            }
        ]
    }
    return jsonify(ans)


@app.route('/performingOps')
def performOps():
    # For the request arguments
    args = request.args
    a = int(args['a'])
    b = int(args['b'])
    #For body
    body = request.json
    operation = body['operation']
    if operation == '+':
        return {"ans":a+b}
    elif operation == '*':
        return {"ans":a*b}
    elif operation == '-':
        return {"ans":a-b}
    elif operation == '/':
        return {"ans":a/b}
    else:
        return "Invalid operation"

@app.route('/requests',methods=['GET','POST'])
def requestType():
    if request.method == 'GET':
        return {"ans":"It is a GET request"}
    else:
        return {"ans":"It is a POST request"}


if __name__ == '__main__':
    app.run(debug=True)