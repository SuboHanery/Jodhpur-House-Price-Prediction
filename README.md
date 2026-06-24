# Jodhpur House Price Prediction

## Overview
A machine learning project to predict residential property prices in Jodhpur using Linear Regression, Decision Tree, and Random Forest algorithms. The model is deployed as a web application using Flask.

## Dataset
- **Source:** jodhpur_housing_dirty.csv
- **Records:** [Your number] properties
- **Features:** [Your number] features including property details, amenities, and distances
- **Target:** Price (in INR)

## Technologies Used
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Machine Learning:** Scikit-learn
- **Web Framework:** Flask
- **Frontend:** HTML, CSS
- **Model Storage:** Joblib

## Project Phases

### 1. Data Exploration & Cleaning
- Loaded and analyzed dataset
- Handled missing values using median imputation
- Removed/capped outliers using IQR method
- Converted categorical variables

### 2. Exploratory Data Analysis
- Created 15+ visualizations
- Identified feature correlations
- Found top features: [List your top 5]

### 3. Feature Engineering
- One-hot encoded categorical variables
- Scaled numerical features using StandardScaler
- Created new features: [List if any]

### 4. Model Development
Trained three models and compared performance:

| Model | R² Score | RMSE | MAE |
|-------|----------|------|-----|
| Linear Regression | 0.XX | ₹XXX | ₹XXX |
| Decision Tree | 0.XX | ₹XXX | ₹XXX |
| Random Forest | 0.XX | ₹XXX | ₹XXX |

**Best Model:** Random Forest (R² = 0.XX)

### 5. Deployment
- Built Flask web application
- Created interactive prediction form
- Deployed locally on localhost:5000

## Installation & Usage

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Clone/download the project
# Navigate to project directory
cd house_price_prediction_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Navigate to flask_app directory
cd flask_app

# Run Flask application
python app.py

# Open browser and visit
http://localhost:5000
```

## Using the Predictor
1. Fill in property details in the form
2. Select amenities and distances
3. Click "Predict Price"
4. View estimated price in rupees

## Project Structure
```
house_price_prediction_project/
├── data/
├── notebooks/
├── models/
├── flask_app/
├── visualizations/
├── reports/
├── scripts/
├── README.md
└── requirements.txt
```

## Key Findings
- Area Size is the strongest predictor of price
- BHK count significantly impacts price
- Location (distances to key amenities) matters
- Properties in [Area Name] are most expensive
- Furnishing status affects price by ~[X]%

## Model Performance
- **Training R² Score:** 0.XX
- **Testing R² Score:** 0.XX
- **RMSE on Test Set:** ₹XX,XXX
- **Mean Absolute Error:** ₹XX,XXX
- **Mean Absolute Percentage Error:** X.XX%

## Limitations & Future Improvements
1. Limited to Jodhpur properties
2. Dataset size: [Number] properties
3. Could benefit from:
   - More recent data
   - Additional features (property images, reviews)
   - Ensemble methods (XGBoost, LightGBM)
   - Confidence intervals for predictions

## Deployment
To deploy on production:
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Using Heroku
heroku create your-app-name
git push heroku main
```

## Author
[Your Name]

## License
This project is open source and available under the MIT License.

## Contact
For questions or suggestions, reach out via [Your Email]
