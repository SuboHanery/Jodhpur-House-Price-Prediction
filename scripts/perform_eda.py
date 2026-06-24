import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def perform_eda():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, '../data/jodhpur_housing_cleaned.csv')
    vis_dir = os.path.join(script_dir, '../visualizations')
    report_path = os.path.join(script_dir, '../reports/EDA_Report.txt')
    
    os.makedirs(vis_dir, exist_ok=True)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    df = pd.read_csv(input_path)
    
    # Identify numerical features for correlation
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
    
    report_lines = []
    report_lines.append("=== EXPLORATORY DATA ANALYSIS REPORT ===")
    report_lines.append(f"Total Properties Analyzed: {len(df)}")
    
    # 1. Univariate Analysis (Distributions)
    plt.figure(figsize=(18, 5))
    
    plt.subplot(1, 3, 1)
    sns.histplot(df['Price'], bins=50, kde=True)
    plt.title('Price Distribution')
    
    plt.subplot(1, 3, 2)
    sns.histplot(df['Area_Size'], bins=50, kde=True)
    plt.title('Area Size Distribution')
    
    plt.subplot(1, 3, 3)
    sns.countplot(x='BHK', data=df)
    plt.title('BHK Distribution')
    
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, 'univariate_analysis.png'))
    plt.close()
    
    # 2. Bivariate Analysis
    plt.figure(figsize=(20, 5))
    
    plt.subplot(1, 4, 1)
    sns.scatterplot(x='Area_Size', y='Price', data=df, alpha=0.5)
    plt.title('Area Size vs Price')
    
    plt.subplot(1, 4, 2)
    sns.boxplot(x='BHK', y='Price', data=df)
    plt.title('BHK vs Price')
    
    plt.subplot(1, 4, 3)
    sns.scatterplot(x='Property_Age', y='Price', data=df, alpha=0.5)
    plt.title('Property Age vs Price')
    
    plt.subplot(1, 4, 4)
    # If Furnishing_Status is object/string, else it might have been missing. We didn't encode it in cleaning.
    if 'Furnishing_Status' in df.columns:
        sns.boxplot(x='Furnishing_Status', y='Price', data=df)
        plt.xticks(rotation=45)
        plt.title('Furnishing Status vs Price')
        
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, 'bivariate_analysis.png'))
    plt.close()
    
    # 3. Correlation Matrix & Heatmap
    corr_matrix = df[numerical_cols].corr()
    
    plt.figure(figsize=(15, 12))
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', linewidths=0.5)
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, 'correlation_matrix.png'))
    plt.close()
    
    # 4. Top 10 Features Correlated with Price
    price_corr = corr_matrix['Price'].sort_values(ascending=False)
    top_10_corr = price_corr.drop('Price').head(10)
    
    report_lines.append("\n=== Top 10 Features Correlated with Price ===")
    for feature, corr in top_10_corr.items():
        report_lines.append(f"{feature}: {corr:.4f}")
        
    # Write report
    with open(report_path, 'w') as f:
        f.write('\n'.join(report_lines))
        
    print(f"EDA completed successfully. Report saved to {report_path}")
    print(f"Visualizations saved to {vis_dir}")

if __name__ == "__main__":
    perform_eda()
