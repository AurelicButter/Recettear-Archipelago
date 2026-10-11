from ...locations import get_location_from_id

class RecettearStore:
    """ Data class dedicated to storing player progression in Recettear """
    last_merchant_level: int
    loans_paid: int

    def __init__(self) -> None:
        self.last_merchant_level = 1
        self.loans_paid = 0        

    def update_state(self, location_id: int) -> None:
        try:
            location_str = get_location_from_id(location_id)
        except KeyError:
            raise ValueError(f"Provided location ID is not in the list of applicable locations. ID given: {location_id}")

        if location_str.startswith("Paid Week"):
            self.loans_paid = self.loans_paid + 1
        elif location_str.startswith("Merchant Level"):
            self.last_merchant_level = location_id - 100 + 2 # Location level IDs start at 100, first location is at level 2

