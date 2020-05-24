from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from pycaret import classification
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

model = classification.load_model(model_name='decision_tree_1')
columns = ["ID", "Age", "Experience", "Income", "ZIP Code", "Family", "CCAvg", "Education", "Mortgage",
           "Securities Account",
           "CD Account", "Online", "CreditCard"]


@app.route('/api/test', methods=['GET'])
def test():
    res = {'test': 'OK'}
    return jsonify(res)


@app.route('/predict', methods=['POST'])
def predict():
    form_data = [x for x in request.form.values()]
    form_data = np.array(form_data)
    data = pd.DataFrame([form_data], columns=columns)
    prediction = classification.predict_model(model, data=data)
    prediction = "Accepted" if bool(prediction.Label[0]) else "Refused"
    return render_template('home.html', prediction=prediction)


@app.route('/')
def catch_all():
    return render_template("home.html")


if __name__ == '__main__':
    app.run()
