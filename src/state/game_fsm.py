#!/usr/bin/env python3
"""
@subsystem: game_fsm
@version: 1.1.0
Cyclical Finite State Machine regulating navigation and kinetic states in state_scalars.
"""


class GameFSM:
    """Regulates state transitions for Sunless Skies navigation (docked -> departing -> enroute -> arriving -> docked)."""

    def __init__(self, repository):
        self.repo = repository

    def get_current_state(self) -> str:
        try:
            return str(self.repo.get_cell("state_scalars", {"key": "navigation_state"}, "value"))
        except (LookupError, ValueError):
            return "docked"

    def transition(self, action: str, **kwargs) -> bool:
        current_state = self.get_current_state()

        transition_table = {
            ("docked", "DEPART"): self._handle_depart,
            ("departing", "CLEAR"): self._handle_clear,
            ("enroute", "ARRIVE"): self._handle_arrive,
            ("arriving", "DOCK"): self._handle_dock,
        }

        handler = transition_table.get((current_state, action))
        if not handler:
            raise ValueError(
                f"Invalid FSM transition: Action '{action}' is not allowed from state '{current_state}'."
            )

        return handler(**kwargs)

    def _pop_and_reindex_itinerary(self) -> bool:
        """
        Pops the top row from state_navigation_itinerary, pushes it to state_navigation_history,
        and renumbers the remaining rows in itinerary. Returns True on success.
        """
        itinerary_df = self.repo.get_table("state_navigation_itinerary")
        if itinerary_df.empty:
            raise LookupError("Itinerary is empty; cannot depart station.")

        itinerary_df = itinerary_df.sort_values(by="sequence_order").reset_index(drop=True)
        top_leg = itinerary_df.iloc[0].to_dict()

        self.repo.append_row("state_navigation_history", top_leg)

        pk_col = "sequence_order" if "sequence_order" in itinerary_df.columns else itinerary_df.columns[0]
        pk_val = top_leg[pk_col]
        self.repo.delete_row("state_navigation_itinerary", {pk_col: pk_val})

        remaining_df = self.repo.get_table("state_navigation_itinerary")
        if not remaining_df.empty:
            remaining_df = remaining_df.sort_values(by="sequence_order").reset_index(drop=True)
            for idx, row in remaining_df.iterrows():
                new_seq = idx + 1
                pk_value = row[pk_col]
                self.repo.set_cell("state_navigation_itinerary", {pk_col: pk_value}, "sequence_order", new_seq)

        return True

    def _handle_depart(self, **kwargs) -> bool:
        self._pop_and_reindex_itinerary()
        self.repo.set_cell("state_scalars", {"key": "navigation_state"}, "value", "departing")
        return True

    def _handle_clear(self, **kwargs) -> bool:
        self.repo.set_cell("state_scalars", {"key": "navigation_state"}, "value", "enroute")
        return True

    def _handle_arrive(self, **kwargs) -> bool:
        self.repo.set_cell("state_scalars", {"key": "navigation_state"}, "value", "arriving")
        return True

    def _handle_dock(self, **kwargs) -> bool:
        self.repo.set_cell("state_scalars", {"key": "navigation_state"}, "value", "docked")
        return True