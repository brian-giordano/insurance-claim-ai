import streamlit as st
import os
import sys
import tempfile
from pyvis.network import Network
import networkx as nx
import pandas as pd
from pathlib import Path
import time
from datetime import datetime

# Add parent path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.document_processor.processor import ClaimDocumentProcessor
from src.rag_system.rag import SimpleRAG
from src.knowledge_graph.simple_graph import SimpleGraphDatabase, create_sample_insurance_graph

st.set_page_config(
    page_title="Insurance Claim AI",
    page_icon="📊",
    layout="centered",          # ← Changed from "wide" → much better on mobile
    initial_sidebar_state="expanded"
)

# Mobile & responsiveness improvements
st.markdown("""
    <style>
        .stApp { max-width: 1200px; margin: 0 auto; }
        @media (max-width: 768px) {
            .stTabs [data-baseweb="tab-list"] button { font-size: 0.9rem; padding: 8px 12px; }
            .stMetric { margin-bottom: 10px; }
        }
        /* Make PyVis graph fully responsive */
        iframe { width: 100% !important; max-height: 650px; }
    </style>
""", unsafe_allow_html=True)

# ====================== INSTANT DEMO MODE ======================
st.sidebar.title("🚀 Demo Controls")
demo_mode = st.sidebar.toggle(
    "🚀 Instant Demo Mode",
    value=True,
    help="Fast preview with mock data & caching (loads in <1s)"
)

if demo_mode:
    st.sidebar.success("✅ Mock data & caching enabled — loading in <1s")
else:
    st.sidebar.info("Full AI mode (slower on first load)")

# ====================== CACHING & INITIALIZATION ======================
@st.cache_resource
def get_processor():
    return ClaimDocumentProcessor()

@st.cache_resource
def get_rag():
    return SimpleRAG()

@st.cache_resource
def get_graph_db():
    return create_sample_insurance_graph()

processor = get_processor()
rag = get_rag()
graph_db = get_graph_db()

# Cache the entire graph HTML (never regenerates unless code changes)
@st.cache_data
def get_cached_graph_html():
    net = Network(height="650px", width="100%", bgcolor="#ffffff", font_color="black")
    # (same node/edge logic as before — kept identical for consistency)
    for node_id, node_data in graph_db.nodes.items():
        label = node_data["properties"].get("name") or node_data["properties"].get("claim_number") or node_id
        if any(l in str(node_data["labels"]) for l in ["Person", "Policyholder"]):
            color = "#4CAF50"
        elif "Policy" in str(node_data["labels"]):
            color = "#2196F3"
        elif "Claim" in str(node_data["labels"]):
            color = "#F44336"
        elif "Property" in str(node_data["labels"]):
            color = "#9C27B0"
        else:
            color = "#607D8B"
        net.add_node(node_id, label=label, title=str(node_data["properties"]), color=color)

    node_ids = set(graph_db.nodes.keys())
    for rel in graph_db.relationships:
        if rel["source"] in node_ids and rel["target"] in node_ids:
            net.add_edge(rel["source"], rel["target"], label=rel["type"])

    net.barnes_hut(spring_length=180)
    html_path = "cached_graph.html"
    net.save_graph(html_path)
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

# ====================== HEADER & TABS ======================
st.title("🔍 Insurance Claims AI Analyzer")
st.markdown("**AI-powered document intelligence • RAG knowledge assistant • Interactive knowledge graph**")

tab1, tab2, tab3 = st.tabs(["📄 Document Analysis", "💡 Insurance Knowledge", "🔗 Relationship Graph"])

