from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stock_prefDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Stock_Pref(db.Model):
    __tablename__ = 'stock_pref'
    stock_PrefID = db.Column(db.Integer, primary_key=True, nullable=False)
    accID = db.Column(db.Integer, nullable=False)
    stock_Industry = db.Column(db.String(100), nullable=False)
    def __init__(self, stock_PrefID, accID, stock_Industry):
        self.stock_PrefID = stock_PrefID
        self.accID = accID
        self.stock_Industry = stock_Industry

    def json(self):
        return {"stock_PrefID": self.stock_PrefID, 
        "accID": self.accID, 
        "stock_Industry": self.stock_Industry}

@app.route("/stock_prefall")
def get_all():
    stock_pref_list = Stock_Pref.query.all()
    if len(stock_pref_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": [stock_pref.json() for stock_pref in stock_pref_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no stock preferences."
        }
    ), 404

@app.route("/stock_pref/<string:accID>")
def find_by_accID(accID):
    user_stock_pref = Stock_Pref.query.filter_by(accID=accID) #.first()
    if user_stock_pref:
        return jsonify(
            {
                "code": 200,
                "data": [stock_pref.json() for stock_pref in user_stock_pref]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404


@app.route("/stock_pref/<string:accID>/<string:stock_Industry>", methods=['POST'])
def create_stock_pref(accID, stock_Industry):
    if (Stock_Pref.query.filter_by(accID=accID, stock_Industry=stock_Industry).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "accID": accID,
                    "stock_Industry": stock_Industry
                },
                "message": "Stock Preference already exists."
            }
        ), 400

    stock_pref = Stock_Pref(stock_PrefID='',accID=accID, stock_Industry = stock_Industry)

    try:
        db.session.add(stock_pref)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "message": "Stock preference successfully added"
                }
            }
        )
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "accID": accID,
                    "stock_Industry": stock_Industry
                },
                "message": "An error occurred creating the book."
            }
        ), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)