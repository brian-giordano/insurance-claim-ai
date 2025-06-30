from typing import Dict, List, Any, Optional, Set, Tuple
import json

class SimpleGraphDatabase:
    """
    A simple in-memory graph database simulation.
    This demonstrates graph concepts without requiring Neo4j installation.
    """

    def __init__(self):
        # Initialize empty graph
        self.nodes = {}                                 # id -> node properties
        self.relationships = []                         # list of (source_id, target_id, type, properies)

    def add_node(self, node_id: str, labels: List[str], properties: Dict[str, Any]) -> str:
        """
        Add a node to the graph.

        Args:
            node_id: Unique identifier for the node
            labels: List of labels for the node (e.g, ["Person", "Customers"])
            properties: Dictionary of node properties

        Returns:
            The node ID
        """

        self.nodes[node_id] = {
            "id": node_id,
            "labels": labels,
            "properties": properties
        }
        return node_id
    
    def add_relationship(self, source_id: str, target_id: str, rel_type: str, properties: Dict[str, Any]) -> int:
        """
        Add a relationship between two nodes.

        Args:
            source_id: ID of the source node
            target_id: Id of the target node
            rel_type: Type of relationship
            properties: Dictionary of relationship properties

        Returns:
            Index of the new relationship
        """

        if source_id not in self.nodes or target_id not in self.nodes:
            raise ValueError("Source or target node does not exist")
        
        relationship = {
            "source": source_id,
            "target": target_id,
            "type": rel_type,
            "properties": properties
        }

        self.relationships.append(relationship)
        return len(self.relationships) - 1
    
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a node by ID.

        Args:
            node_id: ID of the node to retrieve

        Returns: 
            Node dictionary or None if not found
        """

        return self.nodes.get(node_id)
    
    def get_relationships(self, node_id: str, rel_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get relationships for a node.

        Args:
            node_id: ID of the node
            rel_typ: Optional relationship type filter

        Returns:
            List of relationship dictionaries
        """
        relationships = []

        for rel in self.relationships:
            if rel["source"] == node_id or rel["target"] == node_id:
                if rel_type is None or rel["type"] == rel_type:
                    relationships.append(rel)

        return relationships
    
    def query(self, start_node_id: str, relationship_path: List[str]) -> List[Dict[str, Any]]:
        """
        Perform a simple path query.

        Args:
            start_node_id: Id of the starting node
            relationship_path: List of relationship types to traverse

        Returns:
            List of nodes found at the end of the path
        """

        current_nodes = [start_node_id]

        for rel_type in relationship_path:
            next_nodes = []

            for node_id in current_nodes:
                for rel in self.relationships:
                    if rel["source"] == node_id and rel["type"] == rel_type:
                        next_nodes.append(rel["target"])

            current_nodes = next_nodes

            if not current_nodes:
                break

        return [self.nodes[node_id] for node_id in current_nodes if node_id in self.nodes]
    
    def find_paths(self, start_node_id: str, end_node_id: str, max_depth: int = 3) -> List[List[Tuple[str, str, str]]]:
        """
        Find all paths between two nodes up to a maximum depth.
        Consider both directions of relationships.
        
        Args:
            start_node_id: ID of the starting node
            end_node_id: ID of the ending node
            max_depth: Maximum path length
            
        Returns:
            List of paths, where each path is a list of (node_id, relationship_type, node_id) tuples
        """
        # Special case: start and end are the same
        if start_node_id == end_node_id:
            return [[(start_node_id, "SELF", start_node_id)]]
        
        def dfs(current_id, target_id, path, visited, all_paths, depth):
            if depth > max_depth:
                return
            
            if current_id == target_id:
                all_paths.append(path.copy())
                return
            
            visited.add(current_id)
            
            # Check outgoing relationships
            for rel in self.relationships:
                if rel["source"] == current_id and rel["target"] not in visited:
                    path.append((current_id, rel["type"], rel["target"]))
                    dfs(rel["target"], target_id, path, visited, all_paths, depth + 1)
                    path.pop()
            
            # Check incoming relationships (treat them as bidirectional)
            for rel in self.relationships:
                if rel["target"] == current_id and rel["source"] not in visited:
                    # Add with reversed direction indicator
                    path.append((current_id, f"INVERSE_{rel['type']}", rel["source"]))
                    dfs(rel["source"], target_id, path, visited, all_paths, depth + 1)
                    path.pop()
            
            visited.remove(current_id)
        
        all_paths = []
        dfs(start_node_id, end_node_id, [], set(), all_paths, 0)
        return all_paths
    
    def to_json(self) -> str:
        """
        Convert graph data to JSON format.

        Returns:
            JSON string representation of the graph
        """

        graph_dict = {
            "nodes": list(self.nodes.values()),
            "relationships": self.relationships
        }
        return json.dumps(graph_dict, indent=2)
    
    def from_json(self, json_str: str) -> None:
        """
        Load the graph from JSON.

        Args:
            json_str: JSON string representation of the graph
        """
        graph_dict = json.loads(json_str)

        self.nodes = {}
        for node in graph_dict["nodes"]:
            self.nodes[node["id"]] = node

        self.relationships = graph_dict["relationships"]

