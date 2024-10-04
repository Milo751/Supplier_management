import pandas as pd

from utils.logger import Logger

class GoverningLaw:
    def __init__(self, data):
        self.logger = Logger()
        self.data = data[['Document Name', 'Governing Law']]
        