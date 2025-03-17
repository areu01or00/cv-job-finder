import json
from typing import Dict, Any, List, Tuple
from .llm import OpenRouterClient

class AdvancedFeatures:
    """Advanced AI-powered features for the CV-Based Job Finder application."""
    
    def __init__(self, llm_client=None):
        """Initialize the advanced features with an LLM client."""
        self.llm_client = llm_client or OpenRouterClient()
    
    def optimize_cv(self, cv_analysis: Dict[str, Any], target_job_title: str) -> Dict[str, Any]:
        """
        Generate tailored recommendations to optimize a CV for a specific job.
        
        Args:
            cv_analysis: Dictionary with CV analysis results
            target_job_title: The job title to optimize the CV for
            
        Returns:
            Dictionary with optimization recommendations
        """
        prompt = [
            {"role": "system", "content": "You are an expert CV optimization assistant. Your task is to provide specific, actionable recommendations to optimize a CV for a target job."},
            {"role": "user", "content": f"Based on this CV analysis and target job '{target_job_title}', provide specific recommendations to optimize the CV. Include what skills to add, what experiences to emphasize, and what to remove or de-emphasize. Format your response as JSON with the following keys: 'skills_to_add', 'skills_to_emphasize', 'experiences_to_emphasize', 'items_to_remove', and 'general_recommendations'.\n\nCV Analysis: {json.dumps(cv_analysis, indent=2)}"}
        ]
        
        response = self.llm_client.chat_completion(prompt, temperature=0.3)
        content = self.llm_client.extract_content(response)
        
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
            # If JSON parsing fails, return a structured error
            return {
                "error": "Failed to parse optimization recommendations",
                "raw_content": content
            }
    
    def calculate_job_match_score(self, cv_analysis: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """
        Calculate a compatibility score between a CV and job description.
        
        Args:
            cv_analysis: Dictionary with CV analysis results
            job_description: The job description text
            
        Returns:
            Dictionary with compatibility scores and recommendations
        """
        prompt = [
            {"role": "system", "content": "You are an expert job compatibility analyst. Your task is to calculate how well a candidate's CV matches a job description and provide a detailed compatibility analysis."},
            {"role": "user", "content": f"Calculate the compatibility between this CV and job description. Provide an overall match percentage and separate scores for skills match, experience match, and education match. Also identify missing skills and experiences that would improve the match. Format your response as JSON with the following keys: 'overall_score', 'skills_match', 'experience_match', 'education_match', 'missing_skills', 'missing_experiences', and 'recommendations'.\n\nCV Analysis: {json.dumps(cv_analysis, indent=2)}\n\nJob Description: {job_description}"}
        ]
        
        response = self.llm_client.chat_completion(prompt, temperature=0.3)
        content = self.llm_client.extract_content(response)
        
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
            # If JSON parsing fails, return a structured error
            return {
                "error": "Failed to parse job match analysis",
                "raw_content": content
            }
    
    def extract_job_description(self, job_url: str) -> str:
        """
        Extract job description from a job listing URL.
        This is a placeholder - in a real implementation, you would use web scraping.
        
        Args:
            job_url: URL of the job listing
            
        Returns:
            Job description text
        """
        # In a real implementation, you would use web scraping to extract the job description
        # For now, we'll return a placeholder message
        return "This is a placeholder job description. In a real implementation, this would be extracted from the job listing URL."