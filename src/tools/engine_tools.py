#!/usr/bin/env python3
"""
@subsystem: engine_tools
@version: 2.0.0
@file src/tools/engine_tools.py
@description Guarded state mutators for Sunless Skies First Mate.
All state-modifying functions enforce domain invariants, delegate pure math to
src/services/, and obey the 'no silent methods' rule (returning True on success).
"""
import numbers
from typing import Literal

from src.services.calendar import epoch_to_date
from src.services.calculators import compute_mac
from src.state.game_fsm import GameFSM
from src.tools.registry import llm_tool

PERMANENT_BASELINES = {"fuel", "supplies"}

VALID_OFFICER_STATUSES = {"active", "unassigned", "seconded"}

MUTABLE_SCALARS = {
    "sovereigns",
    "current_hull",
    "current_crew",
    "terror_level",
    "nightmares_level",
    "current_location",
    "region_name",
    "skill_iron",
    "skill_mirrors",
    "skill_hearts",
    "skill_veils",
    "affiliation_academe",
    "affiliation_bohemia",
    "affiliation_establishment",
    "affiliation_villainy",
}

NUMERIC_SCALARS = {
    "sovereigns",
    "current_hull",
    "current_crew",
    "terror_level",
    "nightmares_level",
    "skill_iron",
    "skill_mirrors",
    "skill_hearts",
    "skill_veils",
    "affiliation_academe",
    "affiliation_bohemia",
    "affiliation_establishment",
    "affiliation_villainy",
}


def _apply_scalar_bounds(repo, key: str, value):
    """Validates and clamps bounded scalar values."""
    if key == "current_hull":
        max_hull = int(repo.get_cell("state_scalars", {"key": "max_hull"}, "value"))
        return max(0, min(int(value), max_hull))
    if key == "current_crew":
        max_crew = int(repo.get_cell("state_scalars", {"key": "max_crew"}, "value"))
        return max(0, min(int(value), max_crew))
    if key == "terror_level":
        return max(0, min(int(value), 100))
    if key == "nightmares_level":
        return max(0, min(int(value), 4))
    if key == "sovereigns":
        rounded = round(float(value), 2)
        if rounded < 0:
            raise ValueError(f"Sovereigns cannot be negative (attempted {rounded}).")
        return int(rounded) if rounded.is_integer() else rounded
    return value


@llm_tool(category="mutator")
def adjust_scalar(repo, key: str, delta: int | float) -> bool:
    """
    Applies a relative numeric delta (positive or negative) to an allowed gameplay scalar
    such as sovereigns, current_hull, current_crew, terror_level, nightmares_level, or base skills.
    """
    if key not in MUTABLE_SCALARS or key not in NUMERIC_SCALARS:
        raise ValueError(f"Scalar '{key}' does not support numeric delta adjustments.")
    if not isinstance(delta, numbers.Real) or isinstance(delta, bool):
        raise TypeError(f"Delta must be a numeric value, got {delta!r}.")

    current = repo.get_cell("state_scalars", {"key": key}, "value")
    new_val = _apply_scalar_bounds(repo, key, current + delta)
    repo.set_cell("state_scalars", {"key": key}, "value", new_val)
    return True


@llm_tool(category="mutator")
def set_scalar(repo, key: str, value: str | int | float) -> bool:
    """
    Sets an allowed mutable scalar (such as current_location, region_name, or a base attribute)
    to an explicit value while enforcing domain bounds.
    """
    if key not in MUTABLE_SCALARS:
        raise ValueError(f"Scalar '{key}' is protected or invalid.")
    if isinstance(value, bool):
        raise TypeError("Scalar value cannot be a boolean.")

    if key in NUMERIC_SCALARS:
        if not isinstance(value, numbers.Real):
            raise TypeError(f"Scalar '{key}' requires a numeric value, got {value!r}.")
        bounded_val = _apply_scalar_bounds(repo, key, value)
    else:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Scalar '{key}' requires a non-empty string.")
        bounded_val = value.strip()

    repo.set_cell("state_scalars", {"key": key}, "value", bounded_val)
    return True


