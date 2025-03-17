import streamlit as st
import os
import sys

# Add the project root directory to Python path if not already there
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.components import (
    CVAnalyzerComponent,
    JobSearchComponent,
    CVOptimizerComponent,
    JobCompatibilityComponent
)

def main():
    # Set page configuration
    st.set_page_config(
        page_title="CV-Based Job Finder",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state if needed
    if "cv_analysis_results" not in st.session_state:
        st.session_state.cv_analysis_results = None
    if "job_search_results" not in st.session_state:
        st.session_state.job_search_results = None
    
    # Custom CSS
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6f0ff;
    }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("📄 CV-Based Job Finder")
    st.markdown("""
    Analyze your CV, find matching job opportunities, optimize your CV, and score job compatibility.
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This application helps you:
        - Analyze your CV to extract key information
        - Search for job opportunities based on your skills
        - Optimize your CV for specific job roles
        - Score your CV's compatibility with job descriptions
        """)
        
        st.header("How it works")
        st.markdown("""
        1. Upload your CV in the **CV Analysis** tab
        2. Search for jobs in the **Job Search** tab
        3. Get CV optimization recommendations in the **CV Optimization** tab
        4. Calculate job compatibility scores in the **Job Compatibility** tab
        """)
        
        st.header("Settings")
        # Add any settings here if needed
    
    # Initialize components
    cv_analyzer = CVAnalyzerComponent()
    job_search = JobSearchComponent()
    cv_optimizer = CVOptimizerComponent()
    job_compatibility = JobCompatibilityComponent()
    
    # Create tabs
    tabs = st.tabs([
        "📄 CV Analysis", 
        "🔍 Job Search", 
        "✨ CV Optimization", 
        "🎯 Job Compatibility"
    ])
    
    # CV Analysis tab
    with tabs[0]:
        cv_analysis_results = cv_analyzer.render()
        if cv_analysis_results:
            # Store CV analysis results in session state
            st.session_state.cv_analysis_results = cv_analysis_results
            st.success("CV analysis complete! You can now proceed to other tabs.")
    
    # Job Search tab
    with tabs[1]:
        cv_analysis = st.session_state.get('cv_analysis_results', None)
        job_search_results = job_search.render(cv_analysis)
        if job_search_results is not None:
            # Store job search results in session state
            st.session_state.job_search_results = job_search_results
            st.success("Job search complete! You can now optimize your CV or calculate job compatibility.")
    
    # CV Optimization tab
    with tabs[2]:
        cv_analysis = st.session_state.get('cv_analysis_results', None)
        cv_optimizer.render(cv_analysis)
    
    # Job Compatibility tab
    with tabs[3]:
        cv_analysis = st.session_state.get('cv_analysis_results', None)
        job_search_results = st.session_state.get('job_search_results', None)
        job_compatibility.render(cv_analysis, job_search_results)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888;">
    CV-Based Job Finder | Created with ❤️ | 2023
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()