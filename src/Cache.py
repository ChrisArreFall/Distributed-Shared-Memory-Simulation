import globals
import logging

class Cache:
    def __init__(self, cpu_id):
        self.frames = []
        self.cpu_id = cpu_id

    def has_page_frame(self, page_id, mode=False):
        for page in self.frames:
            if page.id == page_id:
                # If we have enabled replication but the status is invalidated
                if globals.replication and not page.status:
                    # We return False
                    globals.PRINT_AND_LOG(f"Page {page_id} found in cache but invalidated in CPU {self.cpu_id}.")
                    return False
                globals.PRINT_AND_LOG(f"Page {page_id} found in cache of CPU {self.cpu_id}")
                if mode != False:
                    if globals.replication and mode == 'w':
                        globals.network_instance.broadcast_invalidation(page, self.cpu_id)
                    page.status = True
                    globals.PRINT_AND_LOG(f"Changing mode from {page.mode} to {mode} in page {page.id} for CPU {self.cpu_id}.")
                    page.mode = mode
                return True
        return False

    def load_page_frame(self, page):
        globals.PRINT_AND_LOG(f"Loading page {page.id} to CPU {self.cpu_id}.")
        if len(self.frames) >= globals.pages_per_cpu:
            return False
        page.status = True
        page.origin_cpu = self.cpu_id
        page.last_access_time = globals.current_time
        if globals.replication:
            self.remove_page_frame(page.id)
        self.frames.append(page)
        return True
    
    def copy_page_frame(self, page_id):
        for i, page in enumerate(self.frames):
            if page.id == page_id:
                self.frames[i].replicated = True
                return self.frames[i]

    def remove_page_frame(self, page_id):
        for i, page in enumerate(self.frames):
            if page.id == page_id:
                return self.frames.pop(i)

    def invalidate_page(self, page):
        for p in self.frames:
            if p.id == page.id:
                p.invalidate()
                globals.PRINT_AND_LOG(f"Page {page.id} invalidated in CPU {self.cpu_id}.")
                return True
        return False
