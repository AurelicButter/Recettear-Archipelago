import unittest
from ..data import ItemClassification, ItemID

class TestDataPairing(unittest.TestCase):
    def test_no_stray_item_classification(self) -> None:
        """
        Verify that all provided item classifications map to an item ID
        """
        missing = []

        for item in ItemClassification.DEFAULT_ITEM_CLASSIFICATION:
            try:
                ItemID.ITEM_NAME_TO_ID[item]
            except Exception:
                missing.append(item)

        self.assertTrue(len(missing) == 0, f"Item(s) in the item set are missing an ID.\n{missing}")

    def test_no_stray_item_id(self) -> None:
        """
        Verify that all provided items IDs map to an item classification
        """
        missing = []

        for item in ItemID.ITEM_NAME_TO_ID:
            try:
                ItemClassification.DEFAULT_ITEM_CLASSIFICATION[item]
            except Exception:
                missing.append(item)

        self.assertTrue(len(missing) == 0, f"Item(s) in the item set are missing a classification.\n{missing}") 