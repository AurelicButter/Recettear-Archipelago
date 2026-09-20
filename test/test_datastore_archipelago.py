import unittest
from ..client.DataStore.ArchipelagoStore import ArchipelagoStore

class TestDatastoreArchipelago(unittest.TestCase):
    def test_valid_progressive_week_update(self) -> None:
        """
        Verify that the store can correctly update the weeks counter accurately
        """
        store = ArchipelagoStore()

        store.update_state("Progressive Finance Approval")

        self.assertTrue(store.weeks_received[0] == 1, f"Store failed to set the first week unlock as received")
        self.assertTrue(store.weeks_received.count(0) == 3, f"Store updated multiple weeks with one unlock")

        store.update_state("Progressive Finance Approval")

        self.assertTrue(store.weeks_received[1] == 1, f"Store failed to set the second week unlock as received")
        self.assertTrue(store.weeks_received.count(0) == 2, f"Store updated more weeks than unlocks received")

    def test_valid_static_week_update(self) -> None:
        """
        Verify that the static weeks ("Terme Approvals") can correctly update the weeks counter based on their values
        """
        store = ArchipelagoStore()

        store.update_state("Terme Finance Approval (Week 4)")

        self.assertTrue(store.weeks_received[2] == 1, f"Store failed to set the fourth week unlock as received. {store.weeks_received}")
        self.assertTrue(store.weeks_received.count(0) == 3, f"Store updated multiple weeks with one unlock. {store.weeks_received}")

        store.update_state("Terme Finance Approval (Week 2)")

        self.assertTrue(store.weeks_received[0] == 1, f"Store failed to set the second week unlock as received")
        self.assertTrue(store.weeks_received.count(0) == 2, f"Store updated more weeks than unlocks received")

    def test_maximum_date_no_weeks_calc(self) -> None:
        """
        Tests the get_maximum_date_unlocked function to see if the default return value is Day 8 if no week unlocks are received
        """
        store = ArchipelagoStore()

        results = store.get_maximum_date_unlocked()
        self.assertTrue(results == 8, f"Maximum date received does not match Day 8. Received: {results}")
        
    def test_maximum_date_weeks_unlocked_calc(self) -> None:
        """
        Tests the get_maximum_date_unlocked function to determine if the store reports an accurate date
        """
        store = ArchipelagoStore()

        store.update_state("Terme Finance Approval (Week 4)")
        store.update_state("Terme Finance Approval (Week 2)")

        results = store.get_maximum_date_unlocked()
        self.assertTrue(results == 15, f"Maximum date received does not match Day 15. Received: {results}")

    def test_invalid_state_update(self) -> None:
        """
        Verify the store errors out on an invalid input
        """
        store = ArchipelagoStore()

        with self.assertRaises(ValueError, msg=f"Store failed to accurately respond to an invalid input"):
            store.update_state("TEST VALUE")