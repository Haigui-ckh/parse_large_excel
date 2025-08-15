# Excel Processing Agent

This agent processes large-scale Excel data and generates conversation context for LLM interactions, following a three-stage pipeline:
1. **Data Parsing** - Extract and analyze Excel data
2. **Intelligent Compression** - Reduce data size while preserving key information
3. **Format Adaptation** - Convert data into LLM-friendly natural language

## Features

- Data parsing with support for multiple sheets and large files
- Intelligent data compression using rule engines and LLMs
- Format adaptation for LLM context windows
- Configurable compression intensity and task types

## Technology Stack

- Python 3.8+
- LangChain for workflow orchestration
- Pandas & OpenPyXL for Excel processing
- NumPy for numerical computations

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from agents.excel_processing_agent import ExcelProcessingAgent
from config.config import ProcessingConfig

# Initialize the agent
agent = ExcelProcessingAgent()

# Configure processing options
config = ProcessingConfig(
    compression_intensity="medium",  # low, medium, high
    task_type="analysis",            # analysis, summary, inference
    max_output_length=2000
)

# Process an Excel file
result = agent.process_excel(
    file_path="path/to/your/file.xlsx",
    task_description="Analyze sales data for trends and anomalies",
    config=config
)

# View the formatted output
print(result["formatted_content"])
```

## Project Architecture

### 1. Tools (`tools/`)
Individual processing units that perform specific tasks:
- `ExcelParseTool` - Parses Excel files with support for multiple sheets
- `DataCompressionTool` - Compresses data using rule-based methods
- `FormatAdapterTool` - Converts data into natural language format

### 2. Chains (`chains/`)
LangChain components that orchestrate tools:
- `ExcelProcessingChain` - Sequential chain that connects all processing steps

### 3. Agents (`agents/`)
High-level controllers that manage the workflow:
- `ExcelProcessingAgent` - Main agent that executes the processing pipeline

### 4. Utilities (`utils/`)
Helper functions for common operations:
- `ExcelParser` - Low-level Excel parsing utilities

### 5. Configuration (`config/`)
Configuration definitions:
- `ProcessingConfig` - Configuration schema for processing parameters

## Sample Data

The repository includes a `generate_sample_data.py` script that creates sample Excel data for testing.

## Output Format

The agent generates context in this format:

```
Task: [Task description]
Core indicators:
- [Key metrics and findings]

Classification analysis:
- [Categorized insights]
```

Example:
```
Task: Analyze profit anomalies in sales data
Core indicators:
- Total profit: 8.6 million yuan
- Product C had negative profit in Q4 (-541 thousand yuan), accounting for 6.3%

Classification analysis:
- North region: 1.8 million profit share
- Raw material costs: Average increase of 12% (affecting profit)
```