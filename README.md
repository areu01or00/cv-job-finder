# CV-Based Job Finder

A Streamlit application that analyzes resumes and searches for matching job opportunities.

## Features

- **CV Analysis**: Upload and analyze your CV to extract key information
- **Job Search**: Find relevant job opportunities based on your CV
- **CV Optimization**: Get personalized recommendations to optimize your CV for specific job roles
- **Job Compatibility Scoring**: Calculate how well your CV matches specific job descriptions
- **Mock Implementation**: Test the application without relying on web scraping

## Project Structure

```
├── app/
│   ├── components/
│   │   ├── cv_analyzer.py    # CV analysis component
│   │   ├── job_search.py     # Job search component
│   │   ├── cv_optimizer.py   # CV optimization component
│   │   ├── job_compatibility.py # Job compatibility scoring component
│   │   └── __init__.py
│   ├── utils/
│   │   ├── cv_parser.py      # PDF parsing utilities
│   │   ├── job_search.py     # LinkedIn job search implementation
│   │   ├── llm.py            # LLM client for CV analysis
│   │   ├── mock_job_search.py # Mock job search for testing
│   │   ├── advanced_features.py # Advanced AI-powered features
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
- **`cv_optimizer.py`** - Streamlit UI component that provides CV optimization recommendations for specific job roles
- **`job_compatibility.py`** - Streamlit UI component that calculates and displays job compatibility scores

#### Utils Folder
Contains the business logic and data processing classes that work behind the scenes:

- **`cv_parser.py`** - Utility that extracts text from PDF files and saves uploaded CVs
- **`job_search.py`** - Utility that implements LinkedIn web scraping logic and handles job search requests
- **`mock_job_search.py`** - Mock implementation that provides sample job data for testing
- **`llm.py`** - Client for the OpenRouter API that handles CV analysis using AI
- **`advanced_features.py`** - Implements advanced AI-powered features like CV optimization and job compatibility scoring
- **`config.py`** - Configuration settings for the application

### Key Files Explained

- **`run.py`** - Main entry point script that runs the Streamlit application with real LinkedIn scraping
- **`run_with_mock.py`** - Alternative entry point that runs the application with mock job data instead of real LinkedIn scraping
- **`main.py`** - The main Streamlit application that sets up the page layout and initializes components
- **`requirements.txt`** - Lists all Python package dependencies with versions
- **`.env.example`** - Template for environment variables that should be copied to `.env` and filled with actual values

## Magical Features

### CV Optimization
The CV optimization feature provides personalized recommendations to improve your CV for specific job roles:

- **Skills to Add**: Identifies skills you should add to your CV based on the target job
- **Skills to Emphasize**: Highlights which of your existing skills should be emphasized
- **Experiences to Emphasize**: Suggests which experiences are most relevant to the target job
- **Items to Remove**: Identifies irrelevant information that could be removed
- **General Recommendations**: Provides overall suggestions to improve your CV

### Job Compatibility Scoring
The job compatibility scoring feature calculates how well your CV matches specific job descriptions:

- **Overall Match Score**: Provides a percentage match between your CV and the job
- **Skills Match**: Scores how well your skills match the job requirements
- **Experience Match**: Scores how well your experience matches the job requirements
- **Education Match**: Scores how well your education matches the job requirements
- **Missing Skills**: Identifies skills required for the job that are missing from your CV
- **Missing Experiences**: Identifies experiences required for the job that are missing from your CV
- **Recommendations**: Provides suggestions to improve your compatibility with the job

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