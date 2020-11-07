from flask import Flask,request
from flask import jsonify
import firebase_admin
from firebase_admin import credentials,firestore
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Headout-App")
import json
app = Flask(__name__)

cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
product_ref = db.collection('products')

@app.route('/')
def index():
    return "Hello World"


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
def sign_up():
    data = request.json
    try:
        vendorId = int(data['vendorId'])
        location = geolocator.geocode(data['vendorAddress'])
        data['vendorLatitude'] = location.latitude
        data['vendorLongitude'] = location.longitude
        vendors.document(str(vendorId)).set(data)
        return jsonify({"success":True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
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


@app.route('/login',methods=['GET'])
def login():
    data = request.json
    try:
        vendorId = int(data['vendorId'])
        vendor = vendors.document(str(vendorId)).get().to_dict()
        print(vendor)
        if vendor == None:
            return {"success":False,"details":"Vendor does not exist"}, 404
        else:
            actualPassword = vendor['vendorPassword']
            sentPassword = data['senderPassword']
            if actualPassword == sentPassword:
                return {"success":True,"vendorId":vendor['vendorId'],"vendorEmail":vendor['vendorEmail']}, 200
            else:
                return {"success":False, "details":"Invalid password"}, 200

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
def getAllOrders():
    args = request.args
    orders = db.collection('orders')
    
    try:
        vendorOrderCollection = orders.document(args['vendorId']).collection('orders')
        all_vendor_orders = [order.to_dict() for order in vendorOrderCollection.stream()]
        return jsonify(all_vendor_orders),200
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
def markProcessed():
    vendorId = request.args['vendorId']
    orderId = request.args['orderId']
    orders = db.collection('orders')
    
    try:
        allOrders = orders.document(vendorId).collection('orders')
        allOrders.document(orderId).update({"orderProcessed":True})
        return {"success":True}, 200
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
def specificOrder():
    vendorId = request.args['vendorId']
    orderId = request.args['orderId']
    orders = db.collection('orders')
    
    try:
        allOrders = orders.document(vendorId).collection('orders')
        order = allOrders.document(orderId).get().to_dict()
        return jsonify(order), 200
    except Exception as e:
        return f"An Error Occured: {e}"



if __name__ == '__main__':
    app.run(debug=True)