import globals
from DSM import DSM
import argparse
import json
import logging
import sys

def load_configuration(config_file, references_file, algorithm, replication):
    with open(config_file, 'r') as cf:
        config = json.load(cf)
    
    with open(references_file, 'r') as rf:
        references = [tuple(ref) for ref in json.load(rf)]
    
    globals.init(
        Total_pages=config['total_pages'], 
        num_CPUs=config['cpus'], 
        Pages_per_cpu=config['pages_per_cpu'], 
        Algorithm=algorithm or config['algorithm'], 
        Replication=replication if replication is not False else config['replication'], 
        References=references
    )

def main():
    parser = argparse.ArgumentParser(description='DSM Simulator')
    parser.add_argument('-c', '--config', type=str, required=False, help='Configuration file')
    parser.add_argument('-r', '--references', type=str, required=False, help='References file')
    parser.add_argument('-o', '--output', type=str, required=False, help='Output file')
    parser.add_argument('-a', '--algorithm', type=str, choices=['LRU', 'OPTIMAL', 'FIFO'], required=False, help='Page replacement algorithm')
    parser.add_argument('-d', '--replication', action='store_true', required=False, help='Replication option')
    parser.add_argument('-i', '--interval', type=str, default=1, help='Reporting interval')
    parser.add_argument('-g', '--gui', action='store_true', help='Run with GUI')

    args = parser.parse_args()
    
    if args.gui:
        import GUI
        GUI.main()
    else:
        if not (args.config and args.references and args.output):
            parser.error("--config, --references, and --output are required when not using --gui")

        # Load configuration and references
        load_configuration(args.config, args.references, args.algorithm, args.replication)
        
        # Initialize DSM
        dsm = DSM()
        interval = 1
        if args.interval == 'N':
            interval = len(globals.references)
        else:
            interval = int(args.interval)
        dsm.simulate(interval)

        # Redirect output to the specified file
        with open(args.output, 'w') as out_file:
            for cpu in globals.cpus:
                stats = cpu.stats
                out_file.write(f"CPU {cpu.id}: Page Faults={stats['page_faults']}, Hits={stats['hits']}, Invalidations={stats['invalidations']}\n")

if __name__ == "__main__":
    main()
