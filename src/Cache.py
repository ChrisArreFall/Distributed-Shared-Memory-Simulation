import globals

class Cache:
    def __init__(self):
        self.frames = []

    def has_page_frame(self, page_id, mode=False):
        for page in self.frames:
            if page.id == page_id:
                page.last_access_time = globals.current_time
                print(f"Page {page_id} found in cache")
                if mode != False and page.mode != mode:
                    print(f"Page {page_id} mode changed from {page.mode} to {mode}.")
                    page.mode = mode
                return True
        return False

    def load_page_frame(self, page):
        if len(self.frames) >= globals.pages_per_cpu:
            return False
        page.last_access_time = globals.current_time
        self.frames.append(page)
        return True

    def remove_page_frame(self, page_id):
        for i, page in enumerate(self.frames):
            if page.id == page_id:
                return self.frames.pop(i)
