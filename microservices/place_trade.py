from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import json

app = Flask(__name__)
CORS(app)

user_info_URL = "http://localhost:5006/account"
trading_acc_URL = "http://localhost:5004/trading_acc"
stock_info_URL = "http://localhost:5001/stock_info"
trade_log_URL = "http://localhost:5003/trade_log/create"
email_notification_URL = "http://localhost:5000/email_noti/send"
error_URL = "http://localhost:5008/error"

@app.route("/place_trade", methods=['POST'])
def place_trade():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            trade = request.get_json()
            print("\nReceived an order in JSON: ", trade)

            # do the actual work
            # 1. Send trade info
            result = processPlaceTrade(trade)
            return jsonify(result), result["code"]
        
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_trade.py internal error: " + ex_str
            }), 500

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processPlaceTrade(trade):
    # 2. Retrieve stock price
    # Invoke the stock_info microservice
    print('\n-----Invoking stock_info microservice-----')
    stock_ticker = trade["stock_ticker"]
    new_stock_info_URL = stock_info_URL +  "/" + stock_ticker 
    stock_info = invoke_http(new_stock_info_URL, method='GET')
    print('stock_info', stock_info)

    trade_balance_json = {
        "Trade_AccID" : trade["trade_AccID"],
        "AccID" : trade["accID"],
        "stock_price" : stock_info["c"],
        "stockQty" : trade["stockQty"],
    }


    # 3. Update trade balance if sufficient
    # Invoke the trading_acc microservice
    print('\n\n-----Invoking trading_acc microservice-----')
    new_trade_acc_URL = trading_acc_URL + "/" + str(trade["accID"])
    trade_balance_result = invoke_http(new_trade_acc_URL, method='PUT', json=trade_balance_json)
    print('trade_balance' , trade_balance_result)

    # Check the trade balance result; if a failure, send it to error microservice
    code = trade_balance_result["code"]
    if code not in range(200, 300):
        print('\n\n-----Invoking error microservice as order fails-----')
        invoke_http(error_URL, method="POST", json=trade_balance_result)
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("Trade status ({:d}) sent to the error microservice:".format(
            code), trade_balance_result)

        # Return error
        return {
            "code": 500,
            "data": {"trade_balance_result": trade_balance_result},
            "message": "Trade creation failure sent for error handling."
        }
    
    trade_log_json = {
        "AccID" : trade["accID"],
        "Trade_Value" : stock_info["c"] * trade["stockQty"],
        "Trade_Stock_Symbol" : trade["stock_ticker"],
        "Trade_Quantity" : trade["stockQty"],
        "Currency" : trade["currency"],
        "Trade_Action" : trade["Trade_Action"]
    }
    # 4. Record trade activity
    # Invoke the trade_log microservice
    print('\n\n-----Invoking trade_log microservice-----')
    new_trade_log_URL = trade_log_URL + '/' + str(trade["accID"])
    trade_log_result = invoke_http(new_trade_log_URL, method='POST', json=trade_log_json)
    code = trade_log_result["code"]
    print('trade_log_result' , trade_log_result)
    if code not in range(200, 300):
        print('\n\n-----Invoking error microservice as order fails-----')
        invoke_http(error_URL, method="POST", json=trade_log_result)
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("Trade status ({:d}) sent to the error microservice:".format(
            code), trade_log_result)

        # Return error
        return {
            "code": 500,
            "data": {"trade_log_result": trade_log_result},
            "message": "Trade Log failure sent for error handling."
        }
    
    email_notification_json = {
        "Email" : trade["Email"],
        "Subject" : "Update on your trading status",
        "Content" : trade_log_result["message"],
    }
    #5. Send trade confirmation
    # Invoke email_notification microservice
    print('\n\n-----Invoking email_notification microservice-----')
    email_notification_result = invoke_http(email_notification_URL, method='POST', json=email_notification_json)
    code = int(email_notification_result["code"])
    print('email_notification_result' , email_notification_result)
    
    if code not in range(200, 300):
        print('\n\n-----Invoking error microservice as order fails-----')
        invoke_http(error_URL, method="POST", json=email_notification_result)
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("Trade status ({:d}) sent to the error microservice:".format(
            code), email_notification_result)

        # Return error
        return {
            "code": 500,
            "data": {"email_notification_result": email_notification_result},
            "message": "Email notification encounter failure sent for error handling."
        }

    return {
        "code": 201,
        "data" : {
            "stock_info" : stock_info,
            "trade_balance_result" : trade_balance_result,
            "trade_log_result" : trade_log_result,
            "email_notification_result" : email_notification_result,
        }
    }


if __name__ == '__main__':
    app.run(port=5100, debug=True)
