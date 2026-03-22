"""
Create Excel file with Indian cities data for PULSE project
Demonstrates Excel data integration capability
"""

import pandas as pd
import numpy as np
from pathlib import Path

def create_excel_dataset():
    """Create comprehensive Excel dataset"""
    
    # Load existing CSV data
    df = pd.read_csv('data/processed/cities_data.csv')
    
    # Add more detailed columns for Excel demonstration
    np.random.seed(42)
    
    # Add infrastructure details
    df['Hospitals_Count'] = (df['Population_2011'] * np.random.uniform(0.3, 0.8, len(df))).round().astype(int)
    df['Universities_Count'] = (df['Population_2011'] * np.random.uniform(0.05, 0.15, len(df))).round().astype(int)
    df['IT_Parks'] = (df['GDP_Billions_USD'] * np.random.uniform(0.1, 0.5, len(df))).round().astype(int)
    
    # Add quality of life metrics
    df['Air_Quality_Index'] = np.random.uniform(50, 300, len(df)).round().astype(int)
    df['Traffic_Index'] = np.random.uniform(20, 80, len(df)).round().astype(int)
    df['Cost_of_Living_Index'] = np.random.uniform(30, 100, len(df)).round().astype(int)
    
    # Add employment data
    df['Employment_Rate'] = np.random.uniform(60, 85, len(df)).round(1)
    df['Startup_Count'] = (df['GDP_Billions_USD'] * np.random.uniform(5, 20, len(df))).round().astype(int)
    df['Tech_Companies'] = (df['GDP_Billions_USD'] * np.random.uniform(2, 10, len(df))).round().astype(int)
    
    # Add education metrics
    df['Literacy_Rate'] = np.random.uniform(65, 95, len(df)).round(1)
    df['Higher_Education_Index'] = np.random.uniform(40, 90, len(df)).round(1)
    
    # Create Excel file with multiple sheets
    excel_path = Path('data/processed/indian_cities_comprehensive.xlsx')
    excel_path.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        # Main dataset
        df.to_excel(writer, sheet_name='Cities_Data', index=False)
        
        # Summary statistics
        summary = df.describe().round(2)
        summary.to_excel(writer, sheet_name='Statistical_Summary')
        
        # Regional analysis
        regional_stats = df.groupby('Region').agg({
            'UGI': ['mean', 'std', 'min', 'max'],
            'Population_2011': 'sum',
            'GDP_Billions_USD': 'sum',
            'City': 'count'
        }).round(2)
        regional_stats.to_excel(writer, sheet_name='Regional_Analysis')
        
        # Top performers
        top_cities = df.nlargest(20, 'UGI')[['City', 'State', 'Region', 'UGI', 'Population_2011', 'GDP_Billions_USD']]
        top_cities.to_excel(writer, sheet_name='Top_Cities', index=False)
        
        # Infrastructure data
        infrastructure = df[['City', 'State', 'Hospitals_Count', 'Universities_Count', 'IT_Parks', 'Metro']].copy()
        infrastructure.to_excel(writer, sheet_name='Infrastructure', index=False)
        
        # Economic indicators
        economic = df[['City', 'State', 'GDP_Billions_USD', 'Employment_Rate', 'Startup_Count', 'Tech_Companies']].copy()
        economic.to_excel(writer, sheet_name='Economic_Indicators', index=False)
    
    print(f"✅ Excel file created: {excel_path}")
    print(f"📊 Sheets included: Cities_Data, Statistical_Summary, Regional_Analysis, Top_Cities, Infrastructure, Economic_Indicators")
    print(f"📋 Total records: {len(df)} cities")
    print(f"📈 Total columns: {len(df.columns)} metrics")
    
    return excel_path

if __name__ == "__main__":
    create_excel_dataset()