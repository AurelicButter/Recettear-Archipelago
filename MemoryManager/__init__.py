import logging
from pymem import Pymem
from .StatsManager import StatsManager
from .TimeManager import TimeManager
from CommonClient import logger
from BaseClasses import ItemClassification
from ..items import lookup_item_name_with_id
from . import MemoryLocations

debug_logger = logging.getLogger("RecettearDebug")

class MemoryManager():
    __game_process: Pymem = None

    # Item tracking to avoid duplicating item retrieval
    __accquired_pixs = 0
    __accquired_exp = 0

    def __init__(self):
        self.stats = StatsManager()
        self.time = TimeManager()

    def update_item_tracking(self, stored_data: dict[str, any]):
        self.__accquired_pixs = stored_data.get("accquired_pixs", 0)
        self.__accquired_exp = stored_data.get("accquired_exp", 0)

    def add_game_process(self, game_process: Pymem):
        self.__game_process = game_process

    def remove_game_process(self):
        self.__game_process = None

    def read_int(self, location, byte_amt):
        return int.from_bytes(self.__game_process.read_bytes(location, byte_amt), byteorder='little')
    
    def write_int(self, location, byte_amt, value: int):
        self.__game_process.write_bytes(location, value.to_bytes(byte_amt, byteorder='little'), byte_amt)

    def received_items(self, ids: list[int]) -> dict[str, int]:
        """
        Handle received items and update the game state accordingly.

        :param items: List of item IDs received.
        """

        storage_value_updates = {
            "accquired_pixs": 0,
            "accquired_exp": 0
        }

        if not self.__game_process:
            logger.warning("Game process not available. Cannot handle received items.")
            return

        for id in ids:
            item = lookup_item_name_with_id(id)

            if item.get("classification") == ItemClassification.filler:
                name = item.get("name")

                if name == "1000 Pixs":
                    if self.__accquired_pixs > 0:
                        self.__accquired_pixs -= 1000
                    else:
                        current_pixs = self.read_int(MemoryLocations.PIX_BALANCE, 4)
                        current_pixs += 1000
                        self.write_int(MemoryLocations.PIX_BALANCE, 4, current_pixs)
                        storage_value_updates["accquired_pixs"] += 1000

                elif name.startswith("Merchant Exp"):
                    exp_amt = int(len(name[12:]) * 200)

                    if self.__accquired_exp > 0:
                        self.__accquired_exp -= exp_amt

                        if self.__accquired_exp < 0:
                            exp_amt = abs(self.__accquired_exp)
                            self.__accquired_exp = 0 

                    if self.__accquired_exp == 0:
                        current_exp = self.read_int(MemoryLocations.EXP_CURRENT, 4)
                        current_exp += exp_amt
                        self.write_int(MemoryLocations.EXP_CURRENT, 4, current_exp)
                        storage_value_updates["accquired_exp"] += exp_amt

        return {k: v for k, v in storage_value_updates.items() if v > 0}