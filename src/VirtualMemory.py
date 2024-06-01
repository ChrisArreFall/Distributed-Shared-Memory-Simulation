import globals
from CPU import CPU
import logging

class VirtualMemory:
    def __init__(self):
        self.cpus = [CPU(cpu_id, globals.pages_per_cpu) for cpu_id in range(globals.cpus)]
        logging.basicConfig(filename='dsm.log', level=logging.INFO)
    
    def handle_reference(self, cpu_id, page, index):
        cpu = self.cpus[cpu_id]
        if cpu.has_page(page):
            cpu.page_hit()
            print(f"Page hit: CPU={cpu_id}, Page={page}")
            if globals.algorithm == 'LRU':
                cpu.page_table_lru.move_to_end(page)
        else:
            cpu.page_fault()
            print(f"Page fault: CPU={cpu_id}, Page={page}")
            if globals.algorithm == 'LRU':
                if len(cpu.page_table_lru) >= globals.pages_per_cpu:
                    self.replace_page(cpu, page, index)
                else:
                    cpu.add_page(page)
                    print(f"Page added: CPU={cpu_id}, Page={page}")
            else:  # FIFO or other algorithms
                if len(cpu.page_table_fifo) >= globals.pages_per_cpu:
                    self.replace_page(cpu, page, index)
                else:
                    cpu.add_page(page)
                    print(f"Page added: CPU={cpu_id}, Page={page}")
    
    def replace_page(self, cpu, page, index):
        if globals.algorithm == 'LRU':
            self.lru_replace(cpu, page)
        elif globals.algorithm == 'OPTIMAL':
            self.optimal_replace(cpu, page, index)
        elif globals.algorithm == 'FIFO':
            self.fifo_replace(cpu, page)
    
    def lru_replace(self, cpu, page):
        # Remove the least recently used page (the first page in the ordered dictionary)
        removed_page = next(iter(cpu.page_table_lru))
        cpu.page_table_lru.pop(removed_page)
        cpu.add_page(page)
        print(f"LRU Replace: CPU={cpu.cpu_id}, Removed Page={removed_page}, Added Page={page}")
        # Log repace
        self.log_event(f"Page replaced using LRU: CPU {cpu.cpu_id}, Page {page}")

    def fifo_replace(self, cpu, page):
        # Remove the oldest page (the first page in the deque)
        removed_page = cpu.page_table_fifo.popleft()
        cpu.add_page(page)
        print(f"FIFO Replace: CPU={cpu.cpu_id}, Removed Page={removed_page}, Added Page={page}")
        # Log repace
        self.log_event(f"Page replaced using FIFO: CPU {cpu.cpu_id}, Page {page}")
    
    def optimal_replace(self, cpu, page, index):
        future_references = globals.references[index + 1:]
        page_usages = {p: float('inf') for p in cpu.page_table_fifo}

        for future_index, ref in enumerate(future_references):
            future_cpu, future_page, future_mode = ref
            if future_cpu == cpu.cpu_id and future_page in page_usages:
                if page_usages[future_page] == float('inf'):
                    page_usages[future_page] = future_index

        #farthest_use = max(page_usages.values())
        page_to_replace = max(page_usages, key=page_usages.get)

        cpu.page_table_fifo.remove(page_to_replace)
        cpu.add_page(page)
        print(f"Optimal Replace: CPU={cpu.cpu_id}, Removed Page={page_to_replace}, Added Page={page}")
        # Log repace
        self.log_event(f"Page replaced using OPTIMAL: CPU {cpu.cpu_id}, Page {page}")
    
    def report_stats(self):
        for cpu in self.cpus:
            stats = cpu.stats
            print(f"CPU {cpu.cpu_id}: Page Faults={stats['page_faults']}, Hits={stats['hits']}, Invalidations={stats['invalidations']}")

    def log_event(self, event):
        logging.info(event)