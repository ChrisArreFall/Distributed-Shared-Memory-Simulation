import globals
import logging

class MMU:
    def __init__(self):
        self.RAM = []

    def store_page(self, page):
        print(f"Page {page.id} added to Virtual Memory")
        self.RAM.append(page)

    def send_page(self, page_id, mode):
        # If we have the page in RAM, we return it
        for i, page in enumerate(self.RAM):
            if page.id == page_id:
                if mode == 'w' and page.replicated:
                    self.invalidate_page(page)
                self.RAM.pop(i)
                return page
        print(f"Page {page_id} not found in Virtual Memory")
        return None

    def invalidate_page(self, page):
        page.invalidate()
        globals.network_instance.broadcast_invalidation(page)
        print(f"Page {page.id} invalidated in Virtual Memory")

    def print_status(self):
        pages = [page.id for page in self.RAM]
        print("----------------Virtual Memory----------------")
        print(pages)
        logging.info(f"Virtual Memory status: {pages}")

