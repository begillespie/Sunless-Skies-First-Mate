import unittest
import pandas as pd
from src.connectors.google_sheets_repo import GoogleSheetsRepository
from src.tools.engine_tools import assign_officer
from src.services.calculators import calculate_attribute_perks


class TestOfficerManagement(unittest.TestCase):

    def setUp(self):
        self.repo = GoogleSheetsRepository("mock_id")
        self.repo._cache["state_fsm"] = pd.DataFrame([
            {"property_key": "navigation_state", "property_value": "docked"},
        ])
        self.repo._cache["state_scalars"] = pd.DataFrame([
            {"property_key": "skill_iron", "property_value": 10},
            {"property_key": "skill_mirrors", "property_value": 3},
            {"property_key": "skill_hearts", "property_value": 6},
            {"property_key": "skill_veils", "property_value": 3},
            {"property_key": "affiliation_academe", "property_value": 0},
            {"property_key": "affiliation_bohemia", "property_value": 0},
            {"property_key": "affiliation_establishment", "property_value": 1},
            {"property_key": "affiliation_villainy", "property_value": 0},
        ])

        self.repo._cache["ref_officers"] = pd.DataFrame([
            {
                "officer_key": "reckless_driver",
                "name": "Reckless Driver",
                "station": "chief_engineer",
                "lineage": "driver",
                "tier": 2,
                "skill_iron": 5,
                "skill_mirrors": 0,
                "skill_hearts": -1,
                "skill_veils": 0,
                "affiliation_academe": 0,
                "affiliation_bohemia": 0,
                "affiliation_establishment": 0,
                "affiliation_villainy": 1,
            },
            {
                "officer_key": "incautious_driver", 
                "name": "Incautious Driver",
                "station": "chief_engineer", 
                "lineage": "driver", 
                "tier": 1,
                "skill_iron": 2, 
                "skill_mirrors": 0, 
                "skill_hearts": 0, 
                "skill_veils": 0,
                "affiliation_academe": 0, 
                "affiliation_bohemia": 0, 
                "affiliation_establishment": 0, 
                "affiliation_villainy": 0,
            },
            {
                "officer_key": "clay_conductor", 
                "name": "Clay Conductor",
                "station": "chief_engineer", 
                "lineage": "conductor", 
                "tier": 1,
                "skill_iron": 0, 
                "skill_mirrors": 4, 
                "skill_hearts": 0, 
                "skill_veils": 0,
                "affiliation_academe": 1, 
                "affiliation_bohemia": 0, 
                "affiliation_establishment": 0, 
                "affiliation_villainy": 0,
            },
        ])
        self.repo._cache["state_officers"] = pd.DataFrame([
            {"officer_key": "incautious_driver", "officer_status": "active"},
            {"officer_key": "clay_conductor", "officer_status": "unassigned"},
        ])

    def test_station_exclusivity_demotes_previous_occupant(self):
        self.assertTrue(assign_officer(self.repo, "clay_conductor", "active"))
        self.assertEqual(
            self.repo.get_cell("state_officers", {"officer_key": "clay_conductor"}, "officer_status"),
            "active",
        )
        self.assertEqual(
            self.repo.get_cell("state_officers", {"officer_key": "incautious_driver"}, "officer_status"),
            "unassigned",
        )

    def test_lineage_upgrade_purges_lower_tier(self):
        self.assertTrue(assign_officer(self.repo, "reckless_driver", "active"))
        roster = self.repo.get_table("state_officers")
        self.assertNotIn("incautious_driver", set(roster["officer_key"]))
        self.assertEqual(
            self.repo.get_cell("state_officers", {"officer_key": "reckless_driver"}, "officer_status"),
            "active",
        )

    def test_lineage_blocks_downgrade(self):
        assign_officer(self.repo, "reckless_driver", "active")
        with self.assertRaises(ValueError):
            assign_officer(self.repo, "incautious_driver", "unassigned")

    def test_calculate_attribute_perks(self):
        assign_officer(self.repo, "reckless_driver", "active")
        totals = calculate_attribute_perks(self.repo)
        self.assertEqual(totals, {
            "skill_iron": 15,
            "skill_mirrors": 3,
            "skill_hearts": 5,
            "skill_veils": 3,
            "affiliation_academe": 0,
            "affiliation_bohemia": 0,
            "affiliation_establishment": 1,
            "affiliation_villainy": 1,
        })