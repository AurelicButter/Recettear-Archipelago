from pymem import Pymem
import math

from . import MemoryLocations as Memory

class TimeManager():
    """
    Compares memory values to various time-related statistics in-game and enables location checks if conditions are met.
    """
    current_week = 1
    current_max_date = 8

    def load_current_stats(self, server_stats: dict):
        """
        Sets the last date recorded from the Archipelago server for comparison to in-game values.
        """

        self.current_week = server_stats.get("Weeks Paid", 0) + 1

    def _check_current_date(self, game_process: Pymem) -> set[str]:
        current_date = int.from_bytes(game_process.read_bytes(Memory.DATE_TIME, 4), byteorder='little')

        if current_date > self.current_max_date:
            self.current_week = math.floor(current_date / 7) + 1
            self.current_max_date = (self.current_week * 7) + 2
            return set([f"Paid Week {self.current_week} Debt"])
        return set()

    def check_time(self, game_process: Pymem) -> set[str]:
        """
        Checks various time-related stats in-game and returns a set of location checks that have been met.
        """
        location_checks: set[str] = set()

        location_checks.update(self._check_current_date(game_process))

        location_checks.discard(None)

        return location_checks