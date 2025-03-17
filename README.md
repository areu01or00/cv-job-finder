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

### Run with Mock Data (for testing)

```bash
python run_with_mock.py
```

## License

MIT