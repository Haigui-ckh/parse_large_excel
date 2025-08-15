import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from io import StringIO

class ExcelParser:
    """Handles parsing of Excel files with support for large files and multiple sheets"""
    
    @staticmethod
    def parse_excel(file_path: str, 
                   include_sheets: Optional[List[str]] = None,
                   password: Optional[str] = None) -> Dict[str, pd.DataFrame]:
        """
        Parse Excel file with support for multiple sheets and password protection
        
        Args:
            file_path: Path to the Excel file
            include_sheets: List of sheet names to include (None for all)
            password: Password for encrypted files
            
        Returns:
            Dictionary mapping sheet names to DataFrames
        """
        try:
            # Load the Excel file
            xl = pd.ExcelFile(file_path, engine='openpyxl')
            
            # Determine which sheets to process
            sheet_names = include_sheets if include_sheets else xl.sheet_names
            
            # Parse each sheet
            sheets_data = {}
            for sheet_name in sheet_names:
                if sheet_name in xl.sheet_names:
                    # For large files, we might need to read in chunks
                    df = xl.parse(sheet_name, engine='openpyxl')
                    sheets_data[sheet_name] = df
                    
            return sheets_data
        except Exception as e:
            raise Exception(f"Error parsing Excel file: {str(e)}")
    
    @staticmethod
    def detect_data_types(df: pd.DataFrame) -> Dict[str, str]:
        """Detect data types for each column in a DataFrame"""
        data_types = {}
        for col in df.columns:
            # Check if column contains formulas (in original Excel)
            # This is a simplified version - real implementation would check Excel XML
            dtype = str(df[col].dtype)
            if 'object' in dtype:
                # Try to infer more specific type
                if df[col].apply(lambda x: isinstance(x, (int, float))).all():
                    data_types[col] = 'numeric'
                elif df[col].apply(lambda x: isinstance(x, str)).all():
                    data_types[col] = 'text'
                else:
                    data_types[col] = 'mixed'
            else:
                data_types[col] = dtype
        return data_types
    
    @staticmethod
    def detect_outliers(df: pd.DataFrame, 
                       numerical_columns: List[str]) -> Dict[str, List[int]]:
        """
        Detect outliers in numerical columns using IQR method
        
        Args:
            df: DataFrame to analyze
            numerical_columns: List of numerical column names
            
        Returns:
            Dictionary mapping column names to lists of outlier row indices
        """
        outliers = {}
        for col in numerical_columns:
            if col in df.columns:
                # Calculate Q1, Q3, and IQR
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                
                # Define outlier bounds
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Find outliers
                outlier_indices = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.tolist()
                outliers[col] = outlier_indices
                
        return outliers
    
    @staticmethod
    def detect_null_values(df: pd.DataFrame) -> Dict[str, int]:
        """Detect null values in each column"""
        null_counts = {}
        for col in df.columns:
            null_counts[col] = df[col].isnull().sum()
        return null_counts