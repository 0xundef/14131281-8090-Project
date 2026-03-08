import networkx as nx
import matplotlib.pyplot as plt

class LimitedGraph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.graph = []
        # Initialize adjacency matrix with 0s
        for _ in range(num_nodes):
            self.graph.append([0] * num_nodes)

    def add_edge(self, u, v):
        if 0 <= u < self.num_nodes and 0 <= v < self.num_nodes:
            self.graph[u][v] = 1
            self.graph[v][u] = 1  # Undirected graph
        else:
            print(f"Error: Nodes {u} and {v} must be between 0 and {self.num_nodes - 1}")

    def draw(self, path=None):
        """
        Visualizes the graph using networkx and matplotlib.
        Reads the adjacency matrix to build the graph structure.
        Optionally highlights a path if provided.
        """
        G = nx.Graph()
        
        # Add nodes
        G.add_nodes_from(range(self.num_nodes))
        
        # Add edges from adjacency matrix
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):  # Only check upper triangle for undirected
                if self.graph[i][j] == 1:
                    G.add_edge(i, j)
        
        # Draw the graph
        plt.figure(figsize=(10, 8))
        # Use seed for consistent layout if needed, or just spring_layout
        pos = nx.spring_layout(G, seed=42)  
        
        # Map indices to A, B, C... labels for display
        labels = {i: chr(65 + i) for i in range(self.num_nodes)}
        
        # Default node and edge colors
        node_colors = ['lightblue'] * self.num_nodes
        edge_colors = ['gray'] * len(G.edges())
        edge_width = [1.0] * len(G.edges())

        # Highlight path if provided
        if path:
            path_edges = list(zip(path, path[1:]))
            path_edges_set = set(tuple(sorted(e)) for e in path_edges)
            
            # Highlight nodes in path
            for node in path:
                node_colors[node] = 'orange'
            node_colors[path[0]] = 'green'  # Start node
            node_colors[path[-1]] = 'red'   # End node
            
            # Highlight edges in path
            for i, edge in enumerate(G.edges()):
                if tuple(sorted(edge)) in path_edges_set:
                    edge_colors[i] = 'red'
                    edge_width[i] = 2.5
        
        nx.draw(G, pos, with_labels=True, labels=labels, 
                node_color=node_colors, node_size=1500, 
                font_size=12, font_weight='bold', 
                edge_color=edge_colors, width=edge_width)
        
        title = "Graph Visualization"
        if path:
            path_str = " -> ".join([labels[n] for n in path])
            title += f"\nShortest Path: {path_str}"
            
        plt.title(title)
        plt.axis('off')
        
        print("Displaying graph... (Close the window to continue)")
        plt.show()
