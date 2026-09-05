from dataclasses import dataclass
from Options import OptionGroup, PerGameCommonOptions, Toggle

class ProgressiveFinanceApproval(Toggle):
    """
    Sets the finance approval items (required item for week progression) to 
    progressive rather than specific week items. 
    """
    display_name = "Progressive Finance Approvals"

@dataclass
class RecettearOptions(PerGameCommonOptions):
    progressive_finance_approval: ProgressiveFinanceApproval


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [ProgressiveFinanceApproval]
    )
]


option_presets = {}