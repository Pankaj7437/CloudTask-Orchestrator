"""
Empirical Benchmark Generator for Analysis of Algorithms
Generates empirical execution times for Quicksort and Parallel Merge Sort across varying n.
Outputs benchmark_results.json for both GUI visualization and the 40-page Technical Report.
"""

import time
import random
import json
from aoa_cloud_engine import run_quicksort, run_parallel_mergesort, sequential_mergesort

def run_empirical_benchmarks():
    # Array sizes as required by Experiment 1 & 2
    n_values = [500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]
    results = {
        "n_values": n_values,
        "quicksort_times_ms": [],
        "parallel_mergesort_times_ms": [],
        "sequential_mergesort_times_ms": [],
        "samples": {}
    }
    
    print("Running empirical benchmarks for Quicksort and Parallel Merge Sort...")
    for n in n_values:
        # Generate random telemetry log timestamps/metrics
        data = [random.uniform(1.0, 100000.0) for _ in range(n)]
        
        # Benchmark Quicksort (average of 3 runs for stability)
        q_times = []
        for _ in range(3):
            _, t = run_quicksort(data)
            q_times.append(t)
        avg_q = sum(q_times) / len(q_times)
        results["quicksort_times_ms"].append(round(avg_q, 4))
        
        # Benchmark Sequential Merge Sort
        s_times = []
        for _ in range(3):
            start = time.perf_counter()
            sequential_mergesort(list(data))
            s_times.append((time.perf_counter() - start) * 1000.0)
        avg_s = sum(s_times) / len(s_times)
        results["sequential_mergesort_times_ms"].append(round(avg_s, 4))
        
        # Benchmark Parallel Merge Sort
        p_times = []
        for _ in range(3):
            _, t = run_parallel_mergesort(data)
            p_times.append(t)
        avg_p = sum(p_times) / len(p_times)
        results["parallel_mergesort_times_ms"].append(round(avg_p, 4))
        
        print(f"n = {n:6d} | Quicksort: {avg_q:8.3f} ms | Seq Merge: {avg_s:8.3f} ms | Parallel Merge: {avg_p:8.3f} ms")

    output_path = "benchmark_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[OK] Benchmark data successfully saved to {output_path}")

if __name__ == "__main__":
    run_empirical_benchmarks()
