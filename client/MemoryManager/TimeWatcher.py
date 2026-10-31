""" 
Watcher module dedicated to functions that monitor various memory locations 
for time-related changes in-game
"""

from . import MemoryLocations as Memory
from ..DataStore import DataStore
from ..RecettearProcess import RecettearProcess
from ..constants.PaymentDates import PAYMENT_DATES
from ..constants.PaymentAmounts import PAYMENT_AMOUNT

def review_current_date(process: RecettearProcess, dataStore: DataStore) -> None:
    """
    Checks the current date in-game to see if the player needs to be reverted to a
    previous day based on unlocks.
    """
    current_date = process.read_int(Memory.DATE_TIME, 4) + 1 # Zero-based, 0 is Day 1

    if current_date == dataStore.ap_store.get_maximum_date_unlocked():
        process.write_int(Memory.DATE_TIME, 4, current_date - 2)

def loan_payment_watcher(process: RecettearProcess, dataStore: DataStore) -> set[str]:
    """
    Method to prevent the player from losing their pixs in the event of a loan payment
    if they do not have the money to pay and the following week unlocked.
    """
    current_date = process.read_int(Memory.DATE_TIME, 4) + 1 # Zero-based, 0 is Day 1
    current_payment_amt = process.read_int(Memory.LOAN_PAYMENT_DISPLAY, 4)

    if current_payment_amt > 0:
        dataStore.event_store.payment_event = True

        if dataStore.ap_store.prevent_bankruptcy:
            dataStore.event_store.temp_values["current_pixs"] = current_payment_amt
    elif dataStore.event_store.payment_event:
        # Loan payment is made. Continue as normal
        if dataStore.event_store.temp_values["current_pixs"] in PAYMENT_AMOUNT:
            if current_date == 37: # Day 37 is goal date
                dataStore.event_store.payment_event = False
                dataStore.event_store.temp_values["current_pixs"] = 0
                return set(["Debt Free"])
            else:
                payment_index = PAYMENT_DATES.index(current_date)
                dataStore.recettear_store.update_loans_paid(payment_index)
            
                dataStore.event_store.payment_event = False
                dataStore.event_store.temp_values["current_pixs"] = 0
                return set([f"Paid Week {payment_index + 1} Debt"])
        # Player failed to make a payment
        elif current_date == 2:
            if dataStore.ap_store.prevent_multi_loans:
                first_date = dataStore.recettear_store.get_loans_paid() * 7 + 1
                process.write_int(Memory.DATE_TIME, 4, first_date)
            
            if dataStore.ap_store.prevent_bankruptcy:
                process.write_int(Memory.PIX_BALANCE, 4, dataStore.event_store.temp_values["current_pixs"])
            dataStore.event_store.payment_event = False
            dataStore.event_store.temp_values["current_pixs"] = 0       

    return set()