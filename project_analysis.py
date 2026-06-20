"""
Project Analysis: Instagram Caption Generator

This script analyzes the caption generator code to understand:
1. How API calls work
2. How data flows through the application
3. Code structure and best practices
"""

import requests
import json
from datetime import datetime

def analyze_api_response(response_data):
    """Study how the API response is structured"""
    print("📊 API Response Analysis")
    print("="*50)
    print(f"Response Keys: {list(response_data.keys())}")
    
    if 'choices' in response_data:
        print(f"Number of choices: {len(response_data['choices'])}")
        print(f"Model used: {response_data.get('model', 'N/A')}")
        print(f"Usage: {response_data.get('usage', {})}")
    
    return response_data

def track_request_metrics(prompt, response):
    """Track performance metrics for analysis"""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "prompt_length": len(prompt),
        "response_length": len(response),
        "response_time": 0.0  # Would be calculated from actual request
    }
    return metrics

# Example usage
if __name__ == "__main__":
    print("🔍 Starting Project Analysis...")
    print("✅ Ready to analyze your AI project!")