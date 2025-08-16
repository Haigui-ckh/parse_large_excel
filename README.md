# Excel Processing Agent

This agent processes large-scale Excel data and generates conversation context for LLM interactions, using LangGraph for workflow orchestration.

## Features

- Data parsing with support for multiple sheets and large files
- Intelligent data compression using rule engines and LLMs
- Format adaptation for LLM context windows
- Configurable compression intensity and task types
- Feedback optimization mechanism
- LangGraph-based workflow orchestration

## Technology Stack

- Python 3.8+
- LangChain & LangGraph for workflow orchestration
- Pandas & OpenPyXL for Excel processing
- NumPy for numerical computations
- DeepSeek API for LLM integration

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

### 4. Sample Data Generation
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
2. **Intelligent Compression** - Reduce data size while preserving key information
3. **Format Adaptation** - Convert data into LLM-friendly natural language

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