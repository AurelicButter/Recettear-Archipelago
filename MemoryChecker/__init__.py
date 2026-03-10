from . import StatsChecker
from . import TimeChecker

class MemoryChecker():
    def __init__(self):
        self.stats = StatsChecker.StatsChecker()
        self.time = TimeChecker.TimeChecker()

        super().__init__()