from __future__ import annotations
from typing import TYPE_CHECKING
from rule_builder.rules import Has, Or, HasAll

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

    pass_week_2 = Or(Has("Terme Finance Approval (Week 2)"), Has("Progressive Finance Approval", 1))
    pass_week_3 = Or(Has("Terme Finance Approval (Week 3)"), Has("Progressive Finance Approval", 2))
    pass_week_4 = Or(Has("Terme Finance Approval (Week 4)"), Has("Progressive Finance Approval", 3))
    pass_week_5 = Or(Has("Terme Finance Approval (Week 5)"), Has("Progressive Finance Approval", 4))

    world.set_rule(week_1_to_2, pass_week_2)
    world.set_rule(week_2_to_3, pass_week_3)
    world.set_rule(week_3_to_4, pass_week_4)
    world.set_rule(week_4_to_5, pass_week_5)


def set_all_location_rules(world: RecettearWorld) -> None:
    can_pay_debt = Or(
        Has("Progressive Finance Approval", 4),
        HasAll(
            "Terme Finance Approval (Week 2)",
            "Terme Finance Approval (Week 3)",
            "Terme Finance Approval (Week 4)",
            "Terme Finance Approval (Week 5)"
        )
    )

    debt_free = world.get_location("Debt Free")
    world.set_rule(debt_free, can_pay_debt)

def set_completion_condition(world: RecettearWorld) -> None:
    world.set_completion_rule(Has("Victory"))