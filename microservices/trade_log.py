#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import json
import os

import amqp_setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/trade_logDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class Trade_Log(db.Model):
    __tablename__ = 'trade_log'
    tradeid = db.Column(db.Integer, primary_key=True, nullable=False)
    accid = db.Column(db.Integer, nullable=False)
    trade_date = db.Column(db.DateTime, nullable=False)
    trade_value = db.Column(db.Numeric(13, 2), nullable=False)
    trade_stock_symbol = db.Column(db.String(5), nullable=False)
    trade_quantity = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    trade_action = db.Column(db.String(20), nullable=False)
    def __init__(self, tradeid, accid, trade_date, trade_value, trade_stock_symbol, trade_quantity, currency, trade_action):
        self.tradeid = tradeid
        self.accid = accid
        self.trade_date = trade_date
        self.trade_value = trade_value
        self.trade_stock_symbol = trade_stock_symbol
        self.trade_quantity = trade_quantity
        self.currency = currency
        self.trade_action = trade_action

    def json(self):
        return {
            "tradeid": self.tradeid, 
            "accid": self.accid, 
            "trade_date": self.trade_date,
            "trade_value": self.trade_value, 
            "trade_stock_symbol": self.trade_stock_symbol,
            "trade_quantity": self.trade_quantity,
            "currency": self.currency,
            "trade_action": self.trade_action
        }

monitorBindingKey = "#"

def receiveTradeLog():
    amqp_setup.check_setup()
        
    queue_name = 'trade_log'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a transaction log by " + __file__)
    processTradeLog(json.loads(body))

    print() # print a new line feed

def processTradeLog(trade):
    print("Recording a trade log:")
    print(trade)
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    trade_log = Trade_Log(tradeid=None,accID=trade["AccID"], tradeid=trade["tradeid"], trade_date=current_time, trade_value=trade["trade_value"], trade_stock_symbol=trade["trade_stock_symbol"],trade_quantity=trade["trade_quantity"],currency=trade["currency"],trade_action=trade["trade_action"] )
    db.session.add(trade_log)
    db.session.commit()
    print("Successful record transaction log into database")
#GET
# @app.route("/trade_log/all")
# def get_all():
#     trade_log_list = Trade_Log.query.all()
#     if len(trade_log_list):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "trade_logs": [trade.json() for trade in trade_log_list]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "There is no trade activity."
#         }
#     ), 404

# @app.route("/trade_log/<string:accid>")
# def find_by_accID(accid):
#     user_trade_log = Trade_Log.query.filter_by(accid=accid) #.first()
#     if user_trade_log:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": [trade.json() for trade in user_trade_log]
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "There is no trade activity."
#         }
#     ), 404

#POST
# @app.route("/trade_log/create/<string:accid>", methods=['POST'])
# def create_trade_log(accid):
#     senddata = request.get_json()
#     #Check if accID matches
#     if (str(accid) != str(senddata['accid'])):
#         return jsonify(
#             {
#                 "code": 401,
#                 "message": "Unauthorised action performed by user."
#             }
#         )
#     now = datetime.now()
#     current_time = now.strftime("%Y-%m-%d %H:%M:%S")
#     try:
#         trade_log = Trade_Log(tradeID="",accid=accid, trade_date=current_time, trade_value=senddata["trade_value"], trade_stock_symbol=str(senddata["trade_stock_symbol"]).upper(), trade_quantity=senddata["trade_quantity"], currency=str(senddata["currency"]).upper(), trade_Action=str(senddata["trade_action"]).upper())
#         db.session.add(trade_log)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "accid": accid,
#                     "data": senddata,
#                     "time":current_time
#                 },
#                 "message": "An error occurred creating trade log."
#             }
#         ), 500
#     return jsonify(
#         {
#             "code": 200,
#             "data":{
#                 "accid": accid,
#                 "data": senddata,
#                 "time":current_time
#             },
#             "message": "Trade log successfully created"
#         }
#     )

if __name__ == '__main__':
    receiveTradeLog()
    app.run(port=5003, debug=True)