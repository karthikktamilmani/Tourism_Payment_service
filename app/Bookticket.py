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

app = flask.Flask(__name__)
app.config["DEBUG"] = True

logging.basicConfig(level=logging.DEBUG)

session = boto3.Session(
aws_access_key_id='ASIAVBLO43SBIV7B2RCC',
aws_secret_access_key='pfzB9Zx5jEVJMJUBN13Sh3jt1XO0yce6MmNckmVF',
aws_session_token='FwoGZXIvYXdzEHwaDEoXRzkySUxZScsH+CK+ATTCZnKnS25vecl4npjl0wp9asN/V874jJF8XxFxHuITd8/3vWNoVaFuwDXYX8nXol/QtYf3kyruYCO1Rsu7jWkbsu5KzcE/1yPgg+UIndyIxpEnkuv0VHJnHCHZRlIPT8662xlAmyINhS5qWICkPlUibU+iGL+BjUtWn01XbP5Sso1WkLLBec7mym4CJrWrhtjT9BgdyXiWuTRX/4XDw5+cM5s/nfTNEFQ89rGULNvkcnpAWgSLoNhWiSCRaxEo6bHp8wUyLQeE9j6gcyvrkQCPgJz6Lv79P25QmPs4ryyDFgezPOvi4bk+NSmyXjMrcEfn0A==',
region_name='us-east-1')

dynamodb = session.resource('dynamodb')

table = dynamodb.Table('Booking')
table2 = dynamodb.Table('Card_detail')

@app.route('/bookticket' , methods=['POST'])
def book_ticket():
    response_json = {}
    response_json["message"] = "error"
    try:
        app.logger.debug(request)
        data = request.get_json()
        # app.logger.debug("Printing")
        app.logger.debug(data)
        email = data.get("email")
        date = data.get("date")
        price = data.get("price")
        frm = data.get("from")
        to = data.get("to")
        name_on_card = data.get("name")

        payment_info = data.get("payment_info")   
        ######## nested attribute of payment_info#######
        card_number = payment_info.get("card_number")
        expiry = payment_info.get("expiry")
        cvv = payment_info.get("cvv")
        
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

        response_json["message"] = "ok"

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

        response = table2.query( KeyConditionExpression=Key('Email').eq(email) )
    
    except Exception as e:
        app.logger.debug(e)
    else:
        # lst = {}
        # for index,i in enumerate(response['Items']):
        #     lst[index] = i
        lst = []
        for i in response['Items']:
            lst.append(i)
        response_json = lst
            
    return jsonify(response_json)

app.run(host='0.0.0.0', port=8081, debug=True)
