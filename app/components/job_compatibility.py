import streamlit as st
import os
import sys
import pandas as pd
from typing import Dict, Any, Optional, List, Union

# Add the project root directory to Python path if not already there
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.utils import AdvancedFeatures

class JobCompatibilityComponent:
    """Streamlit component for job compatibility scoring."""
    
    def __init__(self):
        self.advanced_features = AdvancedFeatures()
        
    def render(self, cv_analysis: Optional[Dict[str, Any]] = None, job_search_results: Optional[List[Dict[str, Any]]] = None):
        """
        Render the job compatibility component.
        
        Args:
            cv_analysis: Dictionary with CV analysis results
            job_search_results: List of job search results
        """
        st.header("Job Compatibility Scoring")
        
        if cv_analysis is None:
            st.info("Please analyze your CV first to calculate job compatibility scores.")
            return
        
        st.write("Calculate how well your CV matches specific job descriptions and get recommendations for improvement.")
        
        # Create tabs for different input methods
        tab1, tab2 = st.tabs(["From Job Search", "Manual Entry"])
        
        with tab1:
            self._render_from_job_search(cv_analysis, job_search_results)
            
        with tab2:
            self._render_manual_entry(cv_analysis)
    
    def _render_from_job_search(self, cv_analysis: Dict[str, Any], job_search_results: Optional[List[Dict[str, Any]]]):
        """Render the job compatibility from job search results."""
        if not job_search_results:
            st.info("Please search for jobs first to calculate compatibility scores.")
            return
        
        # Convert job search results to DataFrame for display if it's not already
        if isinstance(job_search_results, pd.DataFrame):
            df = job_search_results
        else:
            df = pd.DataFrame(job_search_results)
        
        # Select columns to display
        display_columns = ['title', 'company', 'location']
        if all(col in df.columns for col in display_columns):
            display_df = df[display_columns].copy()
            
            # Add a select column
            selected_job_index = st.selectbox(
                "Select a job to calculate compatibility score:",
                range(len(display_df)),
                format_func=lambda i: f"{display_df.iloc[i]['title']} at {display_df.iloc[i]['company']}"
            )
            
            selected_job = df.iloc[selected_job_index].to_dict() if isinstance(df, pd.DataFrame) else job_search_results[selected_job_index]
            
            if st.button("Calculate Compatibility Score"):
                with st.spinner("Calculating job compatibility score..."):
                    try:
                        # Extract job description
                        job_description = selected_job.get('description', '')
                        if not job_description:
                            job_description = f"Job Title: {selected_job.get('title', '')}\nCompany: {selected_job.get('company', '')}\nLocation: {selected_job.get('location', '')}"
                        
                        # Calculate compatibility score
                        compatibility_results = self.advanced_features.calculate_job_match_score(
                            cv_analysis, 
                            job_description
                        )
                        
                        # Display results
                        self._display_compatibility_results(
                            compatibility_results, 
                            selected_job.get('title', 'Selected Job'),
                            selected_job.get('company', '')
                        )
                    except Exception as e:
                        st.error(f"Error calculating compatibility score: {e}")
        else:
            st.error("Job search results do not contain the expected columns.")
    
    def _render_manual_entry(self, cv_analysis: Dict[str, Any]):
        """Render the job compatibility with manual job description entry."""
        st.subheader("Enter Job Details Manually")
        
        job_title = st.text_input("Job Title", placeholder="e.g., Senior Software Engineer")
        company = st.text_input("Company Name (Optional)", placeholder="e.g., Google")
        job_description = st.text_area(
            "Job Description", 
            placeholder="Paste the full job description here...",
            height=300
        )
        
        if job_title and job_description and st.button("Calculate Compatibility Score"):
            with st.spinner("Calculating job compatibility score..."):
                try:
                    # Calculate compatibility score
                    compatibility_results = self.advanced_features.calculate_job_match_score(
                        cv_analysis, 
                        f"Job Title: {job_title}\nCompany: {company}\n\n{job_description}"
                    )
                    
                    # Display results
                    self._display_compatibility_results(compatibility_results, job_title, company)
                except Exception as e:
                    st.error(f"Error calculating compatibility score: {e}")
    
    def _display_compatibility_results(self, compatibility_results: Dict[str, Any], job_title: str, company: str = ""):
        """
        Display job compatibility results.
        
        Args:
            compatibility_results: Dictionary with compatibility scores and recommendations
            job_title: The job title
            company: The company name
        """
        job_display = f"{job_title}" if not company else f"{job_title} at {company}"
        st.subheader(f"Compatibility Score for {job_display}")
        
        # Check if there was an error
        if "error" in compatibility_results:
            st.error(f"Error in compatibility calculation: {compatibility_results['error']}")
            if "raw_content" in compatibility_results:
                st.text_area("Raw Response", compatibility_results["raw_content"], height=300)
            return
        
        # Display overall score
        overall_score = compatibility_results.get("overall_score", 0)
        if isinstance(overall_score, str) and "%" in overall_score:
            try:
                overall_score = int(overall_score.rstrip("%"))
            except ValueError:
                overall_score = 0
        
        st.metric("Overall Match Score", f"{overall_score}%")
        
        # Create columns for detailed scores
        col1, col2, col3 = st.columns(3)
        
        with col1:
            skills_score = compatibility_results.get("skills_match", {}).get("score", 0)
            if isinstance(skills_score, str) and "%" in skills_score:
                try:
                    skills_score = int(skills_score.rstrip("%"))
                except ValueError:
                    skills_score = 0
            st.metric("Skills Match", f"{skills_score}%")
            
        with col2:
            experience_score = compatibility_results.get("experience_match", {}).get("score", 0)
            if isinstance(experience_score, str) and "%" in experience_score:
                try:
                    experience_score = int(experience_score.rstrip("%"))
                except ValueError:
                    experience_score = 0
            st.metric("Experience Match", f"{experience_score}%")
            
        with col3:
            education_score = compatibility_results.get("education_match", {}).get("score", 0)
            if isinstance(education_score, str) and "%" in education_score:
                try:
                    education_score = int(education_score.rstrip("%"))
                except ValueError:
                    education_score = 0
            st.metric("Education Match", f"{education_score}%")
        
        # Display missing skills
        if "skills_match" in compatibility_results and "missing_skills" in compatibility_results["skills_match"]:
            missing_skills = compatibility_results["skills_match"]["missing_skills"]
            if missing_skills:
                st.write("**Missing Skills:**")
                for skill in missing_skills:
                    st.write(f"- {skill}")
        
        # Display missing experiences
        if "experience_match" in compatibility_results and "missing_experiences" in compatibility_results["experience_match"]:
            missing_experiences = compatibility_results["experience_match"]["missing_experiences"]
            if missing_experiences:
                st.write("**Missing Experiences:**")
                for exp in missing_experiences:
                    st.write(f"- {exp}")
        
        # Display recommendations
        if "recommendations" in compatibility_results and compatibility_results["recommendations"]:
            st.write("**Recommendations to Improve Match:**")
            recommendations = compatibility_results["recommendations"]
            if isinstance(recommendations, list):
                for rec in recommendations:
                    st.write(f"- {rec}")
            else:
                st.write(recommendations)
        
        # Add a download button for a formatted report
        st.markdown("---")
        st.write("Download a formatted compatibility report:")
        
        # Create a formatted report
        report = f"""# Job Compatibility Report for {job_display}

## Overall Match Score: {overall_score}%

### Detailed Scores
- Skills Match: {skills_score}%
- Experience Match: {experience_score}%
- Education Match: {education_score}%

## Missing Skills
{self._format_list_or_text(compatibility_results.get("skills_match", {}).get("missing_skills", []))}

## Missing Experiences
{self._format_list_or_text(compatibility_results.get("experience_match", {}).get("missing_experiences", []))}

## Recommendations to Improve Match
{self._format_list_or_text(compatibility_results.get("recommendations", []))}
"""
        
        # Add download button
        st.download_button(
            label="Download Compatibility Report",
            data=report,
            file_name=f"job_compatibility_{job_title.replace(' ', '_')}.md",
            mime="text/markdown"
        )
    
    def _format_list_or_text(self, items: Union[List[str], str]) -> str:
        """Format items as a markdown list or text."""
        if not items:
            return "None identified."
            
        if isinstance(items, list):
            return "\n".join([f"- {item}" for item in items])
        else:
            return items