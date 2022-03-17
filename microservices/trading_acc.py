from locale import currency
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/trading_accDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Trading_Acc(db.Model):
    __tablename__ = 'trading_acc'
    trade_AccID = db.Column(db.Integer, primary_key=True, nullable=False)
    accID = db.Column(db.Integer, nullable=False)
    trade_Acc_Balance = db.Column(db.Numeric(13, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    def __init__(self, trade_AccID, accID, trade_Acc_Balance, currency):
        self.trade_AccID = trade_AccID
        self.accID = accID
        self.trade_Acc_Balance = trade_Acc_Balance
        self.currency = currency

    def json(self):
        return {"trade_AccID": self.trade_AccID, 
        "accID": self.accID, 
        "trade_Acc_Balance": self.trade_Acc_Balance,
        "currency": self.currency}


#GET
@app.route("/trading_acc/all")
def get_all():
    trading_acc_list = Trading_Acc.query.all()
    if len(trading_acc_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "trading_accounts": [trading_acc.json() for trading_acc in trading_acc_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no trading accounts."
        }
    ), 404

@app.route("/trading_acc/<string:accID>/<string:currency>")
def find_by_accID(accID, currency):
    trading_acc = Trading_Acc.query.filter_by(accID=accID, currency=currency).first()
    if trading_acc:
        return jsonify(
            {
                "code": 200,
                "data": trading_acc.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Trading account not found."
        }
    ), 404


#POST
@app.route("/trading_acc/create/<string:accID>", methods=['POST'])
def create_trading_acc(accID):
    senddata = request.get_json()
    #Check if accID matches
    if (str(accID) != str(senddata['AccID'])):
        return jsonify(
            {
                "code": 401,
                "message": "Unauthroised action performed by user."
            }
        )
    currency = str(senddata["Currency"]).upper()
    result = Trading_Acc.query.filter_by(accID=accID, currency=currency).first()
    if result:
        trade_acc_ID = result.json()['trade_AccID']
        return jsonify(
            {
                "code": 400,
                "data": {
                    "trade_acc_ID": trade_acc_ID,
                    "accID": accID,
                    "currency": currency
                },
                "message": "Trading account already exists."
            }
        ), 400
    trading_acc = Trading_Acc(trade_AccID='',accID=accID, trade_Acc_Balance = 0.0, currency=currency)
    try:
        db.session.add(trading_acc)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "message": "Trading account successfully created"
                }
            }
        )
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "accID": accID
                },
                "message": "An error occurred creating a trading account."
            }
        ), 500



#PUT
@app.route("/trading_acc/update/<string:accID>", methods=['PUT'])
def update_book(accID):
    senddata = request.get_json()
    #Check if accID matches
    if (str(accID) != str(senddata['AccID'])):
        return jsonify(
            {
                "code": 401,
                "message": "Unauthroised action performed by user."
            }
        )
    currency = str(senddata['Currency']).upper()
    new_amt = senddata['Trade_Acc_Balance']
    if "." not in str(new_amt):
        new_amt = float(str(new_amt).strip() + ".00")
    trading_acc = Trading_Acc.query.filter_by(accID=accID,currency=currency).first()
    if trading_acc:
        if (senddata['AccID'] == trading_acc.accID) and (currency == trading_acc.currency):
            trading_acc.trade_Acc_Balance = new_amt
            try:    
                db.session.commit()
                return jsonify(
                    {
                        "code": 200,
                        "data": trading_acc.json(),
                        "message": "Successfully updated trading account balance."
                    }
                )
            except:
                return jsonify(
                    {
                        "code": 500,
                        "data": trading_acc.json(),
                        "message": "An error occurred updating account balance. No changes has been made."
                    }
                )
    return jsonify(
        {
            "code": 404,
            "data": {
                "accID": accID
            },
            "message": "Trading account not found."
        }
    ), 404



#DELETE
@app.route("/trading_acc/delete/<string:accID>", methods=['DELETE'])
def delete_trading_acc(accID):
    senddata = request.get_json()
    #Check if accID matches
    if (str(accID) != str(senddata['AccID'])):
        return jsonify(
            {
                "code": 401,
                "message": "Unauthroised action performed by user."
            }
        )
    currency = str(senddata["Currency"]).upper()
    trading_acc = Trading_Acc.query.filter_by(accID=accID, currency=currency).first()
    trading_acc_id = trading_acc.trade_AccID
    try:
        db.session.delete(trading_acc)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "message": "Trading account successfully deleted",
                    "Trading_acc_id": trading_acc_id
                }
            }
        )
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "Trading_acc_id": trading_acc_id
                },
                "message": "An error occurred deleting trading account."
            }
        ), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)



