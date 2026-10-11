from ..constants.PaymentDates import PAYMENT_DATES

class ArchipelagoStore:
    """ Data class dedicated to storing Archipelago unlocks from the multiworld """
    last_check_received: int
    """The integer value of the last check from the server read by the store to prevent duplicate items on connection"""
    weeks_received: bytearray
    """ 
    A bytearray of week unlocks to track what weeks the player can access.  
    Reads from left to right, the weeks starting with Week 2's unlock (ie: Week 2 is index 0)
    """
    prevent_bankruptcy: bool
    """
    Option flag to detect if a player's yaml specifies saving the player from complete bankruptcy
    (Reset back to current pixs rather than 1000 pixs)
    """
    prevent_multi_loans: bool
    """
    Option flag to detect if a player's yaml specifies resetting the player back to Day 2 or 
    the last week's payment date + 1 (ie: Day 9 for Week 3)
    """

    def __init__(self) -> None:
        self.last_check_received = -1
        self.weeks_received = bytearray(4)
        self.prevent_bankruptcy = False
        self.prevent_multi_loans = False

    def update_state(self, item: str) -> None:
        if item.find("Finance"):
            self.update_week_limit(item)
        else:
            raise ValueError(f"ArchipelagoStore cannot update state with given key: {item}")

    def update_week_limit(self, item: str) -> None:
        index: int

        if item.startswith("Progressive"):
            index = self.weeks_received.find(0)
        elif item.startswith("Terme"):
            index = int(item[-2]) - 2 # Offset by 2 as the first week unlock is week 2
        else:
            raise ValueError(f"Week limit cannot be updated with given key: {item}")

        self.weeks_received[index] = 1

    def get_maximum_date_unlocked(self) -> int:
        """
        Helper function to return the maximum possible date the player can play to
        based on the weeks unlocked.
        """
        week_limit = self.weeks_received.find(0)

        if week_limit == -1:
            return 999 # Really large number to indicate all unlocked
        return PAYMENT_DATES[week_limit]