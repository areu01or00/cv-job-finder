#!/usr/bin/env python3
"""
Run the CV-Based Job Finder application with the mock job search implementation.
This is useful for testing or when LinkedIn scraping is not working.
"""
import os
import subprocess
import sys

def main():
    """Run the CV-Based Job Finder application with mock job search."""
    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Add the project root to Python path
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    # Set PYTHONPATH environment variable to include the project root
    os.environ["PYTHONPATH"] = script_dir + os.pathsep + os.environ.get("PYTHONPATH", "")
    
    # Set USE_MOCK_JOB_SEARCH to true
    os.environ["USE_MOCK_JOB_SEARCH"] = "true"
    
    # Check if virtual environment is activated
    if not os.environ.get("VIRTUAL_ENV"):
        print("Warning: Virtual environment not detected. It's recommended to run this application in a virtual environment.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting. Please activate your virtual environment and try again.")
            sys.exit(1)
    
    # Run the Streamlit application
    try:
        print("Starting CV-Based Job Finder application with mock job search...")
        # Use a more direct approach with the streamlit command
        cmd = ["streamlit", "run", "--server.runOnSave=false", "app/main.py"]
        env = os.environ.copy()
        subprocess.run(cmd, env=env, check=True)
    except KeyboardInterrupt:
        print("\nApplication stopped.")
    except Exception as e:
        print(f"Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()