@llm_tool(category="mutator")
def set_game_epoch(repo, epoch: int) -> bool:
    """
    Sets the global game epoch (0-indexed day from 1905-01-01) and synchronizes
    current_date (YYYY-MM-DD) in state_scalars. Returns True on success.
    """
    if not isinstance(epoch, numbers.Integral) or isinstance(epoch, bool) or epoch < 0:
        raise ValueError(f"Epoch must be a non-negative integer, got {epoch}")

    epoch_int = int(epoch)
    date_str = epoch_to_date(epoch_int)
    repo.set_cell("state_scalars", {"key": "epoch"}, "value", epoch_int)
    repo.set_cell("state_scalars", {"key": "current_date"}, "value", date_str)
    return True


@llm_tool(category="mutator")
def buy_goods(repo, good_key: str, qty: int, unit_price: float) -> bool:
    """
    Executes a market purchase into the vessel hold:
    - Validates sovereigns balance and deducts total cost
    - Calculates new Moving Average Unit Cost via compute_mac
    - Appends a new inventory row or updates existing hold_qty and average_unit_cost
    - Returns True on success
    """
    if not isinstance(good_key, str) or not good_key.strip():
        raise ValueError("good_key must be a non-empty string")
    if not isinstance(qty, numbers.Integral) or isinstance(qty, bool) or qty <= 0:
        raise ValueError(f"Purchase quantity must be a positive integer, got {qty}")
    if not isinstance(unit_price, numbers.Real) or isinstance(unit_price, bool) or unit_price < 0:
        raise ValueError(f"Unit price must be a non-negative number, got {unit_price}")

    qty = int(qty)
    unit_price = float(unit_price)
    total_cost = round(qty * unit_price, 2)

    sovereigns = repo.get_cell("state_scalars", {"key": "sovereigns"}, "value")
    if sovereigns < total_cost:
        raise ValueError(
            f"Insufficient sovereigns to buy {qty}x '{good_key}': need {total_cost}, have {sovereigns}."
        )

    new_mac = compute_mac(repo, good_key, qty, unit_price)

    try:
        row = repo.get_row("state_inventory", {"good_key": good_key})
        new_hold_qty = int(row["hold_qty"]) + qty
        repo.update_row(
            "state_inventory",
            {"good_key": good_key},
            {"hold_qty": new_hold_qty, "average_unit_cost": new_mac},
        )
    except LookupError:
        repo.append_row(
            "state_inventory",
            {
                "good_key": good_key,
                "hold_qty": qty,
                "bank_qty": 0,
                "average_unit_cost": new_mac,
            },
        )

    new_sovereigns = round(float(sovereigns) - total_cost, 2)
    if new_sovereigns.is_integer():
        new_sovereigns = int(new_sovereigns)
    repo.set_cell("state_scalars", {"key": "sovereigns"}, "value", new_sovereigns)
    return True


@llm_tool(category="mutator")
def sell_goods(repo, good_key: str, qty: int, unit_price: float) -> bool:
    """
    Executes a market sale from the vessel hold:
    - Validates sufficient hold_qty
    - Deletes row if total stock (hold + bank) reaches 0 (unless in PERMANENT_BASELINES)
    - Resets average_unit_cost to 0.0 if total stock reaches 0; otherwise preserves existing MAC
    - Credits sale revenue to sovereigns
    - Returns True on success
    """
    if not isinstance(good_key, str) or not good_key.strip():
        raise ValueError("good_key must be a non-empty string")
    if not isinstance(qty, numbers.Integral) or isinstance(qty, bool) or qty <= 0:
        raise ValueError(f"Sale quantity must be a positive integer, got {qty}")
    if not isinstance(unit_price, numbers.Real) or isinstance(unit_price, bool) or unit_price < 0:
        raise ValueError(f"Unit sale price must be a non-negative number, got {unit_price}")

    qty = int(qty)
    unit_price = float(unit_price)

    row = repo.get_row("state_inventory", {"good_key": good_key})
    hold_qty = int(row["hold_qty"])
    bank_qty = int(row["bank_qty"])

    if hold_qty < qty:
        raise ValueError(
            f"Insufficient hold quantity to sell {qty}x '{good_key}': have {hold_qty} in hold."
        )

    new_hold_qty = hold_qty - qty
    new_total_qty = new_hold_qty + bank_qty

    if new_total_qty == 0 and good_key not in PERMANENT_BASELINES:
        repo.delete_row("state_inventory", {"good_key": good_key})
    else:
        new_mac = 0.0 if new_total_qty == 0 else float(row["average_unit_cost"])
        repo.update_row(
            "state_inventory",
            {"good_key": good_key},
            {"hold_qty": new_hold_qty, "average_unit_cost": new_mac},
        )

    revenue = round(qty * unit_price, 2)
    sovereigns = repo.get_cell("state_scalars", {"key": "sovereigns"}, "value")
    new_sovereigns = round(float(sovereigns) + revenue, 2)
    if new_sovereigns.is_integer():
        new_sovereigns = int(new_sovereigns)
    repo.set_cell("state_scalars", {"key": "sovereigns"}, "value", new_sovereigns)
    return True


