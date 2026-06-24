import pandas as pd
import numpy as np
import os

def preprocess_data():
    # Define paths relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, '../data/jodhpur_housing_dirty.csv')
    output_path = os.path.join(script_dir, '../data/jodhpur_housing_cleaned.csv')
    report_path = os.path.join(script_dir, '../reports/Data_Cleaning_Report.txt')
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    report_lines = []
    report_lines.append("=== DATA CLEANING REPORT ===")
    
    # 1. Load dataset and inspect shape
    df = pd.read_csv(input_path)
    
    # Drop unwanted columns
    cols_to_drop = ['Distance_Airport', 'Distance_Railway_Station', 'Distance_City_Center', 'Furnishing_Status', 'Total_Floors', 'Floor_No']
    df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True)
    
    initial_shape = df.shape
    report_lines.append(f"Initial shape of dataset: {initial_shape[0]} rows, {initial_shape[1]} columns")
    
    # 2. Check data types of all columns
    report_lines.append("\n=== Data Types ===")
    for col, dtype in df.dtypes.items():
        report_lines.append(f"{col}: {dtype}")
        
    # 3. Identify missing values (count & percentage)
    report_lines.append("\n=== Missing Values Distribution ===")
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100
    for col in df.columns:
        if missing_data[col] > 0:
            report_lines.append(f"{col}: {missing_data[col]} missing ({missing_percent[col]:.2f}%)")
            
    # 4. Handle missing values (imputation)
    # Convert Area_Size to numeric first if it's an object
    if 'Area_Size' in df.columns and df['Area_Size'].dtype == 'object':
        df['Area_Size'] = pd.to_numeric(df['Area_Size'], errors='coerce')
        
    # We will use median for numerical columns and mode for categorical columns
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if df[col].dtype in ['int64', 'float64']:
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna(df[col].mode()[0])
                
    # 5. Identify and handle outliers using IQR method
    report_lines.append("\n=== Outlier Handling ===")
    report_lines.append("Decision: Capping outliers using the 1.5 * IQR rule to prevent extreme values from skewing the model.")
    
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns
    # Exclude ID, boolean columns
    continuous_cols = ['Area_Size', 'Price', 'Property_Age']
    
    for col in continuous_cols:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Count outliers
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            if outliers > 0:
                report_lines.append(f"{col}: Capped {outliers} outliers.")
                # Cap the outliers
                df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
                df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])

    # 6. Convert Yes/No to 1/0
    yes_no_columns = ['Gym', 'Swimming_Pool', 'Market', 'School', 'Hospital', 
                      'Park', 'Mall', 'Security', 'Lift', 'Parking', 'Power_Backup']
    
    report_lines.append("\n=== Categorical Conversion ===")
    converted_cols = []
    for col in yes_no_columns:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0, 1: 1, 0: 0})
            # If there are any NaN mapped, fill with 0
            df[col] = df[col].fillna(0).astype(int)
            converted_cols.append(col)
            
    report_lines.append(f"Converted Yes/No to 1/0 for columns: {', '.join(converted_cols)}")
    
    # 7. Verify no missing values remain
    remaining_missing = df.isnull().sum().sum()
    report_lines.append(f"\nVerification: Total missing values remaining in dataset: {remaining_missing}")
    
    # Save cleaned dataset
    df.to_csv(output_path, index=False)
    final_shape = df.shape
    report_lines.append(f"Final shape of cleaned dataset: {final_shape[0]} rows, {final_shape[1]} columns")
    report_lines.append(f"Cleaned dataset saved to: {output_path}")
    
    # Write report
    with open(report_path, 'w') as f:
        f.write('\n'.join(report_lines))
        
    print(f"Data cleaning completed successfully. Report saved to {report_path}")

if __name__ == "__main__":
    preprocess_data()
