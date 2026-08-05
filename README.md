# Jodhpur House Price Prediction System 🏠
An AI-powered web application for predicting real estate prices in Jodhpur, Rajasthan, using Machine Learning.

## 📁 Project Structure

The project has been aggressively simplified for clean presentation and easy understanding.

```text
?   README.md (This file)
?   PRD.md (Detailed Product Requirements Document)
?   requirements.txt (Dependencies for Python)
?   wsgi.py (Server entry point)
?   
+---data/ (Raw and Cleaned datasets)
?       jodhpur_housing_dirty.csv
?       jodhpur_housing_cleaned.csv
?       1_Data_Cleaning_and_EDA.ipynb (All data preprocessing code)
?       
+---models/ (Trained AI files)
?       price_prediction_model.pkl (The main AI brain)
?       scaler.pkl (Math scaler)
?       feature_names.json (Required inputs order)
?       2_Model_Training.ipynb (All model training code)
?       
+---flask_app/ (The Web Application)
?   ?   app.py (The backend server script)
?   +---templates/ (All Web Code: HTML, CSS, JS)
?           base.html
?           index.html
?           insights.html
?           about.html
?           model_info.html
?           pipeline.html
?           time_lagega.html
?           style.css
?           script.js
```

## 🚀 How to Run Locally

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the Web Server:**
   ```bash
   python wsgi.py
   ```
3. **Open in Browser:** 
   Navigate to `http://localhost:5000`

## 📊 How the AI is Built

If you want to understand how the AI model was trained:
1. Open the **`data/`** folder and view `1_Data_Cleaning_and_EDA.ipynb` to see how the raw Excel data was cleaned.
2. Open the **`models/`** folder and view `2_Model_Training.ipynb` to see how the Random Forest AI algorithm was trained on the cleaned data to create the `.pkl` files.

## 🌍 Cloud Deployment
This project is production-ready. The `requirements.txt` strictly enforces `numpy>=2.0` and `scikit-learn>=1.5` to ensure cloud unpickling compatibility on services like Render.
