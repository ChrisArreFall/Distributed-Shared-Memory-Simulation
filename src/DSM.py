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
        for index, ref in enumerate(globals.references):
            globals.current_time += 1
            globals.current_reference_index = index
            cpu_id, page_id, mode = ref
            if page_id not in self.pages:
                self.pages.append(page_id)
                page = Page(page_id, mode, origin_cpu=cpu_id)
                globals.mmu.store_page(page)
            print(f"++++ Processing reference {index + 1}: CPU={cpu_id}, Page={page_id}, Mode={mode}")
            logging.info(f"++++ Processing reference {index + 1}: CPU={cpu_id}, Page={page_id}, Mode={mode}")
            print(f"Using {globals.algorithm} algorithm.")
            logging.info(f"Using {globals.algorithm} algorithm.")
            globals.cpus[cpu_id].load(page_id, mode)

            if (index + 1) % interval == 0:
                print(f"--------------------STATUS AFTER {index + 1} REFERENCES--------------------")
                self.print_status()
                self.report_stats(index + 1)
            else:
                self.print_status()
                
        logging.info("------- END -------")
        print("------- END -------")

    def print_status(self):
        globals.mmu.print_status()
        for cpu in globals.cpus:
            cpu.print_status()
            cpu.print_pages()

    def report_stats(self, total_references=None):
        total_page_faults = sum(cpu.stats['page_faults'] for cpu in globals.cpus)
        total_hits = sum(cpu.stats['hits'] for cpu in globals.cpus)
        total_invalidations = sum(cpu.stats['invalidations'] for cpu in globals.cpus)
        if total_references is None:
            total_references = len(globals.references)

        logging.info("------- STATISTICS -------")
        print("------- STATISTICS -------")
        for cpu in globals.cpus:
            stats = cpu.stats
            logging.info(f"CPU {cpu.id} - Page Faults: {stats['page_faults']} ({stats['page_faults'] / total_references:.2%}), Hits: {stats['hits']} ({stats['hits'] / total_references:.2%}), Invalidations: {stats['invalidations']} ({stats['invalidations'] / total_references:.2%})")
            print(f"CPU {cpu.id} - Page Faults: {stats['page_faults']} ({stats['page_faults'] / total_references:.2%}), Hits: {stats['hits']} ({stats['hits'] / total_references:.2%}), Invalidations: {stats['invalidations']} ({stats['invalidations'] / total_references:.2%})")
        
        logging.info(f"Total Page Faults: {total_page_faults}")
        logging.info(f"Total Hits: {total_hits}")
        logging.info(f"Total Invalidations: {total_invalidations}")
        print(f"Total Page Faults: {total_page_faults}")
        print(f"Total Hits: {total_hits}")
        print(f"Total Invalidations: {total_invalidations}")
