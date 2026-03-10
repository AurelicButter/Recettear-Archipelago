from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld
from .options import option_groups, option_presets
from . import globals

class RecettearWebWorld(WebWorld):
    game = globals.game
    theme = "grassFlowers"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Recettear for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["AurelicButter"]
    )

    tutorials = [setup_en]
    option_groups = option_groups
    options_presets = option_presets