"""
Test case for error handling and edge cases in the Excel processing agent
"""

from agents.langgraph_agent import ExcelProcessingWorkflow
from config.config import ProcessingConfig
import os

def test_error_handling():
    """Test error handling and edge cases"""
    
    print("=== Error Handling and Edge Cases Test ===\n")
    
    # Initialize workflow
    workflow = ExcelProcessingWorkflow()
    
    # Test Case 1: Non-existent file
    print("Test Case 1: Non-existent file")
    print("-" * 30)
    
    try:
        result = workflow.process_excel(
            file_path="non_existent_file.xlsx",
            task_description="Test with non-existent file",
            config=ProcessingConfig()
        )
        print("Result:")
        print(result)
    except Exception as e:
        print(f"Exception caught (as expected): {e}")
    print("\n")
    
    # Test Case 2: Invalid configuration
    print("Test Case 2: Invalid configuration parameters")
    print("-" * 45)
    
    # Using the simple sample data
    file_path = "simple_sample_data.xlsx"
    
    if os.path.exists(file_path):
        # Test with extreme compression settings
        extreme_config = ProcessingConfig(
            compression_intensity="invalid_value",  # This should be handled gracefully
            task_type="analysis",
            max_output_length=0  # This should be handled gracefully
        )
        
        try:
            result = workflow.process_excel(
                file_path=file_path,
                task_description="Test with extreme configuration",
                config=extreme_config
            )
            print("Result with extreme config:")
            print(result)
        except Exception as e:
            print(f"Exception caught: {e}")
    else:
        print(f"Test file {file_path} not found.")
    print("\n")
    
    # Test Case 3: Very large output constraint
    print("Test Case 3: Very small output constraint")
    print("-" * 38)
    
    if os.path.exists(file_path):
        tiny_config = ProcessingConfig(
            compression_intensity="medium",
            task_type="analysis",
            max_output_length=50  # Very small constraint
        )
        
        result = workflow.process_excel(
            file_path=file_path,
            task_description="Test with tiny output constraint",
            config=tiny_config
        )
        
        print("Result with tiny constraint:")
        print(result)
        print(f"Length: {len(result)} characters")
    print("\n")
    
    # Test Case 4: Different task types
    print("Test Case 4: Different task types")
    print("-" * 30)
    
    if os.path.exists(file_path):
        task_types = ["analysis", "summary", "inference"]
        
        for task_type in task_types:
            print(f"Testing task type: {task_type}")
            config = ProcessingConfig(
                compression_intensity="medium",
                task_type=task_type,
                max_output_length=1000
            )
            
            result = workflow.process_excel(
                file_path=file_path,
                task_description=f"Testing {task_type} task type",
                config=config
            )
            
            print(f"Result for {task_type}:")
            print(result[:200] + "..." if len(result) > 200 else result)
            print()
    
    print("=== Error Handling Test Complete ===")

if __name__ == "__main__":
    test_error_handling()