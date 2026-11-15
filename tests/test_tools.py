#!/usr/bin/env python3
"""
Tier 2 Unit Test Suite for engine_tools.py and ui_renderer.py.
Covers valid operational inputs, boundary conditions, and all variants of invalid inputs.
"""
import unittest

from src.tools.engine_tools import (
    date_to_epoch,
    epoch_to_date,
    compute_mac,
    compute_hold_utilization,
    transfer_inventory,
)
from src.tools.ui_tools import (
    vitals_badge,
    terror_badge,
    reserve_badge,
    calculate_stats,
)


class TestEngineTools(unittest.TestCase):
    def test_date_to_epoch_valid(self):
        self.assertEqual(date_to_epoch("1905-01-01"), 0)
        self.assertEqual(date_to_epoch("1905-01-31"), 30)
        self.assertEqual(date_to_epoch("1906-01-15"), 379)
        self.assertEqual(date_to_epoch("1908-03-01"), 1154)

    def test_date_to_epoch_invalid_inputs(self):
        for bad_date in ["01/01/1905", "1905-1-1", "1905-01-32", "April 15, 1906", "not-a-date", "", None, 19050101, True]:
            with self.assertRaises((ValueError, TypeError), msg=f"Failed with input {bad_date}"):
                date_to_epoch(bad_date)
        with self.assertRaises(ValueError):
            date_to_epoch("1904-12-31")
        with self.assertRaises(ValueError):
            date_to_epoch("1905-02-29")
        with self.assertRaises(ValueError):
            date_to_epoch("1905-04-31")

    def test_epoch_to_date_valid(self):
        self.assertEqual(epoch_to_date(0), "1905-01-01")
        self.assertEqual(epoch_to_date(30), "1905-01-31")
        self.assertEqual(epoch_to_date(31), "1905-02-01")
        self.assertEqual(epoch_to_date(379), "1906-01-15")
        self.assertEqual(epoch_to_date(1153), "1908-02-28")
        self.assertEqual(epoch_to_date(1154), "1908-03-01")

    def test_epoch_to_date_invalid_inputs(self):
        for bad_epoch in [-1, "30", 30.5, None, True]:
            with self.assertRaises((ValueError, TypeError), msg=f"Failed with input {bad_epoch}"):
                epoch_to_date(bad_epoch)

    def test_compute_mac_valid(self):
        self.assertEqual(compute_mac(2, 60.0, 4, 30.0), 40.0)
        self.assertEqual(compute_mac(0, 0.0, 5, 20.0), 20.0)
        self.assertEqual(compute_mac(0, 0.0, 0, 50.0), 0.0)

    def test_compute_mac_invalid_inputs(self):
        for bad_args in [
            (-1, 60.0, 4, 30.0),
            (2, -60.0, 4, 30.0),
            (2, 60.0, -4, 30.0),
            (2, 60.0, 4, -30.0),
            ("2", 60.0, 4, 30.0),
            (2, True, 4, 30.0),
        ]:
            with self.assertRaises((ValueError, TypeError), msg=f"Failed with input {bad_args}"):
                compute_mac(*bad_args)

    def test_compute_hold_utilization_valid(self):
        inv = [{"good_key": "fuel", "hold_qty": 3}, {"good_key": "illicit_literature", "hold_qty": 2}]
        res = compute_hold_utilization(inv, 4)
        self.assertEqual(res, {"standard_hold_used": 3, "hidden_hold_used": 2})

        res2 = compute_hold_utilization(inv, 1)
        self.assertEqual(res2, {"standard_hold_used": 4, "hidden_hold_used": 1})

    def test_compute_hold_utilization_invalid_inputs(self):
        with self.assertRaises((ValueError, TypeError)):
            compute_hold_utilization([{"good_key": "fuel", "hold_qty": -1}], 4)
        with self.assertRaises((ValueError, TypeError)):
            compute_hold_utilization([{"good_key": "fuel", "hold_qty": 3}], -1)
        with self.assertRaises((ValueError, TypeError)):
            compute_hold_utilization("not-an-iterable", 4) #type: ignore
        with self.assertRaises((ValueError, TypeError)):
            compute_hold_utilization([{"missing_keys": 1}], 4)

    def test_transfer_inventory_valid(self):
        row = ["fuel", 4, 0, 20.0]
        self.assertEqual(transfer_inventory(row, "deposit", 1), "fuel,3,1,20.00")
        row2 = ["supplies", 2, 3, 40.0]
        self.assertEqual(transfer_inventory(row2, "withdraw", 2), "supplies,4,1,40.00")

    def test_transfer_inventory_invalid_inputs(self):
        with self.assertRaises(ValueError):
            transfer_inventory(["fuel", 1, 2, 20.0], "deposit", 3)
        with self.assertRaises(ValueError):
            transfer_inventory(["fuel", 1, 2, 20.0], "withdraw", 5)
        with self.assertRaises(ValueError):
            transfer_inventory(["fuel", 4, 0, 20.0], "deposit", 0)
        with self.assertRaises(ValueError):
            transfer_inventory(["fuel", 4, 0, 20.0], "deposit", -2)
        with self.assertRaises(ValueError):
            transfer_inventory(["fuel", 4, 0, 20.0], "transfer", 1) #type: ignore
        with self.assertRaises(ValueError):
            transfer_inventory(["fuel", 4], "deposit", 1)
        for bad_val in ["4", -1, 10.5, True]:
            with self.assertRaises((ValueError, TypeError), msg=f"Failed with input {bad_val}"):
                transfer_inventory(["fuel", bad_val, 0, 20.0], "deposit", 1)


