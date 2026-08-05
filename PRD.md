# Comprehensive Product Requirements Document (PRD)
**Project Name:** Jodhpur House Price Prediction System
**Version:** 2.0 (Detailed Specification)
**Date:** June 2026

---

## 1. Executive Summary
The **Jodhpur House Price Prediction System** is a sophisticated, machine learning-driven web application tailored for the real estate market in Jodhpur, Rajasthan. It empowers prospective homebuyers, property sellers, and real estate professionals by providing an instantaneous, highly accurate estimated market value for properties based on user-defined parameters. The system bridges the gap between complex AI modeling and everyday user accessibility through a premium, highly responsive user interface.

## 2. Problem Statement
The Jodhpur real estate market relies heavily on human estimation, brokers, and word-of-mouth, which can often be biased or inaccurate. Buyers fear overpaying, and sellers struggle to set competitive listing prices. There is currently a lack of a centralized, data-driven, and publicly accessible digital tool specifically trained on Jodhpur's local housing data to provide instant, unbiased property valuations.

## 3. Solution Overview
We provide an intuitive web application where users can input physical attributes of a property (e.g., location, size, amenities). Upon submission, a trained Machine Learning model (Random Forest Regressor) processes these inputs against historical market data to instantly calculate and return an estimated price, a price range, and a price-per-square-foot breakdown. 

## 4. Target Audience & User Personas
1. **The Prospective Buyer (Rahul):** Looking for a 3 BHK in Shastri Nagar. Wants to quickly verify if the price quoted by a broker is fair. Values accuracy and ease of use.
2. **The Property Seller (Anjali):** Wants to list her old family home. Needs a realistic baseline price so her property doesn't sit on the market for too long.
3. **The Real Estate Agent (Vikram):** Needs a fast, mobile-accessible tool to generate rapid estimates for clients while doing property viewings.

## 5. Scope of Work
### 5.1. In-Scope
* Development of the predictive machine learning model using a dataset of 8,000 cleaned property records.
* Web-based user interface featuring form validation, dynamic price generation, and data visualization.
* Educational pages detailing the "Model Architecture" and "Data Insights".
* Cloud deployment ensuring 24/7 public accessibility.

### 5.2. Out-of-Scope (For Current Release)
* User account creation and login systems.
* Direct integration with live broker MLS (Multiple Listing Service) databases.
* Handling of commercial real estate (strictly limited to residential properties).

---

## 6. Functional Requirements
### 6.1. Core Prediction Engine
* **REQ-1:** The system must accept inputs for `Area Name` (12 supported locations), `BHK` (1 to 6+), `Bathrooms` (1-5+), `Balconies` (0-3+), `Property Age` (0-50 years), `Area Size` (sq ft), and 6 distinct `Premium Amenities`.
* **REQ-2:** The frontend must enforce validation (e.g., Area Size must be > 0 and formatted as a number).
* **REQ-3:** Upon submission, the frontend must display a "Loading" state to signify server processing.
* **REQ-4:** The backend API (`/api/predict`) must process the JSON payload, map it to the exact 1-dimensional array required by the model, scale the inputs, and return the prediction.
* **REQ-5:** The prediction must be formatted in standard Indian numbering format (e.g., ₹1.5 Cr, ₹85 Lakhs).

### 6.2. UI/UX & Presentation
* **REQ-6:** The UI must adhere to a "Glassmorphism" aesthetic, featuring frosted glass panels, glowing background orbs, and distinct Dark/Light modes driven by CSS variables.
* **REQ-7:** The application must intercept mobile users with an intentionally humorous "Easter Egg" overlay demanding they use a desktop, clicking a button redirects them to a specialized GIF page (`/time_lagega`).
* **REQ-8:** The final predicted number must physically animate (count up) from 0 to the target value over 1.2 seconds.

