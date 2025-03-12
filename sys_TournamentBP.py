# System:
#   CPU: X86TimingSimpleCPU 200MHz
#   MEM: DDR3_1600_8x8 8GB
#   BranchPredictor: TournamentBP(localPredictorSize=2048, localCtrBits=2)

import os
import m5
from m5.objects import *
import argparse
import subprocess

# Arguments for size of input
parser = argparse.ArgumentParser()
parser.add_argument('-b', '--benchmark', type=str, default="BFS")
parser.add_argument('-i', '--binary')
parser.add_argument('-c', '--config')
args = parser.parse_args()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BINARY = args.binary
DEFAULT_INFILE = f"{ROOT_DIR}/{args.benchmark}/{args.benchmark}-input"
DEFAULT_OUTFILE = f"{ROOT_DIR}/{args.benchmark}/{args.benchmark}-output"
PROCESS_CMD = [
    DEFAULT_BINARY, 
    # "-o", f"{DEFAULT_OUTFILE}",
    DEFAULT_INFILE
]


# System creation
system = System()
## gem5 needs to know the clock and voltage
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '200MHz'
system.clk_domain.voltage_domain = VoltageDomain() # defaults to 1V
## Create a crossbar so that we can connect main memory and the CPU (below)
system.membus = SystemXBar()
system.system_port = system.membus.cpu_side_ports
## Use timing mode for memory modelling
system.mem_mode = 'timing'

# CPU Setup
system.cpu = X86TimingSimpleCPU()
system.cpu.branchPred = TournamentBP(
    localPredictorSize=2048, 
    localHistoryTableSize=2048,
    globalPredictorSize=args.config,
    localCtrBits=2
)

system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
## This is needed when we use x86 CPUs
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
# Memory setup
system.mem_ctrl = MemCtrl()
system.mem_ctrl.port = system.membus.mem_side_ports
## A memory controller interfaces with main memory; create it here
system.mem_ctrl.dram = DDR3_1600_8x8()
## A DDR3_1600_8x8 has 8GB of memory, so setup an 8 GB address range
address_ranges = [AddrRange('8GB')]
system.mem_ranges = address_ranges
system.mem_ctrl.dram.range = address_ranges[0]

# Process setup
process = Process()
binary = DEFAULT_BINARY
process.cmd = PROCESS_CMD

## The necessary gem5 calls to initialize the workload and its threads
system.workload = SEWorkload.init_compatible(binary)
system.cpu.workload = process
system.cpu.createThreads()
# Start the simulation
root = Root(full_system=False, system=system) # must assign a root
m5.instantiate() # must be called before m5.simulate
m5.simulate()

print(f'Finished {args.benchmark} Benchmark, with TournamentBP\n')
print("================================")
