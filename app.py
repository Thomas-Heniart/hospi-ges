from flask import Flask, render_template, url_for, request
import numpy as np
import pandas as pd
from pycaret import classification

app = Flask(__name__)

model = classification.load_model(model_name='decision_tree_1')
columns = ["ID", "Age", "Experience", "Income", "ZIP Code", "Family", "CCAvg", "Education", "Mortgage",
           "Securities Account",
           "CD Account", "Online", "CreditCard"]


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/predict', methods=['POST'])
def predict():
    form_data = [x for x in request.form.values()]
    form_data = np.array(form_data)
    data = pd.DataFrame([form_data], columns=columns)
    prediction = classification.predict_model(model, data=data)
    prediction = "Accepted" if bool(prediction.Label[0]) else "Refused"
    return render_template('home.html', prediction=prediction)


if __name__ == '__main__':
    app.run()
