class Page:
    def __init__(self, id, mode):
        self.id = id
        self.mode = mode
        self.status = True
        self.last_access_time = 0  # Track the last access time for LRU
