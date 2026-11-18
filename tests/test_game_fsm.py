#!/usr/bin/env python3
"""
Tier 2 Unit Test Suite for GameFSM, set_game_epoch, and depart_station.
"""
import unittest
import pandas as pd
from src.connectors.google_sheets_repo import GoogleSheetsRepository
from src.exceptions import InvalidTransitionError
from src.tools.engine_tools import set_game_epoch
from src.state.game_fsm import GameFSM


class TestFSMAndEngineTools(unittest.TestCase):

    def setUp(self):
        self.repo = GoogleSheetsRepository("mock_id")
        self.repo._cache["state_scalars"] = pd.DataFrame([
            {"property_key": "epoch", "property_value": 30},
            {"property_key": "current_date", "property_value": "1905-01-31"},
        ])
        self.repo._cache["state_fsm"] = pd.DataFrame([
            {"property_key": "navigation_state", "property_value": "docked"}
        ])
        self.repo._cache["state_navigation_itinerary"] = pd.DataFrame([
            {"sequence_order": 1, "location_key": "port_avon", "action_summary": "Deliver amber"},
            {"sequence_order": 2, "location_key": "eleutheria", "action_summary": "Meet contact"}
        ])
        self.repo._cache["state_navigation_history"] = pd.DataFrame(columns=["sequence_order", "location_key", "action_summary"])
        self.fsm = GameFSM(self.repo)

    def test_set_game_epoch_valid(self):
        success = set_game_epoch(self.repo, 379)
        self.assertTrue(success)
        self.assertEqual(self.repo.get_cell("state_scalars", {"property_key": "epoch"}, "property_value"), 379)

    def test_depart_station_reindexing(self):
        success = self.fsm.transition("DEPART")
        self.assertTrue(success)
        
        # Check history has port_avon
        history_df = self.repo.get_table("state_navigation_history")
        self.assertEqual(len(history_df), 1)
        self.assertEqual(history_df.iloc[0]["location_key"], "port_avon")
        
        # Check itinerary has eleutheria reindexed to sequence_order 1
        itinerary_df = self.repo.get_table("state_navigation_itinerary")
        self.assertEqual(len(itinerary_df), 1)
        self.assertEqual(itinerary_df.iloc[0]["sequence_order"], 1)
        self.assertEqual(itinerary_df.iloc[0]["location_key"], "eleutheria")

    def test_fsm_valid_cycle(self):
        # Initial state: docked
        self.assertEqual(self.fsm.get_current_state(), "docked")
        
        # Transition: docked -> departing (triggers depart_station)
        self.fsm.transition("DEPART")
        self.assertEqual(self.fsm.get_current_state(), "departing")
        
        # Transition: departing -> enroute
        self.fsm.transition("CLEAR")
        self.assertEqual(self.fsm.get_current_state(), "enroute")
        
        # Transition: enroute -> arriving
        self.fsm.transition("ARRIVE")
        self.assertEqual(self.fsm.get_current_state(), "arriving")
        
        # Transition: arriving -> docked
        self.fsm.transition("DOCK")
        self.assertEqual(self.fsm.get_current_state(), "docked")

    def test_fsm_invalid_transition(self):
        # Cannot 'CLEAR' from 'docked' state
        with self.assertRaises(InvalidTransitionError):
            self.fsm.transition("CLEAR")


if __name__ == "__main__":
    unittest.main()