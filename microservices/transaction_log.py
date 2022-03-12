from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

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
    def __init__(self, transactionID, accID, trade_AccID, transaction_Action, transaction_Value, transaction_Date):
        self.transactionID = transactionID
        self.accID = accID
        self.trade_AccID = trade_AccID
        self.transaction_Action = transaction_Action
        self.transaction_Value = transaction_Value
        self.transaction_Date = transaction_Date

    def json(self):
        return {"transactionID": self.transactionID, 
        "accID": self.accID, 
        "trade_AccID": self.trade_AccID,
        "transaction_Action": self.transaction_Action, 
        "transaction_Value": self.transaction_Value,
        "transaction_Date": self.transaction_Date}

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






if __name__ == '__main__':
    app.run(port=5000, debug=True)