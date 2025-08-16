from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Dict, Any, Optional
import pandas as pd
from config.config import ProcessingConfig
from utils.llm_utils import initialize_deepseek_llm

class DataCompressionInput(BaseModel):
    data: Dict[str, Any] = Field(description="Parsed Excel data from excel_parser tool")
    config: ProcessingConfig = Field(description="Processing configuration")

class DataCompressionTool(BaseTool):
    name: str = "data_compressor"
    description: str = "Compress parsed Excel data using rule-based and LLM-based methods"
    
    def _run(self, data: Dict[str, Any], config: ProcessingConfig) -> Dict[str, Any]:
        """Compress data based on configuration"""
        try:
            # Initialize LLM for dynamic rule generation (if needed)
            llm_config = initialize_deepseek_llm()
            
            compressed_sheets = {}
            
            # Process each sheet
            for sheet_name, sheet_data in data.get("sheets", {}).items():
                df_dict = sheet_data.get("data", {})
                df = pd.DataFrame.from_dict(df_dict)
                
                # Apply compression based on intensity
                if config.compression_intensity == "low":
                    # Minimal compression - just remove null columns with >90% nulls
                    compressed_df = self._apply_low_compression(df)
                elif config.compression_intensity == "medium":
                    # Medium compression - remove null columns, aggregate numerical data
                    compressed_df = self._apply_medium_compression(df, sheet_data)
                else:  # high
                    # High compression - aggressive aggregation and summarization
                    compressed_df = self._apply_high_compression(df, sheet_data, config.task_type)
                
                # Convert back to dict
                compressed_sheets[sheet_name] = {
                    "data": compressed_df.to_dict(),
                    "shape": compressed_df.shape,
                    "columns": list(compressed_df.columns)
                }
            
            return {
                "status": "success",
                "sheets": compressed_sheets,
                "message": f"Successfully compressed {len(compressed_sheets)} sheets"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to compress data: {str(e)}"
            }
    
    def _apply_low_compression(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply minimal compression"""
        # Remove columns with more than 90% null values
        threshold = 0.9 * len(df)
        df_filtered = df.dropna(axis=1, thresh=threshold)
        return df_filtered
    
    def _apply_medium_compression(self, df: pd.DataFrame, sheet_data: Dict) -> pd.DataFrame:
        """Apply medium compression with basic aggregation"""
        # Start with low compression
        df_filtered = self._apply_low_compression(df)
        
        # For numerical columns, add summary statistics
        data_types = sheet_data.get("data_types", {})
        numerical_cols = [col for col, dtype in data_types.items() if dtype in ['int64', 'float64', 'numeric'] and col in df_filtered.columns]
        
        # Create a summary row for numerical data
        if numerical_cols:
            summary_data = {}
            for col in df_filtered.columns:
                if col in numerical_cols:
                    summary_data[col] = {
                        "mean": df_filtered[col].mean(),
                        "median": df_filtered[col].median(),
                        "std": df_filtered[col].std(),
                        "min": df_filtered[col].min(),
                        "max": df_filtered[col].max()
                    }
                else:
                    summary_data[col] = f"Text column with {df_filtered[col].nunique()} unique values"
            
            # Add summary as a new row (in a real implementation, this would be more sophisticated)
            # For now, we'll just return the filtered dataframe
            return df_filtered
        
        return df_filtered
    
    def _apply_high_compression(self, df: pd.DataFrame, sheet_data: Dict, task_type: str) -> pd.DataFrame:
        """Apply high compression with advanced summarization"""
        # Start with medium compression
        df_filtered = self._apply_medium_compression(df, sheet_data)
        
        # Apply task-specific compression
        if task_type == "summary":
            # For summary tasks, we might want to group by categories and aggregate
            # This is a simplified implementation
            pass
        elif task_type == "analysis":
            # For analysis, preserve more detail but still compress
            pass
        elif task_type == "inference":
            # For inference, focus on patterns and relationships
            pass
            
        return df_filtered
    
    async def _arun(self, data: Dict[str, Any], config: ProcessingConfig) -> Dict[str, Any]:
        """Async version of the tool"""
        return self._run(data, config)
    
    args_schema: Type[BaseModel] = DataCompressionInput