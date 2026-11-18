#!/usr/bin/env python3
"""
Tier 2 Unit Test Suite for LLM Tool Registry, Guarded Engine Mutators,
Officer Rules, and Read-Only Service Calculators.
"""
import unittest
import pandas as pd

import src.tools.engine_tools  # noqa: F401 - ensures tools register on import
from src.connectors.google_sheets_repo import GoogleSheetsRepository
from src.exceptions import (
    DomainRuleError,
    EntityNotFoundError,
    InvalidTransitionError,
    MinistryOfStandardsError,
    ToolArgumentTypeError,
    UnknownToolError,
    ValidationError,
)
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
            {"property_key": "epoch", "property_value": 30},
            {"property_key": "current_date", "property_value": "1905-01-31"},
            {"property_key": "sovereigns", "property_value": 1000},
            {"property_key": "current_hull", "property_value": 80},
            {"property_key": "max_hull", "property_value": 100},
            {"property_key": "current_crew", "property_value": 18},
            {"property_key": "max_crew", "property_value": 20},
            {"property_key": "terror_level", "property_value": 15},
            {"property_key": "nightmares_level", "property_value": 0},
            {"property_key": "hidden_slots", "property_value": 2},
            {"property_key": "skill_iron", "property_value": 10},
            {"property_key": "skill_mirrors", "property_value": 3},
            {"property_key": "skill_hearts", "property_value": 6},
            {"property_key": "skill_veils", "property_value": 3},
            {"property_key": "affiliation_academe", "property_value": 0},
            {"property_key": "affiliation_bohemia", "property_value": 0},
            {"property_key": "affiliation_establishment", "property_value": 1},
            {"property_key": "affiliation_villainy", "property_value": 0}
        ])
        self.repo._cache["state_fsm"] = pd.DataFrame([
            {"property_key": "navigation_state", "property_value": "docked"},
            {"property_key": "current_location", "property_value": "new_winchester"},
            {"property_key": "last_location", "property_value": "new_winchester"},
        ])
        self.repo._cache["state_inventory"] = pd.DataFrame([
            {"good_key": "fuel", "hold_qty": 10, "bank_qty": 5, "average_unit_cost": 12.0},
            {"good_key": "supplies", "hold_qty": 8, "bank_qty": 2, "average_unit_cost": 18.0},
        ])
        self.repo._cache["ref_goods"] = pd.DataFrame([
            {"good_key": "fuel", "display_name": "Barrel of Fuel", "is_contraband": False},
            {"good_key": "supplies", "display_name": "Crate of Supplies", "is_contraband": False},
            {"good_key": "red_honey", "display_name": "Cask of Red Honey", "is_contraband": True},
            {"good_key": "bronzewood", "display_name": "Bronzewood", "is_contraband": False}
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
        self.repo._cache["ref_locations"] = pd.DataFrame([
            {"location_key": "new_winchester", "display_name": "New Winchester", "region_name": "The Reach"},
            {"location_key": "port_avon", "display_name": "Port Avon", "region_name": "The Reach"},
        ])

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
            "convert_date_to_epoch",
            "convert_epoch_to_date",
            "format_display_date",
            "get_bridge_report",
            "manage_itinerary",
            "chart_discovered_location",
            "log_bazaar_bargain",
            "upsert_action",
            "resolve_action",
            "publish_logbook",
            "depart_station",
            "arrive_station",
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
        self.assertTrue(dispatch_tool_call(self.repo, "adjust_scalar", {"property_key": "sovereigns", "delta": 50}))
        self.assertEqual(self.repo.get_cell("state_scalars", {"property_key": "sovereigns"}, "property_value"), 1050)

        # Hull repairs clamp at max_hull (100)
        self.assertTrue(dispatch_tool_call(self.repo, "adjust_scalar", {"property_key": "current_hull", "delta": 50}))
        self.assertEqual(self.repo.get_cell("state_scalars", {"property_key": "current_hull"}, "property_value"), 100)

        # FSM-managed keys live in state_fsm, not state_scalars, so set_scalar cannot mutate them
        with self.assertRaises(EntityNotFoundError):
            dispatch_tool_call(self.repo, "set_scalar", {"property_key": "navigation_state", "property_value": "enroute"})

    def test_buy_sell_and_transfer_goods(self):
        # Buy 4 bronzewood @ 25.0 -> appends row, deducts 100 sovereigns
        self.assertTrue(dispatch_tool_call(self.repo, "buy_goods", {"good_key": "bronzewood", "qty": 4, "unit_price": 25.0}))
        self.assertEqual(self.repo.get_cell("state_scalars", {"property_key": "sovereigns"}, "property_value"), 900)
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
        self.assertEqual(self.repo.get_cell("state_scalars", {"property_key": "sovereigns"}, "property_value"), 980)

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

    def test_depart_and_arrive_station_lifecycle(self):
        # Cannot arrive while docked
        with self.assertRaises(InvalidTransitionError):
            dispatch_tool_call(self.repo, "arrive_station", {"location_key": "port_avon"})

        # Depart station: docked -> departing (renders logbook) -> enroute
        dep_res = dispatch_tool_call(
            self.repo,
            "depart_station",
            {"narrative_counsel": "Steaming for Port Avon."},
        )
        self.assertEqual(dep_res["navigation_state"], "enroute")
        self.assertIn("CAPTAIN'S LOG", dep_res["logbook"])
        self.assertEqual(
            self.repo.get_cell("state_fsm", {"property_key": "navigation_state"}, "property_value"),
            "enroute",
        )

        # Dock-only tools and depart_station are blocked while enroute
        with self.assertRaises(InvalidTransitionError):
            dispatch_tool_call(self.repo, "depart_station", {})
        with self.assertRaises(InvalidTransitionError):
            dispatch_tool_call(self.repo, "buy_goods", {"good_key": "fuel", "qty": 1, "unit_price": 10.0})
        with self.assertRaises(InvalidTransitionError):
            dispatch_tool_call(self.repo, "sell_goods", {"good_key": "fuel", "qty": 1, "unit_price": 10.0})
        with self.assertRaises(InvalidTransitionError):
            dispatch_tool_call(self.repo, "transfer_inventory", {"good_key": "fuel", "direction": "deposit", "qty": 1})
        with self.assertRaises(InvalidTransitionError):
            dispatch_tool_call(self.repo, "assign_officer", {"officer_key": "clay_conductor", "officer_status": "active"})

        # Competing parameters are rejected without stranding state
        with self.assertRaises(ValidationError):
            dispatch_tool_call(
                self.repo,
                "arrive_station",
                {"location_key": "port_avon", "fuel_burned": 2, "fuel": 8},
            )
        self.assertEqual(
            self.repo.get_cell("state_fsm", {"property_key": "navigation_state"}, "property_value"),
            "enroute",
        )

        # Arrive using relative deltas: enroute -> arriving -> docked
        arr_res = dispatch_tool_call(
            self.repo,
            "arrive_station",
            {
                "location_key": "port_avon",
                "transit_days": 5,
                "fuel_burned": 3,
                "supplies_burned": 2,
                "hull_delta": -10,
            },
        )
        self.assertEqual(arr_res["navigation_state"], "docked")
        self.assertEqual(arr_res["epoch"], 35)
        self.assertEqual(self.repo.get_cell("state_fsm", {"property_key": "current_location"}, "property_value"), "port_avon")
        self.assertEqual(self.repo.get_cell("state_fsm", {"property_key": "last_location"}, "property_value"), "new_winchester")
        self.assertEqual(self.repo.get_cell("state_scalars", {"property_key": "current_hull"}, "property_value"), 70)
        self.assertEqual(self.repo.get_row("state_inventory", {"good_key": "fuel"})["hold_qty"], 7)
        self.assertEqual(self.repo.get_row("state_inventory", {"good_key": "supplies"})["hold_qty"], 6)

        # Second leg: test absolute values & Horological time anomaly warning
        self.repo.append_row("state_navigation_itinerary", {"sequence_order": 1, "location_key": "new_winchester", "action_summary": "Return"})
        dispatch_tool_call(self.repo, "depart_station", {"narrative_counsel": "Homeward bound."})
        anomaly_res = dispatch_tool_call(
            self.repo,
            "arrive_station",
            {
                "location_key": "new_winchester",
                "epoch": 20,
                "fuel": 5,
                "current_hull": 85,
            },
        )
        self.assertEqual(anomaly_res["navigation_state"], "docked")
        self.assertEqual(anomaly_res["epoch"], 20)
        self.assertTrue(any("Horological anomaly" in w for w in anomaly_res["warnings"]))
        self.assertEqual(self.repo.get_row("state_inventory", {"good_key": "fuel"})["hold_qty"], 5)
        self.assertEqual(self.repo.get_cell("state_scalars", {"property_key": "current_hull"}, "property_value"), 85)

    def test_custom_exceptions_and_ref_key_validation(self):
        # Unblocked identity/vessel scalars can be set via set_scalar
        for key, val in [
            ("first_mate_name", "Mr. Penn"),
            ("captain_name", "Captain Hawthorne"),
            ("vessel_name", "HMS Orpheus"),
            ("model", "Pellicle-class"),
        ]:
            # Ensure scalar row exists in mock state_scalars
            self.repo.append_row("state_scalars", {"property_key": key, "property_value": ""})
            self.assertTrue(dispatch_tool_call(self.repo, "set_scalar", {"property_key": key, "property_value": val}))
            self.assertEqual(self.repo.get_cell("state_scalars", {"property_key": key}, "property_value"), val)

        # Unknown good_key fails fast against ref_goods with EntityNotFoundError
        with self.assertRaises(EntityNotFoundError) as ctx:
            dispatch_tool_call(self.repo, "buy_goods", {"good_key": "imaginary_tea", "qty": 1, "unit_price": 10.0})
        self.assertIsInstance(ctx.exception, MinistryOfStandardsError)
        self.assertIn("ref_goods", str(ctx.exception))

        # Unknown officer_key fails fast against ref_officers with EntityNotFoundError
        with self.assertRaises(EntityNotFoundError):
            dispatch_tool_call(self.repo, "assign_officer", {"officer_key": "phantom_mate", "officer_status": "active"})

        # Bool/type mismatches raise ToolArgumentTypeError
        with self.assertRaises(ToolArgumentTypeError):
            dispatch_tool_call(self.repo, "buy_goods", {"good_key": "fuel", "qty": True, "unit_price": 10.0})

        # Out-of-range values raise ValidationError
        with self.assertRaises(ValidationError):
            dispatch_tool_call(self.repo, "buy_goods", {"good_key": "fuel", "qty": 0, "unit_price": 10.0})

        # Domain rule violations raise DomainRuleError
        with self.assertRaises(DomainRuleError):
            dispatch_tool_call(self.repo, "buy_goods", {"good_key": "fuel", "qty": 500, "unit_price": 10.0})

        # Unexposed tool raises UnknownToolError
        with self.assertRaises(UnknownToolError):
            dispatch_tool_call(self.repo, "nonexistent_tool", {})

    def test_calendar_and_date_formatting_tools(self):
        self.assertEqual(dispatch_tool_call(self.repo, "convert_date_to_epoch", {"iso_date": "1905-01-31"}), 30)
        self.assertEqual(dispatch_tool_call(self.repo, "convert_epoch_to_date", {"epoch": 30}), "1905-01-31")
        self.assertEqual(dispatch_tool_call(self.repo, "format_display_date", {"epoch": 30}), "31 January, 1905")
        self.assertEqual(dispatch_tool_call(self.repo, "format_display_date", {"iso_date": "1905-02-15"}), "15 February, 1905")

        # Competing or missing date arguments raise ValidationError
        with self.assertRaises(ValidationError):
            dispatch_tool_call(self.repo, "format_display_date", {"iso_date": "1905-01-31", "epoch": 30})
        with self.assertRaises(ValidationError):
            dispatch_tool_call(self.repo, "format_display_date", {})
        with self.assertRaises(ValidationError):
            dispatch_tool_call(self.repo, "convert_date_to_epoch", {"iso_date": "1904-12-31"})


if __name__ == "__main__":
    unittest.main()