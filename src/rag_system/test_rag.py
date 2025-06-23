"""
Test script for the SimpleRAG system
"""

import sys
import os

# Add the parent directory to the path so we can use absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.rag_system.rag import SimpleRAG

def test_rag_system():
    # Initialize the RAG system
    rag = SimpleRAG()

    # Test questions
    test_questions = [
        "What does homeowners insurance cover for water damage?",
        "What documents do I need for a water damage claim?",
        "How can I tell if a claim might be fraudulent?",
        "What happens during the claims process?",
        "What is subrogation?",
        "What's the difference between ACV and replacement cost?",
        "Something completely unrelated to insurance"
    ]

    # Test each question
    for question in test_questions:
        print(f"\nQuestion: {question}")
        response = rag.get_answer(question)
        print(f"Confidence: {response['confidence']:.2f}")
        print(f"Answer: {response['answer'][:150]}...")                     # Show first 150 chars

if __name__ == "__main__":
    test_rag_system()