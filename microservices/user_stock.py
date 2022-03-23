from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user_stockDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)


class User_Stock(db.Model):
    __tablename__ = 'user_stock'
    user_stockid = db.Column(db.Integer, primary_key=True, nullable=False)
    accid = db.Column(db.Integer, nullable=False)
    tradeid = db.Column(db.Integer, nullable=False)
    stock_symbol = db.Column(db.String(5), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    purchased_price = db.Column(db.Numeric(13, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    def __init__(self, user_stockid, accid, tradeid, stock_symbol, stock_quantity, purchased_price, currency):
        self.user_stockid = user_stockid
        self.accid = accid
        self.tradeid = tradeid
        self.stock_symbol = stock_symbol
        self.stock_quantity = stock_quantity
        self.purchased_price = purchased_price
        self.currency = currency

    def json(self):
        return {
            "user_stockid": self.user_stockid, 
            "accid": self.accid, 
            "tradeid": self.tradeid, 
            "stock_symbol": self.stock_symbol,
            "stock_quantity": self.stock_quantity,
            "purchased_price,": self.purchased_price,
            "currency": self.currency
        }

#GET
@app.route("/user_stock/all")
def get_all():
    user_stock_list = User_Stock.query.all()
    if len(user_stock_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "user_stocks": [user_stock.json() for user_stock in user_stock_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No such stock found."
        }
    ), 404

@app.route("/user_stock/<string:accid>")
def find_by_accID(accid):
    user_stock_list = User_Stock.query.filter_by(accid=accid)#.first()
    if user_stock_list:
        return jsonify(
            {
                "code": 200,
                "user_stocks": [user_stock.json() for user_stock in user_stock_list]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No such stock found."
        }
    ), 404


#POST
@app.route("/user_stock/buy/<string:accid>", methods=['POST'])
def buying_user_stock(accid):
    stock_info = request.get_json()[0]["data"]
    user_info = request.get_json()[1]["data"]
    trade = request.get_json()[2]
    #Check if accID matches
    if (str(accid) != str(user_info['accid'])):
        return jsonify(
            {
                "code": 401,
                "message": "Unauthorised action performed by user."
            }
        )
    try:
        user_stock = User_Stock(user_stockid="",accid=accid, tradeid=user_info["trade_accid"], stock_symbol=str(trade["stock_symbol"]).upper(), stock_quantity=trade["stock_quantity"], purchased_price=stock_info["c"], currency=str(trade["currency"]).upper())
        db.session.add(user_stock)
        db.session.commit()
        
    except:
        
        return jsonify(
            {
                "code": 500,
                "data": {
                    "accid": accid,
                },
                "message": "An error occurred buying user stock(s)."
            }
        )
    return jsonify(
            {
                "code": 200,
                "data":{
                    "accid": accid,
                },
                "message": "User stock(s) successfully bought"
            }
    )


#DELETE
@app.route("/user_stock/sell/<string:accid>", methods=['DELETE'])
def selling_user_stock(accid):
    #Variables
    senddata = request.get_json()
    #Check if accID matches
    if (str(accid) != str(senddata['accid'])):
        return jsonify(
            {
                "code": 401,
                "message": "Unauthorised action performed by user."
            }
        )
    try:
        user_stock = User_Stock.query.filter_by(accid=accid, tradeid=senddata["tradeid"]).first()
        db.session.delete(user_stock)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "accid": accid,
                },
                "message": "An error occurred selling user stock(s)."
            }
        ), 500
    return jsonify(
            {
                "code": 200,
                "data":{
                    "accid": accid,
                },
                "message": "User stock(s) successfully sold"
            }
        )

#Need find a way to combine stocks and account for selling of all stocks


if __name__ == '__main__':
    app.run(port=5007, debug=True)