from flask import Flask, render_template, request, jsonify
from pycaret import classification
from dotenv import load_dotenv
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import numpy as np
import pandas as pd
import requests
import os

load_dotenv()

app = Flask(__name__, template_folder="client/dist", static_folder="client/dist/static")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('CLEARDB_DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

model = classification.load_model(model_name='decision_tree_1')
columns = ["ID", "Age", "Experience", "Income", "ZIP Code", "Family", "CCAvg", "Education", "Mortgage",
           "Securities Account",
           "CD Account", "Online", "CreditCard"]

db = SQLAlchemy(app)


@app.route('/api/prediction', methods=['POST'])
def prediction():
    data = request.json

    model_data = [-1, data['age'], data['experience'], data['income'], data['zipCode'], data['family'], data['ccAvg'],
                  data['education'], data['mortgage'], data['securities'], data['cdAccount'], data['online'],
                  data['creditCard']]
    model_data = np.array(model_data)
    model_data = pd.DataFrame([model_data], columns=columns)
    accepted = classification.predict_model(model, data=model_data)
    accepted = bool(accepted.Label[0])

    data['prediction'] = accepted

    new_prediction = save_prediction(data)
    db.session.commit()

    return jsonify({'id': new_prediction.id, 'accepted': accepted})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")


class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    prediction = db.Column(db.Boolean)
    decision = db.Column(db.Boolean)
    age = db.Column(db.Integer)
    experience = db.Column(db.Integer)
    income = db.Column(db.Float)
    zip_code = db.Column(db.String(50))
    family = db.Column(db.Integer)
    cc_avg = db.Column(db.Float)
    education = db.Column(db.Integer)
    mortgage = db.Column(db.Integer)
    securities = db.Column(db.Boolean)
    cd_account = db.Column(db.Boolean)
    online = db.Column(db.Boolean)
    credit_card = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


def save_prediction(data: dict):
    new_prediction = Prediction(prediction=data['prediction'], age=data['age'], experience=data['experience'],
                                income=data['income'], zip_code=data['zipCode'], family=data['family'],
                                cc_avg=data['ccAvg'], education=data['education'], mortgage=data['mortgage'],
                                securities=bool(data['securities']), cd_account=bool(data['cdAccount']),
                                online=bool(data['online']), credit_card=bool(data['creditCard']))
    db.session.add(new_prediction)
    return new_prediction


if __name__ == '__main__':
    app.run()
