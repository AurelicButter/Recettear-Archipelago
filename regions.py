from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Region

if TYPE_CHECKING:
    from .world import RecettearWorld

def create_and_connect_regions(world: RecettearWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: RecettearWorld) -> None:
    week_1 = Region("Week 1", world.player, world.multiworld)
    week_2 = Region("Week 2", world.player, world.multiworld)
    week_3 = Region("Week 3", world.player, world.multiworld)
    week_4 = Region("Week 4", world.player, world.multiworld)
    week_5 = Region("Week 5", world.player, world.multiworld)

    regions = [week_1, week_2, week_3, week_4, week_5]

    world.multiworld.regions += regions

def connect_regions(world: RecettearWorld) -> None:
    week_1 = world.get_region("Week 1")
    week_2 = world.get_region("Week 2")
    week_3 = world.get_region("Week 3")
    week_4 = world.get_region("Week 4")
    week_5 = world.get_region("Week 5")

    week_1.connect(week_2, "Week 1 to 2")
    week_2.connect(week_3, "Week 2 to 3")
    week_3.connect(week_4, "Week 3 to 4")
    week_4.connect(week_5, "Week 4 to 5")
    