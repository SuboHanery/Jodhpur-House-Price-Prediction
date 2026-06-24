import pandas as pd
import numpy as np
import os

def feature_engineering():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, '../data/jodhpur_housing_cleaned.csv')
    X_path = os.path.join(script_dir, '../data/X_features.csv')
    y_path = os.path.join(script_dir, '../data/y_target.csv')
    report_path = os.path.join(script_dir, '../reports/Feature_Engineering_Report.txt')
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    df = pd.read_csv(input_path)
    report_lines = ["=== FEATURE ENGINEERING REPORT ==="]
    report_lines.append(f"Initial shape: {df.shape}")
    
    # Drop Property_ID as it's an identifier
    if 'Property_ID' in df.columns:
        df.drop('Property_ID', axis=1, inplace=True)
        report_lines.append("Dropped 'Property_ID' column.")
    
    # 'Area_Name'
    categorical_cols = ['Area_Name']
    df = pd.get_dummies(df, columns=[col for col in categorical_cols if col in df.columns], drop_first=True)
    
    report_lines.append(f"One-hot encoded categorical columns: {categorical_cols}")
    
    # 2. Check for multicollinearity (correlation > 0.9)
    report_lines.append("\n=== Multicollinearity Check ===")
    corr_matrix = df.drop('Price', axis=1, errors='ignore').corr().abs()
    
    # Select upper triangle of correlation matrix
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    
    # Find features with correlation greater than 0.90
    to_drop = [column for column in upper.columns if any(upper[column] > 0.90)]
    
    if to_drop:
        df.drop(to_drop, axis=1, inplace=True)
        report_lines.append(f"Dropped highly correlated features (>0.9): {to_drop}")
    else:
        report_lines.append("No highly correlated features found (>0.9).")
        
    # 3. Separate features (X) and target (y)
    y = df['Price']
    X = df.drop('Price', axis=1)
    
    # 4. Verify all columns are numerical and no missing values
    report_lines.append("\n=== Verification ===")
    report_lines.append(f"X shape: {X.shape}")
    report_lines.append(f"y shape: {y.shape}")
    
    missing_X = X.isnull().sum().sum()
    missing_y = y.isnull().sum()
    
    report_lines.append(f"Missing values in X: {missing_X}")
    report_lines.append(f"Missing values in y: {missing_y}")
    
    non_numeric_cols = X.select_dtypes(exclude=['int64', 'float64', 'uint8', 'int32', 'bool']).columns.tolist()
    if not non_numeric_cols:
        report_lines.append("All features are numerical.")
    else:
        report_lines.append(f"WARNING: Non-numerical features found: {non_numeric_cols}")
        
    # Convert booleans to int just to be safe
    X = X.astype(float)
    
    # Save datasets
    X.to_csv(X_path, index=False)
    y.to_csv(y_path, index=False)
    
    report_lines.append(f"\nSaved X_features to: {X_path}")
    report_lines.append(f"Saved y_target to: {y_path}")
    
    with open(report_path, 'w') as f:
        f.write('\n'.join(report_lines))
        
    print(f"Feature engineering completed successfully. Report saved to {report_path}")

if __name__ == "__main__":
    feature_engineering()
