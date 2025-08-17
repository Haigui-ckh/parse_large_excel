"""
Test script for LLM integration
"""

from utils.llm_utils import call_deepseek_llm, generate_compression_rules, extract_key_insights

def test_llm_integration():
    """Test the LLM integration"""
    
    print("=== Testing LLM Integration ===\n")
    
    # Test 1: Basic LLM call
    print("Test 1: Basic LLM call")
    print("-" * 25)
    
    response = call_deepseek_llm("What are the key benefits of using LLMs for data analysis?")
    print("Response:")
    print(response)
    print("\n")
    
    # Test 2: Compression rules generation
    print("Test 2: Compression rules generation")
    print("-" * 35)
    
    data_description = "Dataset with 1000 rows and 8 columns. Columns: Date, Product, Region, Category, Quantity, Unit_Price, Total_Price, Profit. Data types: Date (datetime), Product (object), Region (object), Category (object), Quantity (int64), Unit_Price (float64), Total_Price (float64), Profit (float64)."
    task_type = "analysis"
    
    rules = generate_compression_rules(data_description, task_type)
    print("Generated rules:")
    print(rules)
    print("\n")
    
    # Test 3: Key insights extraction
    print("Test 3: Key insights extraction")
    print("-" * 30)
    
    data_summary = "Sheet 'Sales_Data': 1000 rows, 8 columns. Columns: Date, Product, Region, Category, Quantity, Unit_Price, Total_Price, Profit."
    task_description = "Analyze profit trends and anomalies in sales data"
    
    insights = extract_key_insights(data_summary, task_description)
    print("Extracted insights:")
    print(insights)
    print("\n")
    
    print("=== LLM Integration Test Complete ===")

if __name__ == "__main__":
    test_llm_integration()