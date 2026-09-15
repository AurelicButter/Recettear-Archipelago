import json
from pkgutil import get_data

__metadata = json.loads(get_data("worlds.recettear", "archipelago.json"))

game: str = __metadata["game"]
world_version: str = __metadata["world_version"]
minimum_ap_version: str = __metadata["minimum_ap_version"]
origin_region = "Week 1"