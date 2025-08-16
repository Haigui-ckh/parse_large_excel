"""
Main entry point for the LangGraph-based Excel processing agent
"""

from agents.langgraph_agent import ExcelProcessingWorkflow
from config.config import ProcessingConfig
import sys
import os

def main():
    # Example usage
    workflow = ExcelProcessingWorkflow()
    
    # Example configuration
    config = ProcessingConfig(
        compression_intensity="medium",
        task_type="analysis",
        max_output_length=2000
    )
    
    # Example file path (you would replace this with your actual file)
    file_path = "sample_data.xlsx"  # Replace with your file path
    
    # Example task description
    task_description = "Analyze profit anomalies in sales data"
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Please provide a valid Excel file.")
        return
    
    # Process the Excel file
    result = workflow.process_excel(
        file_path=file_path,
        task_description=task_description,
        config=config
    )
    
    # Print the result
    print("Successfully processed Excel file!")
    print("Formatted output:")
    print(result)

if __name__ == "__main__":
    main()