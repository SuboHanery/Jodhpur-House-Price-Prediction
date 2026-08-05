# Jodhpur House Price Prediction 🏠
This is my college project for predicting real estate prices in Jodhpur, Rajasthan, using Machine Learning.

## 📁 Project Structure

I tried to keep the folder structure as clean and simple as possible so it's easy to evaluate and understand.

```text
?   README.md (This file)
?   PRD.md (Product Requirements Document for the project)
?   requirements.txt (List of python libraries needed)
?   wsgi.py (File to run the server online)
?   
+---data/ (Datasets)
?       jodhpur_housing_dirty.csv
?       jodhpur_housing_cleaned.csv
?       1_Data_Cleaning_and_EDA.ipynb (Notebook where I cleaned the data)
?       
+---models/ (Trained ML files)
?       price_prediction_model.pkl (The final trained model)
?       scaler.pkl (Used for scaling inputs)
?       feature_names.json (List of columns used)
?       2_Model_Training.ipynb (Notebook where I trained and tested the models)
?       
+---flask_app/ (The Website Code)
?   ?   app.py (The main backend server file)
?   +---templates/ (HTML, CSS, and JS files)
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

## 🚀 How to Run it Locally

1. **Install the libraries:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the server:**
   ```bash
   python wsgi.py
   ```
3. **Open in Browser:** 
   Go to `http://localhost:5000`

## 📊 How I Built the ML Model

If you want to see the actual machine learning work:
1. Open the **`data/`** folder and check out `1_Data_Cleaning_and_EDA.ipynb`. This is where I handled missing values, removed outliers, and did data visualization.
2. Open the **`models/`** folder and check out `2_Model_Training.ipynb`. This is where I tested different algorithms (Linear Regression, Decision Tree, Random Forest) and picked the best one.

## 🌍 Deployment
I deployed this project live on Render. The `requirements.txt` file is set up with specific library versions so the cloud server doesn't crash when unpickling the model.
