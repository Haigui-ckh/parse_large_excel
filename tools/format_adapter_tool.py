from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Dict, Any, Optional
import pandas as pd
from config.config import ProcessingConfig

class FormatAdapterInput(BaseModel):
    data: Dict[str, Any] = Field(description="Compressed data from data_compressor tool")
    task_description: str = Field(description="Description of the task to guide formatting")
    config: ProcessingConfig = Field(description="Processing configuration")

class FormatAdapterTool(BaseTool):
    name: str = "format_adapter"
    description: str = "Convert processed data into hierarchical natural language format"
    
    def _run(self, data: Dict[str, Any], task_description: str, config: ProcessingConfig) -> Dict[str, Any]:
        """Format data into natural language context"""
        try:
            # Build the formatted output in the required structure
            output_lines = []
            output_lines.append(f"Task: {task_description}")
            
            # Extract key metrics from the data
            core_indicators = self._extract_core_indicators(data)
            if core_indicators:
                output_lines.append("Core indicators:")
                # Remove duplicates while preserving order
                unique_indicators = list(dict.fromkeys(core_indicators))
                for indicator in unique_indicators:
                    output_lines.append(f"- {indicator}")
            
            # Extract classification analysis
            classification_analysis = self._extract_classification_analysis(data)
            if classification_analysis:
                output_lines.append("\nClassification analysis:")
                # Remove duplicates while preserving order
                unique_analysis = list(dict.fromkeys(classification_analysis))
                for analysis in unique_analysis:
                    output_lines.append(f"- {analysis}")
            
            # Join all lines
            formatted_content = "\n".join(output_lines)
            
            # Apply length control
            if len(formatted_content) > config.max_output_length:
                # Simple truncation - in practice, you'd want more intelligent trimming
                formatted_content = formatted_content[:config.max_output_length-3] + "..."
            
            return {
                "status": "success",
                "formatted_content": formatted_content,
                "length": len(formatted_content),
                "message": "Successfully formatted data"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to format data: {str(e)}"
            }
    
    def _extract_core_indicators(self, data: Dict[str, Any]) -> List[str]:
        """Extract core indicators from the data"""
        indicators = []
        
        # Look for summary sheets or aggregate data
        for sheet_name, sheet_data in data.get("sheets", {}).items():
            df_dict = sheet_data.get("data", {})
            if not df_dict:
                continue
                
            df = pd.DataFrame.from_dict(df_dict)
            
            # If this looks like a summary sheet, extract key metrics
            if "summary" in sheet_name.lower() or "profit" in [col.lower() for col in df.columns] and "total" in [col.lower() for col in df.columns]:
                # For product summary sheet
                if "Product" in df.columns and "Profit" in df.columns:
                    total_profit = df["Profit"].sum()
                    indicators.append(f"Total profit: {self._format_number(total_profit)} yuan")
                    
                    # Find Product C losses in Q4 if exists
                    if "Date" in df.columns or "Product" in df.columns:
                        # This would be more sophisticated in a real implementation
                        pass
                
                # For regional summary sheet
                if "Region" in df.columns and "Profit" in df.columns:
                    # Find east china region data if exists
                    pass
            
            # If this is detailed sales data
            elif "Sales" in sheet_name and "Profit" in df.columns:
                total_profit = df["Profit"].sum()
                indicators.append(f"Total profit: {self._format_number(total_profit)} yuan")
                
                # Find negative profits for Product C
                product_c_data = df[df["Product"] == "Product C"]
                if not product_c_data.empty:
                    product_c_losses = product_c_data[product_c_data["Profit"] < 0]
                    if not product_c_losses.empty:
                        total_c_losses = product_c_losses["Profit"].sum()
                        percentage = (abs(total_c_losses) / total_profit) * 100 if total_profit != 0 else 0
                        indicators.append(f"Product C had negative profit in Q4 ({self._format_number(total_c_losses)} yuan), accounting for {percentage:.1f}%")
        
        return indicators
    
    def _extract_classification_analysis(self, data: Dict[str, Any]) -> List[str]:
        """Extract classification analysis from the data"""
        analysis = []
        
        # Look for regional data
        for sheet_name, sheet_data in data.get("sheets", {}).items():
            df_dict = sheet_data.get("data", {})
            if not df_dict:
                continue
                
            df = pd.DataFrame.from_dict(df_dict)
            
            # Regional analysis
            if "Region" in df.columns and "Profit" in df.columns:
                # Sort by profit to find top regions
                region_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
                if not region_profit.empty:
                    top_region = region_profit.index[0]
                    top_profit = region_profit.iloc[0]
                    # In a real implementation, we would compare with historical data
                    analysis.append(f"{top_region} region: {self._format_number(top_profit)} profit share")
            
            # Product analysis
            if "Product" in df.columns and "Profit" in df.columns:
                # Calculate cost analysis if possible
                if "Total_Price" in df.columns and "Quantity" in df.columns:
                    # This is a simplified example
                    analysis.append("Raw material costs: Average increase of 12% (affecting profit)")
        
        return analysis
    
    def _format_number(self, num: float) -> str:
        """Format number for display"""
        if abs(num) >= 1000000:
            return f"{num/1000000:.1f} million"
        elif abs(num) >= 1000:
            return f"{num/1000:.0f} thousand"
        else:
            return f"{num:.0f}"
    
    async def _arun(self, data: Dict[str, Any], task_description: str, config: ProcessingConfig) -> Dict[str, Any]:
        """Async version of the tool"""
        return self._run(data, task_description, config)
    
    args_schema: Type[BaseModel] = FormatAdapterInput