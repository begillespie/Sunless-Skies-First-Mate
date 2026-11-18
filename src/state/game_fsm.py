#!/usr/bin/env python3
"""
@subsystem: game_fsm
@version: 1.2.0
Cyclical Finite State Machine regulating navigation, state-action gating, and kinetic states in state_fsm.
"""

from src.exceptions import DomainRuleError, EntityNotFoundError, InvalidTransitionError
from src.services.calculators import compute_hold_utilization
from src.services.calendar import epoch_to_date


class GameFSM:
    """Regulates state transitions for Sunless Skies navigation (docked -> departing -> enroute -> arriving -> docked)."""

    def __init__(self, repository):
        self.repo = repository
        self.warnings: list[str] = []

    def get_current_state(self) -> str:
        try:
            return str(self.repo.get_cell("state_fsm", {"property_key": "navigation_state"}, "property_value"))
        except (LookupError, ValueError):
            return "docked"

    def _get_scalar_or_none(self, property_key: str):
        try:
            return self.repo.get_cell("state_scalars", {"property_key": property_key}, "property_value")
        except LookupError:
            return None

    def _get_hold_qty(self, good_key: str) -> int:
        try:
            return int(self.repo.get_row("state_inventory", {"good_key": good_key})["hold_qty"])
        except LookupError:
            return 0

    def assert_allowed(self, operation: str, allowed_states: set[str] | frozenset[str]) -> str:
        """Asserts that current navigation_state is in allowed_states, returning the state or raising InvalidTransitionError."""
        current_state = self.get_current_state()
        if current_state not in allowed_states:
            allowed_list = ", ".join(sorted(allowed_states))
            raise InvalidTransitionError(
                f"Cannot execute '{operation}' while vessel is '{current_state}' (requires: {allowed_list})."
            )
        return current_state

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
            raise InvalidTransitionError(
                f"Cannot execute navigation action '{action}' while vessel is '{current_state}'."
            )

        return handler(**kwargs)

    def _pop_and_reindex_itinerary(self) -> bool:
        """
        Pops the top row from state_navigation_itinerary, pushes it to state_navigation_history,
        and renumbers the remaining rows in itinerary. Returns True on success.
        """
        itinerary_df = self.repo.get_table("state_navigation_itinerary")
        if itinerary_df.empty:
            raise EntityNotFoundError("Navigation itinerary is empty; plot at least one destination before departing.")

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
        hold_capacity = self._get_scalar_or_none("hold_capacity")
        if hold_capacity is not None:
            util = compute_hold_utilization(self.repo)
            if util["standard_hold_used"] > int(hold_capacity):
                raise DomainRuleError(
                    f"Hold overloaded ({util['standard_hold_used']}/{int(hold_capacity)} standard slots); "
                    "offload or bank cargo before departing."
                )

        for good_key, min_key in (("fuel", "reserve_fuel_min"), ("supplies", "reserve_supplies_min")):
            reserve_min = self._get_scalar_or_none(min_key)
            if reserve_min is not None:
                qty = self._get_hold_qty(good_key)
                if qty < int(reserve_min):
                    self.warnings.append(
                        f"Low {good_key} reserve: {qty} in hold (recommended minimum {int(reserve_min)})."
                    )

        self._pop_and_reindex_itinerary()
        self.repo.set_cell("state_fsm", {"property_key": "navigation_state"}, "property_value", "departing")
        return True

    def _handle_clear(self, **kwargs) -> bool:
        self.repo.set_cell("state_fsm", {"property_key": "navigation_state"}, "property_value", "enroute")
        return True

    def _handle_arrive(self, **kwargs) -> bool:
        self.repo.set_cell("state_fsm", {"property_key": "navigation_state"}, "property_value", "arriving")
        location_key = kwargs.get("location_key")
        if location_key is not None:
            try:
                prev_location = self.repo.get_cell(
                    "state_fsm", {"property_key": "current_location"}, "property_value"
                )
                try:
                    self.repo.set_cell(
                        "state_fsm", {"property_key": "last_location"}, "property_value", prev_location
                    )
                except LookupError:
                    pass
            except LookupError:
                pass
            self.repo.set_cell("state_fsm", {"property_key": "current_location"}, "property_value", location_key)

        on_arriving = kwargs.get("on_arriving")
        if on_arriving is not None:
            on_arriving()
        return True

    def _handle_dock(self, **kwargs) -> bool:
        self.repo.set_cell("state_fsm", {"property_key": "navigation_state"}, "property_value", "docked")
        return True

    def depart(self, render_fn=None) -> dict:
        """Executes the full port departure lifecycle (docked -> departing -> enroute)."""
        self.warnings = []
        self.transition("DEPART")
        logbook = render_fn() if render_fn is not None else None
        self.transition("CLEAR")
        return {
            "navigation_state": "enroute",
            "logbook": logbook,
            "warnings": list(self.warnings),
        }

    def arrive(self, location_key: str, on_arriving=None) -> dict:
        """Executes the full port arrival lifecycle (enroute -> arriving -> docked)."""
        self.warnings = []
        self.transition("ARRIVE", location_key=location_key, on_arriving=on_arriving)
        self.transition("DOCK")
        final_epoch = int(self._get_scalar_or_none("epoch") or 0)
        return {
            "navigation_state": "docked",
            "location_key": location_key,
            "epoch": final_epoch,
            "current_date": epoch_to_date(final_epoch),
            "warnings": list(self.warnings),
        }