@llm_tool(category="mutator")
def adjust_hold_qty(repo, good_key: str, delta: int) -> bool:
    """
    Adjusts hold quantity for non-market events (salvage, transit consumption, event rewards)
    without altering Moving Average Unit Cost or sovereigns. Returns True on success.
    """
    if not isinstance(good_key, str) or not good_key.strip():
        raise ValueError("good_key must be a non-empty string")
    if not isinstance(delta, numbers.Integral) or isinstance(delta, bool) or delta == 0:
        raise ValueError(f"Delta must be a non-zero integer, got {delta}")

    delta = int(delta)
    try:
        row = repo.get_row("state_inventory", {"good_key": good_key})
        hold_qty = int(row["hold_qty"])
        bank_qty = int(row["bank_qty"])
        new_hold_qty = hold_qty + delta
        if new_hold_qty < 0:
            raise ValueError(
                f"Insufficient hold quantity for '{good_key}': have {hold_qty}, delta {delta}."
            )
        new_total_qty = new_hold_qty + bank_qty
        if new_total_qty == 0 and good_key not in PERMANENT_BASELINES:
            repo.delete_row("state_inventory", {"good_key": good_key})
        else:
            new_mac = 0.0 if new_total_qty == 0 else float(row["average_unit_cost"])
            repo.update_row(
                "state_inventory",
                {"good_key": good_key},
                {"hold_qty": new_hold_qty, "average_unit_cost": new_mac},
            )
    except LookupError:
        if delta < 0:
            raise LookupError(f"Cannot deduct {abs(delta)}x '{good_key}'; item is not in inventory.")
        repo.append_row(
            "state_inventory",
            {
                "good_key": good_key,
                "hold_qty": delta,
                "bank_qty": 0,
                "average_unit_cost": 0.0,
            },
        )
    return True


@llm_tool(category="mutator")
def transfer_inventory(
    repo,
    good_key: str,
    direction: Literal["deposit", "withdraw"],
    qty: int,
) -> bool:
    """
    Executes bank transfers on a single item between vessel hold and hub bank.
    - direction: 'deposit' (Hold -> Bank) or 'withdraw' (Bank -> Hold)
    - qty: positive integer quantity to transfer
    - returns True on success
    """
    if not isinstance(qty, numbers.Integral) or isinstance(qty, bool):
        raise TypeError("Transfer quantity must be an integer")
    if qty <= 0:
        raise ValueError(f"Transfer quantity must be positive, got {qty}")

    qty = int(qty)
    row = repo.get_row("state_inventory", {"good_key": good_key})
    hold_qty = int(row["hold_qty"])
    bank_qty = int(row["bank_qty"])

    if direction == "deposit":
        if hold_qty < qty:
            raise ValueError(
                f"Insufficient hold quantity for deposit of '{good_key}': have {hold_qty}, trying to deposit {qty}."
            )
        hold_qty -= qty
        bank_qty += qty
    elif direction == "withdraw":
        if bank_qty < qty:
            raise ValueError(
                f"Insufficient bank quantity for withdrawal of '{good_key}': have {bank_qty}, trying to withdraw {qty}."
            )
        bank_qty -= qty
        hold_qty += qty
    else:
        raise ValueError(f"Invalid transfer direction '{direction}'. Expected 'deposit' or 'withdraw'.")

    repo.update_row(
        "state_inventory",
        {"good_key": good_key},
        {"hold_qty": hold_qty, "bank_qty": bank_qty},
    )
    return True


