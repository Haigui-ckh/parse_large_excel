from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Dict, Any, Optional
import pandas as pd
from utils.excel_utils import ExcelParser
from config.config import ProcessingConfig

class ExcelParseInput(BaseModel):
    file_path: str = Field(description="Path to the Excel file to parse")
    include_sheets: Optional[List[str]] = Field(default=None, description="List of sheet names to include")
    password: Optional[str] = Field(default=None, description="Password for encrypted Excel files")

class ExcelParseTool(BaseTool):
    name: str = "excel_parser"
    description: str = "Parse Excel files with support for multiple sheets and large files"
    
    def _run(self, file_path: str, include_sheets: Optional[List[str]] = None, password: Optional[str] = None) -> Dict[str, Any]:
        """Parse Excel file and return structured data"""
        try:
            # Parse the Excel file
            sheets_data = ExcelParser.parse_excel(file_path, include_sheets, password)
            
            # Process each sheet
            processed_sheets = {}
            for sheet_name, df in sheets_data.items():
                # Detect data types
                data_types = ExcelParser.detect_data_types(df)
                
                # Detect null values
                null_values = ExcelParser.detect_null_values(df)
                
                # Detect numerical columns for outlier detection
                numerical_columns = [col for col, dtype in data_types.items() if dtype in ['int64', 'float64', 'numeric']]
                outliers = ExcelParser.detect_outliers(df, numerical_columns)
                
                # Store processed data
                processed_sheets[sheet_name] = {
                    "data": df.to_dict(),
                    "shape": df.shape,
                    "columns": list(df.columns),
                    "data_types": data_types,
                    "null_values": null_values,
                    "outliers": outliers
                }
            
            return {
                "status": "success",
                "sheets": processed_sheets,
                "message": f"Successfully parsed {len(processed_sheets)} sheets"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to parse Excel file: {str(e)}"
            }
    
    async def _arun(self, file_path: str, include_sheets: Optional[List[str]] = None, password: Optional[str] = None) -> Dict[str, Any]:
        """Async version of the tool"""
        return self._run(file_path, include_sheets, password)
    
    args_schema: Type[BaseModel] = ExcelParseInput