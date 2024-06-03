import logging
from Network import Network
from MMU import MMU

def init(Total_pages, num_CPUs, Pages_per_cpu, Algorithm, Replication, References):
    global total_pages 
    global num_cpus 
    global pages_per_cpu 
    global algorithm 
    global replication 
    global references 
    global network_instance
    global cpus
    global mmu
    global current_time
    global current_reference_index
    global saved_state

    total_pages = Total_pages
    num_cpus = num_CPUs
    pages_per_cpu = Pages_per_cpu
    algorithm = Algorithm
    replication = Replication
    references = References
    network_instance = Network()
    cpus = []
    mmu = MMU()
    current_time = 0
    current_reference_index = 0
    saved_state = []

    # Initialize logging
    logging.basicConfig(filename='dsm.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Initialized DSM with configuration: Total_pages=%d, num_cpus=%d, pages_per_cpu=%d, algorithm=%s, replication=%s', total_pages, num_cpus, pages_per_cpu, algorithm, replication)

def PRINT_AND_LOG(text):
    print(text)
    logging.info(text)