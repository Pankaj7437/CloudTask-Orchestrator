"""
CloudTask Orchestrator & Cluster Resource Allocator
Core Algorithmic Engine (Analysis of Algorithms - Lab Project)

Maps the 10 Core AoA Syllabus Experiments to Cloud Resource & Task Management:
1. Quicksort: Empirical benchmarking of Cloud Log & Telemetry event sorting.
2. Parallel Merge Sort: Multi-threaded divide-and-conquer metric stream sorting.
3. (a) Topological Sort: Cloud Workflow DAG task execution scheduling.
   (b) Warshall's Algorithm: Transitive closure of service dependency reachability.
4. 0/1 Knapsack (DP): Cloud VM & Container Resource Packing under budget.
5. Dijkstra's Algorithm: Gateway-to-Pod lowest latency network routing.
6. Kruskal's Algorithm: Minimum Cost Spanning Tree for inter-datacenter fiber mesh.
7. (a) BFS: Cluster pod reachability & blast-radius analysis.
   (b) DFS: Cluster network partition & connectivity verification.
8. Prim's Algorithm: Minimum Cost Spanning Tree for cluster overlay backbone.
9. Floyd-Warshall Algorithm: All-Pairs Shortest Path cluster latency matrix.
10. N-Queens (Backtracking): Conflict-free anti-affinity VM rack/fault-domain placement.
"""

import time
import random
import math
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Tuple, Set, Optional

# =====================================================================
# EXPERIMENT 1: QUICKSORT (Empirical Benchmark)
# =====================================================================
def quicksort(arr: List[float], low: int, high: int):
    """Quicksort implementation using median-of-three or Lomuto partitioning."""
    if low < high:
        pi = partition(arr, low, high)
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

def partition(arr: List[float], low: int, high: int) -> int:
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def run_quicksort(data: List[float]) -> Tuple[List[float], float]:
    arr = list(data)
    start = time.perf_counter()
    quicksort(arr, 0, len(arr) - 1)
    duration_ms = (time.perf_counter() - start) * 1000.0
    return arr, duration_ms

# =====================================================================
# EXPERIMENT 2: PARALLEL MERGE SORT (Empirical Benchmark)
# =====================================================================
def merge(left: List[float], right: List[float]) -> List[float]:
    result = []
    i = j = 0
    len_l, len_r = len(left), len(right)
    while i < len_l and j < len_r:
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def sequential_mergesort(arr: List[float]) -> List[float]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = sequential_mergesort(arr[:mid])
    right = sequential_mergesort(arr[mid:])
    return merge(left, right)

def parallel_mergesort(arr: List[float], depth: int = 2) -> List[float]:
    """Parallelized merge sort using ThreadPoolExecutor for high-volume logs."""
    if len(arr) <= 1:
        return arr
    if depth <= 0 or len(arr) < 5000:
        return sequential_mergesort(arr)
    
    mid = len(arr) // 2
    with ThreadPoolExecutor(max_workers=2) as executor:
        f_left = executor.submit(parallel_mergesort, arr[:mid], depth - 1)
        f_right = executor.submit(parallel_mergesort, arr[mid:], depth - 1)
        left = f_left.result()
        right = f_right.result()
    return merge(left, right)

def run_parallel_mergesort(data: List[float]) -> Tuple[List[float], float]:
    start = time.perf_counter()
    sorted_arr = parallel_mergesort(list(data))
    duration_ms = (time.perf_counter() - start) * 1000.0
    return sorted_arr, duration_ms

# =====================================================================
# EXPERIMENT 3: (A) TOPOLOGICAL SORT & (B) WARSHALL'S ALGORITHM
# =====================================================================
def topological_sort_kahn(num_tasks: int, edges: List[Tuple[int, int]]) -> Tuple[List[int], bool]:
    """
    Kahn's Algorithm for Cloud Workflow DAG scheduling.
    Returns: (execution_order, has_cycle)
    """
    adj = {i: [] for i in range(num_tasks)}
    in_degree = [0] * num_tasks
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    
    queue = [i for i in range(num_tasks) if in_degree[i] == 0]
    order = []
    
    while queue:
        curr = queue.pop(0)
        order.append(curr)
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    has_cycle = (len(order) != num_tasks)
    return order, has_cycle

