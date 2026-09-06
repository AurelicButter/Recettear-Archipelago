from .ArchipelagoStore import ArchipelagoStore
from .RecettearStore import RecettearStore

class DataStore():
    """
    A utility class dedicated to tracking player and Archipelago progression for the client
    """

    ap_store: ArchipelagoStore
    recettear_store: RecettearStore

    def __init__(self):
        self.ap_store = ArchipelagoStore()
        self.recettear_store = RecettearStore()

    def init_ap_values(self, stored_data: dict[str, any]):
        for k, v in stored_data.items():
            self.ap_store[k] = v

    def get_ap_keys(self) -> list[str]:
        return [k for k in ArchipelagoStore if not k.startswith('__')]

    def init_recettear_values(self, stored_data: dict[str, any]):
        for k, v in stored_data.items():
            self.recettear_store[k] = v

    def get_recettear_keys(self) -> list[str]:
        return [k for k in RecettearStore if not k.startswith('__')]