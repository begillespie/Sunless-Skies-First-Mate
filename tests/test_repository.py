#!/usr/bin/env python3
"""
Tier 2 Unit Tests for GoogleSheetsRepository and BaseRepository contract.
"""
import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.connectors.google_sheets_repo import GoogleSheetsRepository


class TestGoogleSheetsRepository(unittest.TestCase):

    def setUp(self):
        self.repo = GoogleSheetsRepository("mock_spreadsheet_id")
        # Seed cache directly to test without external network calls
        self.repo._cache["state_scalars"] = pd.DataFrame([
            {"key": "current_location", "value": "new_winchester"},
            {"key": "sovereigns", "value": 1000}
        ])
        self.repo._cache["state_inventory"] = pd.DataFrame([
            {"good_key": "fuel", "hold_qty": 14, "bank_qty": 5},
            {"good_key": "supplies", "hold_qty": 12, "bank_qty": 2}
        ])

    def test_get_table(self):
        df = self.repo.get_table("state_scalars")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)

    def test_get_cell_valid(self):
        val = self.repo.get_cell("state_scalars", {"key": "sovereigns"}, "value")
        self.assertEqual(val, 1000)

    def test_set_cell_success(self):
        success = self.repo.set_cell("state_scalars", {"key": "sovereigns"}, "value", 1250)
        self.assertTrue(success)
        self.assertEqual(self.repo.get_cell("state_scalars", {"key": "sovereigns"}, "value"), 1250)

    def test_append_row_success(self):
        success = self.repo.append_row("state_inventory", {"good_key": "bronzewood", "hold_qty": 0, "bank_qty": 5})
        self.assertTrue(success)
        df = self.repo.get_table("state_inventory")
        self.assertEqual(len(df), 3)
        self.assertEqual(df.iloc[-1]["good_key"], "bronzewood")

    def test_delete_row_success(self):
        success = self.repo.delete_row("state_inventory", {"good_key": "supplies"})
        self.assertTrue(success)
        df = self.repo.get_table("state_inventory")
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["good_key"], "fuel")

    def test_no_silent_methods_and_errors(self):
        # Verify lookups raise LookupError instead of failing silently
        with self.assertRaises(LookupError):
            self.repo.get_cell("state_scalars", {"key": "nonexistent"}, "value")
        with self.assertRaises(LookupError):
            self.repo.delete_row("state_inventory", {"good_key": "nonexistent"})


if __name__ == "__main__":
    unittest.main()