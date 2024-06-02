from Cache import Cache
import globals
import logging

class CPU:
    def __init__(self, id):
        self.id = id
        self.cache = Cache()
        self.stats = {'page_faults': 0, 'hits': 0, 'invalidations': 0}

    def load(self, page_id, mode):
        if self.cache.has_page_frame(page_id, mode):
            self.stats['hits'] += 1
            logging.info(f"CPU {self.id}: Page {page_id} loaded from cache")
        else:
            self.page_fault(page_id, mode)

    def page_fault(self, page_id, mode):
        self.stats['page_faults'] += 1
        logging.info(f"CPU {self.id}: Page fault for page {page_id}")
        page = globals.network_instance.request_page(self.id, page_id, mode)
        while not self.cache.load_page_frame(page):
            logging.info(f"CPU {self.id}: Cache is full")
            self.evict_page()

    def store(self, page_id):
        return self.cache.remove_page_frame(page_id)

    def evict_page(self):
        logging.info(f"CPU {self.id}: Evicting page with algorithm {globals.algorithm}")
        if globals.algorithm == 'FIFO':
            self.handle_fifo()
        elif globals.algorithm == 'LRU':
            self.handle_lru()
        elif globals.algorithm == 'OPTIMAL':
            self.handle_optimal()

    def handle_fifo(self):
        evicted_page = self.cache.frames.pop(0)
        globals.mmu.store_page(evicted_page)
        self.stats['invalidations'] += 1
        logging.info(f"CPU {self.id}: FIFO eviction of page {evicted_page.id}")

    def handle_lru(self):
        lru_page = min(self.cache.frames, key=lambda page: page.last_access_time)
        self.cache.frames.remove(lru_page)
        globals.mmu.store_page(lru_page)
        self.stats['invalidations'] += 1
        logging.info(f"CPU {self.id}: LRU eviction of page {lru_page.id}")

    def handle_optimal(self):
        future_references = globals.references[globals.current_reference_index:]
        frames = self.cache.frames

        def next_use_distance(page):
            for index, ref in enumerate(future_references):
                if ref[1] == page.id:
                    return index
            return float('inf')

        optimal_page = max(frames, key=next_use_distance)
        self.cache.frames.remove(optimal_page)
        globals.mmu.store_page(optimal_page)
        self.stats['invalidations'] += 1
        logging.info(f"CPU {self.id}: Optimal eviction of page {optimal_page.id}")

    def receive_page(self, page):
        logging.info(f"CPU {self.id}: Received page {page.id}")
        self.cache.load_page_frame(page)

    def print_status(self):
        pages = [page.id for page in self.cache.frames]
        logging.info(f"CPU {self.id} status: {self.cache.frames}")
        print(f"--------------------CPU {self.id}---------------------")
        print(pages)
