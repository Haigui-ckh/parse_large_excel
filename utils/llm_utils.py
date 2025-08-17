"""
Utility functions for LLM integration with DeepSeek API
"""

from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import os
import httpx
import json

# Load environment variables
load_dotenv()

def get_deepseek_api_key() -> Optional[str]:
    """Get DeepSeek API key from environment variables"""
    return os.getenv("DEEPSEEK_API_KEY")

def get_deepseek_base_url() -> Optional[str]:
    """Get DeepSeek base URL from environment variables"""
    return os.getenv("DEEPSEEK_BASE_URL")

def initialize_deepseek_llm():
    """
    Initialize DeepSeek LLM for use in the compression module
    """
    api_key = get_deepseek_api_key()
    base_url = get_deepseek_base_url()
    
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
    
    if not base_url:
        raise ValueError("DEEPSEEK_BASE_URL not found in environment variables")
    
    return {
        "api_key": api_key,
        "base_url": base_url
    }

def call_deepseek_llm(prompt: str, system_message: str = "", temperature: float = 0.7, max_tokens: int = 500) -> str:
    """
    Call DeepSeek LLM with the given prompt
    
    Args:
        prompt: The user prompt
        system_message: System message to guide the model
        temperature: Sampling temperature (0.0 to 1.0)
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        Generated response from the LLM
    """
    try:
        # Initialize LLM configuration
        llm_config = initialize_deepseek_llm()
        
        # Prepare the API request
        headers = {
            "Authorization": f"Bearer {llm_config['api_key']}",
            "Content-Type": "application/json"
        }
        
        # Prepare messages
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        # Prepare request body
        data = {
            "model": "deepseek-chat",  # Using DeepSeek's chat model
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # Make the API call
        url = f"{llm_config['base_url']}/v1/chat/completions"
        
        # Using httpx for the API call
        response = httpx.post(url, headers=headers, json=data, timeout=30.0)
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        return result["choices"][0]["message"]["content"]
        
    except Exception as e:
        # Return a fallback response in case of API errors
        return f"Error calling LLM: {str(e)}. Using rule-based approach instead."

def generate_compression_rules(data_description: str, task_type: str) -> str:
    """
    Generate dynamic compression rules using LLM
    
    Args:
        data_description: Description of the data structure
        task_type: Type of task (analysis, summary, inference)
        
    Returns:
        Generated compression rules
    """
    system_message = "You are an expert data analyst specializing in data compression for large datasets."
    
    prompt = f"""
    Given the following data structure and task type, generate specific compression rules:
    
    Data Description:
    {data_description}
    
    Task Type: {task_type}
    
    Please provide:
    1. Which columns or data points are most important to preserve
    2. Which columns can be aggregated or removed
    3. What statistical summaries should be generated
    4. Any special handling for anomalies or outliers
    
    Keep your response concise and focused on actionable rules.
    """
    
    return call_deepseek_llm(prompt, system_message, temperature=0.5, max_tokens=300)

def extract_key_insights(data_summary: str, task_description: str) -> str:
    """
    Extract key insights from data summary using LLM
    
    Args:
        data_summary: Summary of the data
        task_description: Description of the analysis task
        
    Returns:
        Extracted key insights
    """
    system_message = "You are an expert data analyst skilled at extracting key insights from complex datasets."
    
    prompt = f"""
    Based on the following data summary and task description, extract the most important insights:
    
    Data Summary:
    {data_summary}
    
    Task Description:
    {task_description}
    
    Please provide:
    1. Key metrics and trends
    2. Notable anomalies or outliers
    3. Important patterns or relationships
    4. Actionable recommendations
    
    Format your response as a concise list of insights.
    """
    
    return call_deepseek_llm(prompt, system_message, temperature=0.3, max_tokens=400)