from flask import Flask, render_template, request, jsonify
from pycaret import classification
from dotenv import load_dotenv
from flask_cors import CORS

import numpy as np
import pandas as pd
import requests

load_dotenv()

app = Flask(__name__, template_folder="client/dist", static_folder="client/dist/static")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

model = classification.load_model(model_name='decision_tree_1')
columns = ["ID", "Age", "Experience", "Income", "ZIP Code", "Family", "CCAvg", "Education", "Mortgage",
           "Securities Account",
           "CD Account", "Online", "CreditCard"]


@app.route('/api/test', methods=['GET'])
def test():
    res = {'test': 'OK'}
    return jsonify(res)


@app.route('/api/predict', methods=['POST'])
def predict():
    form_data = [x for x in request.form.values()]
    form_data = np.array(form_data)
    data = pd.DataFrame([form_data], columns=columns)
    prediction = classification.predict_model(model, data=data)
    prediction = "Accepted" if bool(prediction.Label[0]) else "Refused"
    return render_template('home.html', prediction=prediction)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
