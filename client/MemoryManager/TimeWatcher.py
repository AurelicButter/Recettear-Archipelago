""" 
Watcher module dedicated to functions that monitor various memory locations 
for time-related changes in-game
"""

import math
from . import MemoryLocations as Memory
from ..DataStore import DataStore
from ..RecettearProcess import RecettearProcess

def check_current_date(process: RecettearProcess, dataStore: DataStore) -> set[str]:
    current_date = process.read_int(Memory.DATE_TIME, 4)

    if current_date == dataStore.ap_store.get_maximum_date_unlocked():
        process.write_int(Memory.DATE_TIME, 4, current_date - 1)
        return set()

    recettearStore = dataStore.recettear_store

    # All current dates need to be offset by 1 as Day 1 is the tutorial
    # Day 2 is the start of Week 1 for the player
    if math.floor((current_date - 1) / 7) > recettearStore.loans_paid:
        recettearStore.loans_paid = recettearStore.loans_paid + 1
        return set([f"Paid Week {recettearStore.loans_paid} Debt"])
    return set()