import re
import os
from typing import Dict, Any
from datetime import datetime

class ClaimDocumentProcessor:
    """
    Processes insurance claim documents and extracts key information.
    """

    def __init__(self):
        # Regular expressions for extracting information
        self.regex_patterns = {
            'claim_number': r'Claim\s+Number:?\s*([A-Z0-9\-]+)',
            'policy_number': r'Policy\s+Number:?\s*([A-Z0-9\-]+)',
            'date_of_loss': r'Date\s+of\s+Loss:?\s*(\d{1,4}[-/\.]\d{1,2}[-/\.]\d{1,4})',
            'claimant_name': r'(?:Policyholder|Reported\s+By|Claimant):?\s*([A-Za-z\s\.]+)(?:\(|,|\r|\n|$)',
            'incident_type': r'(?:Type\s+of\s+Loss|Loss\s+Type|Incident\s+Type):?\s*([A-Za-z\s]+)(?:,|\r|\n|$)',
            'property_address': r'(?:Property\s+Address|Location):?\s*([A-Za-z0-9\s\.,#-]+)(?:,|\r|\n|$)',
            'deductible': r'Deductible:?\s*\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            'description': r'Description\s+of\s+Loss:?\s*([^#]+?)(?:\r|\n\r|\n\n)'
        }

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a claim document file and extract information.

        Args:
            file_path: Path to the document file

        Returns:
            Dictionary containing extracted information
        """

        # Initialize result dictionary
        result = {
            "text": "",
            "metadata": {
                "filename": os.path.basename(file_path),
                "processed_at": datetime.now().isoformat(),
                "claim_number": None,
                "policy_number": None,
                "date_of_loss": None,
                "claimant_name": None,
                "incident_type": None,
                "property_address": None,
                "deductible": None,
                "description": None,
            },
            "extracted_entities": []
        }

        # Read file contents based on file type
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.pdf':
            try: 
                import PyPDF2
                result['text'] = self._read_pdf(file_path)
            except Exception as e:
                result["error"] = f"Error reading PDF: {str(e)}"
                return result
        elif file_extension in ['.txt', '.text']:
            with open(file_path, 'r', encoding='utf-8') as file:
                result["text"] = file.read()
        else:
            result["error"] = f"Unsupported file type: {file_extension}"
            return result
        
        # Extract information using regex patterns
        for field, pattern in self.regex_patterns.items():
            match = re.search(pattern, result["text"], re.IGNORECASE)
            if match:
                result["metadata"][field] = match.group(1).strip()
                # Add to extracted entities for highlighting
                result["extracted_entities"].append({
                    "type": field,
                    "value": match.group(1).strip(),
                    "confidence": 0.95                                  # Placeholder confidence score for now
                })
        return result
    
    def _read_pdf(self, file_path: str) -> str:
        """
        Extract text from a PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            Extracted text content
        """
        try:
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""