from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

# import amqp_setup
# import pika
# import json

app = Flask(__name__)
CORS(app)

trading_acc_URL = "http://localhost:5004/trading_acc/plus"
transaction_log_URL = "http://localhost:5005/trans_log/create"
user_info_URL = "http://localhost:5006/account"
email_notification_URL = "http://localhost:5003/email_noti/send"


@app.route("/make_deposit", methods=['POST'])
def make_deposit():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            deposit = request.get_json()
            print("\nReceived an deposit in JSON:", deposit)

            # do the actual work
            # 2. Accept Deposit amount
            result = processDeposit(deposit)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "make_deposit.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processDeposit(deposit):
    # 3. Retrieve the amount trader has 
    # Invoke the user info microservice
    print('\n-----Invoking user info microservice-----')
    new_user_info_URL = user_info_URL + "/email/" + deposit["email"]
    user_info = invoke_http(new_user_info_URL, method='GET')
    print('user_info:', user_info)
    
    update_deposit = {
        "AccID" : user_info["data"]["accID"],
        "Trade_AccID" : deposit["trade_AccID"],
        "Amount" : deposit["amount"]
    }
    # 5. Update amount deposited 
    # Invoke trading account microservice
    print('\n-----Invoking trading account microservice-----')
    new_trading_acc_URL = trading_acc_URL + "/" + str(user_info["data"]["accID"])
    print(new_trading_acc_URL)
    deposit_result = invoke_http(new_trading_acc_URL, method='PUT',json= update_deposit)
    print('deposit_result:', deposit_result)
    
    deposit_log = {
        "AccID" : deposit_result["data"]["accID"], #amend data in database
        "Trade_AccID" : deposit["trade_AccID"], 
        "trade_Acc_Balance" : deposit_result["data"]["trade_Acc_Balance"],
        "Transaction_Action" : deposit["transaction_Action"],
        "Currency" : deposit["Currency"],
    }

    # 7. Sent amount deposited
    # Invoke transaction log microservice
    print('\n\n-----Publishing the (deposit info) message with routing_key=deposit.info-----') 
    new_transaction_log_URL = transaction_log_URL + "/" + str(user_info["data"]["accID"])
    invoke_http(new_transaction_log_URL, method='POST',json=deposit_result)
    # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="deposit.info", 
    #         body=message)
    print("\nDeposit action performed and updated transaction log.\n")

    # Check the deposit result; if a failure, send it to the error microservice.
    code = deposit_result["code"]
    # message = json.dumps(deposit_result)

    if code not in range(200,300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as order fails-----')
        # print('\n\n-----Publishing the (deposit error) message with routing_key=deposit.error-----')

        # # invoke_http(error_URL, method="POST", json=deposit_result)
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="deposit.error", 
        #     body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # # make message persistent within the matching queues until it is received by some receiver 
        # # (the matching queues have to exist and be durable and bound to the exchange)

        # # - reply from the invocation is not used;
        # # continue even if this invocation fails        
        # print("\nDeposit status ({:d}) published to the RabbitMQ Exchange:".format(
        #     code), deposit_result)

        # # 9. Return error
        # return {
        #     "code": 500,
        #     "data": {"deposit_log": deposit_log},
        #     "message": "Deposit action failure sent for error handling."
        # }
        pass
    else:

        # 8. Notify trader
        # Invoke email notification microservice
        # print('\n\n-----Publishing the (deposit info) message with routing_key=deposit.info-----') 
        # invoke_http(email_notification_URL, method='POST',json=deposit_result)           
        # # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="deposit.info", 
        # #     body=message)
        # print("\nDeposit action performed and notified user.\n")
        pass
    print("\nDeposit published to RabbitMQ Exchange.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails


    # 9. Return confirmation of deposit
    return {
        "code": 201,
        "data": {"deposit_log": deposit_log}
    }

if __name__ == '__main__':
    app.run(port=5000, debug=True)