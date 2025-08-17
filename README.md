# Excel Processing Agent

This agent processes large-scale Excel data and generates conversation context for LLM interactions, using LangGraph for workflow orchestration and DeepSeek API for intelligent processing.

## Features

- Data parsing with support for multiple sheets and large files
- Intelligent data compression using rule engines and LLMs
- Format adaptation for LLM context windows
- Configurable compression intensity and task types
- Feedback optimization mechanism
- LangGraph-based workflow orchestration
- DeepSeek LLM integration for intelligent data analysis

## Technology Stack

- Python 3.8+
- LangChain & LangGraph for workflow orchestration
- Pandas & OpenPyXL for Excel processing
- NumPy for numerical computations
- DeepSeek API for LLM integration
- HTTPX for API requests

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with your API configuration:

```env
DEEPSEEK_API_KEY=sk-279a17e1202e4361839e79482a3d5d3e
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

## Usage

### Basic Usage

```python
from agents.langgraph_agent import ExcelProcessingWorkflow
from config.config import ProcessingConfig

# Initialize the workflow
workflow = ExcelProcessingWorkflow()

# Configure processing options
config = ProcessingConfig(
    compression_intensity="medium",  # low, medium, high
    task_type="analysis",            # analysis, summary, inference
    max_output_length=2000
)

# Process an Excel file
result = workflow.process_excel(
    file_path="path/to/your/file.xlsx",
    task_description="Analyze sales data for trends and anomalies",
    config=config
)

# View the formatted output
print(result)
```

### Different Compression Levels

```python
# Low compression for detailed analysis
config_low = ProcessingConfig(
    compression_intensity="low",
    task_type="analysis",
    max_output_length=3000
)

# High compression for summary
config_high = ProcessingConfig(
    compression_intensity="high",
    task_type="summary",
    max_output_length=500
)
```

## LLM Integration

The agent uses the DeepSeek API for intelligent data processing:

1. **Dynamic Compression Rules**: LLM generates compression rules based on data structure and task type
2. **Key Insight Extraction**: LLM extracts important insights from the data
3. **Natural Language Formatting**: LLM formats output in human-readable language

### LLM Functions

- `generate_compression_rules()`: Creates data-specific compression strategies
- `extract_key_insights()`: Identifies important patterns and anomalies
- `call_deepseek_llm()`: Generic LLM calling function

## Test Cases

The repository includes several test cases to demonstrate the agent's capabilities:

### 1. Comprehensive Test (`test_comprehensive.py`)
Tests the agent with different configurations and task types:
```bash
python test_comprehensive.py
```

### 2. Feedback Optimization Test (`test_feedback.py`)
Demonstrates how the agent can adapt to user feedback:
```bash
python test_feedback.py
```

### 3. Error Handling Test (`test_error_handling.py`)
Tests error handling and edge cases:
```bash
python test_error_handling.py
```

### 4. LLM Integration Test (`test_llm.py`)
Tests the LLM integration functions:
```bash
python test_llm.py
```

### 5. Sample Data Generation
Scripts to generate test data:
- `generate_sample_data.py`: Simple sample data
- `generate_complex_sample_data.py`: Complex sample data with anomalies

## Project Architecture

### 1. Tools (`tools/`)
Individual processing units that perform specific tasks:
- `ExcelParseTool` - Parses Excel files with support for multiple sheets
- `DataCompressionTool` - Compresses data using rule-based methods and LLM assistance
- `FormatAdapterTool` - Converts data into natural language format

### 2. Agents (`agents/`)
Workflow controllers:
- `ExcelProcessingAgent` - Traditional LangChain agent
- `LangGraphAgent` - LangGraph-based workflow implementation

### 3. Utilities (`utils/`)
Helper functions:
- `ExcelParser` - Low-level Excel parsing utilities
- `LLMUtils` - LLM integration utilities

### 4. Configuration (`config/`)
Configuration definitions:
- `ProcessingConfig` - Configuration schema for processing parameters

## Workflow Process

The agent follows a three-stage pipeline implemented with LangGraph:

1. **Data Parsing** - Extract and analyze Excel data
2. **Intelligent Compression** - Reduce data size while preserving key information (LLM-assisted)
3. **Format Adaptation** - Convert data into LLM-friendly natural language (LLM-assisted)

## Output Format

The agent generates context in this format:

```
Task: [Task description]

### [LLM-generated insights with key metrics, anomalies, patterns, and recommendations]
```

Example:
```
Task: Analyze profit anomalies in sales data

### Key Insights:  

1. **Key Metrics & Trends**  
   - **Product Performance**:  
     - **Product B** has the highest total sales (9,725,534) and profit (1,926,896), despite **Product A** having nearly the same quantity sold.  
     - **Product C** has the lowest profit margin (~13% of total price) compared to others (~20%).  
   - **Regional Performance**:  
     - **North** generates the highest revenue (9,806,751) and profit (1,836,675), followed by **East**.  
     - **Central** has the lowest profit margin (~18.5% of revenue) despite moderate sales volume.  

2. **Notable Anomalies/Outliers**  
   - **Product C** has high sales volume (39,935 units) but significantly lower profit (~13% margin) compared to others (~20%). Suggests pricing or cost inefficiencies.  
   - **Central Region** underperforms in profit despite decent sales—possible higher costs or lower-margin products dominating sales.  

3. **Important Patterns & Relationships**  
   - **Profit vs. Quantity Mismatch**: High sales volume (e.g., Product C) doesn’t always correlate with high profit.  
   - **Regional Disparities**: North and East outperform Central in profitability, indicating potential market or operational differences.  

4. **Actionable Recommendations**  
   - **Investigate Product C’s Costs**: Optimize pricing or reduce production costs to improve margins.  
   - **Analyze Central Region’s Expenses**: Identify why profit margins lag despite solid sales.  
   - **Promote High-Margin Products**: Prioritize **Product B** and **A** in underperforming regions.  
   - **Regional Strategy Adjustment**: Replicate North/East’s success factors (e.g., pricing, promotions) in Central.  
```