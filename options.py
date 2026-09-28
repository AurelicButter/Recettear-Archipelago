from dataclasses import dataclass
from Options import OptionGroup, PerGameCommonOptions, Toggle

class ProgressiveFinanceApproval(Toggle):
    """
    Sets the finance approval items (required item for week progression) to 
    progressive rather than specific week items.
    """
    display_name = "Progressive Finance Approvals"

class PreventBankruptcy(Toggle):
    """
    Toggle the ability to keep your current pixs instead of getting 1000 pixs
    in the event of a failed payment
    """
    display_name = "Prevent Bankruptcy"

class PreventMultiLoans(Toggle):
    """
    Toggle the ability to reset back to the first day of the current week instead
    of resetting to Day 2 in the event of a failed payment
    """
    display_name = "Prevent Multiweek Reset"

@dataclass
class RecettearOptions(PerGameCommonOptions):
    progressive_finance_approval: ProgressiveFinanceApproval
    prevent_bankruptcy: PreventBankruptcy
    prevent_multi_loans: PreventMultiLoans


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [
            ProgressiveFinanceApproval,
            PreventBankruptcy,
            PreventMultiLoans
        ]
    )
]


option_presets = {}