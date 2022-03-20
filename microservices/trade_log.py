from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/trade_logDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class Trade_Log(db.Model):
    __tablename__ = 'trade_log'
    tradeID = db.Column(db.Integer, primary_key=True, nullable=False)
    accID = db.Column(db.Integer, nullable=False)
    trade_Date = db.Column(db.DateTime, nullable=False)
    trade_Value = db.Column(db.Numeric(13, 2), nullable=False)
    trade_Stock_Symbol = db.Column(db.String(5), nullable=False)
    trade_Quantity = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    trade_Action = db.Column(db.String(20), nullable=False)
    def __init__(self, tradeID, accID, trade_Date, trade_Value, trade_Stock_Symbol, trade_Quantity, currency, trade_Action):
        self.tradeID = tradeID
        self.accID = accID
        self.trade_Date = trade_Date
        self.trade_Value = trade_Value
        self.trade_Stock_Symbol = trade_Stock_Symbol
        self.trade_Quantity = trade_Quantity
        self.currency = currency
        self.trade_Action = trade_Action

    def json(self):
        return {"tradeID": self.tradeID, 
        "accID": self.accID, 
        "trade_Date": self.trade_Date,
        "trade_Value": self.trade_Value, 
        "trade_Stock_Symbol": self.trade_Stock_Symbol,
        "trade_Quantity": self.trade_Quantity,
        "currency": self.currency,
        "trade_Action": self.trade_Action}

#GET
@app.route("/trade_log/all")
def get_all():
    trade_log_list = Trade_Log.query.all()
    if len(trade_log_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "trade_logs": [trade.json() for trade in trade_log_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no trade activity."
        }
    ), 404

@app.route("/trade_log/<string:accID>")
def find_by_accID(accID):
    user_trade_log = Trade_Log.query.filter_by(accID=accID) #.first()
    if user_trade_log:
        return jsonify(
            {
                "code": 200,
                "data": [trade.json() for trade in user_trade_log]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no trade activity."
        }
    ), 404

#POST
@app.route("/trade_log/create/<string:accID>", methods=['POST'])
def create_trade_log(accID):
    senddata = request.get_json()
    #Check if accID matches
    if (str(accID) != str(senddata['AccID'])):
        return jsonify(
            {
                "code": 401,
                "message": "Unauthorised action performed by user."
            }
        )
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    try:
        trade_log = Trade_Log(tradeID="",accID=accID, trade_Date=current_time, trade_Value=senddata["Trade_Value"], trade_Stock_Symbol=senddata["Trade_Stock_Symbol"], trade_Quantity=senddata["Trade_Quantity"], currency=senddata["Currency"], trade_Action=senddata["Trade_Action"])
        db.session.add(trade_log)
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
                "message": "An error occurred creating trade log."
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
            "message": "Trade log successfully created"
        }
    )

if __name__ == '__main__':
    app.run(port=5003, debug=True)