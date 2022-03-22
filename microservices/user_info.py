from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/userDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    accID = db.Column(db.Integer, primary_key=True, nullable=False)
    trad_AccID = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    def __init__(self, accID, trad_AccID, name, birthdate, email, password):
        self.accID = accID
        self.trad_AccID = trad_AccID
        self.name = name
        self.birthdate = birthdate
        self.email = email
        self.password = password

    def json(self):
        return {"accID": self.accID, 
        "trad_AccID": self.trad_AccID, 
        "name": self.name, 
        "birthdate": self.birthdate,
        "email": self.email,
        "password": self.password}

@app.route("/account/all")
def get_all():
    acc_list = User.query.all()
    if len(acc_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": [user.json() for user in acc_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no user."
        }
    ), 404

# To be deleted since we are only using email
# @app.route("/account/accID/<string:accID>")
# def find_by_accID(accID):
#     user = User.query.filter_by(accID=accID).first()
#     if user:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": user.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "User not found."
#         }
#     ), 404

@app.route("/account/email/<string:email>")
def find_by_accID(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5006, debug=True)