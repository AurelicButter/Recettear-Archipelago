import logging
from CommonClient import logger
from BaseClasses import ItemClassification
from ...items import lookup_item_name_with_id
from ..MemoryManager import MemoryLocations
from . import PlayerWatcher
from . import TimeWatcher
from ..RecettearProcess import RecettearProcess
from ..DataStore import ArchipelagoStore, DataStore, RecettearStore
from .MemoryLocations import TEST_BYTES
from ... import locations

debug_logger = logging.getLogger("RecettearDebug")

class MemoryManager():
    __process: RecettearProcess | None = None
    __dataStore: DataStore

    def __init__(self):
        self.__dataStore = DataStore()

    def get_ap_store(self) -> ArchipelagoStore:
        return self.__dataStore.ap_store

    def get_recettear_store(self) -> RecettearStore:
        return self.__dataStore.recettear_store 

    def update_slot_data(self, slot_data: dict[str, any]) -> None:
        self.__dataStore.ap_store.prevent_bankruptcy = "prevent_bankruptcy" in slot_data
        self.__dataStore.ap_store.prevent_multi_loans = "prevent_multi_loans" in slot_data

    def update_item_tracking(self, stored_data: dict[str, any]) -> None:
        if "last_check_received" in stored_data:
            self.__dataStore.ap_store.last_check_received = stored_data.get("last_check_received")

    def add_game_process(self, game_process: RecettearProcess) -> None:
        self.__process = game_process

    def remove_game_process(self) -> None:
        self.__process = None

    def __handle_items(self, item: dict[str, str]) -> None:
        """
        Method to apply items to the player 
        """        
        if item.get("id") < 10: # ID range for week unlocks
            self.__dataStore.ap_store.update_state(item.get("name"))
        elif item.get("classification") == ItemClassification.filler:
            name = item.get("name")
        
            if name.find("Pixs") > -1:
                current_pixs = self.__process.read_int(MemoryLocations.PIX_BALANCE, 4)
                current_pixs += int(name[:name.find("Pixs")])
                self.__process.write_int(MemoryLocations.PIX_BALANCE, 4, current_pixs)
            elif name.startswith("Merchant Exp"):
                current_exp = self.__process.read_int(MemoryLocations.EXP_CURRENT, 4)
                current_exp += int(len(name[12:]) * 200)
                self.__process.write_int(MemoryLocations.EXP_CURRENT, 4, current_exp)
        

    def ready_items(self, ids: list[int]) -> dict[str, int]:
        """
        Handles items received between the last connection to
        the current connection to the AP slot
        """
        if self.__process is None:
            logger.warning("Game process not available. Cannot handle received items.")
            return

        last_check_received = self.__dataStore.ap_store.last_check_received

        for i, id in enumerate(ids):
            item = lookup_item_name_with_id(id)

            if i >= last_check_received:
                self.__handle_items(item)
                last_check_received += 1
            elif item.get("classification") != ItemClassification.filler:
                self.__handle_items(item)

        self.__dataStore.ap_store.last_check_received = last_check_received
        
        return {
            "last_check_received": last_check_received
        }      

    def received_items(self, ids: list[int]) -> dict[str, int]:
        """
        Handle received items and update the game state accordingly.

        :param items: List of item IDs received.
        """
        if self.__process is None:
            logger.warning("Game process not available. Cannot handle received items.")
            return

        for id in ids:
            item = lookup_item_name_with_id(id)
            self.__handle_items(item)

        self.__dataStore.ap_store.last_check_received += len(ids)

        return {
            "last_check_received": len(ids)
        }

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

        TimeWatcher.review_current_date(self.__process, self.__dataStore)

        location_updates.update(PlayerWatcher.check_merchant_level(self.__process, self.__dataStore.recettear_store))
        location_updates.update(TimeWatcher.loan_payment_watcher(self.__process, self.__dataStore))

        location_ids = set(locations.get_location_names_with_ids(location_updates).values())
        location_ids.discard(None)

        return location_ids



        