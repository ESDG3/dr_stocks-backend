from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/trade_logDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Trade_Log(db.Model):
    __tablename__ = 'trade_log'
    tradeID = db.Column(db.Integer, primary_key=True, nullable=False)
    accID = db.Column(db.Integer, nullable=False)
    trade_Date = db.Column(db.DateTime, nullable=False)
    trade_Value = db.Column(db.Numeric(13, 2), nullable=False)
    trade_Stock_Symbol = db.Column(db.String(5), nullable=False)
    trade_Quantity = db.Column(db.Integer, nullable=False)
    def __init__(self, tradeID, accID, trade_Date, trade_Value, trade_Stock_Symbol, trade_Quantity):
        self.tradeID = tradeID
        self.accID = accID
        self.trade_Date = trade_Date
        self.trade_Value = trade_Value
        self.trade_Stock_Symbol = trade_Stock_Symbol
        self.trade_Quantity = trade_Quantity

    def json(self):
        return {"tradeID": self.tradeID, 
        "accID": self.accID, 
        "trade_Date": self.trade_Date,
        "trade_Value": self.trade_Value, 
        "trade_Stock_Symbol": self.trade_Stock_Symbol,
        "trade_Quantity": self.trade_Quantity}

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
            "message": "There are no trade activity."
        }
    ), 404






if __name__ == '__main__':
    app.run(port=5000, debug=True)