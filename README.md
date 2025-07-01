# Insurance Claims AI System

An AI -Powered system for processing insurance claims, answering insurance questions, and visualizing insurance relationships.

## Overview

This project demonstrates the application of AI and data engineering techniques to the insurance industry. It includes:

- **Document Processing**: Extract information from insurance claim douments
- **Knowledge Base**: Answer insurance-related questions using a RAG system
- **Graph Database**: Model and visual relationshiops between insurance entities
- **User Interface**: Streamlit-based interface for interacting with all components

## Demo App

A live demo is available at: [https://insurance-claim-ai.onrender.com](https://insurance-claim-ai.onrender.com)

**Note:** The app is hosted on Render's free tier, which spins down after 15 minutes of inactivity. If you're the first visitor after inactivity, it may take 30-60 seconds to load. If you experience any loading issues, please refresh the page.

## Features

### Document Analysis

- Extract claim information from uploaded documents
- Identify key metadata (claim number, date, incident type)
- Provide risk assessment and recommendations

### Insurance Knowledge Assistant

- Anser questions about insurance policies, claims, and procedures
- Provide accurate information with confidence scores
- Access a comprehensive knowledge base of insurance concepts

### Relationship Graph

- Visualize connections between insurance entities (people, policies, claims)
- Find paths between entities to discover relationships
- Analyze the structure of insurance data

## Technology Used

- **Python**: Core programming language
- **Streamlit**: Web interface
- **Hugging Face Models**: NLP processing
- **RAG (Retrieval-Augmented Generation)**: Knowledge base
- **Graph Database Concepts**: Relationship modeling
- **PyVis**: Graph visualization

## Installation

1. Clone the repository:

```
git clone https://github.com/brian-giordano/insurance-claim-ai.git
cd insurance-claim-ai
```

2. Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate            # On Windows: venv\Scripts\activate
```

3. Install dependencies:
   `pip install -r requirements.txt`

4. Run the application:
   `streamlit fun src/ui/app.py`

## Project Structure

```
insurance-claims-ai/
├── data/
│ └── knowledge_base.json
├── src/
│ ├── document_processor/
│ │ ├── init.py
│ │ └── processor.py
│ ├── knowledge_graph/
│ │ ├── init.py
│ │ ├── simple_graph.py
│ │ └── test_graph.py
│ ├── rag_system/
│ │ ├── init.py
│ │ └── rag.py
│ └── ui/
│ ├── init.py
│ └── app.py
├── requirements.txt
└── README.md
```

## Usage

### Document Analysis

1. Navigate to the "Document Analysis" tab
2. Upload an insurance claim document
3. View extracted information and recommendations

### Insurance Knowledge

1. Navigate to the "Insurance Knowledge" tab
2. Enter a questoin or select a sample question
3. View the answer with confidence score

### Relationship Graph

1. Navigate to the "Relationship Graph" tab
2. Explore the visualization of insurance entities
3. Use the path finder to discover connections between entities

## Future Enhancements

- Integration with real insurance databases
- Advanced fraud detection using machine learning
- Mobile application for field adjusters
- API for integration with existing systems

## License

This project is licensed under the MIT License - see LICENSE file for details.
