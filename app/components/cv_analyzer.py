import streamlit as st
import json
import os
import sys
from typing import Dict, Any, Tuple, Optional

# Add the project root directory to Python path if not already there
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.utils import CVParser, OpenRouterClient

class CVAnalyzerComponent:
    """Streamlit component for CV upload and analysis."""
    
    def __init__(self):
        self.cv_parser = CVParser()
        self.llm_client = OpenRouterClient()
        
    def render(self) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Render the CV analyzer component.
        
        Returns:
            Tuple containing:
            - Boolean indicating if CV analysis is complete
            - CV analysis results (if complete)
            - Path to the uploaded CV file (if complete)
        """
        st.header("CV Analysis")
        st.write("Upload your CV to find relevant job opportunities.")
        
        uploaded_file = st.file_uploader("Upload your CV (PDF format)", type=["pdf"])
        
        if not uploaded_file:
            st.info("Please upload your CV to get started.")
            return False, None, None
        
        # Save the uploaded file
        with st.spinner("Saving your CV..."):
            cv_path = self.cv_parser.save_uploaded_cv(uploaded_file)
            
        # Check if analysis has already been done
        if "cv_analysis" in st.session_state and "cv_path" in st.session_state and st.session_state["cv_path"] == cv_path:
            cv_analysis = st.session_state["cv_analysis"]
            self._display_cv_analysis(cv_analysis)
            return True, cv_analysis, cv_path
        
        # Analyze the CV
        analyze_button = st.button("Analyze CV")
        
        if analyze_button:
            with st.spinner("Analyzing your CV... This may take a moment."):
                try:
                    cv_analysis = self.cv_parser.parse_cv(cv_path)
                    
                    # Store the analysis in session state
                    st.session_state["cv_analysis"] = cv_analysis
                    st.session_state["cv_path"] = cv_path
                    
                    self._display_cv_analysis(cv_analysis)
                    return True, cv_analysis, cv_path
                except Exception as e:
                    st.error(f"Error analyzing CV: {e}")
                    return False, None, None
        
        return False, None, None
    
    def _display_cv_analysis(self, cv_analysis: Dict[str, Any]):
        """
        Display the CV analysis results.
        
        Args:
            cv_analysis: Dictionary with CV analysis results
        """
        st.subheader("CV Analysis Results")
        
        # Check if there was an error in the analysis
        if "error" in cv_analysis:
            st.error(f"Error in CV analysis: {cv_analysis['error']}")
            if "raw_content" in cv_analysis:
                st.text_area("Raw Response", cv_analysis["raw_content"], height=300)
            return
        
        # Display skills
        if "skills" in cv_analysis:
            st.write("**Skills:**")
            if isinstance(cv_analysis["skills"], list):
                for skill in cv_analysis["skills"]:
                    st.write(f"- {skill}")
            else:
                st.write(cv_analysis["skills"])
        
        # Display experience
        if "experience" in cv_analysis:
            st.write("**Experience:**")
            if isinstance(cv_analysis["experience"], list):
                for exp in cv_analysis["experience"]:
                    st.write(f"- {exp}")
            else:
                st.write(cv_analysis["experience"])
        
        # Display education
        if "education" in cv_analysis:
            st.write("**Education:**")
            if isinstance(cv_analysis["education"], list):
                for edu in cv_analysis["education"]:
                    st.write(f"- {edu}")
            else:
                st.write(cv_analysis["education"])
        
        # Display job titles
        if "job_titles" in cv_analysis:
            st.write("**Job Titles:**")
            if isinstance(cv_analysis["job_titles"], list):
                for title in cv_analysis["job_titles"]:
                    st.write(f"- {title}")
            else:
                st.write(cv_analysis["job_titles"])
        
        # Display relevant job keywords
        if "relevant_job_keywords" in cv_analysis:
            st.write("**Relevant Job Keywords:**")
            if isinstance(cv_analysis["relevant_job_keywords"], list):
                for keyword in cv_analysis["relevant_job_keywords"]:
                    st.write(f"- {keyword}")
            else:
                st.write(cv_analysis["relevant_job_keywords"])
        
        # Display raw JSON for debugging
        with st.expander("View Raw Analysis Data"):
            st.json(cv_analysis)