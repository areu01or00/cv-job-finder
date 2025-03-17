# CV-Based Job Finder

A Streamlit application that analyzes resumes and searches for matching job opportunities.

## Features

- CV Analysis: Upload and analyze your CV to extract key information
- Job Search: Find relevant job opportunities based on your CV
- Mock Implementation: Test the application without relying on web scraping

## Project Structure

```
├── app/
│   ├── components/
│   │   ├── cv_analyzer.py    # CV analysis component
│   │   ├── job_search.py     # Job search component
│   │   └── __init__.py
│   ├── utils/
│   │   ├── cv_parser.py      # PDF parsing utilities
│   │   ├── job_search.py     # LinkedIn job search implementation
│   │   ├── llm.py            # LLM client for CV analysis
│   │   ├── mock_job_search.py # Mock job search for testing
│   │   ├── config.py         # Application configuration
│   │   └── __init__.py
│   ├── data/                 # Directory for uploaded CVs
│   ├── main.py               # Main Streamlit application
│   └── __init__.py
├── run.py                    # Script to run the application
├── run_with_mock.py          # Script to run with mock job search
├── requirements.txt          # Project dependencies
└── .env.example              # Example environment variables
```

## Understanding the Project Structure

### Components vs Utils: Similar Named Files

The project follows a separation of concerns pattern:

#### Components Folder
Contains UI components that handle the presentation layer (what the user sees and interacts with):

- **`cv_analyzer.py`** - Streamlit UI component that renders the CV upload interface, displays analysis results, and handles user interactions
- **`job_search.py`** - Streamlit UI component that renders the job search interface, displays results, and handles filtering

#### Utils Folder
Contains the business logic and data processing classes that work behind the scenes:

- **`cv_parser.py`** - Utility that extracts text from PDF files and saves uploaded CVs
- **`job_search.py`** - Utility that implements LinkedIn web scraping logic and handles job search requests
- **`mock_job_search.py`** - Mock implementation that provides sample job data for testing
- **`llm.py`** - Client for the OpenRouter API that handles CV analysis using AI
- **`config.py`** - Configuration settings for the application

### Key Files Explained

- **`run.py`** - Main entry point script that runs the Streamlit application with real LinkedIn scraping
- **`run_with_mock.py`** - Alternative entry point that runs the application with mock job data instead of real LinkedIn scraping
- **`main.py`** - The main Streamlit application that sets up the page layout and initializes components
- **`requirements.txt`** - Lists all Python package dependencies with versions
- **`.env.example`** - Template for environment variables that should be copied to `.env` and filled with actual values

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your OpenRouter API key

## Usage

### Standard Run (with LinkedIn scraping)

```bash
python run.py
```

This runs the application with real LinkedIn job scraping, which will attempt to fetch actual job listings from LinkedIn based on your CV analysis.

### Run with Mock Data (for testing)

```bash
python run_with_mock.py
```

This runs the application with mock job data, which is useful for:
- Testing the application without relying on web scraping
- Demonstrating the application when LinkedIn scraping might be blocked
- Developing and testing new features without waiting for web scraping
- Providing a consistent experience with predefined job listings

## Environment Variables

The application uses the following environment variables (defined in `.env`):

- `OPENROUTER_API_KEY` - API key for OpenRouter (required for CV analysis)
- `OPENROUTER_MODEL_1` - Model to use for CV analysis (default: google/gemini-2.0-flash-001)
- `BROWSER_USE_HEADLESS` - Whether to use headless browser for scraping (default: false)
- `USE_MOCK_JOB_SEARCH` - Whether to use mock job search implementation (default: false)

## License

MIT