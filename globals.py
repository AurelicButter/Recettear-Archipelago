import json
from pkgutil import get_data

metadata = json.loads(get_data("worlds.recettear", "archipelago.json"))

game = "Recettear: An Item Shop's Tale"
filler_item = "Dreams of Sweets"
origin_region = "Week 1"