import globals

class Network:
    def __init__(self):
        pass

    def request_page(self, requesting_cpu, page_id, mode):
        # First the network instance is going to check if another CPU has it
        for i in range(globals.num_cpus):
            if i != requesting_cpu:
                # If a CPU has the page we need
                if globals.cpus[i].cache.has_page_frame(page_id):
                    # I tell the CPU to send them that page
                    page = globals.cpus[i].cache.remove_page_frame(page_id)
                    return page
        print(f"Page {page_id} not found in any CPU")
        return globals.mmu.send_page(page_id)

    def store_page(self, page):
        globals.mmu.store_page(page)

    def send_page(self, from_cpu, to_cpu, page):
        globals.cpus[to_cpu].receive_page(page)