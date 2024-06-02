import globals
from Page import Page

class MMU:
    def __init__(self):
        self.RAM = []

    def store_page(self, page):
        print(f"Page {page.id} added to Virtual Memory")
        self.RAM.append(page)

    def send_page(self, page_id):
        # If we have the page in RAM, we remove it and return it
        for i, page in enumerate(self.RAM):
            if page.id == page_id:
                print(f"Page {page.id} in {i} deleted from Virtual Memory")
                self.RAM.pop(i)
                return page
            
    def print_status(self):
        print(f"--------------------{globals.algorithm}-------------------")
        print("----------------Virtual Memory----------------")
        pages = []
        for page in self.RAM:
            pages.append(page.id)
        print(pages)

    def report_stats(self):
        # Implement the logic to report statistics
        pass
