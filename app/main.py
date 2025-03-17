import streamlit as st
import os
import sys

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import all components
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
    
    # Initialize session state variables if they don't exist
    if "cv_analysis" not in st.session_state:
        st.session_state.cv_analysis = None
    if "job_search_results" not in st.session_state:
        st.session_state.job_search_results = None
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1565C0;
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
    
    # Application header
    st.markdown("<h1 class='main-header'>CV-Based Job Finder</h1>", unsafe_allow_html=True)
    st.markdown(
        "Analyze your CV, find matching job opportunities, optimize your CV, and score job compatibility."
    )
    
    # Sidebar
    with st.sidebar:
        st.markdown("<h2 class='sub-header'>About</h2>", unsafe_allow_html=True)
        st.write(
            "This application helps you:"
        )
        st.write("- Analyze your CV to extract key information")
        st.write("- Search for job opportunities based on your skills")
        st.write("- Optimize your CV for specific job roles")
        st.write("- Score your CV's compatibility with job descriptions")
        
        st.markdown("<h2 class='sub-header'>How it works</h2>", unsafe_allow_html=True)
        st.write("1. Upload your CV in the **CV Analysis** tab")
        st.write("2. Search for jobs in the **Job Search** tab")
        st.write("3. Get CV optimization recommendations in the **CV Optimization** tab")
        st.write("4. Calculate job compatibility scores in the **Job Compatibility** tab")
        
        st.markdown("<h2 class='sub-header'>Settings</h2>", unsafe_allow_html=True)
        # Add any settings here if needed
    
    # Initialize components
    cv_analyzer = CVAnalyzerComponent()
    job_search = JobSearchComponent()
    cv_optimizer = CVOptimizerComponent()
    job_compatibility = JobCompatibilityComponent()
    
    # Create tabs with icons
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 CV Analysis", 
        "🔍 Job Search", 
        "✨ CV Optimization", 
        "🎯 Job Compatibility"
    ])
    
    # CV Analysis tab
    with tab1:
        analysis_complete, cv_analysis, cv_path = cv_analyzer.render()
        
        # Store analysis results in session state
        if analysis_complete and cv_analysis:
            st.session_state.cv_analysis = cv_analysis
            st.session_state.cv_path = cv_path
            st.success("CV analysis complete! You can now proceed to other tabs.")
            
            # Add a button to navigate to job search tab
            if st.button("Proceed to Job Search"):
                # This will be handled by JavaScript to switch tabs
                st.markdown(
                    """
                    <script>
                        var tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');
                        tabs[1].click();
                    </script>
                    """,
                    unsafe_allow_html=True
                )
    
    # Job Search tab
    with tab2:
        # Get analysis results from session state
        cv_analysis = st.session_state.get("cv_analysis", None)
        
        # Render job search component
        job_search_results = job_search.render(cv_analysis)
        
        # Store job search results in session state
        if job_search_results is not None:
            st.session_state.job_search_results = job_search_results
            st.success("Job search complete! You can now optimize your CV or calculate job compatibility.")
            
            # Add buttons to navigate to other tabs
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Optimize Your CV"):
                    # Switch to CV Optimization tab
                    st.markdown(
                        """
                        <script>
                            var tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');
                            tabs[2].click();
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
            with col2:
                if st.button("Calculate Job Compatibility"):
                    # Switch to Job Compatibility tab
                    st.markdown(
                        """
                        <script>
                            var tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');
                            tabs[3].click();
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
    
    # CV Optimization tab
    with tab3:
        # Get analysis results from session state
        cv_analysis = st.session_state.get("cv_analysis", None)
        
        # Render CV optimizer component
        cv_optimizer.render(cv_analysis)
    
    # Job Compatibility tab
    with tab4:
        # Get analysis results and job results from session state
        cv_analysis = st.session_state.get("cv_analysis", None)
        job_search_results = st.session_state.get("job_search_results", None)
        
        # Render job compatibility component
        job_compatibility.render(cv_analysis, job_search_results)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #888;">
        CV-Based Job Finder | Created with ❤️ | 2023
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()