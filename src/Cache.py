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
                    print(f"Page {page_id} found in cache but invalidated in CPU {self.cpu_id}.")
                    logging.info(f"Page {page_id} found in cache but invalidated in CPU {self.cpu_id}.")
                    return False
                print(f"Page {page_id} found in cache of CPU {self.cpu_id}")
                logging.info(f"Page {page_id} found in cache of CPU {self.cpu_id}")
                if mode != False:
                    if mode == 'w':
                        globals.network_instance.broadcast_invalidation(page, self.cpu_id)
                    page.status = True
                    page.mode = mode
                return True
        return False

    def load_page_frame(self, page):
        if len(self.frames) >= globals.pages_per_cpu:
            return False
        page.status = True
        page.origin_cpu = self.cpu_id
        page.last_access_time = globals.current_time
        self.frames.append(page)
        return True
    
    def copy_page_frame(self, page_id):
        for i, page in enumerate(self.frames):
            if page.id == page_id:
                return self.frames[i]

    def remove_page_frame(self, page_id):
        for i, page in enumerate(self.frames):
            if page.id == page_id:
                return self.frames.pop(i)

    def invalidate_page(self, page):
        for p in self.frames:
            if p.id == page.id:
                p.invalidate()
                print(f"Page {page.id} invalidated in CPU {self.cpu_id}.")
                logging.info(f"Page {page.id} invalidated in CPU {self.cpu_id}.")
                return True
        return False
