from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/transaction_logDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Trans_Log(db.Model):
    __tablename__ = 'transaction_log'
    transactionID = db.Column(db.Integer, primary_key=True, nullable=False)
    accID = db.Column(db.Integer, nullable=False)
    trade_AccID = db.Column(db.Integer, nullable=False)
    transaction_Action = db.Column(db.String(20), nullable=False)
    transaction_Value = db.Column(db.Numeric(13, 2), nullable=False)
    transaction_Date = db.Column(db.DateTime, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    def __init__(self, transactionID, accID, trade_AccID, transaction_Action, transaction_Value, transaction_Date, currency):
        self.transactionID = transactionID
        self.accID = accID
        self.trade_AccID = trade_AccID
        self.transaction_Action = transaction_Action
        self.transaction_Value = transaction_Value
        self.transaction_Date = transaction_Date
        self.currency = currency

    def json(self):
        return {"transactionID": self.transactionID, 
        "accID": self.accID, 
        "trade_AccID": self.trade_AccID,
        "transaction_Action": self.transaction_Action, 
        "transaction_Value": self.transaction_Value,
        "transaction_Date": self.transaction_Date,
        "currency": self.currency}

#GET
@app.route("/trans_log/all")
def get_all():
    trans_log_list = Trans_Log.query.all()
    if len(trans_log_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "trans_logs": [trans.json() for trans in trans_log_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no transaction activity."
        }
    ), 404

@app.route("/trans_log/<string:accID>")
def find_by_accID(accID):
    user_transaction_log = Trans_Log.query.filter_by(accID=accID) #.first()
    if user_transaction_log:
        return jsonify(
            {
                "code": 200,
                "data": [trans.json() for trans in user_transaction_log]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no transaction activity."
        }
    ), 404


#POST
@app.route("/trans_log/create/<string:accID>", methods=['POST'])
def create_trade_log(accID):
    senddata = request.get_json()
    #Check if accID matches
    if (str(accID) != str(senddata['AccID'])):
        return jsonify(
            {
                "code": 401,
                "message": "Unauthroised action performed by user."
            }
        )
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        trans_log = Trans_Log(transactionID="",accID=accID, trade_AccID=senddata["Trade_AccID"], transaction_Action=str(senddata["Transaction_Action"]).upper(), transaction_Value=senddata["Transaction_Value"], transaction_Date=current_time, currency= str(senddata["Currency"]).upper())
        db.session.add(trans_log)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "accID": accID,
                    "data": senddata,
                    "time":current_time
                },
                "message": "An error occurred creating transaction log."
            }
        ), 500
    return jsonify(
        {
            "code": 200,
            "data":{
                "accID": accID,
                "data": senddata,
                "time":current_time
            },
            "message": "transaction log successfully created"
        }
    )


if __name__ == '__main__':
    app.run(port=5000, debug=True)