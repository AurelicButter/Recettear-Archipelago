from pymem import Pymem

from . import MemoryLocations as Memory

class StatsChecker:
    """
    Compares memory values to various statistics in-game and enables location checks if conditions are met.
    """
    last_merchant_level = 1

    def __init__(self):
        super().__init__()

    def load_current_stats(self, server_stats: dict):
        """
        Sets the current stats from the Archipelago server for comparison to in-game values.
        """

        self.last_merchant_level = server_stats.get("Merchant Level", 1)

    def _check_merchant_level(self, game_process: Pymem) -> set[str]:
        current_level = int.from_bytes(game_process.read_bytes(Memory.EXP_CURRENT_LEVEL, 4), byteorder='little') + 1

        if current_level > self.last_merchant_level:
            self.last_merchant_level = current_level
            return set([f"Merchant Level {current_level}"])
        return set()

    def check_stats(self, game_process: Pymem) -> set[str]:
        """
        Checks various stats in-game and returns a set of location checks that have been met.
        """
        location_checks: set[str] = set()

        location_checks.update(self._check_merchant_level(game_process))

        location_checks.discard(None)

        return location_checks
