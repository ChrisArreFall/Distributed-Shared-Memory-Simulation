import globals
from DSM import DSM
import argparse
import json

def load_configuration(config_file, references_file, algorithm, replication):
    with open(config_file, 'r') as cf:
        config = json.load(cf)
    
    with open(references_file, 'r') as rf:
        references = [tuple(ref) for ref in json.load(rf)]
    
    # Override config file settings with command-line arguments
    globals.init(
        Total_pages=config['total_pages'], 
        CPUs=config['cpus'], 
        Pages_per_cpu=config['pages_per_cpu'], 
        Algorithm=algorithm or config['algorithm'], 
        Replication=replication if replication is not None else config['replication'], 
        References=references
    )

def main():
    parser = argparse.ArgumentParser(description='DSM Simulator')
    parser.add_argument('-c', '--config', type=str, required=True, help='Configuration file')
    parser.add_argument('-r', '--references', type=str, required=True, help='References file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output file')
    parser.add_argument('-a', '--algorithm', type=str, choices=['LRU', 'OPTIMAL', 'FIFO'], required=False, help='Page replacement algorithm')
    parser.add_argument('-d', '--replication', type=bool, required=False, help='Replication option')

    args = parser.parse_args()

    # Load configuration and references
    load_configuration(args.config, args.references, args.algorithm, args.replication)
    
    # Initialize DSM
    dsm = DSM()
    dsm.simulate()

    # Redirect output to the specified file
    with open(args.output, 'w') as out_file:
        for cpu in dsm.virtual_memory.cpus:
            stats = cpu.stats
            out_file.write(f"CPU {cpu.cpu_id}: Page Faults={stats['page_faults']}, Hits={stats['hits']}, Invalidations={stats['invalidations']}\n")
            cpu.print_status()

if __name__ == "__main__":
    main()
