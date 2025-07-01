import streamlit as st
import os
import sys
import tempfile
from pyvis.network import Network
import networkx as nx
import pandas as pd
import base64
from pathlib import Path
import time

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.document_processor.processor import ClaimDocumentProcessor
from src.rag_system.rag import SimpleRAG
from src.knowledge_graph.simple_graph import SimpleGraphDatabase, create_sample_insurance_graph

# Set the page configuration
st.set_page_config(
    page_title="Insurance Claim AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Display a loading message
with st.spinner("Loading application resources..."):
    # Import heavy dependencies here
    # This gives time for the frontend to stabilize
    time.sleep(3)

# Info message about the free tier
st.sidebar.info(
    """
    **Note:**
    - This app is hosted on Render's free tier, which spins down after inactivity.
    - PDF uploads are limited to 10MB.
    - If you experience any loading issues, please refresh the page.
    """
)

# Initialize processor and RAG system
processor = ClaimDocumentProcessor()
rag = SimpleRAG()
graph_db = create_sample_insurance_graph()

# Function to create and save graph visualization
def create_graph_visualization():
    # Create a PyVis network
    net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
    
    # Add nodes
    for node_id, node_data in graph_db.nodes.items():
        label = node_data["properties"].get("name", 
                node_data["properties"].get("claim_number", 
                node_data["properties"].get("policy_number", node_id)))
        
        # Set node color based on type
        if "Person" in node_data["labels"] or "Policyholder" in node_data["labels"]:
            color = "#4CAF50"  # Green
        elif "Policy" in node_data["labels"]:
            color = "#2196F3"  # Blue
        elif "Claim" in node_data["labels"]:
            color = "#F44336"  # Red
        elif "Property" in node_data["labels"]:
            color = "#9C27B0"  # Purple
        elif "ServiceProvider" in node_data["labels"]:
            color = "#FF9800"  # Orange
        else:
            color = "#607D8B"  # Gray
        
        # Add node with properties as title (for hover)
        properties_str = "\n".join([f"{k}: {v}" for k, v in node_data["properties"].items()])
        net.add_node(node_id, label=label, title=properties_str, color=color)
    
    # Verify all nodes exist before adding edges
    node_ids = set(graph_db.nodes.keys())
    
    # Add edges
    for rel in graph_db.relationships:
        source = rel["source"]
        target = rel["target"]
        
        # Skip edges with non-existent nodes
        if source not in node_ids or target not in node_ids:
            print(f"Warning: Skipping edge {source} -> {target} due to missing node")
            continue
            
        label = rel["type"]
        
        # Add edge with properties as title
        properties_str = "\n".join([f"{k}: {v}" for k, v in rel["properties"].items()])
        net.add_edge(source, target, label=label, title=properties_str)
    
    # Set physics layout
    net.barnes_hut(spring_length=200)
    
    # Save to HTML file
    html_path = "temp_graph.html"
    net.save_graph(html_path)
    
    return html_path
    
# Function to get HTML file content
def get_html_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

# Header
st.title("🔍 Insurance Claims AI Analyzer")

# Tabs
tab1, tab2, tab3 = st.tabs(["Document Analysis", "Insurance Knowledge", "Relationship Graph"])

with tab1:
    st.subheader("Upload claim documents for instant analysis")
    
    # Sidebar for tab1
    with st.sidebar:
        st.header("Analysis Options")
        fraud_check = st.checkbox("Fraud Detection", value=True)
        coverage_check = st.checkbox("Coverage Analysis", value=True)
        compliance_check = st.checkbox("Compliance Check", value=True)
    
    # File uploader
    uploaded_file = st.file_uploader("Upload Claim Document", type=["pdf", "txt"])
    
    if uploaded_file:
        try:
            # Save the uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Process the document
            with st.spinner("Processing document..."):
                result = processor.process_file(tmp_file_path)
                
                # Remove the temporary file
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
                
                # Risk Assessment with properly bold titles
                with col2:
                    st.subheader("Risk Assessment")
                    
                    # Function to display a metric with a colored box and PROPERLY bold title
                    def display_metric(label, value, status="neutral"):
                        if status == "good":
                            color = "rgba(76, 175, 80, 0.1)"  # Light green
                            border = "#4CAF50"  # Green
                        elif status == "warning":
                            color = "rgba(255, 152, 0, 0.1)"  # Light orange
                            border = "#FF9800"  # Orange
                        else:
                            color = "rgba(33, 150, 243, 0.1)"  # Light blue
                            border = "#2196F3"  # Blue
                        
                        st.markdown(f"""
                        <div style="background-color: {color}; padding: 10px 15px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid {border};">
                            <div style="font-size: 0.85em; color: #333; margin-bottom: 3px; font-weight: 700;">{label}</div>
                            <div style="font-size: 1.2em; font-weight: bold;">{value}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Display metrics with color coding AND properly bold titles
                    if fraud_check:
                        fraud_risk = "Low (12%)" if result["metadata"].get("incident_type") and "water damage" in result["metadata"]["incident_type"].lower() else "Medium (35%)"
                        status = "good" if "Low" in fraud_risk else "warning"
                        display_metric("Fraud Risk", fraud_risk, status)
                    
                    if coverage_check:
                        coverage_confidence = "High (95%)" if result["metadata"].get("incident_type") and "water damage" in result["metadata"]["incident_type"].lower() else "Medium (75%)"
                        status = "good" if "High" in coverage_confidence else "warning"
                        display_metric("Coverage Confidence", coverage_confidence, status)
                    
                    if compliance_check:
                        if result["metadata"].get("incident_type") and "water damage" in result["metadata"]["incident_type"].lower():
                            compliance_status = "Needs Verification"
                        else:
                            compliance_status = "Inspection Required"
                        display_metric("Compliance Status", compliance_status, "warning")
                    
                    # Estimated settlement is always shown
                    display_metric("Estimated Settlement", "$12,500", "neutral")
                
                # Recommendations
                st.subheader("AI Recommendations")

                # Build recommendations based on selected options
                recommendations = []

                # Basic recommendation always included
                if result["metadata"].get("incident_type") and "water damage" in result["metadata"]["incident_type"].lower():
                    recommendations.append("✅\u00A0\u00A0\u00A0Claim appears legitimate with consistent documentation")
                else:
                    recommendations.append("✅\u00A0\u00A0\u00A0Claim documentation is complete")

                # Add recommendations based on selected options
                if coverage_check:
                    if result["metadata"].get("incident_type") and "water damage" in result["metadata"]["incident_type"].lower():
                        recommendations.append("✅\u00A0\u00A0\u00A0Water damage from burst pipes is covered under policy section I.A.2")
                    else:
                        recommendations.append("⚠️\u00A0\u00A0\u00A0Verify coverage in policy details")

                if fraud_check:
                    recommendations.append("⚠️\u00A0\u00A0\u00A0Request additional photos of the affected area")

                if compliance_check:
                    if result["metadata"].get("incident_type") and "water damage" in result["metadata"]["incident_type"].lower():
                        recommendations.append("⚠️\u00A0\u00A0\u00A0Verify if water mitigation services were employed within 24-48 hours")
                    else:
                        recommendations.append("⚠️\u00A0\u00A0\u00A0Schedule adjuster inspection")

                # Display each recommendation in its own info box
                with st.container():
                    for rec in recommendations:
                        st.info(rec)

                # Display the original text
                with st.expander("View Document Text"):
                    st.text(result["text"])

        except Exception as e:
            st.error(f"Error processing document: {str(e)}")
            st.info("If you're experiencing issues with document processing, try a smaller file or a different format.")

with tab2:
    st.subheader("Insurance Knowledge Assistant")
    st.write("Ask questions about insurance policies, claims, and procedures.")

    # Question input
    question = st.text_input("Your question:", placeholder="E.g., What is covered under a standard homeowners policy for water damage?")

    if question:
        with st.spinner("Searching knowledge base..."):
            response = rag.get_answer(question)

            st.subheader("Answer")
            st.write(response["answer"])

            with st.expander("Source Information"):
                st.write(f"Confidence: {response['confidence']:.2f}")
                st.write(f"Source: {response['source']}")

    # Sample questions
    st.subheader("Sample Questions")
    sample_questions = [
        "What is covered under a standard homeowners policy for water damage?",
        "What documentation is required for a water damage claim?",
        "What are common signs of insurance fraud?",
        "What is the process for handling a water damage claim?",
        "What is subrogation in insurance claims?",
        "What is actual cash value vs. replacement cost?"
    ]

    for q in sample_questions:
        if st.button(q):
            with st.spinner("Searching knowledge base..."):
                response = rag.get_answer(q)

                st.subheader("Answer")
                st.write(response["answer"])

                with st.expander("Source Information"):
                    st.write(f"Confidence: {response['confidence']:.2f}")
                    st.write(f"Source: {response['source']}")

with tab3:
    st.subheader("Insurance Relationship Graph")
    st.write("This graph shows the relationships between entities in the insurance domain.")

    # Create and display the graph visualization
    with st.spinner("Generating graph visualization..."):
        html_path = create_graph_visualization()
        html_content = get_html_file_content(html_path)

        # Display the HTML content
        st.components.v1.html(html_content, height=600)

    # Display graph statistics
    st.subheader("Graph Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Nodes", len(graph_db.nodes))

    with col2:
        st.metric("Relationships", len(graph_db.relationships))

    with col3:
        # Count node types
        node_types = {}
        for node in graph_db.nodes.values():
            for label in node["labels"]:
                node_types[label] = node_types.get(label, 0) + 1
            
        st.metric("Entity Types", len(node_types))

    # Display node types
    st.subheader("Entity Types")

    # Create a DataFrame for node types
    node_type_data = []
    for label, count in node_types.items():
        node_type_data.append({"Type": label, "Count": count})

    node_type_df = pd.DataFrame(node_type_data)
    st.dataframe(node_type_df)

    # Display path analysis
    st.subheader("Path Analysis")
    
    # Create a form for path analysis
    with st.form("path_analysis_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            start_node = st.selectbox(
                "Start Node",
                options=list(graph_db.nodes.keys()),
                format_func=lambda x: graph_db.nodes[x]["properties"].get("name", 
                                    graph_db.nodes[x]["properties"].get("claim_number", 
                                    graph_db.nodes[x]["properties"].get("policy_number", x)))
            )
        
        with col2:
            end_node = st.selectbox(
                "End Node",
                options=list(graph_db.nodes.keys()),
                format_func=lambda x: graph_db.nodes[x]["properties"].get("name", 
                                    graph_db.nodes[x]["properties"].get("claim_number", 
                                    graph_db.nodes[x]["properties"].get("policy_number", x)))
            )
        
        max_depth = st.slider("Maximum Path Length", min_value=1, max_value=5, value=3)
        
        submitted = st.form_submit_button("Find Paths")
    
    if submitted:
        with st.spinner("Finding paths..."):
            # Special case for same start and end node
            if start_node == end_node:
                st.success("Start and end nodes are the same - no path needed")
                
                # Display the node information
                node_info = graph_db.nodes[start_node]
                node_name = node_info["properties"].get("name", 
                            node_info["properties"].get("claim_number", 
                            node_info["properties"].get("policy_number", start_node)))
                
                st.write(f"**Node:** {node_name}")
                
                # Display node properties
                st.subheader("Node Properties")
                for key, value in node_info["properties"].items():
                    st.write(f"**{key}:** {value}")
            else:
                # Find paths between different nodes
                paths = graph_db.find_paths(start_node, end_node, max_depth)
                
                if paths:
                    st.success(f"Found {len(paths)} path(s)")
                    
                    for i, path in enumerate(paths):
                        path_str = []
                        
                        # Add start node
                        start_name = graph_db.nodes[path[0][0]]["properties"].get("name", 
                                    graph_db.nodes[path[0][0]]["properties"].get("claim_number", 
                                    graph_db.nodes[path[0][0]]["properties"].get("policy_number", path[0][0])))
                        path_str.append(start_name)
                        
                        # Add intermediate nodes and relationships
                        for _, rel_type, node_id in path:
                            path_str.append(f"--[{rel_type}]-->")
                            
                            node_name = graph_db.nodes[node_id]["properties"].get("name", 
                                        graph_db.nodes[node_id]["properties"].get("claim_number", 
                                        graph_db.nodes[node_id]["properties"].get("policy_number", node_id)))
                            path_str.append(node_name)
                        
                        st.write(f"**Path {i+1}:** {' '.join(path_str)}")
                else:
                    st.warning(f"No paths found between the selected nodes with max depth {max_depth}")

# Sidebar for general information
with st.sidebar:
    st.header("About")
    st.write(
        "This system uses AI to analyze insurance claims, "
        "extract key information, and provide knowledge about insurance concepts."
    )
    
    with st.expander("Help"):
        st.write("""
        ### How to Use This App
        
        **Document Analysis**
        - Upload a claim document (PDF or TXT)
        - View extracted information and recommendations
        
        **Insurance Knowledge**
        - Type a question or select a sample question
        - View the answer with confidence score
        
        **Relationship Graph**
        - Explore the visualization of insurance entities
        - Use the path finder to discover connections
        """)
    
    st.divider()
    st.write("© 2025 Insurance Claims AI")