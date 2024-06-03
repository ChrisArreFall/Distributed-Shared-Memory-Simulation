import globals
from MMU import MMU
from CPU import CPU
from Page import Page
import logging

class DSM:
    def __init__(self):
        globals.cpus = [CPU(i) for i in range(globals.num_cpus)]
        self.pages = []

    def simulate(self, interval):
        if globals.replication:
            globals.PRINT_AND_LOG("Replication is enabled")
        else:
            globals.PRINT_AND_LOG("Replication is disabled")
        for index, ref in enumerate(globals.references):
            globals.PRINT_AND_LOG(f"++++++++++++Processing reference {index + 1}++++++++++++")
            
            globals.current_time += 1
            globals.current_reference_index = index
            cpu_id, page_id, mode = ref
            globals.PRINT_AND_LOG(f"Reference {index + 1}: CPU={cpu_id}, Page={page_id}, Mode={mode}")
            
            globals.PRINT_AND_LOG(f"Using {globals.algorithm} algorithm.")

            if page_id not in self.pages:
                globals.PRINT_AND_LOG(f"First time processing page {page_id}")
                self.pages.append(page_id)
                page = Page(page_id, mode, origin_cpu=cpu_id)
                globals.mmu.store_page(page)
                globals.mmu.print_status()
            
            globals.cpus[cpu_id].load(page_id, mode)
            if (index + 1) % interval == 0:
                globals.PRINT_AND_LOG(f"--------------------STATUS AFTER {index + 1} REFERENCES--------------------")
                self.print_status()
                self.report_stats(index + 1)
            else:
                self.print_status()
            self.save_state()
            print(globals.saved_state)
            globals.PRINT_AND_LOG("++++++++++++++++++++++++++++++++++++++++++++++")
                
        globals.PRINT_AND_LOG("------- END -------")

    def print_status(self):
        globals.mmu.print_status()
        for cpu in globals.cpus:
            cpu.print_status()
            cpu.print_pages()

    def save_state(self):
        saved_state = []
        pages = []
        for page in globals.mmu.RAM:
                pages.append(page.id)
        saved_state.append(pages)
        for cpu in globals.cpus:
            pages = []
            for frame in cpu.cache.frames:
                pages.append(frame.id)
            saved_state.append(pages)
        globals.saved_state.append(saved_state)

    def report_stats(self, total_references=None):
        total_page_faults = sum(cpu.stats['page_faults'] for cpu in globals.cpus)
        total_hits = sum(cpu.stats['hits'] for cpu in globals.cpus)
        total_invalidations = sum(cpu.stats['invalidations'] for cpu in globals.cpus)
        if total_references is None:
            total_references = len(globals.references)

        globals.PRINT_AND_LOG("------- STATISTICS -------")
        for cpu in globals.cpus:
            stats = cpu.stats
            globals.PRINT_AND_LOG(f"CPU {cpu.id} - Page Faults: {stats['page_faults']} ({stats['page_faults'] / total_references:.2%}), Hits: {stats['hits']} ({stats['hits'] / total_references:.2%}), Invalidations: {stats['invalidations']} ({stats['invalidations'] / total_references:.2%})")
        
        globals.PRINT_AND_LOG(f"Total Page Faults: {total_page_faults}")
        globals.PRINT_AND_LOG(f"Total Hits: {total_hits}")
        globals.PRINT_AND_LOG(f"Total Invalidations: {total_invalidations}")
