from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Item, ItemClassification
from . import globals
from .data import ItemClassification as DataItem, ItemID
import logging

debug_logger = logging.getLogger("RecettearDebug")

if TYPE_CHECKING:
    from .world import RecettearWorld

key_lookup = { v: k for k, v in ItemID.ITEM_NAME_TO_ID.items() }

class RecettearItem(Item):
    game = globals.game

def get_random_filler_item_name(world: RecettearWorld) -> str:
    filler_items = [item_name for item_name, classification in DataItem.DEFAULT_ITEM_CLASSIFICATION.items() if classification == ItemClassification.filler]
    
    return world.random.choice(filler_items)

def lookup_item_name_with_id(item_id: int) -> dict[str, str] | None:
    try:
        return {
            "id": item_id,
            "name": key_lookup.get(item_id),
            "classification": DataItem.DEFAULT_ITEM_CLASSIFICATION[key_lookup.get(item_id)]
        }
    except KeyError:
        debug_logger.error(f"Item with ID {item_id} not found in mapping. Continuing with no item given, please report this issue.")
        return None

def create_item_with_correct_classification(world: RecettearWorld, name: str) -> RecettearItem:
    classification = DataItem.DEFAULT_ITEM_CLASSIFICATION[name]

    return RecettearItem(name, classification, ItemID.ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: RecettearWorld) -> None:
    itempool: list[Item] = []

    if world.options.progressive_finance_approval.option_true:
        itempool.extend([
            world.create_item("Progressive Finance Approval"),
            world.create_item("Progressive Finance Approval"),
            world.create_item("Progressive Finance Approval"),
            world.create_item("Progressive Finance Approval")
        ])
    else:
        itempool.extend([
            world.create_item("Terme Finance Approval (Week 2)"),
            world.create_item("Terme Finance Approval (Week 3)"),
            world.create_item("Terme Finance Approval (Week 4)"),
            world.create_item("Terme Finance Approval (Week 5)")
        ])

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool
