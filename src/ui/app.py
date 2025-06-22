import streamlit as st
import os
import sys
import tempfile

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.document_processor.processor import ClaimDocumentProcessor

# Set the page configuration
st.set_page_config(
    page_title="Insurance Claims AI",
    page_icon="🔍",
    layout="wide"
)

# Initialize processor
processor = ClaimDocumentProcessor()

# Header
st.title("🔍 Insurance Claims AI Analyzer")
st.subheader("Upload claim documents for instant analysis")

# Sidebar
with st.sidebar:
    st.header("About")
    st.write(
        "This system uses AI to analyze insurance claims, "
        "extract key information, and asses risk factors."
    )
    st.divider()
    st.subheader("Analysis Options")
    fraud_check = st.checkbox("Fraud Detection", value=True)
    coverage_check = st.checkbox("Coverage Analysis", value=True)
    compliance_check = st.checkbox("Compliance Check", value=True)

# File uploader
uploaded_file = st.file_uploader("Upload Cliam Document", type=["pdf", "txt"])

if uploaded_file:
    # Save the uploaded file to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # Process the document
    with st.spinner("Processing document..."):
        result = processor.process_file(tmp_file_path)

        # Remove the temp file
        os.unlink(tmp_file_path)

        st.success("Document processed successfully!")

        # Display extracted information
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Claim Information")

            # Display extracted metadata
            for field, value in result["metadata"].items():
                if field not in ["filename", "processed_at"] and value is not None:
                    # Format the field name for display
                    display_name = " ".join(word.capitalize() for word in field.split("_"))
                    st.write(f"**{display_name}:** {value}")

        with col2:
            st.subheader("Risk Assessment")

            # Placeholder metrics
            # TODO: replace with AI-generated values
            if result["metadata"].get("incident_type") and "water damage" in result["metadata"]["incident_type"].lower():
                fraud_risk = "Low (12%)"
                coverage_confidence = "High (95%)"
            else:
                fraud_risk = "Medium (35%)"
                coverage_confidence = "Medium (75%)"
            
            st.metric("Fraud Risk", fraud_risk)
            st.metric("Coverage Confidence", coverage_confidence)
            st.metric("Estimated Settlement", "$12,500")

        # Recommendations
        st.subheader("AI Recommendations")

        # Placeholder recommendations
        # TODO: Replace with AI-generated values
        if result["metadata"].get("incident_type") and "water damage" in result["metadata"]["incident_type"].lower():
            st.info(
                "✅ Claim appears legitimate with consistent documentation\n"
                "✅ Water damage from burst pipes is covered under policy section I.A.2\n"
                "⚠️ Request additional photos of the affected area\n"
                "⚠️ Verify if water mitigation services were employed within 24-48 hours"
            )
        else:
            st.info(
                "✅ Claim documentation is complete\n"
                "⚠️ Verify coverage in policy details\n"
                "⚠️ Request additional documentation\n"
                "⚠️ Schedule adjuster inspection"
            )

        # Display the original text
        with st.expander("View Document Text"):
            st.text(result["text"])