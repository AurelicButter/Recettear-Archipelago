from pymem import Pymem

from . import MemoryLocations as Memory

class StatsManager:
    """
    Compares memory values to various statistics in-game and enables location checks if conditions are met.
    """
    last_merchant_level = 0

    def load_current_stats(self, server_stats: dict):
        """
        Sets the current stats from the Archipelago server for comparison to in-game values.
        """

        self.last_merchant_level = server_stats.get("Merchant Level", 0)

    def _check_merchant_level(self, game_process: Pymem) -> set[str]:
        current_level = int.from_bytes(game_process.read_bytes(Memory.EXP_CURRENT_LEVEL, 4), byteorder='little')

        if current_level > self.last_merchant_level:
            level_locations = set()

            # Offsets by 1 to account for non-zero level counting
            for level in range(self.last_merchant_level+1, current_level+1):
                level_locations.add(f"Merchant Level {level+1}")

            self.last_merchant_level = current_level
            return level_locations
        return set()

    def check_stats(self, game_process: Pymem) -> set[str]:
        """
        Checks various stats in-game and returns a set of location checks that have been met.
        """
        location_checks: set[str] = set()

        location_checks.update(self._check_merchant_level(game_process))

        location_checks.discard(None)

        return location_checks