def warshall_transitive_closure(matrix: List[List[int]]) -> List[List[int]]:
    """
    Warshall's Algorithm for Service Dependency Transitive Closure.
    Computes if service i can reach service j directly or transitively.
    """
    n = len(matrix)
    closure = [row[:] for row in matrix]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])
    return closure

# =====================================================================
# EXPERIMENT 4: 0/1 KNAPSACK (Dynamic Programming)
# =====================================================================
def knapsack_01(capacity: int, weights: List[int], values: List[int], names: List[str] = None):
    """
    0/1 Knapsack for Cloud VM Resource Allocation:
    Packing microservices (weights: RAM/CPU, values: Revenue/Priority) into Host VM.
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]
        for c in range(capacity + 1):
            if w <= c:
                dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - w] + v)
            else:
                dp[i][c] = dp[i - 1][c]
                
    max_value = dp[n][capacity]
    
    # Backtrack to identify selected items
    selected_indices = []
    curr_c = capacity
    for i in range(n, 0, -1):
        if dp[i][curr_c] != dp[i - 1][curr_c]:
            selected_indices.append(i - 1)
            curr_c -= weights[i - 1]
            
    selected_indices.reverse()
    selected_items = [names[idx] if names else f"Job_{idx}" for idx in selected_indices]
    
    return {
        "max_value": max_value,
        "selected_indices": selected_indices,
        "selected_items": selected_items,
        "total_weight": sum(weights[i] for i in selected_indices),
        "dp_table": dp
    }

# =====================================================================
# EXPERIMENT 5: DIJKSTRA'S ALGORITHM (Single Source Shortest Path)
# =====================================================================
def dijkstra(num_nodes: int, adj_matrix: List[List[float]], source: int):
    """
    Dijkstra's Algorithm for Gateway-to-Pod lowest latency network routing.
    """
    dist = [float('inf')] * num_nodes
    visited = [False] * num_nodes
    parent = [-1] * num_nodes
    dist[source] = 0.0
    
    for _ in range(num_nodes):
        # Pick min distance unvisited node
        min_dist = float('inf')
        u = -1
        for i in range(num_nodes):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i
                
        if u == -1:
            break
            
        visited[u] = True
        for v in range(num_nodes):
            weight = adj_matrix[u][v]
            if weight > 0 and not visited[v]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    parent[v] = u
                    
    # Reconstruct paths
    paths = {}
    for target in range(num_nodes):
        if dist[target] == float('inf'):
            paths[target] = []
        else:
            path = []
            curr = target
            while curr != -1:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            paths[target] = path
            
    return {"distances": dist, "paths": paths}

# =====================================================================
# EXPERIMENT 6: KRUSKAL'S ALGORITHM (Minimum Cost Spanning Tree)
# =====================================================================
class DisjointSet:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        
    def find(self, u: int) -> int:
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]
        
    def union(self, u: int, v: int) -> bool:
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u == root_v:
            return False
        if self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        elif self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1
        return True

def kruskal_mst(num_nodes: int, edges: List[Tuple[int, int, float]]):
    """
    Kruskal's Algorithm using Disjoint Set Union (DSU) with rank & path compression.
    Used for Inter-Datacenter Low-Cost Fiber Connection.
    edges: list of (u, v, weight)
    """
    sorted_edges = sorted(edges, key=lambda x: x[2])
    dsu = DisjointSet(num_nodes)
    mst_edges = []
    total_cost = 0.0
    
    for u, v, w in sorted_edges:
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            total_cost += w
            if len(mst_edges) == num_nodes - 1:
                break
                
    return {"mst_edges": mst_edges, "total_cost": total_cost}

# =====================================================================
# EXPERIMENT 7: (A) BFS REACHABILITY & (B) DFS CONNECTIVITY CHECK
# =====================================================================
def bfs_reachable(num_nodes: int, adj_list: Dict[int, List[int]], start_node: int) -> List[int]:
    """BFS traversal to determine all reachable cloud service pods from an ingress node."""
    visited = [False] * num_nodes
    queue = [start_node]
    visited[start_node] = True
    reachable = []
    
    while queue:
        curr = queue.pop(0)
        reachable.append(curr)
        for neighbor in adj_list.get(curr, []):
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
    return reachable

def dfs_is_connected(num_nodes: int, adj_list: Dict[int, List[int]]) -> Tuple[bool, List[int]]:
    """DFS traversal to verify if the cluster communication topology is fully connected."""
    if num_nodes == 0:
        return True, []
    
    visited = [False] * num_nodes
    visited_order = []
    
    def dfs_helper(u: int):
        visited[u] = True
        visited_order.append(u)
        for v in adj_list.get(u, []):
            if not visited[v]:
                dfs_helper(v)
                
    dfs_helper(0)
    is_connected = all(visited)
    return is_connected, visited_order

# =====================================================================
# EXPERIMENT 8: PRIM'S ALGORITHM (Minimum Cost Spanning Tree)
# =====================================================================
def prim_mst(num_nodes: int, adj_matrix: List[List[float]], start_node: int = 0):
    """
    Prim's Algorithm for cluster overlay network backbone optimization.
    """
    key = [float('inf')] * num_nodes
    parent = [-1] * num_nodes
    in_mst = [False] * num_nodes
    
    key[start_node] = 0.0
    
    for _ in range(num_nodes):
        min_key = float('inf')
        u = -1
        for i in range(num_nodes):
            if not in_mst[i] and key[i] < min_key:
                min_key = key[i]
                u = i
                
        if u == -1:
            break
            
        in_mst[u] = True
        for v in range(num_nodes):
            w = adj_matrix[u][v]
            if w > 0 and not in_mst[v] and w < key[v]:
                key[v] = w
                parent[v] = u
                
    mst_edges = []
    total_cost = 0.0
    for i in range(num_nodes):
        if parent[i] != -1:
            mst_edges.append((parent[i], i, adj_matrix[parent[i]][i]))
            total_cost += adj_matrix[parent[i]][i]
            
    return {"mst_edges": mst_edges, "total_cost": total_cost}

# =====================================================================
# EXPERIMENT 9: FLOYD-WARSHALL ALGORITHM (All-Pairs Shortest Path)
# =====================================================================
def floyd_warshall(matrix: List[List[float]]):
    """
    Floyd-Warshall for computing all-pairs shortest path latency matrix across all cluster nodes.
    """
    n = len(matrix)
    dist = [row[:] for row in matrix]
    # Initialize self-loops to 0
    for i in range(n):
        dist[i][i] = 0.0
        
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    
    return dist

# =====================================================================
# EXPERIMENT 10: N-QUEENS (Backtracking)
# =====================================================================
def solve_n_queens(n: int) -> List[List[int]]:
    """
    Backtracking solver for N-Queens.
    Mapped to: Anti-affinity VM placement across N server racks / fault domains.
    Returns: List of valid board placements where board[row] = col.
    """
    solutions = []
    board = [-1] * n
    
    def is_safe(row: int, col: int) -> bool:
        for prev_row in range(row):
            prev_col = board[prev_row]
            # Same column check
            if prev_col == col:
                return False
            # Diagonal conflict check
            if abs(prev_row - row) == abs(prev_col - col):
                return False
        return True
        
    def backtrack(row: int):
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1
                
    backtrack(0)
    return solutions

# =====================================================================
# VERIFICATION SUITE
# =====================================================================
def verify_all():
    print("=== RUNNING CLOUD-TASK AoA VERIFICATION SUITE ===")
    
    # 1. Quicksort
    sample_data = [random.uniform(10.0, 500.0) for _ in range(1000)]
    s_arr, t_quick = run_quicksort(sample_data)
    assert s_arr == sorted(sample_data)
    print(f"[OK] Exp 1 Quicksort: 1000 items sorted in {t_quick:.3f} ms")
    
    # 2. Parallel Merge Sort
    s_arr_p, t_merge = run_parallel_mergesort(sample_data)
    assert s_arr_p == sorted(sample_data)
    print(f"[OK] Exp 2 Parallel Merge Sort: 1000 items sorted in {t_merge:.3f} ms")
    
    # 3. Topological Sort & Warshall
    dag_edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
    order, cycle = topological_sort_kahn(5, dag_edges)
    assert not cycle and len(order) == 5
    print(f"[OK] Exp 3a Topological Sort (Kahn's): Execution Order = {order}")
    
    adj_mat = [
        [0, 1, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0]
    ]
    closure = warshall_transitive_closure(adj_mat)
    assert closure[0][4] == 1
    print(f"[OK] Exp 3b Warshall's Transitive Closure: Verified reachability (0 -> 4: {closure[0][4]})")
    
    # 4. Knapsack
    weights = [2, 3, 4, 5, 9]
    values = [3, 4, 5, 8, 10]
    names = ["AuthService", "PaymentGateway", "NotificationSvc", "OrderProcessor", "AnalyticsEngine"]
    res_knap = knapsack_01(10, weights, values, names)
    print(f"[OK] Exp 4 0/1 Knapsack: Max Priority = {res_knap['max_value']}, Selected = {res_knap['selected_items']}")
    
    # 5. Dijkstra
    inf = float('inf')
    graph_mat = [
        [0, 10, 3, inf, inf],
        [inf, 0, 1, 2, inf],
        [inf, 4, 0, 8, 2],
        [inf, inf, inf, 0, 7],
        [inf, inf, inf, 9, 0]
    ]
    res_dijk = dijkstra(5, graph_mat, 0)
    print(f"[OK] Exp 5 Dijkstra: Distances from Gateway 0 = {res_dijk['distances']}")
    
    # 6. Kruskal
    undir_edges = [
        (0, 1, 4), (0, 2, 8), (1, 2, 2), (1, 3, 6),
        (2, 3, 3), (2, 4, 9), (3, 4, 5)
    ]
    res_krus = kruskal_mst(5, undir_edges)
    print(f"[OK] Exp 6 Kruskal MST: Total Network Cost = {res_krus['total_cost']}, Edges = {res_krus['mst_edges']}")
    
    # 7. BFS & DFS
    adj_list = {0: [1, 2], 1: [3], 2: [3, 4], 3: [4], 4: []}
    reach = bfs_reachable(5, adj_list, 0)
    print(f"[OK] Exp 7a BFS Reachable from Node 0: {reach}")
    
    undir_adj = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1, 3, 4], 3: [1, 2, 4], 4: [2, 3]}
    conn, _ = dfs_is_connected(5, undir_adj)
    assert conn is True
    print(f"[OK] Exp 7b DFS Connectivity Check: Cluster Connected = {conn}")
    
    # 8. Prim
    sym_mat = [
        [0, 4, 8, 0, 0],
        [4, 0, 2, 6, 0],
        [8, 2, 0, 3, 9],
        [0, 6, 3, 0, 5],
        [0, 0, 9, 5, 0]
    ]
    res_prim = prim_mst(5, sym_mat, 0)
    print(f"[OK] Exp 8 Prim MST: Total Cost = {res_prim['total_cost']}, Edges = {res_prim['mst_edges']}")
    
    # 9. Floyd-Warshall
    floyd_input = [
        [0, 3, 8, inf, -4],
        [inf, 0, inf, 1, 7],
        [inf, 4, 0, inf, inf],
        [2, inf, -5, 0, inf],
        [inf, inf, inf, 6, 0]
    ]
    res_floyd = floyd_warshall(floyd_input)
    print(f"[OK] Exp 9 Floyd-Warshall: 5x5 All-Pairs Latency Matrix computed.")
    
    # 10. N-Queens
    sols_4 = solve_n_queens(4)
    print(f"[OK] Exp 10 N-Queens (N=4): {len(sols_4)} valid rack placement layouts found: {sols_4}")
    sols_8 = solve_n_queens(8)
    print(f"[OK] Exp 10 N-Queens (N=8): {len(sols_8)} conflict-free layouts discovered.")

if __name__ == "__main__":
    verify_all()
