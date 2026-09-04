from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Location
from . import items, globals
from .data import LocationID

if TYPE_CHECKING:
    from .world import RecettearWorld

class RecettearLocation(Location):
    game = globals.game

def get_location_names_with_ids(location_name: list[str]) -> dict[str, int | None]:
    return { location_name: LocationID.LOCATION_NAME_TO_ID[location_name] for location_name in location_name }

def create_all_locations(world: RecettearWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: RecettearWorld) -> None:
    week_1 = world.get_region("Week 1")
    week_2 = world.get_region("Week 2")
    week_3 = world.get_region("Week 3")
    week_4 = world.get_region("Week 4")
    week_5 = world.get_region("Week 5")

    week_1_locations = get_location_names_with_ids(
        ["Paid Week 1 Debt"]
    )
    for i in range(2, 12):
        week_1_locations = week_1_locations | get_location_names_with_ids([f"Merchant Level {i}"])

    week_1.add_locations(week_1_locations, RecettearLocation)

    week_2_locations = get_location_names_with_ids(
        ["Paid Week 2 Debt"]
    )
    for i in range(12, 22):
        week_2_locations = week_2_locations | get_location_names_with_ids([f"Merchant Level {i}"])

    week_2.add_locations(week_2_locations, RecettearLocation)

    week_3_locations = get_location_names_with_ids(
        ["Paid Week 3 Debt"]
    )
    for i in range(22, 32):
        week_3_locations = week_3_locations | get_location_names_with_ids([f"Merchant Level {i}"])

    week_3.add_locations(week_3_locations, RecettearLocation)

    week_4_locations = get_location_names_with_ids(
        ["Paid Week 4 Debt"]
    )
    for i in range(32, 51):
        week_4_locations = week_4_locations | get_location_names_with_ids([f"Merchant Level {i}"])
    week_4.add_locations(week_4_locations, RecettearLocation)

    week_5_locations = get_location_names_with_ids(
        []
    )
    week_5.add_locations(week_5_locations, RecettearLocation)

def create_events(world: RecettearWorld) -> None:
    week_5 = world.get_region("Week 5")

    week_5.add_event(
        "Debt Free", "Victory", location_type=RecettearLocation, item_type=items.RecettearItem
    )
