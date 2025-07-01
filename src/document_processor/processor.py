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
            'claim_number': r'Claim Number:\s*([A-Z0-9\-]+)',
            'policy_number': r'Policy Number:\s*([A-Z0-9\-]+)',
            'date_of_loss': r'Date of (?:Loss|Incident):\s*([0-9\-/]+)',
            'claimant_name': r'(?:Policyholder|Reported By):\s*([A-Za-z\s\.]+?)(?:\s*\(|$)',
            'incident_type': r'Type of (?:Loss|Claim):\s*([A-Za-z\s\-–]+?)(?=\s+Description|$)',
            'property_address': r'Property Address:\s*([0-9][^P]+?)(?=Policy)',
            'deductible': r'Deductible:\s*\$?([0-9,]+)',
            'description': r'Description of (?:Loss|Incident):\s*([^.]+\.)'
        }

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a claim document file and extract information.
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
        
        # Print the raw extracted text for debugging
        print("=== RAW EXTRACTED TEXT ===")
        print(result["text"])
        print("==========================")
        
        # Clean the text before processing
        cleaned_text = self._preprocess_text(result["text"])
        
        # Extract information using regex patterns
        for field, pattern in self.regex_patterns.items():
            match = re.search(pattern, cleaned_text, re.IGNORECASE)
            if match:
                extracted_value = match.group(1).strip()
                result["metadata"][field] = extracted_value
                result["extracted_entities"].append({
                    "type": field,
                    "value": extracted_value,
                    "confidence": 0.95
                })
        
        # Try context-aware extraction for fields that might have failed
        result = self._context_aware_extraction(cleaned_text, result)
        
        return result
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and normalize text for better extraction."""
        # Remove bullets and normalize whitespace
        text = re.sub(r'[•·]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _context_aware_extraction(self, text: str, result: Dict) -> Dict:
        """
        Perform context-aware extraction for fields that might need special handling.
        """
        # Extract claimant name from "Name:" pattern if not found
        if not result["metadata"]["claimant_name"]:
            name_match = re.search(r'Name:\s*([A-Za-z\s\.]+?)(?:\s*Address|\s*Phone|\s*Email|$)', text, re.IGNORECASE)
            if name_match:
                name = name_match.group(1).strip()
                result["metadata"]["claimant_name"] = name
                result["extracted_entities"].append({
                    "type": "claimant_name",
                    "value": name,
                    "confidence": 0.90
                })
        
        # Extract incident type - try "Type of Loss:" pattern specifically
        if not result["metadata"]["incident_type"]:
            incident_match = re.search(r'Type of Loss:\s*([A-Za-z\s\-–]+?)(?=\s*Description|\s*$)', text, re.IGNORECASE)
            if incident_match:
                incident_type = incident_match.group(1).strip()
                result["metadata"]["incident_type"] = incident_type
                result["extracted_entities"].append({
                    "type": "incident_type",
                    "value": incident_type,
                    "confidence": 0.90
                })
            else:
                # Fallback for Auto Insurance format
                auto_match = re.search(r'Auto Insurance\s*[–-]\s*([A-Za-z\s]+)', text, re.IGNORECASE)
                if auto_match:
                    incident_type = f"Auto Insurance - {auto_match.group(1).strip()}"
                    result["metadata"]["incident_type"] = incident_type
                    result["extracted_entities"].append({
                        "type": "incident_type",
                        "value": incident_type,
                        "confidence": 0.90
                    })
        
        # Extract property address with precise patterns
        if not result["metadata"]["property_address"]:
            # For TXT files - exact match for your format
            txt_match = re.search(r'Property Address:\s*([0-9][^\n]*?)(?=\s*Policy Type)', text, re.IGNORECASE)
            if txt_match:
                address = txt_match.group(1).strip()
                result["metadata"]["property_address"] = address
                result["extracted_entities"].append({
                    "type": "property_address",
                    "value": address,
                    "confidence": 0.85
                })
            else:
                # For PDF files - Address under Claimant Information
                pdf_match = re.search(r'Address:\s*([0-9][^,]+(?:,[^,]+){1,3})(?=\s+Phone)', text, re.IGNORECASE)
                if pdf_match:
                    address = pdf_match.group(1).strip()
                    result["metadata"]["property_address"] = address
                    result["extracted_entities"].append({
                        "type": "property_address",
                        "value": address,
                        "confidence": 0.85
                    })
        
        return result
    
    def _read_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file."""
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