class TestUIRenderer(unittest.TestCase):
    def test_vitals_badge_valid(self):
        self.assertEqual(vitals_badge(8, 10), "🟢")
        self.assertEqual(vitals_badge(5, 10), "🟡")
        self.assertEqual(vitals_badge(2, 10), "🔴")

    def test_vitals_badge_invalid_inputs(self):
        for args in [(-1, 10), (8, 0), (8, -5), ("8", 10), (8, "10"), (True, 10), (8, False)]:
            with self.assertRaises((ValueError, TypeError), msg=f"Failed with input {args}"):
                vitals_badge(*args)

    def test_terror_badge_valid(self):
        self.assertEqual(terror_badge(20), "🟢")
        self.assertEqual(terror_badge(50), "🟡")
        self.assertEqual(terror_badge(80), "🔴")

    def test_terror_badge_invalid_inputs(self):
        for bad_t in [-1, 101, "50", 45.5, True, None]:
            with self.assertRaises((ValueError, TypeError), msg=f"Failed with input {bad_t}"):
                terror_badge(bad_t)

    def test_reserve_badge_valid(self):
        self.assertEqual(reserve_badge(4, 3), "🟢")
        self.assertEqual(reserve_badge(3, 3), "⚠️")
        self.assertEqual(reserve_badge(1, 3), "🚨")

    def test_reserve_badge_invalid_inputs(self):
        for args in [(-1, 3), (4, -1), ("4", 3), (4, "3"), (True, 3), (4, True)]:
            with self.assertRaises((ValueError, TypeError), msg=f"Failed with input {args}"):
                reserve_badge(*args)

    def test_calculate_stats_valid(self):
        base = {"iron": 10, "mirrors": 3, "hearts": 6, "veils": 3, "academe": 0, "bohemia": 0, "establishment": 1, "villainy": 0}
        officers = [
            {"officer_key": "aunt_inconvenient", "officer_status": "active", "perk_iron": 6, "perk_veils": 2},
            {"officer_key": "forged-companion_pugilistic","officer_status": "unassigned", "perk_iron": 10},
            {"officer_key": "navigator_fortunate", "officer_status": "active", "perk_establishment": 1}
        ]
        res = calculate_stats(base, officers)
        self.assertEqual(res["iron"], 16)
        self.assertEqual(res["mirrors"], 3)
        self.assertEqual(res["veils"], 5)
        self.assertEqual(res["establishment"], 2)

        officers = [
            {"officer_key": "aunt_inconvenient", "officer_status": "active", "perk_iron": 6, "perk_veils": 2},
            {"officer_key": "mascot_dilly", "officer_status": "active", "perk_hearts": -1},
            {"officer_key": "navigator_fortunate", "officer_status": "active", "perk_establishment": 1}
        ]
        res = calculate_stats(base, officers)
        self.assertEqual(res["hearts"], 5)


    def test_calculate_stats_invalid_inputs(self):
        base = {"iron": 10, "mirrors": 3, "hearts": 6, "veils": 3, "academe": 0, "bohemia": 0, "establishment": 1, "villainy": 0}
        with self.assertRaises(TypeError):
            calculate_stats("not-a-dict", []) #type: ignore
        with self.assertRaises(ValueError):
            calculate_stats({"iron": -10}, [])
        with self.assertRaises(TypeError):
            calculate_stats(base, ["not-a-dict"]) #type: ignore
        with self.assertRaises(ValueError):
            calculate_stats(base, [{"officer_key": "aunt_inconvenient", "officer_status": "active", "perk_iron": "ten"}])
        with self.assertRaises(ValueError):
            calculate_stats(base, [{"officer_key": "aunt_inconvenient", "officer_status": "active", "perk_hearts": -1}])
        with self.assertRaises(ValueError):
            calculate_stats(base, [{"officer_key": "aunt_inconvenient", "officer_status": "active", "perk_bohemia": -1}])


if __name__ == "__main__":
    unittest.main()