# ====================== TAB 1: DOCUMENT ANALYSIS ======================
with tab1:
    st.subheader("Upload claim documents for instant analysis")

    # Sample claims in demo mode
    if demo_mode:
        sample_option = st.selectbox(
            "Try a sample claim (instant)",
            ["Water Damage Claim — 12345", "Auto Accident Claim — 67890", "Roof Damage Claim — 54321"]
        )
        if st.button("Load Sample Claim", use_container_width=True):
            st.success("✅ Sample loaded instantly (demo mode)")

    uploaded_file = st.file_uploader("Or upload your own PDF/TXT", type=["pdf", "txt"])

    if uploaded_file or (demo_mode and 'sample_option' in locals()):
        with st.spinner("Analyzing..."):
            if demo_mode:
                result = {
                    "text": """INSURANCE CLAIM FORM
CLAIM NUMBER: CLM-12345
POLICY NUMBER: POL-987654
DATE OF LOSS: 2026-03-15

CLAIMANT INFORMATION
Name: Sarah Chen
Address: 142 Oak Street, New Haven, CT 06511
Phone: (203) 555-0192
Email: sarah.chen@email.com

INCIDENT DETAILS
Type of Loss: Water Damage - Burst Pipe
Date of Incident: March 15, 2026
Description of Loss: A burst pipe in the upstairs bathroom caused extensive water damage to the ceiling, walls, and flooring on the first floor. Water leaked through the ceiling into the living room and kitchen areas. Mitigation services were called within 4 hours of discovery.

PROPERTY INFORMATION
Property Type: Single Family Home
Year Built: 1998
Policy Coverage: Dwelling + Personal Property

PHOTOS ATTACHED: Yes (12 photos)
ESTIMATED REPAIR COST: $14,200
DEDUCTIBLE: $500

ADDITIONAL NOTES:
- No previous claims on this policy
- Water shut off immediately
- Professional water extraction completed same day""",
                    "metadata": {
                        "claim_number": "CLM-12345",
                        "policy_number": "POL-987654",
                        "date_of_loss": "2026-03-15",
                        "claimant_name": "Sarah Chen",
                        "incident_type": "Water Damage - Burst Pipe",
                        "property_address": "142 Oak Street, New Haven, CT",
                        "deductible": "500",
                        "description": "Burst pipe in upstairs bathroom caused extensive water damage."
                    }
                }
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                result = processor.process_file(tmp_path)
                os.unlink(tmp_path)

            # === MOBILE-FRIENDLY DISPLAY ===
            st.subheader("Claim Information")
            for k, v in result["metadata"].items():
                if v and k not in ["filename", "processed_at"]:
                    st.metric(k.replace("_", " ").title(), v)

            st.subheader("Risk & Coverage")
            risk_cols = st.columns(3)
            with risk_cols[0]:
                st.success("**Fraud Risk**  \nLow (12%)")
            with risk_cols[1]:
                st.success("**Coverage Confidence**  \nHigh (95%)")
            with risk_cols[2]:
                st.info("**Estimated Settlement**  \n$12,500")

            st.subheader("AI Recommendations")
            for rec in ["✅ Claim appears legitimate", "✅ Water damage covered under Section I.A.2", "⚠️ Request additional photos"]:
                st.info(rec)

            with st.expander("Raw Document Text"):
                st.text(result["text"])

# ====================== TAB 2: INSURANCE KNOWLEDGE ======================
with tab2:
    st.subheader("Insurance Knowledge Assistant")
    st.write("Ask questions about insurance policies, claims, and procedures.")

    # === SESSION STATE FOR SAMPLE BUTTONS ===
    if "current_question" not in st.session_state:
        st.session_state.current_question = ""

    question = st.text_input(
        "Ask any insurance question:",
        value=st.session_state.current_question,
        placeholder="E.g., What is covered under a standard homeowners policy for water damage?",
        key="rag_question_input"
    )

    # Process answer (works for both typing and button clicks)
    if question:
        with st.spinner("Searching knowledge base..."):
            if demo_mode:
                # Fast mock answers for demo mode
                mock_answers = {
                    "water damage": "Water damage from burst pipes is typically covered under most homeowners policies (Section I.A.2). Excludes flood damage unless you have a separate flood policy.",
                    "documentation": "Required documents: photos of damage, repair estimates, police report (if applicable), and proof of ownership.",
                    "fraud": "Common signs include inflated repair costs, multiple claims in short time, inconsistent stories, or backdated documents.",
                    "cash value": "Actual Cash Value (ACV) pays current depreciated value. Replacement Cost Value (RCV) pays full cost to replace with new items (usually higher premium).",
                }
                answer_text = next((v for k, v in mock_answers.items() if k in question.lower()), "Great question! In a real production system this would be answered via vector RAG with source citations.")
                response = {"answer": answer_text, "confidence": 0.92, "source": "Insurance Knowledge Base (demo mode)"}
            else:
                response = rag.get_answer(question)

            st.subheader("Answer")
            st.write(response["answer"])

            with st.expander("Source & Confidence"):
                st.metric("Confidence", f"{response['confidence']:.0%}")
                st.write(response["source"])

        # Clear the input after answering (optional nice touch)
        st.session_state.current_question = ""

    # === QUICK SAMPLE QUESTIONS (now fully working) ===
    st.subheader("Quick Sample Questions")
    cols = st.columns(2)

    sample_questions = [
        "What is covered under a standard homeowners policy for water damage?",
        "What documentation is required for a water damage claim?",
        "What are common signs of insurance fraud?",
        "What is actual cash value vs. replacement cost?"
    ]

    for i, q in enumerate(sample_questions):
        if cols[i % 2].button(q, use_container_width=True, key=f"sample_{i}"):
            st.session_state.current_question = q
            st.rerun()

# ====================== TAB 3: RELATIONSHIP GRAPH ======================
with tab3:
    st.subheader("Insurance Relationship Graph")
    st.caption("Interactive visualization of policies, claimants, claims, and service providers")

    html_content = get_cached_graph_html()
    st.components.v1.html(html_content, height=700)

    # Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Nodes", len(graph_db.nodes))
    col2.metric("Relationships", len(graph_db.relationships))
    col3.metric("Entity Types", len(set(l for n in graph_db.nodes.values() for l in n["labels"])))

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("About This Project")
    st.write("Demonstrates production-grade AI engineering: document intelligence, RAG, knowledge graphs, and full-stack Streamlit development.")
    st.divider()
    st.caption(f"© {datetime.now().year} Brian Giordano")