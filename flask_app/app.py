from flask import Flask, render_template, request, jsonify, send_file
import pickle
import numpy as np
import json
import warnings
import os
from datetime import datetime

warnings.filterwarnings('ignore')

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size

# Load model, scaler, and feature names using absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'models', 'price_prediction_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, '..', 'models', 'scaler.pkl')
FEATURES_PATH = os.path.join(BASE_DIR, '..', 'models', 'feature_names.json')

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    with open(FEATURES_PATH, 'r') as f:
        feature_names = json.load(f)
    print("[SUCCESS] Model loaded successfully!")
except Exception as e:
    print(f"[ERROR] Error loading model: {e}")
    model = None
    scaler = None
    feature_names = None

# Define constants
AREAS = ['Bhagat Ki Kothi', 'Magra Punjla', 'Basni', 'Chopasni Housing Board', 
         'Shastri Nagar', 'Sardarpura', 'Soorsagar', 'Mahamandir', 
         'Air Force Area', 'Pal Road', 'Jalori Gate', 'Pratap Nagar']

def format_currency(amount):
    """Format amount as Indian currency"""
    return f"₹{amount:,.2f}"

@app.route('/predict')
def predict():
    """Single Page Application for Price Prediction"""
    return render_template('index.html', areas=AREAS, active='predict')

@app.route('/time_lagega')
def time_lagega():
    """Mobile Easter Egg"""
    return render_template('time_lagega.html')

@app.route('/insights')
def insights():
    """Data Insights Page"""
    return render_template('insights.html', active='insights')

@app.route('/model_info')
def model_info():
    """Model Architecture Page"""
    return render_template('model_info.html', active='model_info')

@app.route('/')
def about():
    """About Project Page"""
    return render_template('about.html', active='about')

@app.route('/pipeline')
def pipeline():
    """Project Pipeline Page for Presentation"""
    return render_template('pipeline.html', active='pipeline')

def create_input_array(bhk, bathrooms, balconies, area_size, property_age, amenities, area_name):
    """Create properly formatted input array for model"""
    # Initialize array of zeros with the same length as feature_names
    input_dict = {feature: 0 for feature in feature_names}
    
    # Set numeric inputs
    input_dict['BHK'] = bhk
    input_dict['Bathrooms'] = bathrooms
    input_dict['Balconies'] = balconies
    input_dict['Area_Size'] = area_size
    input_dict['Property_Age'] = property_age
    
    # Set amenities
    for amenity, value in amenities.items():
        if amenity in input_dict:
            input_dict[amenity] = value
            
    # Set area
    area_col = f'Area_Name_{area_name}'
    if area_col in input_dict:
        input_dict[area_col] = 1
        
    # Convert dictionary to numpy array in the exact order of feature_names
    input_list = [input_dict[feature] for feature in feature_names]
    
    return np.array(input_list).reshape(1, -1)

def make_prediction(input_array):
    """Make prediction using trained model"""
    if model is None or scaler is None:
        raise Exception("Model not loaded. Check model files.")
    
    # Scale input
    input_scaled = scaler.transform(input_array)
    
    # Make prediction
    predicted_price = model.predict(input_scaled)[0]
    
    # Ensure price is positive
    predicted_price = max(predicted_price, 0)
    
    return predicted_price

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """JSON API endpoint for programmatic access"""
    try:
        data = request.json
        
        # Validate
        if not all(k in data for k in ['bhk', 'area_size']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Process prediction
        predicted_price = make_prediction(create_input_array(
            bhk=data.get('bhk'),
            bathrooms=data.get('bathrooms', 1),
            balconies=data.get('balconies', 0),
            area_size=data.get('area_size'),
            property_age=data.get('property_age', 0),
            amenities={k: data.get(k.lower(), 0) for k in 
                      ['Gym', 'Swimming_Pool', 'Market', 'School', 
                       'Hospital', 'Park', 'Mall', 'Security', 
                       'Lift', 'Parking', 'Power_Backup']},
            area_name=data.get('area_name', AREAS[0])
        ))
        
        return jsonify({
            'predicted_price': round(predicted_price, 2),
            'price_formatted': format_currency(predicted_price),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/download-model')
def download_model():
    """Serve the trained model file for download"""
    try:
        model_path = os.path.join(os.path.dirname(__file__), '../models/price_prediction_model.pkl')
        return send_file(model_path, as_attachment=True, download_name='jodhpur_price_model.pkl')
    except Exception as e:
        return jsonify({"error": "Model file not found"}), 404

@app.route('/api/download-data')
def download_data():
    """Serve the cleaned dataset for download"""
    try:
        data_path = os.path.join(os.path.dirname(__file__), '../data/jodhpur_housing_cleaned.csv')
        return send_file(data_path, as_attachment=True, download_name='jodhpur_housing_cleaned.csv', mimetype='text/csv')
    except Exception as e:
        return jsonify({"error": "Dataset file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
