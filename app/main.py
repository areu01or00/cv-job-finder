import streamlit as st
import os
import sys

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import the components
from app.components import CVAnalyzerComponent, JobSearchComponent

# Set page configuration
st.set_page_config(
    page_title="CV-Based Job Finder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function."""
    # Add custom CSS
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
    </style>
    """, unsafe_allow_html=True)
    
    # Application header
    st.markdown("<h1 class='main-header'>CV-Based Job Finder</h1>", unsafe_allow_html=True)
    st.markdown(
        "An agentic system that analyzes your CV, finds relevant job opportunities on LinkedIn, "
        "and presents them in a user-friendly interface."
    )
    
    # Sidebar
    with st.sidebar:
        st.markdown("<h2 class='sub-header'>About</h2>", unsafe_allow_html=True)
        st.write(
            "This application uses AI to analyze your CV and find relevant job opportunities "
            "on LinkedIn based on your skills, experience, and qualifications."
        )
        
        st.markdown("<h2 class='sub-header'>How it works</h2>", unsafe_allow_html=True)
        st.write("1. Upload your CV (PDF format)")
        st.write("2. The system analyzes your CV to extract key information")
        st.write("3. Based on your profile, it generates job search queries")
        st.write("4. It searches for relevant job listings on LinkedIn")
        st.write("5. Results are presented in a filterable, user-friendly interface")
        
        st.markdown("<h2 class='sub-header'>Settings</h2>", unsafe_allow_html=True)
        # Add any settings here if needed
        
    # Main content
    # Initialize components
    cv_analyzer = CVAnalyzerComponent()
    job_search = JobSearchComponent()
    
    # Create tabs
    tab1, tab2 = st.tabs(["CV Analysis", "Job Search"])
    
    with tab1:
        # Render CV analyzer component
        analysis_complete, cv_analysis, cv_path = cv_analyzer.render()
        
        # Store analysis results in session state
        if analysis_complete and cv_analysis:
            st.session_state["cv_analysis_complete"] = True
            st.session_state["cv_analysis"] = cv_analysis
            st.session_state["cv_path"] = cv_path
            
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
    
    with tab2:
        # Get analysis results from session state
        cv_analysis = st.session_state.get("cv_analysis", None)
        
        # Render job search component
        job_search.render(cv_analysis)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Powered by OpenRouter AI | "
        "Built with Streamlit | "
        "© 2024 CV-Based Job Finder"
    )

if __name__ == "__main__":
    main()