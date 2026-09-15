from .bases import RecettearTestBase
from ..client.DataStore.RecettearStore import RecettearStore
from ..data.LocationID import LOCATION_NAME_TO_ID

class TestDatastoreRecettear(RecettearTestBase):
    def test_valid_location_id_update(self) -> None:
        """
        Verify that the store can correctly update a store value based on the location ID
        """
        store = RecettearStore()

        store.update_state(LOCATION_NAME_TO_ID["Merchant Level 7"])

        self.assertTrue(store.last_merchant_level == 7, f"Store failed to update the location with ID: {LOCATION_NAME_TO_ID["Merchant Level 7"]}")

    def test_invalid_location_id_update(self) -> None:
        """
        Verify the store errors out on an invalid location ID input
        """
        store = RecettearStore()

        with self.assertRaises(ValueError, msg=f"Store failed to accurately respond to an invalid location ID: {-1}"):
            store.update_state(-1)