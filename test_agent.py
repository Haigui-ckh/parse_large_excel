"""
Test script for the Excel processing agent with different configurations
"""

from agents.excel_processing_agent import ExcelProcessingAgent
from config.config import ProcessingConfig
import os

def test_different_configs():
    """Test the agent with different configurations"""
    
    # Initialize the agent
    agent = ExcelProcessingAgent()
    
    # Test file
    file_path = "sample_data.xlsx"
    
    if not os.path.exists(file_path):
        print(f"Test file {file_path} not found.")
        return
    
    # Test 1: Low compression, summary task
    print("=== Test 1: Low compression, summary task ===")
    config1 = ProcessingConfig(
        compression_intensity="low",
        task_type="summary",
        max_output_length=1500
    )
    
    result1 = agent.process_excel(
        file_path=file_path,
        task_description="Summarize sales performance",
        config=config1
    )
    
    if result1["status"] == "success":
        print(result1["formatted_content"])
        print(f"Output length: {result1['length']} characters\n")
    else:
        print(f"Error: {result1['message']}\n")
    
    # Test 2: High compression, analysis task
    print("=== Test 2: High compression, analysis task ===")
    config2 = ProcessingConfig(
        compression_intensity="high",
        task_type="analysis",
        max_output_length=1000
    )
    
    result2 = agent.process_excel(
        file_path=file_path,
        task_description="Analyze profit trends and anomalies",
        config=config2
    )
    
    if result2["status"] == "success":
        print(result2["formatted_content"])
        print(f"Output length: {result2['length']} characters\n")
    else:
        print(f"Error: {result2['message']}\n")

if __name__ == "__main__":
    test_different_configs()