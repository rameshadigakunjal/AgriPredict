from flask import Blueprint, request, jsonify, session
import joblib
import numpy as np

main = Blueprint('main', __name__)

# Load new models and encoder
rf_yield = joblib.load("app/models/rf_yield.pkl")
rf_n = joblib.load("app/models/rf_n.pkl")
rf_p = joblib.load("app/models/rf_p.pkl")
rf_k = joblib.load("app/models/rf_k.pkl")
district_encoder = joblib.load("preprocessing/district_encoder_combined.pkl")

@main.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    try:
        # Get user inputs
        district = data.get('district', '')
        year = int(data.get('year', 0))
        area = float(data.get('area', 0))
        production = float(data.get('production', 0))
        temperature = float(data.get('temperature', 0))
        rainfall = float(data.get('rainfall', 0))
        humidity = float(data.get('humidity', 0))

        # Encode district
        district_encoded = district_encoder.transform([district])[0]

        # Build feature vector
        features = np.array([[district_encoded, year, area, production, temperature, rainfall, humidity]])

        # Predict
        predicted_yield = rf_yield.predict(features)[0]
        predicted_n = rf_n.predict(features)[0]
        predicted_p = rf_p.predict(features)[0]
        predicted_k = rf_k.predict(features)[0]

        # Save prediction to DB if user is logged in
        user_id = session.get('user_id')
        if user_id:
            import sqlite3
            conn = sqlite3.connect('anaconda_projects/db/project_filebrowser.db')
            cur = conn.cursor()
            cur.execute('''INSERT INTO predictions (user_id, district, year, area, production, temperature, rainfall, humidity, predicted_yield, predicted_n, predicted_p, predicted_k)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (user_id, district, year, area, production, temperature, rainfall, humidity, predicted_yield, predicted_n, predicted_p, predicted_k))
            conn.commit()
            conn.close()

        return jsonify({
            'predicted_yield': float(predicted_yield),
            'predicted_n': float(predicted_n),
            'predicted_p': float(predicted_p),
            'predicted_k': float(predicted_k)
        })
    except Exception as e:
        return jsonify({'message': f'Prediction error: {str(e)}'}), 400
