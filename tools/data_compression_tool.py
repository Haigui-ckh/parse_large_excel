from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Dict, Any, Optional
import pandas as pd
from config.config import ProcessingConfig
from utils.llm_utils import initialize_deepseek_llm, generate_compression_rules

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
                
                # Get data description for LLM
                data_description = self._get_data_description(df, sheet_data)
                
                # Generate dynamic compression rules using LLM
                compression_rules = generate_compression_rules(data_description, config.task_type)
                
                # Apply compression based on intensity
                if config.compression_intensity == "low":
                    # Minimal compression - just remove null columns with >90% nulls
                    compressed_df = self._apply_low_compression(df)
                elif config.compression_intensity == "medium":
                    # Medium compression - remove null columns, aggregate numerical data
                    compressed_df = self._apply_medium_compression(df, sheet_data, compression_rules)
                else:  # high
                    # High compression - aggressive aggregation and summarization
                    compressed_df = self._apply_high_compression(df, sheet_data, config.task_type, compression_rules)
                
                # Convert back to dict
                compressed_sheets[sheet_name] = {
                    "data": compressed_df.to_dict(),
                    "shape": compressed_df.shape,
                    "columns": list(compressed_df.columns),
                    "compression_rules": compression_rules  # Include rules for debugging
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
    
    def _get_data_description(self, df: pd.DataFrame, sheet_data: Dict) -> str:
        """Generate a description of the data for the LLM"""
        description = f"Dataset with {df.shape[0]} rows and {df.shape[1]} columns. "
        description += f"Columns: {', '.join(df.columns)} "
        
        data_types = sheet_data.get("data_types", {})
        if data_types:
            description += "Data types: "
            for col, dtype in data_types.items():
                description += f"{col} ({dtype}), "
            description = description.rstrip(", ") + " "
        
        null_values = sheet_data.get("null_values", {})
        if null_values:
            description += "Null value counts: "
            for col, null_count in null_values.items():
                if null_count > 0:
                    description += f"{col} ({null_count}), "
            description = description.rstrip(", ") + " "
        
        outliers = sheet_data.get("outliers", {})
        if outliers:
            description += "Outliers detected in: "
            for col, outlier_indices in outliers.items():
                if outlier_indices:
                    description += f"{col} ({len(outlier_indices)} outliers), "
            description = description.rstrip(", ") + " "
        
        return description.strip()
    
    def _apply_low_compression(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply minimal compression"""
        # Remove columns with more than 90% null values
        threshold = 0.9 * len(df)
        df_filtered = df.dropna(axis=1, thresh=threshold)
        return df_filtered
    
    def _apply_medium_compression(self, df: pd.DataFrame, sheet_data: Dict, compression_rules: str) -> pd.DataFrame:
        """Apply medium compression with LLM-assisted rules"""
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
                    # Use LLM rules for text columns
                    unique_count = df_filtered[col].nunique()
                    summary_data[col] = f"Text column with {unique_count} unique values. Rules: {compression_rules[:100]}..."
            
            # Add summary as a new row (in a real implementation, this would be more sophisticated)
            # For now, we'll just return the filtered dataframe
            return df_filtered
        
        return df_filtered
    
    def _apply_high_compression(self, df: pd.DataFrame, sheet_data: Dict, task_type: str, compression_rules: str) -> pd.DataFrame:
        """Apply high compression with LLM-assisted summarization"""
        # Start with medium compression
        df_filtered = self._apply_medium_compression(df, sheet_data, compression_rules)
        
        # Apply task-specific compression with LLM guidance
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