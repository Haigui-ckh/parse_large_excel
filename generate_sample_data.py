"""
Sample data generation script
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_sample_data():
    """Generate sample sales data for testing"""
    
    # Generate date range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = pd.date_range(start_date, end_date, freq='D')
    
    # Generate sample data
    data = []
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    for date in date_range:
        for _ in range(random.randint(5, 15)):  # Random number of transactions per day
            product = random.choice(products)
            region = random.choice(regions)
            quantity = random.randint(1, 100)
            unit_price = random.uniform(10, 500)
            total_price = quantity * unit_price
            
            # Introduce some anomalies
            if product == 'Product C' and date.month in [10, 11, 12]:
                # Product C has negative profits in Q4
                unit_price = random.uniform(5, 20)
                total_price = quantity * unit_price
                profit = -abs(random.uniform(100, 5000))
            else:
                profit = total_price * random.uniform(0.1, 0.3)
            
            data.append({
                'Date': date,
                'Product': product,
                'Region': region,
                'Quantity': quantity,
                'Unit_Price': unit_price,
                'Total_Price': total_price,
                'Profit': profit
            })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel with multiple sheets
    with pd.ExcelWriter('sample_data.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sales_Data', index=False)
        
        # Create a summary sheet
        summary = df.groupby('Product').agg({
            'Quantity': 'sum',
            'Total_Price': 'sum',
            'Profit': 'sum'
        }).reset_index()
        summary.to_excel(writer, sheet_name='Product_Summary', index=False)
        
        # Create a regional summary
        regional = df.groupby('Region').agg({
            'Quantity': 'sum',
            'Total_Price': 'sum',
            'Profit': 'sum'
        }).reset_index()
        regional.to_excel(writer, sheet_name='Regional_Summary', index=False)
    
    print("Sample data saved to 'sample_data.xlsx'")

if __name__ == "__main__":
    generate_sample_data()