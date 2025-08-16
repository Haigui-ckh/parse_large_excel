"""
Comprehensive test case for the Excel processing agent
"""

from agents.langgraph_agent import ExcelProcessingWorkflow
from config.config import ProcessingConfig
import os
import time

def run_comprehensive_test():
    """Run a comprehensive test of the Excel processing agent"""
    
    print("=== Comprehensive Test Case for Excel Processing Agent ===\n")
    
    # Initialize workflow
    workflow = ExcelProcessingWorkflow()
    
    # Test with simple data first
    file_path = "simple_sample_data.xlsx"
    
    if not os.path.exists(file_path):
        print(f"Test file {file_path} not found.")
        return
    
    print(f"Testing with file: {file_path}")
    print(f"File size: {os.path.getsize(file_path) / 1024:.2f} KB\n")
    
    # Test Case 1: Analysis task with medium compression
    print("Test Case 1: Analysis task with medium compression")
    print("-" * 50)
    
    config1 = ProcessingConfig(
        compression_intensity="medium",
        task_type="analysis",
        max_output_length=1500
    )
    
    start_time = time.time()
    result1 = workflow.process_excel(
        file_path=file_path,
        task_description="Analyze profit anomalies and trends in sales data",
        config=config1
    )
    end_time = time.time()
    
    print(f"Processing time: {end_time - start_time:.2f} seconds")
    print("Output:")
    print(result1)
    print("\n")
    
    # Test Case 2: Summary task with high compression
    print("Test Case 2: Summary task with high compression")
    print("-" * 50)
    
    config2 = ProcessingConfig(
        compression_intensity="high",
        task_type="summary",
        max_output_length=800
    )
    
    start_time = time.time()
    result2 = workflow.process_excel(
        file_path=file_path,
        task_description="Summarize key sales metrics and performance indicators",
        config=config2
    )
    end_time = time.time()
    
    print(f"Processing time: {end_time - start_time:.2f} seconds")
    print("Output:")
    print(result2)
    print("\n")
    
    # Test Case 3: Inference task with low compression
    print("Test Case 3: Inference task with low compression")
    print("-" * 50)
    
    config3 = ProcessingConfig(
        compression_intensity="low",
        task_type="inference",
        max_output_length=2000
    )
    
    start_time = time.time()
    result3 = workflow.process_excel(
        file_path=file_path,
        task_description="Identify patterns and relationships in the sales data",
        config=config3
    )
    end_time = time.time()
    
    print(f"Processing time: {end_time - start_time:.2f} seconds")
    print("Output:")
    print(result3)
    print("\n")
    
    # Test Case 4: Length constraint test
    print("Test Case 4: Strict length constraint test")
    print("-" * 50)
    
    config4 = ProcessingConfig(
        compression_intensity="medium",
        task_type="analysis",
        max_output_length=300  # Very strict limit
    )
    
    start_time = time.time()
    result4 = workflow.process_excel(
        file_path=file_path,
        task_description="Brief analysis of sales performance",
        config=config4
    )
    end_time = time.time()
    
    print(f"Processing time: {end_time - start_time:.2f} seconds")
    print(f"Output length: {len(result4)} characters")
    print("Output:")
    print(result4)
    print("\n")
    
    print("=== Test Complete ===")

if __name__ == "__main__":
    run_comprehensive_test()