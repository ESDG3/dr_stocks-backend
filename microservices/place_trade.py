from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

# import amqp_setup
# import pika
import json

app = Flask(__name__)
CORS(app)

user_info_URL = "http://localhost:5006/account"
trading_acc_URL = "http://localhost:5004/trading_acc/minus/"
stock_info_URL = "http://localhost:5001/stock_info"
trade_log_URL = "http://localhost:5003/trade_log/create"
email_notification_URL = "http://localhost:5000/email_noti/send"
user_stock_URL = "http://localhost:5007/user_stock/buy"


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


#trade {
#   "email" : "abc@gmail.com".
#   "stock_symbol" : "AAPL"
#   "stock_qty" : 5
#   "currency" : "USD"
# }
def processPlaceTrade(trade):

    # 2.Retrieve trade_accid
    # Inoke the user_info microservice
    print('\n-----Invoking user_info microservice-----')
    new_user_info_URL = user_info_URL + '/email/' + trade["email"]
    user_info = invoke_http(new_user_info_URL, method='GET')
    print('user_info', user_info)
    # 3. Retrieve stock price
    # Invoke the stock_info microservice
    print('\n-----Invoking stock_info microservice-----')
    new_stock_info_URL = stock_info_URL +  "/" + trade["stock_symbol"] 
    stock_info = invoke_http(new_stock_info_URL, method='GET')
    print('stock_info', stock_info)
    # 4. Update trade balance if sufficient
    # Invoke the trading_acc microservice
    print('\n\n-----Invoking trading_acc microservice-----')
    new_trade_acc_URL = trading_acc_URL + str(user_info["data"]["accid"])
    trade_balance_result = invoke_http(new_trade_acc_URL, method='PUT', json= [stock_info, user_info, trade])
    print('trade_balance_result' , trade_balance_result)

    # Check the trade balance result; if a failure, send it to error microservice
    code = trade_balance_result["code"]
    message = json.dumps(trade_balance_result)
    if code not in range(200, 300):

        print('\n\n-----Publishing the (trade_log) message with routing_key = trade_log.trade-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="trade_log.trad", body=message, properties=pika.BasicProperties(delivery_mode = 2))
        print("\nTrade status ({:d}) published to the RabbitMQ Exchange:".format(
            code), trade_balance_result)
        

        print('\n\n-----Publishing the (order error) message with routing_key=trade_balance.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="trade_balance.error", body=message, properties=pika.BasicProperties(delivery_mode = 2))
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("\nTrade status ({:d}) published to the RabbitMQ Exchange:".format(
            code), trade_balance_result)

        # Return error
        return {
            "code": 500,
            "data": {"trade_balance_result": trade_balance_result},
            "message": "Trade creation failure sent for error handling."
        }
    
    print('\n-----Invoking user_stock microservice-----')
    new_user_stock_URL = user_stock_URL + '/' + str(user_info["data"]["accid"])
    user_stock_result = invoke_http(new_user_stock_URL, method='POST', json= [stock_info, user_info, trade])
    print('user_stock_result' , user_stock_result)


    # 5. Record trade activity
    # Invoke the trade_log microservice
    print('\n\n-----Invoking trade_log microservice-----')
    new_trade_log_URL = trade_log_URL + '/' + str(user_info["data"]["accid"])
    trade_log_result = invoke_http(new_trade_log_URL, method='POST', json=[user_info, stock_info, trade])
    print('trade_log_result' , trade_log_result)
    
    code = trade_log_result["code"]
    message = json.dumps(trade_balance_result)
    
    if code not in range(200, 300):
        print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="trade_log.error", body=message, properties=pika.BasicProperties(delivery_mode = 2))
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), trade_balance_result)

        # Return error
        return {
            "code": 500,
            "data": {"trade_balance_result": trade_balance_result},
            "message": "Trade creation failure sent for error handling."
        }
    
    email_notification_json = {
        "Email" : trade["Email"],
        "Subject" : "Update on your trading status",
        "Content" : trade_log_result["message"],
    }
    #6. Send trade confirmation
    # Invoke email_notification microservice
    print('\n\n-----Invoking email_notification microservice-----')
    email_notification_result = invoke_http(email_notification_URL, method='POST', json=email_notification_json)
    code = int(email_notification_result["code"])
    print('email_notification_result' , email_notification_result)
    
    if code not in range(200, 300):
        print('\n\n-----Publishing the (order error) message with routing_key=email_notification.error-----')
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="email_notification.error", body=message, properties=pika.BasicProperties(delivery_mode = 2))
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), trade_balance_result)

        # Return error
        return {
            "code": 500,
            "data": {"trade_balance_result": trade_balance_result},
            "message": "Trade creation failure sent for error handling."
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
