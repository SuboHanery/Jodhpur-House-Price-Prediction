import pandas as pd
import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import shutil

def mean_absolute_percentage_error(y_true, y_pred): 
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def evaluate_models():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    X_test_path = os.path.join(script_dir, '../data/X_test.csv')
    y_test_path = os.path.join(script_dir, '../data/y_test.csv')
    models_dir = os.path.join(script_dir, '../models')
    vis_dir = os.path.join(script_dir, '../visualizations')
    report_path = os.path.join(script_dir, '../reports/Model_Performance_Report.txt')
    info_path = os.path.join(models_dir, 'model_info.txt')
    
    os.makedirs(vis_dir, exist_ok=True)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    # 1. Load Data
    X_test = pd.read_csv(X_test_path)
    y_test = pd.read_csv(y_test_path).values.ravel()
    
    # 2. Load scaler
    with open(os.path.join(models_dir, 'scaler.pkl'), 'rb') as f:
        scaler = pickle.load(f)
    X_test_scaled = scaler.transform(X_test)
    
    # 3. Load Models
    models = {}
    with open(os.path.join(models_dir, 'lr_model.pkl'), 'rb') as f:
        models['Linear Regression'] = pickle.load(f)
    with open(os.path.join(models_dir, 'dt_model.pkl'), 'rb') as f:
        models['Decision Tree'] = pickle.load(f)
    with open(os.path.join(models_dir, 'rf_model.pkl'), 'rb') as f:
        models['Random Forest'] = pickle.load(f)
    
    report_lines = ["=== MODEL PERFORMANCE REPORT ===\n"]
    
    results = []
    
    # 4. Evaluate Models
    for name, model in models.items():
        y_pred = model.predict(X_test_scaled)
        
        # Ensure no negative predictions or zeros for MAPE
        y_pred = np.maximum(y_pred, 1)
        y_true = np.maximum(y_test, 1)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred)
        
        results.append({
            'Model': name,
            'MAE': mae,
            'RMSE': rmse,
            'R2': r2,
            'MAPE': mape
        })
        
        report_lines.append(f"--- {name} ---")
        report_lines.append(f"MAE: {mae:.2f}")
        report_lines.append(f"RMSE: {rmse:.2f}")
        report_lines.append(f"R² Score: {r2:.4f}")
        report_lines.append(f"MAPE: {mape:.2f}%\n")
        
    # Create comparison table
    results_df = pd.DataFrame(results)
    report_lines.append("=== COMPARISON TABLE ===")
    report_lines.append(results_df.to_string(index=False))
    
    # 5. Identify Best Model (Highest R2)
    best_row = results_df.loc[results_df['R2'].idxmax()]
    best_model_name = best_row['Model']
    report_lines.append(f"\n=== BEST MODEL ===")
    report_lines.append(f"Selected Model: {best_model_name}")
    report_lines.append(f"R² Score: {best_row['R2']:.4f}")
    
    # 6. Save Best Model as price_prediction_model.pkl
    model_files = {
        'Linear Regression': 'lr_model.pkl',
        'Decision Tree': 'dt_model.pkl',
        'Random Forest': 'rf_model.pkl'
    }
    
    best_model_filename = model_files[best_model_name]
    best_model_path = os.path.join(models_dir, best_model_filename)
    final_model_path = os.path.join(models_dir, 'price_prediction_model.pkl')
    
    shutil.copy(best_model_path, final_model_path)
    report_lines.append(f"Best model copied to {final_model_path}")
    
    # Generate Visualizations for Best Model
    best_model = models[best_model_name]
    y_pred_best = best_model.predict(X_test_scaled)
    
    # Actual vs Predicted Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred_best, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Price')
    plt.ylabel('Predicted Price')
    plt.title(f'Actual vs Predicted Price ({best_model_name})')
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, 'model_comparison.png'))
    plt.close()
    
    # Residual Plot
    residuals = y_test - y_pred_best
    plt.figure(figsize=(10, 6))
    sns.histplot(residuals, bins=50, kde=True)
    plt.xlabel('Residuals')
    plt.title(f'Residual Distribution ({best_model_name})')
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, 'residual_plots.png'))
    plt.close()
    
    # Feature Importance (if applicable)
    if hasattr(best_model, 'feature_importances_'):
        importances = best_model.feature_importances_
        feature_names = pd.read_csv(X_test_path).columns
        indices = np.argsort(importances)[::-1][:15] # top 15
        
        plt.figure(figsize=(12, 8))
        plt.title('Top 15 Feature Importances')
        plt.bar(range(15), importances[indices], align='center')
        plt.xticks(range(15), feature_names[indices], rotation=90)
        plt.xlim([-1, 15])
        plt.tight_layout()
        plt.savefig(os.path.join(vis_dir, 'feature_importance.png'))
        plt.close()
    
    # Write reports
    report_content = '\n'.join(report_lines)
    with open(report_path, 'w') as f:
        f.write(report_content)
        
    with open(info_path, 'w') as f:
        f.write(report_content)
        
    print(f"Model evaluation completed successfully. Report saved to {report_path}")

if __name__ == "__main__":
    evaluate_models()
