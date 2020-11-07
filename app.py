from flask import Flask,request
from flask import jsonify
import firebase_admin
from firebase_admin import credentials,firestore
from geopy.geocoders import Nominatim

from flask_cors import CORS,cross_origin

geolocator = Nominatim(user_agent="Headout-App")
import json
app = Flask(__name__)
CORS(app)
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
product_ref = db.collection('products')

@app.route('/')
def index():
    response =  jsonify("Hello World")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


'''

    Sign Up API 
        1. This is to sign up the user.
        2. Data it receives (json)
            vendorName : name (string)
            vendorId: id (int)
            vendorGovRegsNumber: number(int)
            vendorPassword: password(string)
            vendorAddress: address(string)
            vendorEmail: email(string)
            vendorNumber: number(int)
        3. Returns
            Success/Error
    
'''
vendors = db.collection('vendors')
@app.route('/signup',methods=['POST'])
@cross_origin()
def sign_up():
    data = request.json
    print(data)
    print("ji")
    try:
        print("hello")
        vendorId = int(data['vendorId'])
        print(vendorId)
        location = geolocator.geocode(data['vendorAddress'])
        print(location)
        data['vendorLatitude'] = location.latitude
        data['vendorLongitude'] = location.longitude
        vendors.document(str(vendorId)).set(data)
        response = jsonify({"success":True})
        return response
    except Exception as e:
        return f"An Error Occured: {e}",404
    
'''

    Log In API:
        1. This is the LogIn API
        2. Data it receives 
            vendorId : vendorId(string)
            vendorPassword: password(string)
        3. Returns (json)
            success -> True/False
            if success == True
                returns "vendorId"
            else:
                returns "details"
'''


@app.route('/login',methods=['GET','POST'])
@cross_origin()
def login():
    data = request.json
    try:
        vendorId = int(data['vendor_id'])
        vendor = vendors.document(str(vendorId)).get().to_dict()
        print(vendor)
        if vendor == None:
            return {"success":False,"details":"Vendor does not exist"}, 404
        else:
            actualPassword = vendor['vendorPassword']
            sentPassword = data['password']
            if actualPassword == sentPassword:
                response =  jsonify({"success":True,"vendorId":vendor['vendorId'],"vendorEmail":vendor['vendorEmail'],"vendorName":vendor['vendorName']})
                return response
            else:
                response =  jsonify({"success":False, "details":"Invalid password"})
                return response
    except Exception as e:
        return f"An Error Occured: {e}"


'''
    1.This API returns all the orders that a vendor has.
    2. API receives as a query parameter
        the vendorId
    3. Based on the vendorId it receives all the orders in JSON format
        {
            "orders":[
                {
                    "orderId":1234(integer)
                    "orderBy":name(string)
                    "orderAddress":address(string)
                    "orderPhoneNo":83848529439(int)
                    "orderProcessed":false(boolean)
                },
                {

                    "orderId":1235(integer)
                    "orderBy":name(string)
                    "orderAddress":address(string)
                    "orderPhoneNo":83848529439(int)
                    "orderProcessed":false(boolean)
                },
                {

                    "orderId":1236(integer)
                    "orderBy":name(string)
                    "orderAddress":address(string)
                    "orderPhoneNo":83848529439(int)
                    "orderProcessed":false(boolean)
                }
            ]
        }


'''
@app.route('/getAllOrders',methods=['GET'])
@cross_origin()
def getAllOrders():
    args = request.args
    orders = db.collection('orders')
    
    try:
        vendorOrderCollection = orders.document(args['vendorId']).collection('orders')
        all_vendor_orders = [order.to_dict() for order in vendorOrderCollection.stream()]
        response = jsonify(all_vendor_orders)
        return response
    except Exception as e:
        return f"An Error Occured: {e}"

'''
    1. API to mark dispatched
    2. Receives
        vendorId
        orderId
    3. returns response success or not


'''
@app.route('/markProcessed',methods=['GET'])
@cross_origin()
def markProcessed():
    vendorId = request.args['vendorId']
    orderId = request.args['orderId']
    orders = db.collection('orders')
    
    try:
        allOrders = orders.document(vendorId).collection('orders')
        allOrders.document(orderId).update({"orderProcessed":True})
        response = jsonify({"success":True})
        return response
    except Exception as e:
        return f"An Error Occured: {e}"

'''

    1. An API to get details of a particular order.
    2. receives
        orderId -> orderId(int)
        vendorId -> vendorId(int)
    3. Retruns details fo particular order
        {
            "orderDetails":[
                Array of orders -> This is the order
            ]
        }
'''
@app.route('/specificOrder')
@cross_origin()
def specificOrder():
    vendorId = request.args['vendorId']
    orderId = request.args['orderId']
    orders = db.collection('orders')
    
    try:
        allOrders = orders.document(vendorId).collection('orders')
        order = allOrders.document(orderId).get().to_dict()
        response = jsonify(order)
        return response
    except Exception as e:
        return f"An Error Occured: {e}"



if __name__ == '__main__':
    app.run(debug=True,port=8080)