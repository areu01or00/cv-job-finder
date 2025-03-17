import requests
import json
from typing import List, Dict, Any, Optional
from .config import OPENROUTER_API_KEY, OPENROUTER_MODEL_1

class OpenRouterClient:
    """Client for interacting with the OpenRouter API."""
    
    def __init__(self, api_key: str = OPENROUTER_API_KEY, model: str = OPENROUTER_MODEL_1):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to OpenRouter.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness (0-1)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Response from the API
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code != 200:
            raise Exception(f"Error from OpenRouter API: {response.text}")
        
        return response.json()
    
    def extract_content(self, response: Dict[str, Any]) -> str:
        """Extract the content from an OpenRouter API response."""
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise Exception(f"Failed to extract content from response: {e}")
    
    def analyze_cv(self, cv_text: str) -> Dict[str, Any]:
        """
        Analyze a CV to extract relevant information.
        
        Args:
            cv_text: The text content of the CV
            
        Returns:
            Dictionary with extracted information
        """
        prompt = [
            {"role": "system", "content": "You are an expert CV analyzer and job recruiter. Your task is to analyze the CV provided and extract key information to help find relevant job opportunities."},
            {"role": "user", "content": f"Please analyze this CV and extract the following information in JSON format: skills, experience, education, job_titles, and relevant_job_keywords. Here's the CV text:\n\n{cv_text}"}
        ]
        
        response = self.chat_completion(prompt, temperature=0.3)
        content = self.extract_content(response)
        
        # Try to parse the JSON response
        try:
            # Find JSON content in the response (it might be wrapped in markdown code blocks)
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].strip()
            else:
                json_str = content
                
            return json.loads(json_str)
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw content
            return {
                "error": "Failed to parse JSON response",
                "raw_content": content
            }
    
    def generate_job_search_queries(self, cv_analysis: Dict[str, Any]) -> List[str]:
        """
        Generate job search queries based on CV analysis.
        
        Args:
            cv_analysis: Dictionary with CV analysis results
            
        Returns:
            List of job search queries
        """
        prompt = [
            {"role": "system", "content": "You are an expert job search assistant. Your task is to generate effective LinkedIn job search queries based on CV analysis."},
            {"role": "user", "content": f"Based on this CV analysis, generate 3-5 effective LinkedIn job search queries. Each query should be optimized to find relevant job opportunities. Return only the list of queries, one per line.\n\nCV Analysis: {json.dumps(cv_analysis, indent=2)}"}
        ]
        
        response = self.chat_completion(prompt, temperature=0.5)
        content = self.extract_content(response)
        
        # Extract queries (one per line)
        queries = [q.strip() for q in content.split('\n') if q.strip()]
        
        # Remove any numbering or bullet points
        queries = [q.lstrip('0123456789.- "\'').strip() for q in queries]
        
        return queries