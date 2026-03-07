from collections import deque

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

    def bfs(self, start_node):
        if not (0 <= start_node < self.num_nodes):
            print(f"Error: Start node {start_node} is out of bounds")
            return []

        visited = set()
        queue = deque([start_node])
        visited.add(start_node)
        traversal_order = []

        while queue:
            vertex = queue.popleft()
            traversal_order.append(vertex)

            # Check neighbors in adjacency matrix
            for neighbor in range(self.num_nodes):
                if self.graph[vertex][neighbor] == 1:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
        
        return traversal_order

def main():
    print("Starting Graph & BFS Algorithm Demo (Adjacency Matrix)...")
    
    num_nodes = 6
    g = LimitedGraph(num_nodes)
    
    # Map nodes to names for display
    node_names = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F'}
    
    # Adding edges: A-B, A-C, B-D, B-E, C-F
    # 0-1, 0-2, 1-3, 1-4, 2-5
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(1, 4)
    g.add_edge(2, 5)
    
    print("\nAdjacency Matrix:")
    for row in g.graph:
        print(row)

    start_node = 0
    print(f"\nStarting BFS from node {start_node} ({node_names[start_node]})...")
    result = g.bfs(start_node)
    
    result_names = [node_names[n] for n in result]
    print("BFS Traversal Order:", " -> ".join(result_names))

if __name__ == "__main__":
    main()
