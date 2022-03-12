from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user_stockDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User_Stock(db.Model):
    __tablename__ = 'user_stock'
    user_StockID = db.Column(db.Integer, primary_key=True, nullable=False)
    accID = db.Column(db.Integer, nullable=False)
    tradeID = db.Column(db.Integer, nullable=False)
    stock_Symbol = db.Column(db.String(5), nullable=False)
    stock_Quantity = db.Column(db.Integer, nullable=False)
    purchased_Price = db.Column(db.Numeric(13, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    def __init__(self, user_StockID, accID, tradeID, stock_Symbol, stock_Quantity, purchased_Price, currency):
        self.user_StockID = user_StockID
        self.accID = accID
        self.tradeID = tradeID
        self.stock_Symbol = stock_Symbol
        self.stock_Quantity = stock_Quantity
        self.purchased_Price = purchased_Price
        self.currency = currency

    def json(self):
        return {"user_StockID": self.user_StockID, 
        "accID": self.accID, 
        "tradeID": self.tradeID, 
        "stock_Symbol": self.stock_Symbol,
        "stock_Quantity": self.stock_Quantity,
        "purchased_Price,": self.purchased_Price,
        "currency": self.currency}

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
            "message": "There are no user stocks."
        }
    ), 404




if __name__ == '__main__':
    app.run(port=5000, debug=True)