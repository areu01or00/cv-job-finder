import pandas as pd
from typing import List, Dict, Any

class MockLinkedInJobSearch:
    """Mock implementation of LinkedIn job search for testing purposes."""
    
    def __init__(self):
        """Initialize the mock job search."""
        # Sample job data
        self.sample_jobs = [
            {
                "title": "Software Engineer",
                "company": "Google",
                "location": "Mountain View, CA",
                "url": "https://www.linkedin.com/jobs/view/software-engineer-at-google",
                "query": "software engineer"
            },
            {
                "title": "Data Scientist",
                "company": "Microsoft",
                "location": "Redmond, WA",
                "url": "https://www.linkedin.com/jobs/view/data-scientist-at-microsoft",
                "query": "data scientist"
            },
            {
                "title": "Product Manager",
                "company": "Amazon",
                "location": "Seattle, WA",
                "url": "https://www.linkedin.com/jobs/view/product-manager-at-amazon",
                "query": "product manager"
            },
            {
                "title": "Frontend Developer",
                "company": "Facebook",
                "location": "Menlo Park, CA",
                "url": "https://www.linkedin.com/jobs/view/frontend-developer-at-facebook",
                "query": "frontend developer"
            },
            {
                "title": "Machine Learning Engineer",
                "company": "Apple",
                "location": "Cupertino, CA",
                "url": "https://www.linkedin.com/jobs/view/machine-learning-engineer-at-apple",
                "query": "machine learning engineer"
            },
            {
                "title": "DevOps Engineer",
                "company": "Netflix",
                "location": "Los Gatos, CA",
                "url": "https://www.linkedin.com/jobs/view/devops-engineer-at-netflix",
                "query": "devops engineer"
            },
            {
                "title": "UX Designer",
                "company": "Adobe",
                "location": "San Jose, CA",
                "url": "https://www.linkedin.com/jobs/view/ux-designer-at-adobe",
                "query": "ux designer"
            },
            {
                "title": "Data Engineer",
                "company": "IBM",
                "location": "New York, NY",
                "url": "https://www.linkedin.com/jobs/view/data-engineer-at-ibm",
                "query": "data engineer"
            },
            {
                "title": "Full Stack Developer",
                "company": "Twitter",
                "location": "San Francisco, CA",
                "url": "https://www.linkedin.com/jobs/view/full-stack-developer-at-twitter",
                "query": "full stack developer"
            },
            {
                "title": "AI Research Scientist",
                "company": "NVIDIA",
                "location": "Santa Clara, CA",
                "url": "https://www.linkedin.com/jobs/view/ai-research-scientist-at-nvidia",
                "query": "ai research scientist"
            }
        ]
    
    def search_jobs(self, query: str, location: str = "", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Mock search for jobs based on a query and location.
        
        Args:
            query: Job search query
            location: Location for job search
            limit: Maximum number of job listings to return
            
        Returns:
            List of job listings
        """
        # Filter jobs based on query (case-insensitive partial match)
        query_lower = query.lower()
        filtered_jobs = [
            job for job in self.sample_jobs 
            if query_lower in job["title"].lower() or query_lower in job["query"].lower()
        ]
        
        # Filter by location if provided
        if location:
            location_lower = location.lower()
            filtered_jobs = [
                job for job in filtered_jobs
                if location_lower in job["location"].lower()
            ]
        
        # Return limited results
        return filtered_jobs[:limit]
    
    def search_multiple_queries(self, queries: List[str], location: str = "", limit_per_query: int = 5) -> pd.DataFrame:
        """
        Search for jobs using multiple queries and return results as a DataFrame.
        
        Args:
            queries: List of job search queries
            location: Location for job search
            limit_per_query: Maximum number of job listings per query
            
        Returns:
            DataFrame with job listings
        """
        all_results = []
        
        for query in queries:
            results = self.search_jobs(query, location, limit_per_query)
            all_results.extend(results)
            
        # Convert to DataFrame
        if all_results:
            df = pd.DataFrame(all_results)
            # Remove duplicates based on URL
            df = df.drop_duplicates(subset=["url"])
            return df
        else:
            return pd.DataFrame(columns=["title", "company", "location", "url", "query"])