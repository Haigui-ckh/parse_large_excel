"""
Utility functions for LLM integration with DeepSeek API
"""

from typing import Optional
from dotenv import load_dotenv
import os

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
    This is a placeholder implementation - in a full implementation,
    this would return a configured LLM instance
    """
    api_key = get_deepseek_api_key()
    base_url = get_deepseek_base_url()
    
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
    
    if not base_url:
        raise ValueError("DEEPSEEK_BASE_URL not found in environment variables")
    
    # In a full implementation, this would create and return an LLM instance
    # For now, we'll just return the configuration
    return {
        "api_key": api_key,
        "base_url": base_url
    }