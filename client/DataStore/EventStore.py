class EventStore:
    payment_event: bool
    """
    Boolean toggle to detect when player is within the loan payment event
    """
    temp_values: dict
    """
    A temp dict value to store any values needed over cycles that are not needed
    to remain in use over the course of the slot
    """

    def __init__(self) -> None:
        self.payment_event = False
        self.temp_values = dict()

    def clear_temp_cache(self) -> None:
        self.temp_values.clear()
    