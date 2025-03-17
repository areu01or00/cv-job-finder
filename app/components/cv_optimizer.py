import streamlit as st
import os
import sys
from typing import Dict, Any, Optional

# Add the project root directory to Python path if not already there
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.utils import AdvancedFeatures

class CVOptimizerComponent:
    """Streamlit component for CV optimization."""
    
    def __init__(self):
        self.advanced_features = AdvancedFeatures()
        
    def render(self, cv_analysis: Optional[Dict[str, Any]] = None):
        """
        Render the CV optimizer component.
        
        Args:
            cv_analysis: Dictionary with CV analysis results
        """
        st.header("CV Optimization")
        
        if cv_analysis is None:
            st.info("Please analyze your CV first to get optimization recommendations.")
            return
        
        st.write("Get tailored recommendations to optimize your CV for specific job roles.")
        
        # Input for target job title
        target_job_title = st.text_input("Target Job Title", 
                                         placeholder="e.g., Senior Software Engineer, Data Scientist, Product Manager")
        
        if target_job_title and st.button("Get Optimization Recommendations"):
            with st.spinner("Generating CV optimization recommendations..."):
                try:
                    optimization_results = self.advanced_features.optimize_cv(cv_analysis, target_job_title)
                    self._display_optimization_results(optimization_results, target_job_title)
                except Exception as e:
                    st.error(f"Error generating optimization recommendations: {e}")
    
    def _display_optimization_results(self, optimization_results: Dict[str, Any], target_job_title: str):
        """
        Display CV optimization results.
        
        Args:
            optimization_results: Dictionary with optimization recommendations
            target_job_title: The job title the CV was optimized for
        """
        st.subheader(f"CV Optimization for {target_job_title}")
        
        # Check if there was an error
        if "error" in optimization_results:
            st.error(f"Error in optimization: {optimization_results['error']}")
            if "raw_content" in optimization_results:
                st.text_area("Raw Response", optimization_results["raw_content"], height=300)
            return
        
        # Display skills to add
        if "skills_to_add" in optimization_results and optimization_results["skills_to_add"]:
            st.write("**Skills to Add:**")
            skills_to_add = optimization_results["skills_to_add"]
            if isinstance(skills_to_add, list):
                for skill in skills_to_add:
                    st.write(f"- {skill}")
            else:
                st.write(skills_to_add)
        
        # Display skills to emphasize
        if "skills_to_emphasize" in optimization_results and optimization_results["skills_to_emphasize"]:
            st.write("**Skills to Emphasize:**")
            skills_to_emphasize = optimization_results["skills_to_emphasize"]
            if isinstance(skills_to_emphasize, list):
                for skill in skills_to_emphasize:
                    st.write(f"- {skill}")
            else:
                st.write(skills_to_emphasize)
        
        # Display experiences to emphasize
        if "experiences_to_emphasize" in optimization_results and optimization_results["experiences_to_emphasize"]:
            st.write("**Experiences to Emphasize:**")
            experiences = optimization_results["experiences_to_emphasize"]
            if isinstance(experiences, list):
                for exp in experiences:
                    st.write(f"- {exp}")
            else:
                st.write(experiences)
        
        # Display items to remove or de-emphasize
        if "items_to_remove" in optimization_results and optimization_results["items_to_remove"]:
            st.write("**Items to Remove or De-emphasize:**")
            items = optimization_results["items_to_remove"]
            if isinstance(items, list):
                for item in items:
                    st.write(f"- {item}")
            else:
                st.write(items)
        
        # Display general recommendations
        if "general_recommendations" in optimization_results and optimization_results["general_recommendations"]:
            st.write("**General Recommendations:**")
            recommendations = optimization_results["general_recommendations"]
            if isinstance(recommendations, list):
                for rec in recommendations:
                    st.write(f"- {rec}")
            else:
                st.write(recommendations)
        
        # Add a download button for a formatted report
        st.markdown("---")
        st.write("Download a formatted optimization report:")
        
        # Create a formatted report
        report = f"""# CV Optimization Report for {target_job_title}

## Skills to Add
{self._format_list_or_text(optimization_results.get('skills_to_add', []))}

## Skills to Emphasize
{self._format_list_or_text(optimization_results.get('skills_to_emphasize', []))}

## Experiences to Emphasize
{self._format_list_or_text(optimization_results.get('experiences_to_emphasize', []))}

## Items to Remove or De-emphasize
{self._format_list_or_text(optimization_results.get('items_to_remove', []))}

## General Recommendations
{self._format_list_or_text(optimization_results.get('general_recommendations', []))}
"""
        
        # Add download button
        st.download_button(
            label="Download Optimization Report",
            data=report,
            file_name=f"cv_optimization_{target_job_title.replace(' ', '_')}.md",
            mime="text/markdown"
        )
    
    def _format_list_or_text(self, items):
        """Format items as a markdown list or text."""
        if not items:
            return "None provided."
            
        if isinstance(items, list):
            return "\n".join([f"- {item}" for item in items])
        else:
            return items