from collections import deque

class BreadthFirstSearch:
    def __init__(self, graph):
        self.graph = graph

    def traverse(self, start_node):
        if not (0 <= start_node < self.graph.num_nodes):
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
            for neighbor in range(self.graph.num_nodes):
                if self.graph.graph[vertex][neighbor] == 1:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
        
        return traversal_order

    def find_shortest_path(self, start_node, end_node):
        if not (0 <= start_node < self.graph.num_nodes):
            print(f"Error: Start node {start_node} is out of bounds")
            return None
        if not (0 <= end_node < self.graph.num_nodes):
            print(f"Error: End node {end_node} is out of bounds")
            return None

        # Queue stores (current_node, path_to_node)
        queue = deque([(start_node, [start_node])])
        visited = {start_node}

        while queue:
            current, path = queue.popleft()

            if current == end_node:
                return path

            # Check neighbors in adjacency matrix
            for neighbor in range(self.graph.num_nodes):
                if self.graph.graph[current][neighbor] == 1:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        new_path = list(path)
                        new_path.append(neighbor)
                        queue.append((neighbor, new_path))
        
        return None  # No path found
