# Project Requirements Document
**Project:** Jodhpur House Price Prediction Website
**Student Project Version**

---

## 1. What is this project?
This is a web application built to predict house prices in Jodhpur, Rajasthan using Machine Learning. The idea is to take inputs like the size of the house, location, and amenities, and use historical data to guess a fair market price. I built this to make it easier for people to check property rates without just relying on brokers.

## 2. Why did I build this?
Usually, people in Jodhpur rely on word-of-mouth or brokers to find out how much a house should cost, which can sometimes be misleading. I wanted to create a simple, data-driven tool that gives an instant, unbiased estimated price based on real numbers. 

## 3. Who is this for?
1. **Homebuyers:** People who want to double-check if they are getting a fair deal on a house.
2. **Sellers:** Property owners who need a rough idea of what to list their house for.
3. **Students/Reviewers:** Anyone checking out this college project to see how the Machine Learning model was trained and deployed.

## 4. Main Features
* **Prediction Form:** A simple UI where you enter details like Area Name, BHK, Bathrooms, Balconies, Age, Size, and check off amenities (Gym, Park, Security, etc.).
* **Instant ML Prediction:** The backend uses a Random Forest Machine Learning model to calculate the price instantly.
* **Data Insights Page:** Shows some basic charts (like price distribution) so users can see the data behind the model.
* **Mobile Easter Egg:** Since I designed the UI mainly for desktop browsers, anyone visiting on a phone will get a funny popup telling them to switch to a laptop.

## 5. Technology Stack (What I used)
* **Frontend:** HTML, standard CSS, and vanilla JavaScript. (I used a "Glassmorphism" transparent design style).
* **Backend:** Python and Flask.
* **Machine Learning:** Pandas (for data cleaning), NumPy, Scikit-Learn (for training the Random Forest algorithm).
* **Deployment:** Hosted live on Render, with all code managed on GitHub.

## 6. How the Data Works
* **The Dataset:** I used a dataset of Jodhpur property listings. 
* **Data Cleaning:** I wrote a Jupyter Notebook to drop useless columns, fill in missing values (using median for numbers and mode for text), and cap extreme outliers so the model doesn't get confused.
* **Training:** I tested Linear Regression, Decision Trees, and Random Forest. Random Forest gave the best accuracy, so I saved it as a `.pkl` file to use in the live website.

## 7. Future Ideas
If I had more time to work on this, I would add:
* A real map where users can drop a pin instead of picking a location from a dropdown menu.
* A database so users can create accounts and save their predictions to look at later.
