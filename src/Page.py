class Page:
    def __init__(self, id, mode, origin_cpu=None):
        self.id = id
        self.mode = mode
        self.status = True
        self.last_access_time = 0  # Track the last access time for LRU
        self.replicated = mode == 'r'  # Initially set replicated based on mode
        self.origin_cpu = origin_cpu  # Track the CPU that originated the page or invalidation

    def invalidate(self):
        self.status = False
        self.replicated = False

    def __str__(self):
        return (f"Page(id={self.id}, mode={self.mode}, status={self.status}, "
                f"last_access_time={self.last_access_time}, replicated={self.replicated}, "
                f"origin_cpu={self.origin_cpu})")