from app import app, encoder, helper
import logging
import flask
from flask import request, jsonify
from datetime import datetime
import json
import time
import base64
import boto3
from boto3.dynamodb.conditions import Key, Attr
from random import randint

# app = flask.Flask(__name__)
# app.config["DEBUG"] = True

logging.basicConfig(level=logging.DEBUG)

session = boto3.Session(
aws_access_key_id='ASIAVBLO43SBDJCVMVPJ',
aws_secret_access_key='G2lBrd+OIi0rqXmkqUwuXiudtqRdTvm5M/Dm4Yvo',
aws_session_token='FwoGZXIvYXdzEK///////////wEaDDZLNPI49fTwo6TMfiK+AawwbftpiNdPkVXm5kJi8lxhhKlRCLiph+fkRBxiab5aaGF8TkpHmzzDxm9qUbLEsBYn4rBtqFHiGzxgPXFfP5xQhiXeoeB0tTLN26rgKkW/kaUfS7G63JNUggTU7VFCQmjflAM911eCHc95mdVF7IFeuqJ3ta98Dg9/psNVoCiHRFSN9yEmNwTc8HmMOT7qCIpxB1eiUjrjuMCzwuDcL/g+pHA7Ud+rCjNjwy3kim29mu0TOnBHal08ssKsMoco/rP08wUyLZRpoWu3bmLK4Uw2rKLqlEKrzBHYhri5n0Xww0rQygpZo6lk4n+FFHYDLxt27Q==',
region_name='us-east-1')

dynamodb = session.resource('dynamodb')

table = dynamodb.Table('Booking')
table2 = dynamodb.Table('Card_detail')

def b64decoding(value,requestObj=None):
        return base64.b64decode(value).decode("ascii")

def getDataFromRequest(dataObj,keyValue,requestObj=None):
    if dataObj is not None:
        return base64.b64decode(dataObj.get(keyValue)).decode("ascii")
    else:
        return base64.b64decode(request.args.get(keyValue)).decode("ascii")

@app.route('/bookticket' , methods=['POST'])
def book_ticket():
    response_json = {}
    response_json["message"] = "error"
    try:
        app.logger.debug(request)
        data = request.get_json()

        # app.logger.debug("Printing")
        app.logger.debug(data)
        email = getDataFromRequest(dataObj=data,keyValue="email")
        date = getDataFromRequest(dataObj=data,keyValue="date")
        price = getDataFromRequest(dataObj=data,keyValue="price")
        frm = getDataFromRequest(dataObj=data,keyValue="from")
        to = getDataFromRequest(dataObj=data,keyValue="to")
        name_on_card = getDataFromRequest(dataObj=data,keyValue="name")
        # email = data.get("email")
        # date = data.get("date")
        # price = data.get("price")
        # frm = data.get("from")
        # to = data.get("to")
        # name_on_card = data.get("name")

        payment_info = getDataFromRequest(dataObj=data,keyValue="payment_info")   
        ######## nested attribute of payment_info#######
        card_number = getDataFromRequest(dataObj=payment_info,keyValue="card_number")
        card_number = helper.encryptValue(card_number)
        expiry = getDataFromRequest(dataObj=payment_info,keyValue="expiry")
        expiry = helper.encryptValue(expiry)
        cvv = getDataFromRequest(dataObj=payment_info,keyValue="cvv")
        
        if encoder.check_validity_token(request.headers['token'],email):
            response_json["message"] = "ok"
        
        # Print out some data about the table.
        # This will cause a request to be made to DynamoDB and its attribute
        # values will be set based on the response.
        app.logger.debug(table.creation_date_time)
        ##
        # tempid = datetime.utcnow().strftime('%f')[:-3]
        tempid = randint(0, 100000)
        # insert values into the database and return message
        table.put_item(
            Item={
                'ID' : tempid, 
                'email' : email,
                'date' : date,
                'price' : price,
                'from': frm,
                'to': to,
            }
        )

        table2.put_item(
            Item={
                'Email' : email,
                'Name' : name_on_card,
                'Card' : card_number,
                'Expiry' : expiry,
            }
        )

    except Exception as e:
        app.logger.debug(e)
    
    return json.dumps(response_json)

@app.route('/bookticket/carddetails/<email>' , methods=['GET'])
def card_details(email):
    response_json = {}
    response_json["message"] = "error"
    try:
        app.logger.debug(request)
        # data = request.get_json()
        # app.logger.debug(data)

        #email = data.get("email")
        email = b64decoding(email)

        if encoder.check_validity_token(request.headers['token'],email):
            response_json["message"] = "ok"

        response = table2.query( KeyConditionExpression=Key('Email').eq(email) )
        
        # lst = {}
        # for index,i in enumerate(response['Items']):
        #     lst[index] = i
        lst = []
        for i in response['Items']:
            i = helper.decryptValue(i['Card'])
            i = helper.decryptValue(i['Expiry'])
            lst.append(i)
        response_json = lst

    except Exception as e:
        app.logger.debug(e)
            
    return jsonify(response_json)