### 6.3. Data Insights & Transparency
* **REQ-9:** The system must provide a dedicated `/insights` page featuring pre-generated EDA (Exploratory Data Analysis) charts (Correlation matrices, distribution plots).
* **REQ-10:** The system must provide a `/model_info` page explaining the Random Forest algorithm to academic reviewers.

---

## 7. Non-Functional Requirements
### 7.1. Performance & Speed
* The prediction API must respond in under 800 milliseconds.
* The frontend must achieve a Google Lighthouse score of 90+ for performance.

### 7.2. Reliability & Availability
* The system is deployed on Render, targeting 99.9% uptime.
* If the ML model fails to load in memory on the server, the API must elegantly fail and return a descriptive `500 Internal Server Error` message to the UI instead of crashing the application.

### 7.3. Compatibility
* Optimized for modern desktop browsers (Chrome, Edge, Safari, Firefox). Mobile users are purposefully restricted as part of the project's presentation design.

---

## 8. Technical Architecture
### 8.1. Frontend Layer
* **HTML5:** Semantic structuring of 5 distinct pages.
* **CSS3:** Heavy use of Flexbox/Grid, CSS variables for theming, `backdrop-filter` for glassmorphism, and media queries for the mobile overlay.
* **JavaScript (Vanilla):** Asynchronous `fetch` calls to the Flask API, DOM manipulation, and request payload structuring.

### 8.2. Backend Layer
* **Framework:** Flask (Python 3.10+).
* **API Endpoints:** 
  * `POST /api/predict`: Handles ML inference.
  * `GET /api/download-model`: Serves the `.pkl` file.
  * `GET /api/download-data`: Serves the `.csv` file.

### 8.3. Machine Learning Layer
* **Model:** Scikit-Learn `RandomForestRegressor`.
* **Preprocessing:** `StandardScaler` applied to numeric data. One-hot encoding utilized for categorical areas.
* **Artifacts:** `price_prediction_model.pkl` (51MB), `scaler.pkl`, `feature_names.json`.

---

## 9. Data Pipeline & Management
* **Data Source:** Raw CSV data containing Jodhpur property listings.
* **Cleaning Protocol:** Removal of outliers (e.g., properties < 200 sq ft), handling missing values via median imputation, limiting properties to 8,000 core reliable records.
* **Serialization:** The trained model and scaler are serialized via `pickle` and loaded into RAM when the Flask server initializes via `wsgi.py`.

---

## 10. Deployment Strategy
* **Source Control:** GitHub repository (`Jodhpur-House-Price-Prediction`).
* **PaaS Provider:** Render (Free Tier).
* **Environment Configuration:** 
  * `requirements.txt` strictly pins dependencies (`numpy>=2.0.0`, `scikit-learn>=1.5.0`, `pandas>=2.2.0`) to prevent pip resolver downgrades and pickling errors.
  * Start Command: `gunicorn wsgi:app`

---

## 11. Risks & Mitigation
* **Risk 1: Pickling Incompatibilities.** Cloud server resolving to a different Numpy version than the training environment.
  * *Mitigation:* Aggressive dependency pinning in `requirements.txt` to strictly enforce Numpy 2.x and Scikit-Learn 1.5.x.
* **Risk 2: File Path Resolution.** Gunicorn launching from different root directories causing model load failures.
  * *Mitigation:* Implementation of strict absolute path resolution (`os.path.abspath(__file__)`) in `app.py`.
* **Risk 3: Model Size Limits.** GitHub blocking the 51MB `.pkl` file.
  * *Mitigation:* The file sits just below the hard 100MB cutoff, bypassing Git LFS requirements.

---

## 12. Future Roadmap (Phase 2)
1. **Dynamic Model Retraining:** Building an admin portal where new CSV data can be uploaded, automatically retraining the `.pkl` file and hot-reloading the Flask server.
2. **Interactive Map UI:** Integrating Mapbox or Google Maps API to allow users to click a location rather than using the `Area Name` dropdown.
3. **Database Integration:** Moving from a static model to a PostgreSQL database to store user queries and build a history of searched valuations.
