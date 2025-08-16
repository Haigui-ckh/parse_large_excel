"""
Test script for the LangGraph-based Excel processing agent with feedback optimization
"""

from agents.langgraph_agent import ExcelProcessingWorkflow
from config.config import ProcessingConfig
import os

def test_with_feedback():
    """Test the agent with feedback optimization"""
    
    # Initialize workflow
    workflow = ExcelProcessingWorkflow()
    
    # Test file
    file_path = "sample_data.xlsx"
    
    if not os.path.exists(file_path):
        print(f"Test file {file_path} not found.")
        return
    
    # Test 1: Standard processing
    print("=== Test 1: Standard processing ===")
    config1 = ProcessingConfig(
        compression_intensity="medium",
        task_type="analysis",
        max_output_length=1000
    )
    
    result1 = workflow.process_excel(
        file_path=file_path,
        task_description="Analyze profit anomalies in sales data",
        config=config1
    )
    
    print(result1)
    print()
    
    # Test 2: High compression for concise output
    print("=== Test 2: High compression ===")
    config2 = ProcessingConfig(
        compression_intensity="high",
        task_type="summary",
        max_output_length=500
    )
    
    result2 = workflow.process_excel(
        file_path=file_path,
        task_description="Summarize key sales metrics",
        config=config2
    )
    
    print(result2)
    print()

if __name__ == "__main__":
    test_with_feedback()