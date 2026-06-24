import pandas as pd
import numpy as np
import os
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

def train_models():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    X_path = os.path.join(script_dir, '../data/X_features.csv')
    y_path = os.path.join(script_dir, '../data/y_target.csv')
    models_dir = os.path.join(script_dir, '../models')
    
    os.makedirs(models_dir, exist_ok=True)
    
    # 1. Load data
    print("Loading features and target...")
    X = pd.read_csv(X_path)
    y = pd.read_csv(y_path)
    
    # Save feature names
    feature_names = list(X.columns)
    feature_names_path = os.path.join(models_dir, 'feature_names.json')
    with open(feature_names_path, 'w') as f:
        json.dump(feature_names, f)
    
    # 2. Train-Test Split (80% train, 20% test)
    print("Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Save test sets for evaluation script
    X_test.to_csv(os.path.join(script_dir, '../data/X_test.csv'), index=False)
    y_test.to_csv(os.path.join(script_dir, '../data/y_test.csv'), index=False)
    
    # 3. Initialize and fit StandardScaler
    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Save the scaler
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Saved scaler to {scaler_path}")
    
    # 4. Initialize Models
    models = {
        'lr_model': LinearRegression(),
        'dt_model': DecisionTreeRegressor(random_state=42),
        'rf_model': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    # 5. Train and Save Models
    for model_name, model in models.items():
        print(f"Training {model_name}...")
        model.fit(X_train_scaled, y_train.values.ravel())
        
        model_path = os.path.join(models_dir, f'{model_name}.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        print(f"Saved {model_name} to {model_path}")
        
    print("Model training completed successfully.")

if __name__ == "__main__":
    train_models()
