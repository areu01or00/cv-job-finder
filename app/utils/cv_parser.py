import os
import PyPDF2
from typing import Dict, Any, Optional
from .config import CV_UPLOAD_FOLDER
from .llm import OpenRouterClient

class CVParser:
    """Parser for extracting text and information from CV files."""
    
    def __init__(self, llm_client: Optional[OpenRouterClient] = None):
        self.llm_client = llm_client or OpenRouterClient()
        
    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text()
                return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {e}")
    
    def parse_cv(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a CV file and extract relevant information.
        
        Args:
            file_path: Path to the CV file
            
        Returns:
            Dictionary with extracted information
        """
        # Extract text from the CV
        cv_text = self.extract_text_from_pdf(file_path)
        
        # Use LLM to analyze the CV
        cv_analysis = self.llm_client.analyze_cv(cv_text)
        
        return cv_analysis
    
    def save_uploaded_cv(self, uploaded_file) -> str:
        """
        Save an uploaded CV file to the data directory.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Path to the saved file
        """
        os.makedirs(CV_UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(CV_UPLOAD_FOLDER, uploaded_file.name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        return file_path