from worlds.AutoWorld import World

from . import items, locations, options, regions, rules, web_world, globals
from .data import ItemID, LocationID

class RecettearWorld(World):
    game = globals.game
    web = web_world.RecettearWebWorld()

    options_dataclass = options.RecettearOptions
    options: options.RecettearOptions

    location_name_to_id = LocationID.LOCATION_NAME_TO_ID
    item_name_to_id = ItemID.ITEM_NAME_TO_ID

    origin_region_name = globals.origin_region

    def fill_slot_data(self):
        return {
            "game_version": globals.world_version,
            "prevent_bankruptcy": self.options.prevent_bankruptcy.option_true,
            "prevent_multi_loans": self.options.prevent_multi_loans.option_true
        }

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self):
        rules.set_all_rules(self)

    def create_items(self):
        items.create_all_items(self)

    def create_item(self, name: str) -> items.RecettearItem:
        return items.create_item_with_correct_classification(self, name)
    
    def get_filler_item_name(self):
        return items.get_random_filler_item_name(self)