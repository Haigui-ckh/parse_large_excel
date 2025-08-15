from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate
from typing import Dict, Any, List, Optional
from tools.excel_parser_tool import ExcelParseTool
from tools.data_compression_tool import DataCompressionTool
from tools.format_adapter_tool import FormatAdapterTool
from config.config import ProcessingConfig

class ExcelProcessingChain:
    """Chain that orchestrates the Excel processing workflow"""
    
    def __init__(self):
        # Initialize tools
        self.parser_tool = ExcelParseTool()
        self.compression_tool = DataCompressionTool()
        self.format_tool = FormatAdapterTool()
    
    def create_chain(self) -> SequentialChain:
        """Create the processing chain"""
        # This is a simplified version - a real implementation would use LangChain's
        # SequentialChain or other chain compositions
        
        # For now, we'll define the workflow logic in the run method
        pass
    
    def run(self, 
            file_path: str, 
            task_description: str,
            config: ProcessingConfig,
            password: Optional[str] = None) -> Dict[str, Any]:
        """
        Run the complete Excel processing pipeline
        
        Args:
            file_path: Path to the Excel file
            task_description: Description of the task to guide processing
            config: Processing configuration
            password: Password for encrypted files
            
        Returns:
            Formatted context content for LLM
        """
        
        # Step 1: Parse Excel file
        parse_result = self.parser_tool._run(
            file_path=file_path,
            include_sheets=config.include_sheets,
            password=password
        )
        
        if parse_result["status"] != "success":
            return parse_result
        
        # Step 2: Compress data
        compression_result = self.compression_tool._run(
            data=parse_result,
            config=config
        )
        
        if compression_result["status"] != "success":
            return compression_result
        
        # Step 3: Format output
        format_result = self.format_tool._run(
            data=compression_result,
            task_description=task_description,
            config=config
        )
        
        return format_result