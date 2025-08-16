"""
Generate complex sample data for testing the Excel processing agent
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_complex_sample_data():
    """Generate complex sample sales data for testing"""
    
    # Generate date range for a full year
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = pd.date_range(start_date, end_date, freq='D')
    
    # Generate sample data
    data = []
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E', 'Product F']
    regions = ['North', 'South', 'East', 'West', 'Central', 'Northeast', 'Southeast', 'Northwest', 'Southwest']
    categories = ['Electronics', 'Clothing', 'Home Goods', 'Food & Beverage', 'Automotive']
    
    # Seasonal factors
    seasonal_factors = {
        1: 0.8, 2: 0.7, 3: 0.9, 4: 1.0, 5: 1.1, 6: 1.2,
        7: 1.3, 8: 1.2, 9: 1.1, 10: 1.0, 11: 1.2, 12: 1.5
    }
    
    for date in date_range:
        # Determine number of transactions based on day of week and season
        base_transactions = random.randint(10, 30)
        weekend_multiplier = 1.3 if date.weekday() >= 5 else 1.0
        seasonal_multiplier = seasonal_factors[date.month]
        num_transactions = int(base_transactions * weekend_multiplier * seasonal_multiplier)
        
        for _ in range(num_transactions):
            product = random.choice(products)
            region = random.choice(regions)
            category = random.choice(categories)
            quantity = random.randint(1, 200)
            
            # Base price varies by category
            category_base_prices = {
                'Electronics': 300,
                'Clothing': 50,
                'Home Goods': 100,
                'Food & Beverage': 20,
                'Automotive': 500
            }
            
            base_price = category_base_prices[category]
            unit_price = base_price * random.uniform(0.8, 1.5)
            total_price = quantity * unit_price
            
            # Calculate profit with some variations
            profit_margin = random.uniform(0.1, 0.4)
            
            # Special cases for anomalies
            if product == 'Product C' and date.month in [10, 11, 12]:
                # Product C has negative profits in Q4
                profit = -abs(random.uniform(500, 5000))
            elif product == 'Product F' and date.month == 12:
                # Product F has exceptionally high profits in December
                profit = total_price * random.uniform(0.5, 0.8)
            else:
                profit = total_price * profit_margin
            
            # Add some null values to test null detection
            if random.random() < 0.02:  # 2% chance of null quantity
                quantity = None
                
            if random.random() < 0.01:  # 1% chance of null unit_price
                unit_price = None
            
            data.append({
                'Date': date,
                'Product': product,
                'Region': region,
                'Category': category,
                'Quantity': quantity,
                'Unit_Price': unit_price,
                'Total_Price': total_price,
                'Profit': profit
            })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel with multiple sheets
    with pd.ExcelWriter('complex_sample_data.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sales_Data', index=False)
        
        # Create a product summary sheet
        product_summary = df.groupby('Product').agg({
            'Quantity': 'sum',
            'Total_Price': 'sum',
            'Profit': ['sum', 'mean', 'std']
        }).reset_index()
        product_summary.columns = ['Product', 'Total_Quantity', 'Total_Revenue', 'Total_Profit', 'Avg_Profit', 'Std_Profit']
        product_summary.to_excel(writer, sheet_name='Product_Summary', index=False)
        
        # Create a regional summary
        regional_summary = df.groupby('Region').agg({
            'Quantity': 'sum',
            'Total_Price': 'sum',
            'Profit': 'sum'
        }).reset_index()
        regional_summary.to_excel(writer, sheet_name='Regional_Summary', index=False)
        
        # Create a category summary
        category_summary = df.groupby('Category').agg({
            'Quantity': 'sum',
            'Total_Price': 'sum',
            'Profit': 'sum'
        }).reset_index()
        category_summary.to_excel(writer, sheet_name='Category_Summary', index=False)
        
        # Create a monthly trend sheet
        df['Month'] = df['Date'].dt.month
        monthly_summary = df.groupby('Month').agg({
            'Quantity': 'sum',
            'Total_Price': 'sum',
            'Profit': 'sum'
        }).reset_index()
        monthly_summary.to_excel(writer, sheet_name='Monthly_Trend', index=False)
    
    print("Complex sample data saved to 'complex_sample_data.xlsx'")
    
    # Also create a simple version for quick testing
    simple_df = df.sample(n=1000)  # Take a sample of 1000 rows
    simple_df.to_excel('simple_sample_data.xlsx', index=False)
    print("Simple sample data saved to 'simple_sample_data.xlsx'")

if __name__ == "__main__":
    generate_complex_sample_data()