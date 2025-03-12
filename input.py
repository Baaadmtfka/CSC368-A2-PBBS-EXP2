import os
import subprocess
import argparse

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

benchmarks = ["BFS", "SORT", "LRS", "KNN"]

# Input and output file paths
infiles = {
    "BFS": f"{ROOT_DIR}/BFS/BFS-input",
    "SORT": f"{ROOT_DIR}/SORT/SORT-input",
    "LRS": f"{ROOT_DIR}/LRS/LRS-input",
    "KNN": f"{ROOT_DIR}/KNN/KNN-input"
}

# Input generation commands
input_cmds = {
    "BFS": [    
        "/u/csc368h/winter/pub/workloads/pbbsbench/testData/graphData/randLocalGraph", 
        "-j", 
        "-d", "3",  # unchanged 3D
        "-m", "500",  # number of edges
        "500",  # number of nodes
        infiles["BFS"]
    ],
    "SORT": [
        "/u/csc368h/winter/pub/workloads/pbbsbench/testData/sequenceData/randomSeq", 
        "-t", "double",  # data type
        "50",  # sequence size
        infiles["SORT"]
    ],
    "LRS": [
        "/u/csc368h/winter/pub/workloads/pbbsbench/testData/sequenceData/randomSeq",  # sequence data
        "-t", "int",  # data type
        "-r", "10",  # range [0,9]
        "20",  # sequence size
        infiles["LRS"]
    ],
    "KNN": [
        "/u/csc368h/winter/pub/workloads/pbbsbench/testData/geometryData/randPoints", 
        "-d", "3",  # dimensions
        "500",  # number of points
        infiles["KNN"]
    ]
}

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-b', '--benchmark', type=str, default="BFS", choices=benchmarks)
args = parser.parse_args()

# Generate Input File
benchmark_dir = os.path.join(ROOT_DIR, args.benchmark)
os.makedirs(benchmark_dir, exist_ok=True)

if not os.path.exists(infiles[args.benchmark]):
    print(f"Creating input for {args.benchmark}...\n================================")
    subprocess.run(input_cmds[args.benchmark], cwd=benchmark_dir, check=True)
else:
    print(f"Input file for {args.benchmark} already exists. Updating.\n================================")
    subprocess.run(input_cmds[args.benchmark], cwd=benchmark_dir, check=True)
