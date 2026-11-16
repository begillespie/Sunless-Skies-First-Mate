#!/usr/bin/env python3
"""
Tier 2 Unit Test Suite for LLM Tool Registry, Guarded Engine Mutators,
Officer Rules, and Read-Only Service Calculators.
"""
import unittest
import pandas as pd

import src.tools.engine_tools  # noqa: F401 - ensures tools register on import
from src.connectors.google_sheets_repo import GoogleSheetsRepository
from src.services.calculators import (
    calculate_attribute_perks,
    compute_hold_utilization,
    compute_mac,
)
from src.tools.registry import (
    TOOL_REGISTRY,
    dispatch_tool_call,
    get_tool_declarations,
)


class TestToolsAndRegistry(unittest.TestCase):

    def setUp(self):
        self.repo = GoogleSheetsRepository("mock_id")
        self.repo._cache["state_scalars"] = pd.DataFrame([
            {"key": "epoch", "value": 30},
            {"key": "current_date", "value": "1905-01-31"},
            {"key": "navigation_state", "value": "docked"},
            {"key": "sovereigns", "value": 1000},
            {"key": "current_hull", "value": 80},
            {"key": "max_hull", "value": 100},
            {"key": "current_crew", "value": 18},
            {"key": "max_crew", "value": 20},
            {"key": "terror_level", "value": 15},
            {"key": "nightmares_level", "value": 0},
            {"key": "hidden_slots", "value": 2},
            {"key": "current_location", "value": "new_winchester"},
            {"key": "skill_iron", "value": 10},
            {"key": "skill_mirrors", "value": 3},
            {"key": "skill_hearts", "value": 6},
            {"key": "skill_veils", "value": 3},
            {"key": "affiliation_academe", "value": 0},
            {"key": "affiliation_bohemia", "value": 0},
            {"key": "affiliation_establishment", "value": 1},
            {"key": "affiliation_villainy", "value": 0}
        ])
        self.repo._cache["state_inventory"] = pd.DataFrame([
            {"good_key": "fuel", "hold_qty": 10, "bank_qty": 5, "average_unit_cost": 12.0},
            {"good_key": "supplies", "hold_qty": 8, "bank_qty": 2, "average_unit_cost": 18.0},
        ])
        self.repo._cache["ref_goods"] = pd.DataFrame([
            {"good_key": "fuel", "is_contraband": False},
            {"good_key": "supplies", "is_contraband": False},
            {"good_key": "red_honey", "is_contraband": True},
            {"good_key": "bronzewood", "is_contraband": False}
        ])
        self.repo._cache["ref_officers"] = pd.DataFrame([
            {
                "officer_key": "incautious_driver",
                "name": "Incautious Driver",
                "station": "chief_engineer",
                "lineage": "driver",
                "tier": 1,
                "skill_iron": 2, "skill_mirrors": 0, "skill_hearts": 0, "skill_veils": 0,
                "affiliation_academe": 0, "affiliation_bohemia": 0,
                "affiliation_establishment": 0, "affiliation_villainy": 0,
            },
            {
                "officer_key": "reckless_driver",
                "name": "Reckless Driver",
                "station": "chief_engineer",
                "lineage": "driver",
                "tier": 2,
                "skill_iron": 5, "skill_mirrors": 0, "skill_hearts": -1, "skill_veils": 0,
                "affiliation_academe": 0, "affiliation_bohemia": 0,
                "affiliation_establishment": 0, "affiliation_villainy": 1,
            },
            {
                "officer_key": "clay_conductor",
                "name": "Clay Conductor",
                "station": "chief_engineer",
                "lineage": "conductor",
                "tier": 1,
                "skill_iron": 0, "skill_mirrors": 4, "skill_hearts": 0, "skill_veils": 0,
                "affiliation_academe": 1, "affiliation_bohemia": 0,
                "affiliation_establishment": 0, "affiliation_villainy": 0,
            },
        ])
        self.repo._cache["state_officers"] = pd.DataFrame([
            {"officer_key": "incautious_driver", "officer_status": "active"},
            {"officer_key": "clay_conductor", "officer_status": "unassigned"},
        ])
        self.repo._cache["state_navigation_itinerary"] = pd.DataFrame([
            {"sequence_order": 1, "location_key": "port_avon", "action_summary": "Deliver cargo"},
        ])
        self.repo._cache["state_navigation_history"] = pd.DataFrame(
            columns=["sequence_order", "location_key", "action_summary"]
        )

    def test_registry_schema_generation_and_isolation(self):
        declarations = get_tool_declarations()
        decl_map = {d["name"]: d for d in declarations}

        expected_tools = {
            "adjust_scalar",
            "set_scalar",
            "set_game_epoch",
            "buy_goods",
            "sell_goods",
            "adjust_hold_qty",
            "transfer_inventory",
            "assign_officer",
            "transition_navigation",
        }
        self.assertEqual(set(decl_map.keys()), expected_tools)

        # Ensure 'repo' is stripped from every parameter schema
        for decl in declarations:
            self.assertNotIn("repo", decl["parameters"]["properties"])
            self.assertNotIn("repo", decl["parameters"]["required"])

        # Ensure Literal compiles to enum
        transfer_props = decl_map["transfer_inventory"]["parameters"]["properties"]
        self.assertEqual(transfer_props["direction"]["enum"], ["deposit", "withdraw"])

        # Ensure read-only helpers are blocked from LLM dispatch
        with self.assertRaises(KeyError):
            dispatch_tool_call(self.repo, "compute_mac", {"good_key": "fuel", "acquired_qty": 2, "unit_price": 10})

    def test_adjust_and_set_scalar_guards(self):
        # Loot 50 sovereigns from Marauder wreckage
        self.assertTrue(dispatch_tool_call(self.repo, "adjust_scalar", {"key": "sovereigns", "delta": 50}))
        self.assertEqual(self.repo.get_cell("state_scalars", {"key": "sovereigns"}, "value"), 1050)

        # Hull repairs clamp at max_hull (100)
        self.assertTrue(dispatch_tool_call(self.repo, "adjust_scalar", {"key": "current_hull", "delta": 50}))
        self.assertEqual(self.repo.get_cell("state_scalars", {"key": "current_hull"}, "value"), 100)

        # Protected scalar cannot be mutated directly
        with self.assertRaises(ValueError):
            dispatch_tool_call(self.repo, "set_scalar", {"key": "navigation_state", "value": "enroute"})

    def test_buy_sell_and_transfer_goods(self):
        # Buy 4 bronzewood @ 25.0 -> appends row, deducts 100 sovereigns
        self.assertTrue(dispatch_tool_call(self.repo, "buy_goods", {"good_key": "bronzewood", "qty": 4, "unit_price": 25.0}))
        self.assertEqual(self.repo.get_cell("state_scalars", {"key": "sovereigns"}, "value"), 900)
        bw_row = self.repo.get_row("state_inventory", {"good_key": "bronzewood"})
        self.assertEqual(bw_row["hold_qty"], 4)
        self.assertEqual(bw_row["average_unit_cost"], 25.0)

        # Compute MAC helper has zero side effects
        self.assertEqual(compute_mac(self.repo, "bronzewood", 4, 25.0), 25.0)

        # Deposit 2 bronzewood to bank via update_row-backed transfer_inventory
        self.assertTrue(dispatch_tool_call(self.repo, "transfer_inventory", {"good_key": "bronzewood", "direction": "deposit", "qty": 2}))
        bw_row = self.repo.get_row("state_inventory", {"good_key": "bronzewood"})
        self.assertEqual(bw_row["hold_qty"], 2)
        self.assertEqual(bw_row["bank_qty"], 2)

        # Sell remaining 2 in hold -> row remains because bank_qty == 2
        self.assertTrue(dispatch_tool_call(self.repo, "sell_goods", {"good_key": "bronzewood", "qty": 2, "unit_price": 40.0}))
        self.assertEqual(self.repo.get_cell("state_scalars", {"key": "sovereigns"}, "value"), 980)

        # Withdraw 2 and sell 2 -> total stock hits 0, non-baseline row is deleted
        dispatch_tool_call(self.repo, "transfer_inventory", {"good_key": "bronzewood", "direction": "withdraw", "qty": 2})
        dispatch_tool_call(self.repo, "sell_goods", {"good_key": "bronzewood", "qty": 2, "unit_price": 40.0})
        with self.assertRaises(LookupError):
            self.repo.get_row("state_inventory", {"good_key": "bronzewood"})

    def test_hold_utilization_contraband_spillover(self):
        # Add 3 red_honey (contraband) against 2 hidden_slots -> 2 hidden, 1 spillover + 18 standard = 19 standard
        dispatch_tool_call(self.repo, "adjust_hold_qty", {"good_key": "red_honey", "delta": 3})
        util = compute_hold_utilization(self.repo)
        self.assertEqual(util, {"standard_hold_used": 19, "hidden_hold_used": 2})

    def test_officer_rules_and_attribute_perks(self):
        # Station exclusivity: activating clay_conductor demotes incautious_driver
        self.assertTrue(dispatch_tool_call(self.repo, "assign_officer", {"officer_key": "clay_conductor", "officer_status": "active"}))
        self.assertEqual(
            self.repo.get_cell("state_officers", {"officer_key": "incautious_driver"}, "officer_status"),
            "unassigned",
        )

        # Lineage upgrade: activating reckless_driver (Tier 2) purges incautious_driver (Tier 1) and demotes clay_conductor
        self.assertTrue(dispatch_tool_call(self.repo, "assign_officer", {"officer_key": "reckless_driver", "officer_status": "active"}))
        roster_keys = set(self.repo.get_table("state_officers")["officer_key"])
        self.assertNotIn("incautious_driver", roster_keys)
        self.assertEqual(
            self.repo.get_cell("state_officers", {"officer_key": "clay_conductor"}, "officer_status"),
            "unassigned",
        )

        # Downgrade blocked
        with self.assertRaises(ValueError):
            dispatch_tool_call(self.repo, "assign_officer", {"officer_key": "incautious_driver", "officer_status": "unassigned"})

        # Attribute perks calculation
        totals = calculate_attribute_perks(self.repo)
        self.assertEqual(totals["skill_iron"], 15)
        self.assertEqual(totals["skill_hearts"], 5)
        self.assertEqual(totals["affiliation_villainy"], 1)
        self.assertEqual(totals["affiliation_establishment"], 1)

    def test_transition_navigation_via_dispatch(self):
        self.assertTrue(dispatch_tool_call(self.repo, "transition_navigation", {"action": "DEPART"}))
        self.assertEqual(self.repo.get_cell("state_scalars", {"key": "navigation_state"}, "value"), "departing")


if __name__ == "__main__":
    unittest.main()