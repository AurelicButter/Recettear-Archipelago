""" 
Watcher module dedicated to functions that monitor various memory locations 
for time-related changes in-game
"""

import math
from . import MemoryLocations as Memory
from ..DataStore import RecettearStore
from ..RecettearProcess import RecettearProcess

def check_current_date(process: RecettearProcess, dataStore: RecettearStore) -> set[str]:
    current_date = process.read_int(Memory.DATE_TIME, 4)

    if current_date == dataStore.current_max_date:
        process.write_int(Memory.DATE_TIME, 4, current_date - 1)
        return set()

    # All current dates need to be offset by 1 as Day 1 is the tutorial
    # Day 2 is the start of Week 1 for the player
    if math.floor((current_date - 1) / 7) > dataStore.loans_paid:
        dataStore.loans_paid = dataStore.loans_paid + 1
        return set([f"Paid Week {dataStore.loans_paid} Debt"])
    return set()