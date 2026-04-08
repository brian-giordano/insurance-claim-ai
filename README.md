# Insurance Claim AI Assistant

**AI-powered insurance claims processing platform** — Document intelligence, RAG knowledge assistant, and interactive knowledge graph.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://brian-giordano-insurance-claim-ai-srcuiapp-udsijp.streamlit.app/)

**Live Demo** → [https://brian-giordano-insurance-claim-ai-srcuiapp-udsijp.streamlit.app/](https://brian-giordano-insurance-claim-ai-srcuiapp-udsijp.streamlit.app/)

---

### ✨ Features

- **📄 Document Analysis** — Instantly extracts metadata, risk scores, and AI recommendations from PDFs/TXT
- **💡 Insurance Knowledge Assistant** — Accurate, source-grounded answers via custom RAG pipeline
- **🔗 Interactive Knowledge Graph** — Visualize relationships between policies, claimants, claims, and providers
- **🚀 Instant Demo Mode** — Lightning-fast portfolio preview with mock data and caching

---

### 🛠️ Tech Stack & Skills Demonstrated

- **AI Engineering**: Document intelligence, custom RAG system, entity extraction
- **Data Engineering**: Knowledge graph modeling (NetworkX + PyVis), rule-based retrieval
- **Full-Stack Development**: Production-grade Streamlit app with caching, responsive design, and instant demo mode
- **Performance Optimization**: Zero cold-start experience, heavy `@st.cache` usage

### Architecture

```mermaid
graph TD
    A[PDF/TXT Claim] --> B[Document Processor]
    B --> C[Metadata + Risk Extraction]
    A --> D[RAG Knowledge Base]
    D --> E[Grounded Answers]
    C --> F[Knowledge Graph]
    F --> G[Interactive PyVis Visualization]
```

### Screenshots

<img src="https://github.com/brian-giordano/insurance-claim-ai/blob/main/screenshots/01-hero.png" alt="Hero View">
Full app overview with all three tabs visible
<img src="https://github.com/brian-giordano/insurance-claim-ai/blob/main/screenshots/02-document-analysis.png" alt="Document Analysis">
Sample claim processed with metrics, risk scores, and recommendations
<img src="https://github.com/brian-giordano/insurance-claim-ai/blob/main/screenshots/03-rag-assistant.png" alt="Knowledge Assistant">
RAG-powered insurance knowledge assistant with sample questions
<img src="https://github.com/brian-giordano/insurance-claim-ai/blob/main/screenshots/04-knowledge-graph.png" alt="Relationship Graph">
Interactive knowledge graph with statistics and path analysis
