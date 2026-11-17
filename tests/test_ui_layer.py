#!/usr/bin/env python3
"""
Tier 2 UI Unit Test Suite (Step 3.4):
Covers src/ui/ui_tools.py, src/ui/logbook_service.py, src/ui/ui_renderer.py,
and Jinja2 rendering of src/templates/logbook.j2 with StrictUndefined.
Seed tables strictly follow data/data_package.json and data/tables/state_scalars.csv.
"""
import unittest
from jinja2 import UndefinedError
import pandas as pd

from src.connectors.google_sheets_repo import GoogleSheetsRepository
from src.ui.logbook_service import (
    _assemble_attributes,
    _assemble_header_vitals,
    _assemble_inventory,
    _assemble_navigation,
    _assemble_officers,
    _load_scalars_dict,
    should_render_logbook,
)
from src.ui.ui_renderer import render_logbook, render_template
from src.ui.ui_tools import (
    format_iso_date,
    format_officer_perks,
    nightmares_badge,
    reserve_badge,
    resupply_badge,
    terror_badge,
    vitals_badge,
)


class TestUILayer(unittest.TestCase):

    def setUp(self):
        self.repo = GoogleSheetsRepository("mock_id")

        # state_scalars schema: domain_group, property_key, property_value, data_type, description
        self.repo._cache["state_scalars"] = pd.DataFrame([
            {"domain_group": "captain", "property_key": "captain_name", "property_value": "Captain Hawthorne", "data_type": "string", "description": "Active captain's callsign"},
            {"domain_group": "session", "property_key": "first_mate_name", "property_value": "Mr. Penn", "data_type": "string", "description": "Active first mate name"},
            {"domain_group": "locomotive", "property_key": "vessel_name", "property_value": "HMS Orpheus", "data_type": "string", "description": "Name of the vessel"},
            {"domain_group": "locomotive", "property_key": "model", "property_value": "Pellicle-class", "data_type": "string", "description": "Locomotive class model"},
            {"domain_group": "session", "property_key": "current_location_key", "property_value": "new_winchester", "data_type": "string", "description": "Current location key"},
            {"domain_group": "session", "property_key": "last_location_visited_key", "property_value": "new_winchester", "data_type": "string", "description": "Last visited location key"},
            {"domain_group": "session", "property_key": "current_epoch", "property_value": 30, "data_type": "integer", "description": "Current game time epoch"},
            {"domain_group": "session", "property_key": "navigation_state", "property_value": "docked", "data_type": "string", "description": "Navigation state"},
            {"domain_group": "session", "property_key": "sovereigns", "property_value": 1250, "data_type": "integer", "description": "Sovereigns currency balance"},
            {"domain_group": "locomotive", "property_key": "current_hull", "property_value": 85, "data_type": "integer", "description": "Current hull integrity"},
            {"domain_group": "locomotive", "property_key": "max_hull", "property_value": 100, "data_type": "integer", "description": "Maximum hull integrity"},
            {"domain_group": "crew", "property_key": "current_crew", "property_value": 10, "data_type": "integer", "description": "Current number of crew aboard"},
            {"domain_group": "crew", "property_key": "max_crew", "property_value": 20, "data_type": "integer", "description": "Maximum crew capacity"},
            {"domain_group": "crew", "property_key": "terror", "property_value": 32, "data_type": "integer", "description": "Current terror level (0-100)"},
            {"domain_group": "crew", "property_key": "nightmares", "property_value": 2, "data_type": "integer", "description": "Current nightmares level (0-4)"},
            {"domain_group": "locomotive", "property_key": "hold_capacity", "property_value": 30, "data_type": "integer", "description": "Cargo hold capacity"},
            {"domain_group": "locomotive", "property_key": "hidden_slots", "property_value": 2, "data_type": "integer", "description": "Hidden contraband slot capacity"},
            {"domain_group": "locomotive", "property_key": "reserve_fuel_min", "property_value": 5, "data_type": "integer", "description": "Minimum reserve fuel threshold"},
            {"domain_group": "locomotive", "property_key": "reserve_supplies_min", "property_value": 5, "data_type": "integer", "description": "Minimum reserve supplies threshold"},
            {"domain_group": "captain", "property_key": "skill_iron", "property_value": 10, "data_type": "integer", "description": "Iron attribute score"},
            {"domain_group": "captain", "property_key": "skill_mirrors", "property_value": 4, "data_type": "integer", "description": "Mirrors attribute score"},
            {"domain_group": "captain", "property_key": "skill_hearts", "property_value": 6, "data_type": "integer", "description": "Hearts attribute score"},
            {"domain_group": "captain", "property_key": "skill_veils", "property_value": 3, "data_type": "integer", "description": "Veils attribute score"},
            {"domain_group": "captain", "property_key": "affiliation_academe", "property_value": 1, "data_type": "integer", "description": "Academe affiliation rank"},
            {"domain_group": "captain", "property_key": "affiliation_bohemia", "property_value": 0, "data_type": "integer", "description": "Bohemia affiliation rank"},
            {"domain_group": "captain", "property_key": "affiliation_establishment", "property_value": 2, "data_type": "integer", "description": "Establishment affiliation rank"},
            {"domain_group": "captain", "property_key": "affiliation_villainy", "property_value": 0, "data_type": "integer", "description": "Villainy affiliation rank"},
        ])

        # state_inventory schema: good_key, hold_qty, bank_qty, average_unit_cost
        self.repo._cache["state_inventory"] = pd.DataFrame([
            {"good_key": "fuel", "hold_qty": 8, "bank_qty": 4, "average_unit_cost": 12.5},
            {"good_key": "supplies", "hold_qty": 3, "bank_qty": 0, "average_unit_cost": 18.0},
            {"good_key": "red_honey", "hold_qty": 3, "bank_qty": 0, "average_unit_cost": 95.0},
        ])

        # ref_goods schema: good_key, display_name, base_price, weight, is_contraband
        self.repo._cache["ref_goods"] = pd.DataFrame([
            {"good_key": "fuel", "display_name": "Barrel of Fuel", "base_price": 15, "weight": 1, "is_contraband": False},
            {"good_key": "supplies", "display_name": "Crate of Supplies", "base_price": 20, "weight": 1, "is_contraband": False},
            {"good_key": "red_honey", "display_name": "Cask of Red Honey", "base_price": 100, "weight": 1, "is_contraband": True},
        ])

        # ref_officers schema: officer_key, lexical_name, lineage, parent_key, position_slot, tier,
        #                      academe, bohemia, establishment, villainy, hearts, iron, mirrors, veils
        self.repo._cache["ref_officers"] = pd.DataFrame([
            {
                "officer_key": "reckless_driver",
                "lexical_name": "Reckless Driver",
                "lineage": "driver",
                "parent_key": "",
                "position_slot": "chief_engineer",
                "tier": 2,
                "academe": 0,
                "bohemia": 0,
                "establishment": 0,
                "villainy": 1,
                "hearts": -1,
                "iron": 5,
                "mirrors": 0,
                "veils": 0,
            },
            {
                "officer_key": "rat_brigade",
                "lexical_name": "The Rat Brigade",
                "lineage": "mascot_rat",
                "parent_key": "",
                "position_slot": "mascot",
                "tier": 1,
                "academe": 0,
                "bohemia": 1,
                "establishment": 0,
                "villainy": 0,
                "hearts": 0,
                "iron": 0,
                "mirrors": 2,
                "veils": 3,
            },
        ])

        # state_officers schema: officer_key, officer_status
        self.repo._cache["state_officers"] = pd.DataFrame([
            {"officer_key": "reckless_driver", "officer_status": "active"},
            {"officer_key": "rat_brigade", "officer_status": "seconded"},
        ])

        # state_navigation_itinerary schema: sequence_order, location_key
        self.repo._cache["state_navigation_itinerary"] = pd.DataFrame([
            {"sequence_order": 2, "location_key": "pan"},
            {"sequence_order": 1, "location_key": "port_avon"},
        ])

        # ref_locations schema: location_key, display_name, region, ring_depth, location_type, waypoint_location_key, lore_snippet
        self.repo._cache["ref_locations"] = pd.DataFrame([
            {"location_key": "new_winchester", "display_name": "New Winchester", "region": "reach", "ring_depth": "center", "location_type": "port", "waypoint_location_key": "", "lore_snippet": "The capital of the Reach."},
            {"location_key": "port_avon", "display_name": "Port Avon", "region": "reach", "ring_depth": "inner", "location_type": "port", "waypoint_location_key": "", "lore_snippet": "Fog-wreathed customs quay."},
            {"location_key": "pan", "display_name": "Pan (Eleutheria)", "region": "eleutheria", "ring_depth": "center", "location_type": "port", "waypoint_location_key": "", "lore_snippet": "City of eternal night."},
            {"location_key": "london", "display_name": "London", "region": "albion", "ring_depth": "center", "location_type": "port", "waypoint_location_key": "", "lore_snippet": "The Empress's seat."},
            {"location_key": "magdalenes", "display_name": "Magdalene's", "region": "reach", "ring_depth": "middle", "location_type": "port", "waypoint_location_key": "", "lore_snippet": "A quiet sanctuary."},
        ])

        # ref_location_goods schema: location_key, good_key
        self.repo._cache["ref_location_goods"] = pd.DataFrame([
            {"location_key": "port_avon", "good_key": "fuel"},
            {"location_key": "port_avon", "good_key": "supplies"},
            {"location_key": "pan", "good_key": "supplies"},
        ])

        # state_action schema: action_id, parent_action_id, title, action_type, action_status,
        #                      target_location_key, target_entity_key, quantity_required, quantity_delivered,
        #                      priority, is_pinned, created_epoch, updated_epoch, deadline_epoch, notes
        self.repo._cache["state_action"] = pd.DataFrame([
            {
                "action_id": "ACT-1000",
                "parent_action_id": "",
                "title": "Offload Red Honey",
                "action_type": "prospect",
                "action_status": "active",
                "target_location_key": "port_avon",
                "target_entity_key": "red_honey",
                "quantity_required": 3,
                "quantity_delivered": 0,
                "priority": "routine",
                "is_pinned": False,
                "created_epoch": 20,
                "updated_epoch": 30,
                "deadline_epoch": "",
                "notes": "Deliver to customs contact.",
            },
            {
                "action_id": "ACT-1001",
                "parent_action_id": "",
                "title": "Deliver Royal Dispatches",
                "action_type": "ambition",
                "action_status": "active",
                "target_location_key": "pan",
                "target_entity_key": "",
                "quantity_required": 1,
                "quantity_delivered": 0,
                "priority": "high",
                "is_pinned": False,
                "created_epoch": 22,
                "updated_epoch": 30,
                "deadline_epoch": "",
                "notes": "Bring Establishment credentials.",
            },
            {
                "action_id": "ACT-1002",
                "parent_action_id": "",
                "title": "The Smuggler's Debt",
                "action_type": "quest",
                "action_status": "active",
                "target_location_key": "london",
                "target_entity_key": "",
                "quantity_required": 1,
                "quantity_delivered": 0,
                "priority": "high",
                "is_pinned": True,
                "created_epoch": 15,
                "updated_epoch": 30,
                "deadline_epoch": "",
                "notes": "Settle ledger in London.",
            },
            {
                "action_id": "ACT-1003",
                "parent_action_id": "",
                "title": "Pensive Curate",
                "action_type": "passenger",
                "action_status": "active",
                "target_location_key": "port_avon",
                "target_entity_key": "",
                "quantity_required": 1,
                "quantity_delivered": 0,
                "priority": "routine",
                "is_pinned": False,
                "created_epoch": 25,
                "updated_epoch": 30,
                "deadline_epoch": 45,
                "notes": "First-Class Cabin",
            },
            {
                "action_id": "ACT-1004",
                "parent_action_id": "",
                "title": "Secondment: The Rat Brigade",
                "action_type": "secondment",
                "action_status": "active",
                "target_location_key": "magdalenes",
                "target_entity_key": "rat_brigade",
                "quantity_required": 1,
                "quantity_delivered": 0,
                "priority": "low",
                "is_pinned": False,
                "created_epoch": 26,
                "updated_epoch": 30,
                "deadline_epoch": 40,
                "notes": "Investigating cellar vaults",
            },
        ])

    def test_ui_tools_badge_boundaries(self):
        self.assertEqual(vitals_badge(70, 100), "🟢")
        self.assertEqual(vitals_badge(50, 100), "🟡")
        self.assertEqual(vitals_badge(20, 100), "🔴")
        self.assertEqual(vitals_badge(0, 100), "🔴")

        self.assertEqual(reserve_badge(6, 5), "🟢")
        self.assertEqual(reserve_badge(5, 5), "⚠️")
        self.assertEqual(reserve_badge(4, 5), "🔴")
        self.assertEqual(reserve_badge(3, 5), "🔴")
        self.assertEqual(reserve_badge(2, 5), "🚨")
        self.assertEqual(reserve_badge(3, 6), "🔴")

        self.assertEqual(terror_badge(0), "🟢")
        self.assertEqual(terror_badge(49), "🟡")
        self.assertEqual(terror_badge(50), "🔴")
        self.assertEqual(terror_badge(75), "🚨")
        self.assertEqual(terror_badge(100), "🚨")

        self.assertEqual(nightmares_badge(0), "🟢")
        self.assertEqual(nightmares_badge(1), "🟡")
        self.assertEqual(nightmares_badge(2), "🔴")
        self.assertEqual(nightmares_badge(3), "🚨")
        self.assertEqual(nightmares_badge(4), "🚨")

        self.assertEqual(resupply_badge(True, True), "🟢")
        self.assertEqual(resupply_badge(True, False), "🟡")
        self.assertEqual(resupply_badge(False, True), "🟡")
        self.assertEqual(resupply_badge(False, False), "🔴")

    def test_ui_tools_date_formatting(self):
        self.assertEqual(format_iso_date("1905-01-31"), "31 January, 1905")
        self.assertEqual(format_iso_date("1906-11-05"), "5 November, 1906")

    def test_ui_tools_officer_perk_formatting(self):
        row = {
            "iron": 5,
            "mirrors": 0,
            "hearts": -1,
            "veils": 0,
            "villainy": 1,
        }
        self.assertEqual(format_officer_perks(row, "skill_"), "+5 Iron, -1 Hearts")
        self.assertEqual(format_officer_perks(row, "affiliation_"), "+1 Villainy")
        self.assertEqual(format_officer_perks({}, "skill_"), "—")

    # ------------------------------------------------------------------
    # Incremental Section Builder Tests
    # ------------------------------------------------------------------

    def test_assemble_header_vitals(self):
        scalars = _load_scalars_dict(self.repo)
        header = _assemble_header_vitals(self.repo, scalars)

        self.assertEqual(header["display_date"], "31 January, 1905")
        self.assertEqual(header["epoch"], 30)
        self.assertEqual(header["location_name"], "New Winchester")
        self.assertEqual(header["kinetic_state"], "🟢 Docked")
        self.assertEqual(header["captain_name"], "Captain Hawthorne")
        self.assertEqual(header["first_mate_name"], "Mr. Penn")
        self.assertEqual(header["vessel_name"], "HMS Orpheus")
        self.assertEqual(header["model"], "Pellicle-class")
        self.assertEqual(header["sovereigns"], 1250)
        self.assertEqual(header["hull_badge"], "🟢")
        self.assertEqual(header["crew_badge"], "🟡")
        self.assertEqual(header["terror_badge"], "🟡")
        self.assertEqual(header["nightmares_badge"], "🔴")

    def test_assemble_attributes(self):
        scalars = _load_scalars_dict(self.repo)
        attrs = _assemble_attributes(self.repo, scalars)

        self.assertEqual(attrs["skill_iron"], 10)
        self.assertEqual(attrs["iron_total"], 15)
        self.assertEqual(attrs["skill_hearts"], 6)
        self.assertEqual(attrs["hearts_total"], 5)
        self.assertEqual(attrs["affiliation_villainy"], 0)
        self.assertEqual(attrs["villainy_total"], 1)

    def test_assemble_officers(self):
        officers_data = _assemble_officers(self.repo)
        officers = officers_data["officers"]
        secondments = officers_data["secondment_outlook"]

        self.assertEqual(officers["first_officer"]["name"], "🔘 Vacant")
        self.assertEqual(officers["chief_engineer"]["name"], "Reckless Driver")
        self.assertEqual(officers["chief_engineer"]["skills"], "+5 Iron, -1 Hearts")
        self.assertEqual(officers["chief_engineer"]["affiliation"], "+1 Villainy")

        self.assertEqual(len(secondments), 1)
        self.assertEqual(secondments[0]["officer_key"], "rat_brigade")
        self.assertIn("The Rat Brigade", secondments[0]["status_note"])
        self.assertIn("Magdalene's", secondments[0]["status_note"])
        self.assertIn("Investigating cellar vaults", secondments[0]["status_note"])

    def test_assemble_inventory(self):
        scalars = _load_scalars_dict(self.repo)
        inv = _assemble_inventory(self.repo, scalars)

        self.assertEqual(inv["hold_capacity"], 30)
        self.assertEqual(inv["hidden_slots"], 2)
        self.assertEqual(inv["standard_hold_used"], 12)
        self.assertEqual(inv["hidden_hold_used"], 2)
        self.assertEqual(inv["fuel_qty"], 8)
        self.assertEqual(inv["supplies_qty"], 3)
        self.assertEqual(len(inv["inventory_rows"]), 3)

    def test_assemble_navigation(self):
        nav = _assemble_navigation(self.repo)

        legs = nav["legs"]
        self.assertEqual([leg["sequence_order"] for leg in legs], [1, 2])
        self.assertEqual(legs[0]["location_name"], "Port Avon")
        self.assertEqual(legs[0]["resupply_badge"], "🟢")
        self.assertEqual(legs[1]["location_name"], "Pan (Eleutheria)")
        self.assertEqual(legs[1]["resupply_badge"], "🟡")

        # Port Avon has both ACT-1000 (prospect) and ACT-1003 (passenger)
        self.assertEqual(len(legs[0]["actions"]), 2)
        self.assertEqual(legs[0]["actions"][0]["title"], "Offload Red Honey")
        self.assertEqual(legs[1]["actions"][0]["title"], "Deliver Royal Dispatches")

        # Pinned off-itinerary objective
        self.assertEqual(len(nav["pinned_objectives"]), 1)
        self.assertEqual(nav["pinned_objectives"][0]["title"], "The Smuggler's Debt")
        self.assertEqual(nav["pinned_objectives"][0]["port"], "London")

        # Active passenger
        self.assertEqual(len(nav["active_passengers"]), 1)
        self.assertEqual(nav["active_passengers"][0]["name"], "Pensive Curate")
        self.assertEqual(nav["active_passengers"][0]["destination"], "Port Avon")
        self.assertIn("Day 45", nav["active_passengers"][0]["deadline"])

    def test_empty_conditional_sections_omitted(self):
        self.repo.set_cell("state_scalars", {"property_key": "hidden_slots"}, "property_value", 0)
        self.repo._cache["state_action"] = self.repo._cache["state_action"].iloc[0:0].copy()
        self.repo._cache["state_officers"] = pd.DataFrame([
            {"officer_key": "reckless_driver", "officer_status": "active"}
        ])

        rendered = render_logbook(self.repo)
        assert rendered is not None
        self.assertNotIn("PINNED OBJECTIVES", rendered)
        self.assertNotIn("ACTIVE PASSENGERS", rendered)
        self.assertNotIn("SECONDMENT OUTLOOK", rendered)
        self.assertNotIn("Hidden Hold Utilization", rendered)

    def test_fsm_enroute_suppression_and_force_override(self):
        self.repo.set_cell("state_scalars", {"property_key": "navigation_state"}, "property_value", "enroute")
        self.assertFalse(should_render_logbook(self.repo))
        self.assertIsNone(render_logbook(self.repo))

        forced = render_logbook(self.repo, force_render=True)
        self.assertIsNotNone(forced)
        assert forced is not None
        self.assertIn("🚀 Enroute", forced)

    def test_strict_undefined_and_prose_patch_guards(self):
        with self.assertRaises(UndefinedError):
            render_template("logbook.j2", {"display_date": "31 January, 1905"})

        with self.assertRaises(ValueError):
            render_logbook(self.repo, prose_patch={"sovereigns": 999999})

    # ------------------------------------------------------------------
    # Full Render & Conditional / Guard Tests
    # ------------------------------------------------------------------

    def test_full_logbook_render_with_active_conditional_sections(self):
        prose_patch = {
            "narrative_counsel": "Keep the boiler stoked; Port Avon customs are brisk this season.",
            "action_notes": {
                "ACT-1000": "Dock under cover of fog.",
            },
        }
        rendered = render_logbook(self.repo, prose_patch=prose_patch)
        self.assertIsNotNone(rendered)
        assert rendered is not None

        self.assertIn("# 🚂 CAPTAIN'S LOG 🚀", rendered)
        self.assertIn("31 January, 1905 (Day 30) | ⚓ New Winchester | 🟢 Docked", rendered)
        self.assertIn("**👤 Captain:** Captain Hawthorne | **🪙 Wallet:** 1250 Sovereigns", rendered)
        self.assertIn("**🚂 Current Engine:** HMS Orpheus (Pellicle-class)", rendered)
        self.assertIn("| **Terror** | 🟡 | 32 / 100 |", rendered)
        self.assertIn("| **Nightmares** | 🔴 | 2 / 4 |", rendered)

        self.assertIn("| - 👊 Iron | 10 | 5 | **15** |", rendered)
        self.assertIn("| - ❤️ Hearts | 6 | -1 | **5** |", rendered)
        self.assertIn("| - 🎩 Villainy | 0| 1 | **1** |", rendered)

        self.assertIn("Executive Officer's Counsel (Mr. Penn — Operations Update):", rendered)
        self.assertIn("> Keep the boiler stoked; Port Avon customs are brisk this season.", rendered)
        self.assertIn("### ➡️ STOP 1 Port Avon 🟢", rendered)
        self.assertIn("🔑 **PROSPECT:** Offload Red Honey", rendered)
        self.assertIn("Dock under cover of fog.", rendered)
        self.assertIn("### ➡️ STOP 2 Pan (Eleutheria) 🟡", rendered)
        self.assertIn("‼️ 🎯 **AMBITION:** Deliver Royal Dispatches", rendered)

        self.assertIn("## 📌 PINNED OBJECTIVES (OFF-ITINERARY)", rendered)
        self.assertIn("**The Smuggler's Debt:** Settle ledger in London. *⚓(London)*", rendered)
        self.assertIn("## 👤 ACTIVE PASSENGERS", rendered)
        self.assertIn("**Pensive Curate** (Destination: Port Avon)", rendered)

        self.assertIn("**Hold Utilization:** 12 / 30 Standard Slots", rendered)
        self.assertIn("**🗝️ Hidden Hold Utilization:** 2 / 2 Slots Occupied", rendered)
        self.assertIn("| Cask of Red Honey | 3 | 0 | £95.00 | Contraband | — |", rendered)

        self.assertIn("| ⚓ **First Officer** | 🔘 Vacant | — | — |", rendered)
        self.assertIn("| ⚙️ **Chief Engineer** | Reckless Driver | +5 Iron, -1 Hearts | +1 Villainy |", rendered)
        self.assertIn("## ⏳ SECONDMENT OUTLOOK", rendered)
        self.assertIn("**The Rat Brigade:** The Rat Brigade (Magdalene's) — Investigating cellar vaults", rendered)

        self.assertIn("### 🪶 **_Mr. Penn_**", rendered)
        self.assertIn("*Executive Officer, HMS Orpheus*", rendered)


        print("\n" + "=" * 72)
        print("FULLY RENDERED LOGBOOK TEMPLATE:")
        print("=" * 72)
        print(rendered)
        print("=" * 72 + "\n")