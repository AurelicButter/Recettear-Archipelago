from dataclasses import dataclass
from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

class ProgressiveWeeks(Toggle):
    """
    (Not Implemented) Sets the week unlocks to a progressive system meaning players will have access to Week 2 first
    compared to a keyed lock where each week must be individually unlocked.
    """
    display_name = "Progressive Weeks"

class MaxMerchantLevel(Range):
    """
    Restrict the number of available locations used with leveling up Recette's Merchant Level. Defaults to 50 to match vanilla unlocks.
    """
    display_name = "Max Level Checks"

    range_start = 1
    range_end = 99
    default = 50

class IncrementMerchantLevel(Range):
    """
    Bundles level locations to have a check every x level instead of every level. Defaults to 1 for every level.
    """

    display_name = "Incremental Level Checks"

    range_start = 1
    range_end = 10
    default = 1

# Commenting out options for now as none are implemented and will be at a later date.
@dataclass
class RecettearOptions(PerGameCommonOptions):
    progressive_weeks: ProgressiveWeeks
    #max_merchant_level: MaxMerchantLevel
    #increment_merchant_level: IncrementMerchantLevel


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [ProgressiveWeeks]
    )
]


option_presets = {
    """
    "sync-friendly": {
        "progressive_weeks": True,
        "max_merchant_level": 30,
        "increment_merchant_level": 1
    }
    """
}