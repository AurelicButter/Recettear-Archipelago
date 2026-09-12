from ...locations import get_location_from_id

class RecettearStore:
    """ Data class dedicated to storing player progression in Recettear """
    last_merchant_level: int = 0
    current_max_date: int = 8
    loans_paid: int = 0

    def update_state(self, location_id: int) -> None:
        try:
            location_str = get_location_from_id(location_id)
        except KeyError:
            raise ValueError(f"Provided location ID is not in the list of applicable locations. ID given: {location_id}")

        if location_str.startswith("Paid Week"):
            self.loans_paid += self.loans_paid
        elif location_str.startswith("Merchant Level"):
            self.last_merchant_level = location_id - 100 + 2 # Location level IDs start at 100, first location is at level 2

