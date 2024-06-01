from collections import deque, OrderedDict
import globals

class CPU:
    def __init__(self, cpu_id, pages_per_cpu):
        self.cpu_id = cpu_id
        self.pages_per_cpu = pages_per_cpu
        self.page_table_fifo = deque()  # For FIFO
        self.page_table_lru = OrderedDict()  # For LRU
        self.stats = {'page_faults': 0, 'hits': 0, 'invalidations': 0}
    
    def add_page(self, page):
        if globals.algorithm == 'LRU':
            self.page_table_lru[page] = None
            self.page_table_lru.move_to_end(page)  # Update order for LRU
        else:
            self.page_table_fifo.append(page)
        self.print_status()
    
    def remove_page(self):
        if globals.algorithm == 'LRU':
            removed_page = next(iter(self.page_table_lru))
            del self.page_table_lru[removed_page]
        else:
            removed_page = self.page_table_fifo.popleft()
        self.print_status()
        return removed_page
    
    def has_page(self, page):
        if globals.algorithm == 'LRU':
            return page in self.page_table_lru
        else:
            return page in self.page_table_fifo
    
    def page_hit(self):
        self.stats['hits'] += 1
    
    def page_fault(self):
        self.stats['page_faults'] += 1
    
    def print_status(self):
        print(f"--------------------\nCPU {self.cpu_id}\n--------------------")
        if globals.algorithm == 'LRU':
            print(", ".join(map(str, self.page_table_lru.keys())))
        else:
            print(", ".join(map(str, self.page_table_fifo)))
        print("--------------------")