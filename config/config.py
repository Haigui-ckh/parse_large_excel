from dataclasses import dataclass
from typing import Optional, Dict, Any, List

@dataclass
class ProcessingConfig:
    """Configuration for the Excel processing pipeline"""
    compression_intensity: str = "medium"  # low, medium, high
    task_type: str = "analysis"  # analysis, summary, inference
    max_output_length: int = 2000
    exclude_columns: List[str] = None
    include_sheets: List[str] = None
    
    def __post_init__(self):
        if self.exclude_columns is None:
            self.exclude_columns = []
        if self.include_sheets is None:
            self.include_sheets = []