import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter API configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL_1 = os.getenv("OPENROUTER_MODEL_1", "google/gemini-2.0-flash-001")
OPENROUTER_MODEL_2 = os.getenv("OPENROUTER_MODEL_2", "google/gemini-2.0-flash-001")

# Application configuration
CV_UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(CV_UPLOAD_FOLDER, exist_ok=True)

# LinkedIn search configuration
LINKEDIN_JOBS_URL = "https://www.linkedin.com/jobs/search/"
BROWSER_HEADLESS = os.getenv("BROWSER_USE_HEADLESS", "false").lower() == "true"

# Use mock implementation for job search (for testing or when LinkedIn scraping fails)
USE_MOCK_JOB_SEARCH = os.getenv("USE_MOCK_JOB_SEARCH", "false").lower() == "true"

# Ensure API key is available
if not OPENROUTER_API_KEY:
    raise ValueError("OpenRouter API key not found. Please set OPENROUTER_API_KEY in your .env file.")