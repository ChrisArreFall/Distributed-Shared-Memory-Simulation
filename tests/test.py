import os
import subprocess

configurations = ['config1.json']
references = ['references2.json']
algorithms = ['LRU', 'FIFO', 'OPTIMAL']

results_dir = 'results'
os.makedirs(results_dir, exist_ok=True)

def run_test(config_file, references_file, algorithm):
    output_file = f"{results_dir}/output_{config_file.split('.')[0]}_{references_file.split('.')[0]}_{algorithm}.txt"
    cmd = [
        'python', '../src/main.py', 
        '-c', config_file, 
        '-r', references_file, 
        '-o', 'test_results.txt', 
        '-a', algorithm, 
        '-i', 'N'
    ]
    with open(output_file, 'w') as f:
        print(cmd)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end='')  # Print to console
            f.write(line)  # Write to file
        process.wait()  # Wait for the process to complete

for config in configurations:
    for ref in references:
        for algo in algorithms:
            print(f"Running test with {config}, {ref}, {algo}")
            run_test(config, ref, algo)