@llm_tool(category="mutator")
def assign_officer(
    repo,
    officer_key: str,
    officer_status: Literal["active", "unassigned", "seconded"],
) -> bool:
    """
    Assigns or updates an officer's roster status while enforcing bridge & lineage rules:
    1. Fixed Slot: An officer only occupies the station defined in ref_officers.
    2. Lineage Exclusivity: Removes all lower-tier officers in the same lineage;
       blocks downgrading if a higher-tier officer of that lineage is already rostered.
    3. Station Exclusivity: When setting status to 'active', demotes any existing
       'active' officer in the same station to 'unassigned'.
    Returns True on success.
    """
    if not isinstance(officer_key, str) or not officer_key.strip():
        raise ValueError("officer_key must be a non-empty string.")
    if officer_status not in VALID_OFFICER_STATUSES:
        raise ValueError(
            f"Invalid officer_status '{officer_status}'. Expected one of {sorted(VALID_OFFICER_STATUSES)}."
        )

    target_ref = repo.get_row("ref_officers", {"officer_key": officer_key})
    target_station = target_ref["station"]
    target_lineage = target_ref["lineage"]
    target_tier = int(target_ref["tier"])

    roster_df = repo.get_table("state_officers")
    ref_df = repo.get_table("ref_officers")

    if not roster_df.empty:
        merged_roster = roster_df.merge(
            ref_df[["officer_key", "station", "lineage", "tier"]],
            on="officer_key",
            how="left",
        )

        same_lineage = merged_roster[
            (merged_roster["lineage"] == target_lineage)
            & (merged_roster["officer_key"] != officer_key)
        ]
        for _, row in same_lineage.iterrows():
            existing_tier = int(row["tier"])
            if existing_tier > target_tier:
                raise ValueError(
                    f"Cannot roster '{officer_key}' (Tier {target_tier}): higher-tier "
                    f"'{row['officer_key']}' (Tier {existing_tier}) of lineage '{target_lineage}' is already present."
                )
            if existing_tier < target_tier:
                repo.delete_row("state_officers", {"officer_key": row["officer_key"]})

        if officer_status == "active":
            station_occupants = merged_roster[
                (merged_roster["station"] == target_station)
                & (merged_roster["officer_status"] == "active")
                & (merged_roster["officer_key"] != officer_key)
            ]
            for _, occupant in station_occupants.iterrows():
                if occupant["officer_key"] in set(repo.get_table("state_officers")["officer_key"]):
                    repo.set_cell(
                        "state_officers",
                        {"officer_key": occupant["officer_key"]},
                        "officer_status",
                        "unassigned",
                    )

    current_roster = repo.get_table("state_officers")
    if not current_roster.empty and officer_key in set(current_roster["officer_key"]):
        repo.set_cell("state_officers", {"officer_key": officer_key}, "officer_status", officer_status)
    else:
        repo.append_row(
            "state_officers",
            {"officer_key": officer_key, "officer_status": officer_status},
        )

    return True


@llm_tool(category="mutator")
def transition_navigation(
    repo,
    action: Literal["DEPART", "CLEAR", "ARRIVE", "DOCK"],
) -> bool:
    """
    Advances the vessel's cyclical navigation FSM (docked -> departing -> enroute -> arriving -> docked).
    Automatically archives the departed itinerary leg and renumbers remaining legs on DEPART.
    Returns True on success.
    """
    fsm = GameFSM(repo)
    return fsm.transition(action)


def depart_station(repo) -> bool:
    """Convenience wrapper executing a DEPART navigation transition via GameFSM."""
    return transition_navigation(repo, "DEPART")