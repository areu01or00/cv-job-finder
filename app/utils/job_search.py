import time
import urllib.parse
import pandas as pd
from typing import List, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from .config import LINKEDIN_JOBS_URL, BROWSER_HEADLESS

class LinkedInJobSearch:
    """Class for searching and scraping job listings from LinkedIn."""
    
    def __init__(self, headless: bool = BROWSER_HEADLESS):
        self.headless = headless
        self.driver = None
        self.ua = UserAgent()
        
    def _setup_driver(self):
        """Set up the Selenium WebDriver with improved options."""
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")  # Use the new headless mode
        
        # Add additional options to improve stability
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f"--user-agent={self.ua.random}")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Disable images to speed up loading
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.images": 2,
            "profile.managed_default_content_settings.images": 2
        })
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            self.driver = None
            
    def _close_driver(self):
        """Close the Selenium WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error closing driver: {e}")
            finally:
                self.driver = None
                
    def _search_jobs_with_requests(self, query: str, location: str = "", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for jobs using requests library (more reliable than Selenium).
        
        Args:
            query: Job search query
            location: Location for job search
            limit: Maximum number of job listings to return
            
        Returns:
            List of job listings
        """
        # Encode query parameters
        params = {
            "keywords": query,
            "sortBy": "R",  # Sort by relevance
            "f_WT": "2",  # Remote jobs
        }
        
        if location:
            params["location"] = location
            
        url = f"{LINKEDIN_JOBS_URL}?{urllib.parse.urlencode(params)}"
        
        headers = {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.linkedin.com/",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "lxml")
            job_cards = soup.select(".job-search-card")
            
            results = []
            for card in job_cards[:limit]:
                try:
                    # Extract job details
                    title_elem = card.select_one(".base-search-card__title")
                    company_elem = card.select_one(".base-search-card__subtitle")
                    location_elem = card.select_one(".job-search-card__location")
                    link_elem = card.select_one(".base-card__full-link")
                    
                    if title_elem and company_elem and location_elem and link_elem:
                        job_info = {
                            "title": title_elem.get_text(strip=True),
                            "company": company_elem.get_text(strip=True),
                            "location": location_elem.get_text(strip=True),
                            "url": link_elem["href"],
                            "query": query
                        }
                        results.append(job_info)
                except Exception as e:
                    print(f"Error extracting job details: {e}")
                    continue
                    
            return results
        except Exception as e:
            print(f"Error searching jobs with requests: {e}")
            return []
    
    def search_jobs(self, query: str, location: str = "", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for jobs on LinkedIn.
        
        Args:
            query: Job search query
            location: Location for job search
            limit: Maximum number of job listings to return
            
        Returns:
            List of job listings
        """
        # First try with requests (more reliable)
        results = self._search_jobs_with_requests(query, location, limit)
        if results:
            return results
            
        # Fall back to Selenium if requests approach didn't work
        if not self.driver:
            self._setup_driver()
            
        if not self.driver:
            raise Exception("Failed to set up Chrome driver")
            
        try:
            # Encode query parameters
            params = {
                "keywords": query,
                "sortBy": "R",  # Sort by relevance
                "f_WT": "2",  # Remote jobs
            }
            
            if location:
                params["location"] = location
                
            url = f"{LINKEDIN_JOBS_URL}?{urllib.parse.urlencode(params)}"
            
            # Navigate to the search URL
            self.driver.get(url)
            
            # Wait for job listings to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".job-search-card"))
            )
            
            # Extract job listings
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job-search-card")
            
            results = []
            for card in job_cards[:limit]:
                try:
                    # Extract job details
                    title = card.find_element(By.CSS_SELECTOR, ".base-search-card__title").text.strip()
                    company = card.find_element(By.CSS_SELECTOR, ".base-search-card__subtitle").text.strip()
                    job_location = card.find_element(By.CSS_SELECTOR, ".job-search-card__location").text.strip()
                    url = card.find_element(By.CSS_SELECTOR, ".base-card__full-link").get_attribute("href")
                    
                    job_info = {
                        "title": title,
                        "company": company,
                        "location": job_location,
                        "url": url,
                        "query": query
                    }
                    
                    results.append(job_info)
                except Exception as e:
                    print(f"Error extracting job details: {e}")
                    continue
                    
            return results
        except Exception as e:
            raise Exception(f"Error searching for jobs: {e}")
        finally:
            self._close_driver()
            
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
            try:
                results = self.search_jobs(query, location, limit_per_query)
                all_results.extend(results)
                # Add a small delay to avoid rate limiting
                time.sleep(1)
            except Exception as e:
                print(f"Error searching for '{query}': {e}")
                continue
                
        # Convert to DataFrame
        if all_results:
            df = pd.DataFrame(all_results)
            # Remove duplicates based on URL
            df = df.drop_duplicates(subset=["url"])
            return df
        else:
            return pd.DataFrame(columns=["title", "company", "location", "url", "query"])