def create_sample_insurance_graph():
    """
    Create a sample insurance graph with claims, policies, and people.
    """
    graph = SimpleGraphDatabase()

    # Add policy nodes
    graph.add_node("policy1", ["Policy"], {
        "policy_number": "POL-HDI-45678",
        "type": "Homeowners",
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "premium": 1200.00,
        "deductible": 1000.00
    })

    # Add person nodes
    graph.add_node("person1", ["Policyholder"], {
        "name": "John Smith",
        "type": "Homeowners",
        "address": "123 Main Street, Hartford, CT 06103",
        "phone": "(555) 123-4567",
        "email": "john.smith@email.com"
    })

    # Add claim nodes
    graph.add_node("claim1", ["Claim"], {
        "claim_number": "CLM-2023-78945",
        "date_of_loss": "2023-05-15",
        "incident_type": "Water Damage",
        "status": "Open",
        "reported_date": "2023-05-15"
    })

    # Add property nodes
    graph.add_node("property1", ["Property"], {
        "address": "123 Main Street, Hartford, CT 06103",
        "type": "Single Family Home",
        "year_built": 1985,
        "square_feet": 2200 
    })

    # Add service provider nodes
    graph.add_node("provider1", ["ServiceProvider"], {
        "name": "ABC Plumbing",
        "service_type": "Plumbing",
        "phone": "(555) 987-6543"
    })

    graph.add_node("provider2", ["ServiceProvider"], {
        "name": "XYZ Water Restoration",
        "service_type": "Water Mitigation",
        "phone": "(555) 456-7890"
    })

    # Add relationships
    graph.add_relationship("person1", "policy1", "HOLDS", {"role": "Primary Insured"})
    graph.add_relationship("person1", "property1", "OWNS", {"since": "2011"})
    graph.add_relationship("person1", "claim1", "FILED", {"date": "2023-05-15"})
    graph.add_relationship("claim1", "policy1", "COVERED_BY", {"coverage_type": "Dwelling"})
    graph.add_relationship("claim1", "property1", "AFFECTS", {"damage_extent": "Moderate"})
    graph.add_relationship("claim1", "provider1", "SERVICED_BY", {"service_date": "2023-03-15", "service_type": "Pipe Repair"})
    graph.add_relationship("claim1", "provider2", "SERVICED_BY", {"service_date": "2023-05-15", "service_type": "Water Extraction"})

    return graph

if __name__ == "__main__":
    # Create a sample graph
    graph = create_sample_insurance_graph()

    # Print the graph as JSON
    print(graph.to_json())

    # Example query: Find all service providers who worked on John Smith's claims
    paths = graph.find_paths("person1", "provider1")
    print(f"Paths from John Smith to ABC Plumbing: {len(paths)}")
    for path in paths:
        print(" -> ".join([f"({graph.get_node(node_id)['properties'].get('name', node_id)})" for node_id, _, _ in path] + 
                         [f"({graph.get_node(paths[-1][2])['properties'].get('name', paths[-1][2])})"]))