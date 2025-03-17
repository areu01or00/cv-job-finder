# CV-Based Job Finder

A Streamlit application that analyzes resumes and searches for job opportunities based on the extracted information. The application provides CV analysis, job search capabilities, CV optimization recommendations, and job compatibility scoring.

## Features

- **CV Analysis**: Upload and analyze your CV to extract key information such as skills, experience, education, and more.
- **Job Search**: Search for job opportunities based on your CV analysis results or custom search queries.
- **CV Optimization**: Get personalized recommendations to optimize your CV for specific job roles.
- **Job Compatibility Scoring**: Calculate how well your CV matches specific job descriptions and get recommendations for improvement.
- **Mock Implementation**: Includes a mock implementation for testing or when LinkedIn scraping is not functioning.

## Project Structure

```
cv-job-finder/
├── app/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── cv_analyzer.py      # CV analysis component
│   │   ├── job_search.py       # Job search component
│   │   ├── cv_optimizer.py     # CV optimization component
│   │   └── job_compatibility.py # Job compatibility scoring component
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration settings
│   │   ├── pdf_parser.py       # PDF parsing utilities
│   │   ├── linkedin_job_search.py # LinkedIn job search implementation
│   │   ├── mock_linkedin_job_search.py # Mock job search implementation
│   │   ├── openrouter_client.py # OpenRouter API client
│   │   └── advanced_features.py # Advanced AI-powered features
│   ├── data/
│   │   └── mock_jobs.json      # Mock job data for testing
│   └── main.py                 # Main application entry point
├── .env.example                # Example environment variables
├── requirements.txt            # Python dependencies
├── run.py                      # Script to run the application
├── run_with_mock.py            # Script to run with mock implementation
└── README.md                   # Project documentation
```

## Magical Features

### CV Optimization

The CV optimization feature provides tailored recommendations to enhance your CV for specific job roles:

- **Skills to Add**: Identifies relevant skills missing from your CV that are valuable for the target job.
- **Skills to Emphasize**: Highlights existing skills in your CV that should be emphasized for the target job.
- **Experiences to Emphasize**: Suggests which experiences to highlight or elaborate on to better match the job requirements.
- **Items to Remove or De-emphasize**: Identifies content in your CV that may be less relevant for the target job.
- **General Recommendations**: Provides overall suggestions to improve your CV's effectiveness.

### Job Compatibility Scoring

The job compatibility scoring feature calculates how well your CV matches specific job descriptions:

- **Overall Match Score**: A percentage indicating the overall compatibility between your CV and the job.
- **Skills Match**: A breakdown of how well your skills align with the job requirements, including missing skills.
- **Experience Match**: An assessment of how your experience aligns with the job requirements, including missing experiences.
- **Education Match**: An evaluation of how your education aligns with the job requirements.
- **Recommendations**: Specific suggestions to improve your CV's compatibility with the job.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/areu01or00/cv-job-finder.git
   cd cv-job-finder
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and add your API keys.

## Usage

1. Run the application:
   ```
   python run.py
   ```

2. Or run with mock implementation (for testing):
   ```
   python run_with_mock.py
   ```

3. Open your browser and navigate to `http://localhost:8501`

## Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `OPENROUTER_MODEL_1`: Primary model to use (default: google/gemini-2.0-flash-001)
- `OPENROUTER_MODEL_2`: Secondary model to use (default: google/gemini-2.0-flash-001)
- `BROWSER_USE_HEADLESS`: Whether to use headless browser for scraping (default: false)
- `USE_MOCK_JOB_SEARCH`: Whether to use mock implementation for job search (default: false)