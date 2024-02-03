# -*- coding: utf-8 -*-
"""
Created on Mon Nov 6 15:20:48 2023

@author: Punam
"""

from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__, template_folder="templates")

# Load the saved model
model_file_path = "D:/Job_ready/projects/diabetes-Prediction-mains/diabetes-Prediction-main/trained_model.sav"

try:
    loaded_model = pickle.load(open(model_file_path, 'rb'))
except Exception as e:
    print(f"Error loading the model: {e}")
    loaded_model = None

# Create a function for prediction
def diabetes_prediction(input_data):
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)
    return prediction[0]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_data = {
            'Pregnancies': int(request.form['Pregnancies']),
            'Glucose': int(request.form['Glucose']),
            'BloodPressure': int(request.form['BloodPressure']),
            'SkinThickness': int(request.form['SkinThickness']),
            'Insulin': int(request.form['Insulin']),
            'BMI': float(request.form['BMI']),
            'DiabetesPedigreeFunction': float(request.form['DiabetesPedigreeFunction']),
            'Age': int(request.form['Age'])
        }

        result = diabetes_prediction(list(input_data.values()))

        if result == 0:
            diagnosis = 'The person is not diabetic'
        else:
            diagnosis = 'The person is diabetic'

        return render_template('result.html', diagnosis=diagnosis)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)
