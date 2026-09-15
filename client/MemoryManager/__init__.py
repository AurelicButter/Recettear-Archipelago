import logging
from CommonClient import logger
from BaseClasses import ItemClassification
from ...items import lookup_item_name_with_id
from ..MemoryManager import MemoryLocations
from . import PlayerWatcher
from . import TimeWatcher
from ..RecettearProcess import RecettearProcess
from ..DataStore import DataStore
from .MemoryLocations import TEST_BYTES
from ... import locations

debug_logger = logging.getLogger("RecettearDebug")

class MemoryManager():
    __process: RecettearProcess | None = None
    __dataStore: DataStore

    # Item tracking to avoid duplicating item retrieval
    __accquired_pixs = 0
    __accquired_exp = 0

    def __init__(self):
        self.__dataStore = DataStore()     

    def update_item_tracking(self, stored_data: dict[str, any]):
        self.__accquired_pixs = stored_data.get("accquired_pixs", 0)
        self.__accquired_exp = stored_data.get("accquired_exp", 0)

        self.__dataStore.ap_store.accquired_exp = stored_data.get("accquired_exp", 0)
        self.__dataStore.ap_store.accquired_pixs = stored_data.get("accquired_pixs", 0)

    def add_game_process(self, game_process: RecettearProcess):
        self.__process = game_process

    def remove_game_process(self):
        self.__process = None

    def received_items(self, ids: list[int]) -> dict[str, int]:
        """
        Handle received items and update the game state accordingly.

        :param items: List of item IDs received.
        """

        storage_value_updates = {
            "accquired_pixs": 0,
            "accquired_exp": 0
        }

        if self.__process is None or not self.__process.has_process():
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
                        current_pixs = self.__process.read_int(MemoryLocations.PIX_BALANCE, 4)
                        current_pixs += 1000
                        self.__process.write_int(MemoryLocations.PIX_BALANCE, 4, current_pixs)
                        storage_value_updates["accquired_pixs"] += 1000

                elif name.startswith("Merchant Exp"):
                    exp_amt = int(len(name[12:]) * 200)

                    if self.__accquired_exp > 0:
                        self.__accquired_exp -= exp_amt

                        if self.__accquired_exp < 0:
                            exp_amt = abs(self.__accquired_exp)
                            self.__accquired_exp = 0 

                    if self.__accquired_exp == 0:
                        current_exp = self.__process.read_int(MemoryLocations.EXP_CURRENT, 4)
                        current_exp += exp_amt
                        self.__process.write_int(MemoryLocations.EXP_CURRENT, 4, current_exp)
                        storage_value_updates["accquired_exp"] += exp_amt

        return {k: v for k, v in storage_value_updates.items() if v > 0}

    def set_location_checks(self, location_ids: list[int]) -> None:
        for location_id in location_ids:
            self.__dataStore.recettear_store.update_state(location_id)

    def search_locations(self) -> set[str]:
        """
        Function to call all watchers to search and discover new updates to prepare to send
        to the AP server
        """
        # Test a byte read before performing checks. Will cause an error if unable to.
        self.__process.read_bytes(TEST_BYTES, 4)

        location_updates: set[str] = set()

        location_updates.update(PlayerWatcher.check_merchant_level(self.__process, self.__dataStore.recettear_store))
        location_updates.update(TimeWatcher.check_current_date(self.__process, self.__dataStore))

        location_ids = set(locations.get_location_names_with_ids(location_updates).values())
        location_ids.discard(None)

        return location_ids



        