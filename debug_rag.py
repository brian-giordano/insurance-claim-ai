from src.rag_system.rag import SimpleRAG

# Initialize the RAG system
rag = SimpleRAG()

# Test the unrelated question specifically
question = "Something completely unrelated to insurance"
print(f"Question: {question}")

# Debug the insurance-related check
is_insurance = rag._is_insurance_related(question.lower())
print(f"Is insurance-related: {is_insurance}")

# Debug the keywords extraction
keywords = rag._extract_keywords(question.lower())
print(f"Keywords: {keywords}")

# Get the answer
response = rag.get_answer(question)
print(f"Confidence: {response['confidence']:.2f}")
print(f"Answer: {response['answer'][:150]}...")