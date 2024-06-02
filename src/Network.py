import globals
import logging

class Network:
    def request_page(self, requesting_cpu, page_id, mode):
        for cpu in globals.cpus:
            if cpu.id != requesting_cpu:
                if cpu.cache.has_page_frame(page_id):
                    # If we have replication enabled and we are only reading
                    if globals.replication:
                        # If we are copying it read only
                        print(f"mode is {mode}")
                        logging.info(f"mode is {mode}")
                        if mode == 'r':
                            # We copy instead of removing it from the Cache
                            print("Mode is read only, copying page")
                            logging.info("Mode is read only, copying page")
                            page = cpu.copy(page_id)
                            page.mode = mode
                        # If we are writing, we need to invalidate every other CPUs
                        # copy and remove it from this one.
                        else:
                            print("Mode is write, removing page and invalidating rest.")
                            logging.info("Mode is write, removing page and invalidating rest.")
                            page = cpu.store(page_id)
                            page.origin_cpu = cpu.id
                            self.broadcast_invalidation(page)
                    else:
                        # Else We pop it (copy and remove)
                        page = cpu.store(page_id)
                    return page
        print(f"Page {page_id} not found in any CPU")
        return globals.mmu.send_page(page_id, mode)

    def broadcast_invalidation(self, page, requesting_cpu=False):
        for cpu in globals.cpus:
            if cpu.id != requesting_cpu:
                cpu.invalidate_page(page)

