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

#GET
@app.route("/stock_pref/all")
def get_all():
    stock_pref_list = Stock_Pref.query.all()
    if len(stock_pref_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "stock preferences": [stock_pref.json() for stock_pref in stock_pref_list]
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
            "message": "Stock preferences not found."
        }
    ), 404


#POST
@app.route("/stock_pref/add/<string:accID>", methods=['POST'])
def create_stock_pref(accID):
    #Variables
    to_add_list, added_list, success_list, error_list  = [], [], [], []
    senddata = request.get_json()

    #Check if accID matches
    if (str(accID) != str(senddata['AccID'])):
        return jsonify(
            {
                "code": 401,
                "message": "Unauthroised action performed by user."
            }
        )
    #Loop thru items in preferences
    for stock_Industry in senddata['Stock_Industry']:
        stock_Industry = str(stock_Industry).capitalize()
        if (Stock_Pref.query.filter_by(accID=accID, stock_Industry=stock_Industry).first()):
            added_list.append(stock_Industry)
        else:
            to_add_list.append(stock_Industry)
    #If there is an item in preference that is added before, return
    if len(added_list):
        return jsonify(
                {
                    "code": 400,
                    "data": {
                        "accID": accID,
                        "stock_Industry": added_list
                    },
                    "message": "Stock(s) preference already exists. Please remove added stock(s) preference"
                }
            ), 400
    #Loop thru items in to_add_list
    for stock_Industry in to_add_list:
        stock_Industry = str(stock_Industry).capitalize()
        try:
            stock_pref = Stock_Pref(stock_PrefID='',accID=accID, stock_Industry = stock_Industry)
            db.session.add(stock_pref)
            db.session.commit()
            success_list.append(stock_Industry)
        except:
            error_list.append(stock_Industry)
    
    #If there are errors and success items, delete success list and try all again
    if (len(error_list)) and (len(success_list)):
        #delete success_list
        for success in success_list:
            stock_pref = Stock_Pref.query.filter_by(accID=accID, stock_Industry=success).first()
            db.session.delete(stock_pref)
            db.session.commit()
        return jsonify(
            {
                "code": 500,
                "data": {
                    "accID": accID,
                    "stock_Industry": error_list
                },
                "message": "An error occurred adding the stock(s) preference. Please try adding the same preferences again."
            }
        ), 500
    #If all have errors
    elif (len(error_list)) and (not len(success_list)):
        return jsonify(
            {
                "code": 500,
                "data": {
                    "accID": accID,
                    "stock_Industry": error_list
                },
                "message": "An error occurred adding the stock preference."
            }
        ), 500
    #If all successfully added
    else:
        return jsonify(
            {
                "code": 200,
                "data":{
                    "accID": accID,
                    "stock_Industry": success_list
                },
                "message": "Stock preference successfully added"
            }
        )


#DELETE
@app.route("/stock_pref/remove/<string:accID>", methods=['DELETE'])
def delete_stock_pref(accID):
    #Variables
    deleted_list, error_list = [], []
    senddata = request.get_json()

    #Check if accID matches
    if (str(accID) != str(senddata['AccID'])):
        return jsonify(
            {
                "code": 401,
                "message": "Unauthroised action performed by user."
            }
        )
    #Loop thru items in preferences
    for stock_Industry in senddata["Stock_Industry"]:
        stock_Industry = str(stock_Industry).capitalize()
        stock_pref = Stock_Pref.query.filter_by(accID=accID, stock_Industry=stock_Industry).first()
        if stock_pref:
            db.session.delete(stock_pref)
            db.session.commit()
            deleted_list.append(stock_Industry)
        else:
            #If error occured
            error_list.append(stock_Industry)
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "accID": accID,
                        "stock_Industry": stock_Industry
                    },
                    "message": "Stock preference not found."
                }
            ), 404
    #If successfully deleted
    if len(deleted_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "accID": accID,
                    "stock_Industry": deleted_list
                },
                "message": "Stock preference successfully deleted."
            }
        )

if __name__ == '__main__':
    app.run(port=5000, debug=True)