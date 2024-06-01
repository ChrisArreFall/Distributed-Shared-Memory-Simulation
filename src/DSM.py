import globals
from VirtualMemory import VirtualMemory


class DSM:
    def __init__(self):
        self.virtual_memory = VirtualMemory()
    
    def simulate(self):
        for index, ref in enumerate(globals.references):
            cpu_id, page, mode = ref
            print(f"Processing reference: CPU={cpu_id}, Page={page}, Mode={mode}")
            self.virtual_memory.handle_reference(cpu_id, page, index)
        self.report_stats()
    
    def report_stats(self):
        self.virtual_memory.report_stats()
    
    
