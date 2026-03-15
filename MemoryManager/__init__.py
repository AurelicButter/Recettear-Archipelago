import logging
from pymem import Pymem
from . import StatsChecker
from . import TimeChecker
from CommonClient import logger
from BaseClasses import ItemClassification
from ..items import lookup_item_name_with_id
from . import MemoryLocations

debug_logger = logging.getLogger("RecettearDebug")

class MemoryManager():
    game_process: Pymem = None

    def __init__(self):
        self.stats = StatsChecker.StatsChecker()
        self.time = TimeChecker.TimeChecker()

    def add_game_process(self, game_process: Pymem):
        self.game_process = game_process

    def remove_game_process(self):
        self.game_process = None

    def received_items(self, ids: list[int]) -> None:
        """
        Handle received items and update the game state accordingly.

        :param items: List of item IDs received.
        """
        if not self.game_process:
            logger.warning("Game process not available. Cannot handle received items.")
            return

        for id in ids:
            item = lookup_item_name_with_id(id)

            if item.get("classification") == ItemClassification.filler:
                name = item.get("name")

                if name == "1000 Pixs":
                    current_pixs = int.from_bytes(self.game_process.read_bytes(MemoryLocations.PIX_BALANCE, 4), byteorder='little')
                    current_pixs += 1000
                    self.game_process.write_bytes(MemoryLocations.PIX_BALANCE, current_pixs.to_bytes(4, byteorder='little'), 4)
                elif name.startswith("Merchant Exp"):
                    current_exp = int.from_bytes(self.game_process.read_bytes(MemoryLocations.EXP_CURRENT, 4), byteorder='little')
                    current_exp += int(len("Merchant Exp++"[12:]) * 200) 
                    self.game_process.write_bytes(MemoryLocations.EXP_CURRENT, current_exp.to_bytes(4, byteorder='little'), 4)