# T2: Algorithm Study - Graph & BFS

This project focuses on the study and implementation of the **Graph** data structure and the **Breadth-First Search (BFS)** algorithm.

## Key Concepts

### 1. Data Structure: Graph (Adjacency Matrix Implementation)
A non-linear data structure consisting of nodes (vertices) and edges.
In this implementation (`LimitedGraph`), we use an **Adjacency Matrix** to represent the graph:
- A 2D array where `matrix[i][j] = 1` indicates an edge between node `i` and node `j`.
- Suitable for dense graphs where the number of edges is close to the square of the number of nodes.

### 2. Algorithm: Breadth-First Search (BFS)
A graph traversal algorithm that explores all neighbor nodes at the present depth prior to moving on to the nodes at the next depth level. It is commonly used for finding the shortest path in unweighted graphs.

## Structure

- `main.py`: Implementation of `LimitedGraph` (using Adjacency Matrix) and BFS traversal.

## Usage

Run the application:

```bash
python3 T2-Algorithm/main.py
```
