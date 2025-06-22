import os
import sys
print(f"Current directory: {os.getcwd()}")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(f"Python path: {sys.path}")

try:
    from src.document_processor.processor import ClaimDocumentProcessor
    print("Successfully imported ClaimDocumentProcessor")
except Exception as e:
    print(f"Error importing ClaimDocumentProcessor: {e}")

def test_document_processor():
    try:
        processor = ClaimDocumentProcessor()
        print("Created processor instance")
        
        # Process the sample claim document
        sample_path = "data/sample_claims/water_damage_claim.txt"
        print(f"Sample path: {sample_path}")
        print(f"File exists: {os.path.exists(sample_path)}")
        
        result = processor.process_file(sample_path)
        print("Processed file")
        
        print("\n===== EXTRACTED CLAIM INFORMATION =====\n")
        
        # Print extracted metadata
        for field, value in result["metadata"].items():
            if field not in ["filename", "processed_at"] and value is not None:
                print(f"{field}: {value}")
        
        # Rest of the function...
        # ...
    except Exception as e:
        print(f"Error in test_document_processor: {e}")

if __name__ == "__main__":
    print("Running test_processor.py")
    test_document_processor()
    print("Finished test_processor.py")