# main script

import os
import subprocess
import argparse

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

benchmarks = ["BFS", "SORT", "LRS", "KNN"]
infiles = {
    "BFS": f"{ROOT_DIR}/BFS/bfs-input",
    "SORT": f"{ROOT_DIR}/SORT/sort-input",
    "LRS": f"{ROOT_DIR}/LRS/lrs-input",
    "KNN": f"{ROOT_DIR}/KNN/knn-input"
}
outfiles = {
    "BFS": f"{ROOT_DIR}/BFS/bfs-output",
    "SORT": f"{ROOT_DIR}/SORT/sort-output",
    "LRS": f"{ROOT_DIR}/LRS/lrs-output",
    "KNN": f"{ROOT_DIR}/KNN/knn-output"
}
binaries = {
    "BFS": "/u/csc368h/winter/pub/workloads/pbbsbench/benchmarks/breadthFirstSearch/serialBFS/BFS",
    "SORT": "/u/csc368h/winter/pub/workloads/pbbsbench/benchmarks/comparisonSort/sampleSort/sort",
    "LRS": "/u/csc368h/winter/pub/workloads/pbbsbench/benchmarks/longestRepeatedSubstring/doubling/lrs",
    "KNN": "/u/csc368h/winter/pub/workloads/pbbsbench/benchmarks/nearestNeighbors/octTree/neighbors"
}

# select benchmark
parser = argparse.ArgumentParser(usage='[-b <benchmark>]')
parser.add_argument('-b', '--benchmark', type=str, 
                    default="BFS", choices=benchmarks)
args = parser.parse_args()


# generate input files
input_cmd = [
    "python3",
    f"{ROOT_DIR}/input.py", 
    "-b", args.benchmark
]
subprocess.run(input_cmd)


# Gem5 simulator 
configs = ["256", "512", "1024", "2048", "4096"]
# configs = ["1024", "2048", "4096", "8192", "16384"]
# gem5_binary = "/u/csc368h/winter/pub/bin/gem5.opt"
gem5_binary = "/u/csc368h/winter/pub/bin/gem5-24.1.0.1.opt"

# Option 1: single config
# outdir = f"{ROOT_DIR}/{args.benchmark}/LocalBP/m5out-{args.benchmark}"
# gem5_cmd = [
#     gem5_binary, 
#     f"--outdir={outdir}", 
#     f"{ROOT_DIR}/sys_LocalBP.py",
#     "-b", f"{args.benchmark}",
#     "-i", f"{binaries[args.benchmark]}"
# ]
# print(f"Running LocalBP on {args.benchmark}...")
# print("================================\n")
# subprocess.run(gem5_cmd)

# Option 2: multiple configs
for c in configs:
    outdir = f"{ROOT_DIR}/{args.benchmark}/globalPredictorSize/m5out-{args.benchmark}-{c}"
    gem5_cmd = [
        gem5_binary, 
        f"--outdir={outdir}", 
        f"{ROOT_DIR}/sys_TournamentBP.py",
        "-b", f"{args.benchmark}",
        "-i", f"{binaries[args.benchmark]}",
        "-c", c
    ]
    # Run Benchmark Script
    print(f"Running {c} on {args.benchmark}...")
    print("================================\n")
    subprocess.run(gem5_cmd)