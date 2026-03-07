import sys
import os

# Add current directory to path so imports work
sys.path.append(os.path.dirname(__file__))

from graph import LimitedGraph
from bfs import BreadthFirstSearch

def main():
    print("Starting Graph & BFS Algorithm Demo (Decoupled Structure)...")
    
    # 1. Initialize the Graph structure with fewer nodes for clarity
    num_nodes = 12  # Simplified to 12 nodes (A-L)
    g = LimitedGraph(num_nodes)
    
    # Map nodes to names for display (A, B, C, ..., L)
    node_names = {i: chr(65 + i) for i in range(num_nodes)}
    
    # Define a set of edges that clearly illustrates BFS pathfinding
    # This structure provides multiple routes from A (0) to L (11) of varying lengths
    edges = [
        # Path 1: The "Long" Scenic Route (Top) - 5 steps
        # A -> B -> C -> D -> E -> L
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 11),
        
        # Path 2: The "Medium" Route (Bottom) - 4 steps
        # A -> F -> G -> H -> L
        (0, 5), (5, 6), (6, 7), (7, 11),
        
        # Path 3: The "Shortest" Path (Middle) - 3 steps
        # A -> I -> J -> L
        (0, 8), (8, 9), (9, 11),
        
        # Cross-links to add complexity and cycles
        # B -> F (Connects Top to Bottom early)
        (1, 5),
        # C -> G (Connects Top to Bottom middle)
        (2, 6),
        # D -> H (Connects Top to Bottom late)
        (3, 7),
        # I -> G (Connects Shortest to Medium)
        (8, 6),
        # J -> E (Connects Shortest to Long end)
        (9, 4)
    ]
    
    # Add all edges to the graph
    for u, v in edges:
        g.add_edge(u, v)
    
    print("\nAdjacency Matrix (Partial View):")
    for row in g.graph:
        print(str(row) + " ...") # Print rows
    
    # 2. Initialize the Algorithm with the Graph
    bfs_algo = BreadthFirstSearch(g)
    
    start_node = 0  # A
    end_node = 11   # L (Target node)
    
    print(f"\nFinding shortest path from {node_names[start_node]} to {node_names[end_node]}...")
    
    # 3. Execute the algorithm to find shortest path
    path = bfs_algo.find_shortest_path(start_node, end_node)
    
    if path:
        path_names = [node_names[n] for n in path]
        print("Shortest Path Found:", " -> ".join(path_names))
        print(f"Path Length: {len(path) - 1} steps")
    else:
        print("No path found.")

    # 4. Visualize the graph with the highlighted path
    print("\nVisualizing graph with highlighted path...")
    try:
        g.draw(path=path)
    except Exception as e:
        print(f"Could not visualize graph: {e}")

if __name__ == "__main__":
    main()
