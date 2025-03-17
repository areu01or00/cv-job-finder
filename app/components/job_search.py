import streamlit as st
import pandas as pd
import os
import sys
from typing import Dict, Any, List, Optional

# Add the project root directory to Python path if not already there
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.utils import LinkedInJobSearch, OpenRouterClient, MockLinkedInJobSearch
from app.utils.config import USE_MOCK_JOB_SEARCH

class JobSearchComponent:
    """Streamlit component for job search."""
    
    def __init__(self):
        # Use mock implementation if configured or as a fallback
        if USE_MOCK_JOB_SEARCH:
            self.job_searcher = MockLinkedInJobSearch()
            st.info("Using mock job search implementation for demonstration purposes.")
        else:
            self.job_searcher = LinkedInJobSearch()
        
        self.llm_client = OpenRouterClient()
        
    def render(self, cv_analysis: Optional[Dict[str, Any]] = None):
        """
        Render the job search component.
        
        Args:
            cv_analysis: Dictionary with CV analysis results
        """
        st.header("Job Search")
        
        if cv_analysis is None:
            st.info("Please analyze your CV first to get job recommendations.")
            return
        
        # Generate search queries if not already done
        if "search_queries" not in st.session_state:
            with st.spinner("Generating job search queries..."):
                try:
                    search_queries = self.llm_client.generate_job_search_queries(cv_analysis)
                    st.session_state["search_queries"] = search_queries
                except Exception as e:
                    st.error(f"Error generating search queries: {e}")
                    st.session_state["search_queries"] = []
        
        search_queries = st.session_state.get("search_queries", [])
        
        # Display and allow editing of search queries
        st.subheader("Job Search Queries")
        
        if not search_queries:
            st.warning("No search queries generated. Please enter your own queries below.")
            
        # Allow user to edit queries
        edited_queries = []
        for i, query in enumerate(search_queries):
            edited_query = st.text_input(f"Query {i+1}", value=query)
            edited_queries.append(edited_query)
            
        # Allow user to add a new query
        new_query = st.text_input("Add a new query")
        if new_query:
            edited_queries.append(new_query)
            
        # Update session state with edited queries
        if edited_queries != search_queries:
            st.session_state["search_queries"] = edited_queries
            search_queries = edited_queries
            
        # Location input
        location = st.text_input("Location (optional)", value=st.session_state.get("location", ""))
        if location != st.session_state.get("location", ""):
            st.session_state["location"] = location
            
        # Number of results per query
        results_per_query = st.slider(
            "Results per query", 
            min_value=1, 
            max_value=10, 
            value=st.session_state.get("results_per_query", 5)
        )
        if results_per_query != st.session_state.get("results_per_query", 5):
            st.session_state["results_per_query"] = results_per_query
        
        # Add option to use mock implementation
        use_mock = st.checkbox("Use mock data (for testing)", value=USE_MOCK_JOB_SEARCH)
        if use_mock and not isinstance(self.job_searcher, MockLinkedInJobSearch):
            self.job_searcher = MockLinkedInJobSearch()
            st.info("Switched to mock job search implementation.")
        elif not use_mock and isinstance(self.job_searcher, MockLinkedInJobSearch):
            self.job_searcher = LinkedInJobSearch()
            st.info("Switched to real LinkedIn job search implementation.")
            
        # Search button
        search_button = st.button("Search Jobs")
        
        if search_button and search_queries:
            with st.spinner("Searching for jobs... This may take a moment."):
                try:
                    # Perform job search
                    job_results = self.job_searcher.search_multiple_queries(
                        search_queries, 
                        location, 
                        results_per_query
                    )
                    
                    # Store results in session state
                    st.session_state["job_results"] = job_results
                    
                    # Display results
                    self._display_job_results(job_results)
                except Exception as e:
                    st.error(f"Error searching for jobs: {e}")
                    
                    # Fallback to mock implementation if real search fails
                    if not isinstance(self.job_searcher, MockLinkedInJobSearch):
                        st.warning("Falling back to mock job search implementation.")
                        self.job_searcher = MockLinkedInJobSearch()
                        
                        try:
                            # Try with mock implementation
                            job_results = self.job_searcher.search_multiple_queries(
                                search_queries, 
                                location, 
                                results_per_query
                            )
                            
                            # Store results in session state
                            st.session_state["job_results"] = job_results
                            
                            # Display results
                            self._display_job_results(job_results)
                        except Exception as e2:
                            st.error(f"Error with mock job search: {e2}")
        elif "job_results" in st.session_state:
            # Display previously found results
            self._display_job_results(st.session_state["job_results"])
            
    def _display_job_results(self, job_results: pd.DataFrame):
        """
        Display job search results.
        
        Args:
            job_results: DataFrame with job listings
        """
        st.subheader("Job Search Results")
        
        if job_results.empty:
            st.warning("No job listings found. Try different search queries or location.")
            return
            
        # Display number of results
        st.write(f"Found {len(job_results)} job listings.")
        
        # Add a filter for job titles
        all_titles = job_results["title"].unique().tolist()
        selected_titles = st.multiselect(
            "Filter by job title",
            options=all_titles,
            default=[]
        )
        
        # Add a filter for companies
        all_companies = job_results["company"].unique().tolist()
        selected_companies = st.multiselect(
            "Filter by company",
            options=all_companies,
            default=[]
        )
        
        # Add a filter for locations
        all_locations = job_results["location"].unique().tolist()
        selected_locations = st.multiselect(
            "Filter by location",
            options=all_locations,
            default=[]
        )
        
        # Apply filters
        filtered_results = job_results.copy()
        if selected_titles:
            filtered_results = filtered_results[filtered_results["title"].isin(selected_titles)]
        if selected_companies:
            filtered_results = filtered_results[filtered_results["company"].isin(selected_companies)]
        if selected_locations:
            filtered_results = filtered_results[filtered_results["location"].isin(selected_locations)]
            
        # Display filtered results
        if filtered_results.empty:
            st.warning("No job listings match the selected filters.")
            return
            
        # Display job listings
        for _, job in filtered_results.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### [{job['title']}]({job['url']})")
                    st.write(f"**Company:** {job['company']}")
                    st.write(f"**Location:** {job['location']}")
                    st.write(f"**Search Query:** {job['query']}")
                    
                with col2:
                    st.markdown(f"[Apply on LinkedIn]({job['url']})")
                    
                st.divider()