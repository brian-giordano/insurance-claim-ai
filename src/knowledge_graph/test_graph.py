"""
Test script for the SimpleGraphDatabase
"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.knowledge_graph.simple_graph import SimpleGraphDatabase, create_sample_insurance_graph

def test_graph_database():
    # Create a sample graph
    graph = create_sample_insurance_graph()
    
    # Print basic graph information
    print(f"Number of nodes: {len(graph.nodes)}")
    print(f"Number of relationships: {len(graph.relationships)}")
    
    # Test node retrieval
    person = graph.get_node("person1")
    print(f"\nPerson node: {person['properties']['name']}")
    
    # Test relationship retrieval
    person_rels = graph.get_relationships("person1")
    print(f"\nRelationships for {person['properties']['name']}:")
    for rel in person_rels:
        target_node = graph.get_node(rel["target"])
        target_name = target_node["properties"].get("name", target_node["properties"].get("claim_number", target_node["properties"].get("policy_number", target_node["id"])))
        print(f"- {rel['type']} -> {target_name}")
    
    # Test path finding
    print("\nPaths from John Smith to service providers:")
    
    # Path to ABC Plumbing
    paths = graph.find_paths("person1", "provider1")
    print(f"Paths to ABC Plumbing: {len(paths)}")
    if paths:
        for i, path in enumerate(paths):
            path_str = " -> ".join([f"{graph.get_node(node_id)['properties'].get('name', node_id)}" for node_id, _, _ in path]) + f" -> {graph.get_node('provider1')['properties']['name']}"
            print(f"Path {i+1}: {path_str}")
    else:
        print("No paths found to ABC Plumbing")
    
    # Path to XYZ Water Restoration
    paths = graph.find_paths("person1", "provider2")
    print(f"\nPaths to XYZ Water Restoration: {len(paths)}")
    if paths:
        for i, path in enumerate(paths):
            path_str = " -> ".join([f"{graph.get_node(node_id)['properties'].get('name', node_id)}" for node_id, _, _ in path]) + f" -> {graph.get_node('provider2')['properties']['name']}"
            print(f"Path {i+1}: {path_str}")
    else:
        print("No paths found to XYZ Water Restoration")
    
    # Test query
    print("\nQuery: Find all claims filed by John Smith")
    claims = graph.query("person1", ["FILED"])
    for claim in claims:
        print(f"- {claim['properties']['claim_number']}: {claim['properties']['incident_type']}")

if __name__ == "__main__":
    test_graph_database()