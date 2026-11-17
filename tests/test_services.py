#!/usr/bin/env python3
"""
Tier 2 Unit Test Suite for LLM Tool Registry, Guarded Engine Mutators,
Officer Rules, and Read-Only Service Calculators.
"""
import unittest
import pandas as pd
from src.connectors.google_sheets_repo import GoogleSheetsRepository
from src.services.calendar import epoch_to_date, date_to_epoch
from src.services.calculators import exports_good

class TestDateConversion(unittest.TestCase):
    def test_date_to_epoch(self):
        self.assertEqual(date_to_epoch("1905-01-01"), 0)
        self.assertEqual(date_to_epoch("1905-01-31"), 30)
        self.assertEqual(date_to_epoch("1906-01-15"), 379)
        self.assertEqual(date_to_epoch("1908-03-01"), 1154)

        for bad_date in ["01/01/1905", "1905-1-1", "1905-01-32", "April 15, 1906", "not-a-date", "", None, 19050101, True]:
            with self.assertRaises((ValueError, TypeError), msg=f"Failed with input {bad_date}"):
                date_to_epoch(bad_date)
        with self.assertRaises(ValueError):
            date_to_epoch("1904-12-31")
        with self.assertRaises(ValueError):
            date_to_epoch("1905-02-29")
        with self.assertRaises(ValueError):
            date_to_epoch("1905-04-31")

    def test_epoch_to_date(self):
        self.assertEqual(epoch_to_date(0), "1905-01-01")
        self.assertEqual(epoch_to_date(30), "1905-01-31")
        self.assertEqual(epoch_to_date(31), "1905-02-01")
        self.assertEqual(epoch_to_date(379), "1906-01-15")
        self.assertEqual(epoch_to_date(1153), "1908-02-28")
        self.assertEqual(epoch_to_date(1154), "1908-03-01")

        for bad_epoch in [-1, "30", 30.5, None, True]:
            with self.assertRaises((ValueError, TypeError), msg=f"Failed with input {bad_epoch}"):
                epoch_to_date(bad_epoch)

class TestExports(unittest.TestCase):
    def setUp(self):
        self.repo = GoogleSheetsRepository("mock_id")
        self.repo._cache["ref_location_goods"] = pd.DataFrame([
            {"location_key": "new_winchester", "good_key": "fuel"},
            {"location_key": "new_winchester", "good_key": "supplies"},
            {"location_key": "carillon", "good_key": "supplies"},
            {"location_key": "brabazon_workworld", "good_key": "fuel"}
        ])

    def test_exports(self):
        self.assertTrue(exports_good(self.repo, "new_winchester", "fuel"))
        self.assertTrue(exports_good(self.repo, "new_winchester", "supplies"))
        self.assertTrue(exports_good(self.repo, "carillon", "supplies"))
        self.assertFalse(exports_good(self.repo, "carillon", "fuel"))
        self.assertFalse(exports_good(self.repo, "brabazon_worlworld", "supplies"))
        self.assertFalse(exports_good(self.repo, "brabazon_worlworld", "dried_tea"))
        self.assertFalse(exports_good(self.repo, "company_house", "fuel"))
