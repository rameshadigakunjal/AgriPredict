from flask import Blueprint, jsonify
import pandas as pd

options_api = Blueprint('options_api', __name__)

@options_api.route('/api/options')
def get_options():
    try:
        # Use correct relative path for CSV
        df = pd.read_csv('data/combined_rice_data.csv')
        # Use exact column names from CSV header
        districts = sorted(df['Dist Name'].dropna().unique())
        years = sorted(df['Year'].dropna().unique(), reverse=True)
        # Convert numpy types to native Python types for JSON serialization
        districts = [str(d) for d in districts]
        years = [int(y) for y in years]
        return jsonify({
            'districts': districts,
            'years': years
        })
    except Exception as e:
        # Return error as JSON for easier debugging
        return jsonify({'error': str(e)}), 500
