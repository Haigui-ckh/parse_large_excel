"""
LangGraph-based implementation of the Excel processing agent
"""

from typing import Annotated, Literal, TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
from agents.excel_processing_agent import ExcelProcessingAgent
from config.config import ProcessingConfig

# Load environment variables
load_dotenv()

class ExcelProcessingState(TypedDict):
    """State definition for the Excel processing workflow"""
    file_path: str
    task_description: str
    config: ProcessingConfig
    parsed_data: Dict[str, Any]
    compressed_data: Dict[str, Any]
    formatted_output: str
    messages: Annotated[list, add_messages]
    next_action: Literal["parse", "compress", "format", "end"]

class ExcelProcessingWorkflow:
    """LangGraph-based workflow for Excel processing"""
    
    def __init__(self):
        self.agent = ExcelProcessingAgent()
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow"""
        workflow = StateGraph(ExcelProcessingState)
        
        # Add nodes
        workflow.add_node("parse_excel", self._parse_excel)
        workflow.add_node("compress_data", self._compress_data)
        workflow.add_node("format_output", self._format_output)
        
        # Add edges
        workflow.add_edge(START, "parse_excel")
        workflow.add_edge("parse_excel", "compress_data")
        workflow.add_edge("compress_data", "format_output")
        workflow.add_edge("format_output", END)
        
        return workflow
    
    def _parse_excel(self, state: ExcelProcessingState) -> Dict[str, Any]:
        """Parse Excel file"""
        print("Parsing Excel file...")
        result = self.agent.parser_tool._run(
            file_path=state["file_path"],
            include_sheets=state["config"].include_sheets,
            password=None  # Not implemented in this example
        )
        
        if result["status"] == "success":
            return {
                "parsed_data": result,
                "messages": [{"role": "system", "content": "Excel file parsed successfully"}]
            }
        else:
            return {
                "messages": [{"role": "system", "content": f"Error parsing Excel: {result['message']}"}],
                "next_action": "end"
            }
    
    def _compress_data(self, state: ExcelProcessingState) -> Dict[str, Any]:
        """Compress parsed data"""
        print("Compressing data...")
        result = self.agent.compression_tool._run(
            data=state["parsed_data"],
            config=state["config"]
        )
        
        if result["status"] == "success":
            return {
                "compressed_data": result,
                "messages": [{"role": "system", "content": "Data compressed successfully"}]
            }
        else:
            return {
                "messages": [{"role": "system", "content": f"Error compressing data: {result['message']}"}],
                "next_action": "end"
            }
    
    def _format_output(self, state: ExcelProcessingState) -> Dict[str, Any]:
        """Format compressed data"""
        print("Formatting output...")
        result = self.agent.format_tool._run(
            data=state["compressed_data"],
            task_description=state["task_description"],
            config=state["config"]
        )
        
        if result["status"] == "success":
            return {
                "formatted_output": result["formatted_content"],
                "messages": [{"role": "system", "content": "Output formatted successfully"}]
            }
        else:
            return {
                "messages": [{"role": "system", "content": f"Error formatting output: {result['message']}"}],
                "next_action": "end"
            }
    
    def process_excel(self, 
                     file_path: str, 
                     task_description: str,
                     config: ProcessingConfig) -> str:
        """
        Process Excel file using LangGraph workflow
        
        Args:
            file_path: Path to the Excel file
            task_description: Description of the task to guide processing
            config: Processing configuration
            
        Returns:
            Formatted context content for LLM
        """
        # Compile the workflow
        app = self.workflow.compile()
        
        # Initial state
        initial_state = ExcelProcessingState(
            file_path=file_path,
            task_description=task_description,
            config=config,
            parsed_data={},
            compressed_data={},
            formatted_output="",
            messages=[],
            next_action="parse"
        )
        
        # Execute the workflow
        final_state = app.invoke(initial_state)
        
        return final_state.get("formatted_output", "Error: No output generated")

# Example usage
if __name__ == "__main__":
    # Initialize workflow
    workflow = ExcelProcessingWorkflow()
    
    # Configuration
    config = ProcessingConfig(
        compression_intensity="medium",
        task_type="analysis",
        max_output_length=2000
    )
    
    # Process Excel file
    result = workflow.process_excel(
        file_path="sample_data.xlsx",
        task_description="Analyze profit anomalies in sales data",
        config=config
    )
    
    print("Final Output:")
    print(result)