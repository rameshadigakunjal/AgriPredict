# utils/predictor.py

import joblib
import numpy as np
import os

# Load models
mlr_model_p1 = joblib.load("app/models/mlr_p1.pkl")
svm_n = joblib.load("app/models/svm_n.pkl")
svm_p = joblib.load("app/models/svm_p.pkl")
svm_k = joblib.load("app/models/svm_k.pkl")
final_model_path = "app/models/final_model.pkl"
encoder = joblib.load("preprocessing/encoders.pkl")

def predict_yield_p1(district: str, year: int, production: float):
    district_encoded = encoder.transform([district])[0]
    input_array = np.array([[district_encoded, year, production]])
    prediction = mlr_model_p1.predict(input_array)[0]
    return prediction

def predict_npk(rainfall: float, temperature: float, humidity: float):
    climate_input = np.array([[rainfall, temperature, humidity]])
    n = svm_n.predict(climate_input)[0]
    p = svm_p.predict(climate_input)[0]
    k = svm_k.predict(climate_input)[0]
    return n, p, k

def predict_final_yield(district: str, year: int, production: float,
                         rainfall: float, temperature: float, humidity: float):
    n, p, k = predict_npk(rainfall, temperature, humidity)
    district_encoded = encoder.transform([district])[0]
    input_combined = np.array([[district_encoded, year, production, n, p, k, rainfall, temperature, humidity]])

    if os.path.exists(final_model_path):
        final_model = joblib.load(final_model_path)
        final_prediction = final_model.predict(input_combined)[0]
        return final_prediction
    else:
        raise FileNotFoundError("Final model not found. Please train final_model.pkl.")
