import globals
from DSM import DSM
import argparse
import json

def load_configuration(config_file, references_file):
    with open(config_file, 'r') as cf:
        config = json.load(cf)
    
    with open(references_file, 'r') as rf:
        references = [tuple(ref) for ref in json.load(rf)]
    
    globals.init(
        Total_pages=config['total_pages'], 
        Nodes=config['nodes'], 
        Pages_per_node=config['pages_per_node'], 
        Algorithm=config['algorithm'], 
        Replication=config['replication'], 
        References=references
    )

def main():
    parser = argparse.ArgumentParser(description='DSM Simulator')
    parser.add_argument('-c', '--config', type=str, required=True, help='Configuration file')
    parser.add_argument('-r', '--references', type=str, required=True, help='References file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output file')
    parser.add_argument('-a', '--algorithm', type=str, choices=['LRU', 'OPTIMAL', 'FIFO'], required=True, help='Page replacement algorithm')
    parser.add_argument('-d', '--replication', type=bool, required=True, help='Replication option')

    args = parser.parse_args()

    globals.init(Total_pages=16, Nodes=4, Pages_per_node=6, Algorithm=args.algorithm, Replication=args.replication, References=[])
    # Init DSM
    dsm = DSM()

if __name__ == "__main__":
    main()