"""
Test case demonstrating feedback optimization for the Excel processing agent
"""

from agents.langgraph_agent import ExcelProcessingWorkflow
from config.config import ProcessingConfig
import os

class FeedbackOptimizationTest:
    """Test class for demonstrating feedback optimization"""
    
    def __init__(self):
        self.workflow = ExcelProcessingWorkflow()
        self.file_path = "simple_sample_data.xlsx"
        
    def run_feedback_test(self):
        """Run a test demonstrating feedback optimization"""
        print("=== Feedback Optimization Test Case ===\n")
        
        if not os.path.exists(self.file_path):
            print(f"Test file {self.file_path} not found.")
            return
        
        # Initial processing
        print("Step 1: Initial processing with default configuration")
        print("-" * 55)
        
        initial_config = ProcessingConfig(
            compression_intensity="medium",
            task_type="analysis",
            max_output_length=1000
        )
        
        initial_result = self.workflow.process_excel(
            file_path=self.file_path,
            task_description="Analyze sales data for anomalies and trends",
            config=initial_config
        )
        
        print("Initial output:")
        print(initial_result)
        print(f"Length: {len(initial_result)} characters\n")
        
        # Simulate user feedback - "I need more details about regional performance"
        print("Step 2: Processing with feedback - 'I need more details about regional performance'")
        print("-" * 80)
        
        # Adjust configuration based on feedback
        feedback_config = ProcessingConfig(
            compression_intensity="low",  # Lower compression for more details
            task_type="analysis",
            max_output_length=1500,
            # In a real implementation, we could also pass specific feedback to influence processing
        )
        
        feedback_result = self.workflow.process_excel(
            file_path=self.file_path,
            task_description="Analyze sales data with focus on regional performance differences",
            config=feedback_config
        )
        
        print("Feedback-optimized output:")
        print(feedback_result)
        print(f"Length: {len(feedback_result)} characters\n")
        
        # Simulate another feedback - "Make it more concise"
        print("Step 3: Processing with feedback - 'Make it more concise'")
        print("-" * 55)
        
        concise_config = ProcessingConfig(
            compression_intensity="high",  # Higher compression for conciseness
            task_type="summary",
            max_output_length=500
        )
        
        concise_result = self.workflow.process_excel(
            file_path=self.file_path,
            task_description="Provide a concise summary of sales performance",
            config=concise_config
        )
        
        print("Concise output:")
        print(concise_result)
        print(f"Length: {len(concise_result)} characters\n")
        
        print("=== Feedback Optimization Test Complete ===")
        print("\nKey Takeaways:")
        print("1. The agent can adapt to different compression levels based on user needs")
        print("2. Task type can be adjusted to focus on different aspects of the data")
        print("3. Output length can be controlled to meet specific requirements")
        print("4. In a full implementation, specific feedback could be used to guide processing")

def main():
    test = FeedbackOptimizationTest()
    test.run_feedback_test()

if __name__ == "__main__":
    main()