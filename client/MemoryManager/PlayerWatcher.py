""" 
Watcher module dedicated to functions that monitor various memory locations 
for player updates in-game
"""

from . import MemoryLocations as Memory
from ..DataStore import RecettearStore
from ..RecettearProcess import RecettearProcess

def check_merchant_level(process: RecettearProcess, dataStore: RecettearStore) -> set[str]:
    current_level = process.read_int(Memory.EXP_CURRENT_LEVEL, 4) + 1 # Offset 1 for non-zero counting
        
    if current_level > dataStore.last_merchant_level:
        level_locations = set()
        
        for level in range(dataStore.last_merchant_level, current_level):
            level_locations.add(f"Merchant Level {level+1}")
        
        dataStore.last_merchant_level = current_level
        return level_locations
    return set()