from agents.excel_processing_agent import ExcelProcessingAgent
from config.config import ProcessingConfig
import sys
import os

def main():
    # Example usage
    agent = ExcelProcessingAgent()
    
    # Example configuration
    config = ProcessingConfig(
        compression_intensity="medium",
        task_type="analysis",
        max_output_length=2000
    )
    
    # Use the generated sample file
    file_path = "sample_data.xlsx"
    
    # Example task description
    task_description = "Analyze profit anomalies in sales data"
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Please provide a valid Excel file.")
        return
    
    # Process the Excel file
    result = agent.process_excel(
        file_path=file_path,
        task_description=task_description,
        config=config
    )
    
    # Print the result
    if result["status"] == "success":
        print("Successfully processed Excel file!")
        print("Formatted output:")
        print(result["formatted_content"])
        print(f"Output length: {result['length']} characters")
    else:
        print(f"Error processing Excel file: {result['message']}")

if __name__ == "__main__":
    main()