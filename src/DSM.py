import globals
from collections import deque
import logging

# Basic functions for DSM, I need to implement the functions.
class DSM:
    def __init__(self):
    

    def handle_page_fault(self, node, page):
        pass
    def replace_page(self, node, page):
        pass
    def lru_replace(self, node, page):
        pass

    def optimal_replace(self, node, page):
        pass
    
    def fifo_replace(self, node, page):
        pass
    def report_stats(self):
        pass
    def log_event(self, event):
        logging.info(event)
