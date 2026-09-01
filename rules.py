from __future__ import annotations
from typing import TYPE_CHECKING
from rule_builder.rules import Has

if TYPE_CHECKING:
    from .world import RecettearWorld

def set_all_rules(world: RecettearWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_entrance_rules(world: RecettearWorld) -> None:
    week_1_to_2 = world.get_entrance("Week 1 to 2")
    week_2_to_3 = world.get_entrance("Week 2 to 3")
    week_3_to_4 = world.get_entrance("Week 3 to 4")
    week_4_to_5 = world.get_entrance("Week 4 to 5")

    pass_week_2 = Has("Terme Finance Approval (Week 2)")
    pass_week_3 = Has("Terme Finance Approval (Week 3)")
    pass_week_4 = Has("Terme Finance Approval (Week 4)")
    pass_week_5 = Has("Terme Finance Approval (Week 5)")

    world.set_rule(week_1_to_2, pass_week_2)
    world.set_rule(week_2_to_3, pass_week_3)
    world.set_rule(week_3_to_4, pass_week_4)
    world.set_rule(week_4_to_5, pass_week_5)


def set_all_location_rules(world: RecettearWorld) -> None:
    pass

def set_completion_condition(world: RecettearWorld) -> None:
    world.set_completion_rule(Has("Victory"))