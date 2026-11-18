#!/usr/bin/env python3
"""
@subsystem: engine_tools
@version: 2.1.0
@file src/tools/engine_tools.py
@description Guarded state mutators for Sunless Skies First Mate.
All state-modifying functions enforce domain invariants, delegate pure math to
src/services/, and obey the 'no silent methods' rule (returning True on success).
"""
import numbers
from typing import Literal

from src.exceptions import (
    DomainRuleError,
    EntityNotFoundError,
    ToolArgumentTypeError,
    ValidationError,
)
from src.services.calendar import date_to_epoch, epoch_to_date
from src.services.calculators import compute_mac
from src.state.game_fsm import GameFSM
from src.tools.registry import llm_tool
from src.ui.ui_renderer import render_logbook
from src.ui.ui_tools import format_iso_date

PERMANENT_BASELINES = {"fuel", "supplies"}

VALID_OFFICER_STATUSES = {"active", "unassigned", "seconded"}

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


def _require_int(value, name: str) -> int:
    """Validates that a value is a non-boolean integer and returns it as int."""
    if not isinstance(value, numbers.Integral) or isinstance(value, bool):
        raise ToolArgumentTypeError(f"'{name}' must be an integer, got {value!r}.")
    return int(value)


def _require_number(value, name: str) -> float:
    """Validates that a value is a non-boolean real number and returns it as float."""
    if not isinstance(value, numbers.Real) or isinstance(value, bool):
        raise ToolArgumentTypeError(f"'{name}' must be a numeric value, got {value!r}.")
    return float(value)


def _validate_ref_key(repo, table_name: str, key_col: str, key_val: str, entity_label: str) -> dict:
    """Validates a non-empty string key against a ref_* or lkup_* table and returns the matched row."""
    if not isinstance(key_val, str):
        raise ToolArgumentTypeError(f"'{key_col}' must be a string, got {key_val!r}.")
    clean_key = key_val.strip()
    if not clean_key:
        raise ValidationError(f"'{key_col}' must be a non-empty string.")
    try:
        return repo.get_row(table_name, {key_col: clean_key})
    except LookupError as exc:
        raise EntityNotFoundError(
            f"Unknown {entity_label} '{clean_key}': no matching '{key_col}' found in '{table_name}'."
        ) from exc


def _scalar_data_type(repo, property_key: str) -> str:
    """Returns the declared data_type from state_scalars, falling back to NUMERIC_SCALARS."""
    try:
        row = repo.get_row("state_scalars", {"property_key": property_key})
    except LookupError as exc:
        raise EntityNotFoundError(f"Scalar '{property_key}' was not found in 'state_scalars'.") from exc
    raw_type = row.get("data_type")
    if isinstance(raw_type, str) and raw_type.strip():
        return raw_type.strip().lower()
    return "integer" if property_key in NUMERIC_SCALARS else "string"


def _apply_scalar_bounds(repo, property_key: str, property_value):
    """Validates and clamps bounded scalar values."""
    if property_key == "current_hull":
        max_hull = int(repo.get_cell("state_scalars", {"property_key": "max_hull"}, "property_value"))
        return max(0, min(int(property_value), max_hull))
    if property_key == "current_crew":
        max_crew = int(repo.get_cell("state_scalars", {"property_key": "max_crew"}, "property_value"))
        return max(0, min(int(property_value), max_crew))
    if property_key == "terror_level":
        return max(0, min(int(property_value), 100))
    if property_key == "nightmares_level":
        return max(0, min(int(property_value), 4))
    if property_key == "sovereigns":
        val = int(round(float(property_value)))
        if val < 0:
            raise DomainRuleError(
                f"Sovereigns cannot drop below zero (attempted balance: {val})."
            )
        return val
    return property_value


@llm_tool(category="mutator", allowed_states={"docked", "enroute", "arriving"})
def adjust_scalar(repo, property_key: str, delta: int | float) -> bool:
    """
    Applies a relative numeric delta (positive or negative) to a numeric scalar in state_scalars
    such as sovereigns, current_hull, current_crew, terror_level, nightmares_level, or base skills.
    """
    data_type = _scalar_data_type(repo, property_key)
    if data_type not in ("integer", "int", "float", "number"):
        raise DomainRuleError(
            f"Scalar '{property_key}' has data_type '{data_type}' and does not support numeric delta adjustments."
        )
    _require_number(delta, "delta")

    current = repo.get_cell("state_scalars", {"property_key": property_key}, "property_value")
    new_val = _apply_scalar_bounds(repo, property_key, current + delta)
    repo.set_cell("state_scalars", {"property_key": property_key}, "property_value", new_val)
    return True


@llm_tool(category="mutator", allowed_states={"docked", "enroute", "arriving"})
def set_scalar(repo, property_key: str, property_value: str | int | float) -> bool:
    """
    Sets a scalar in state_scalars (such as region_name, vessel_name, or a base attribute)
    to an explicit value while enforcing its declared data_type and domain bounds.
    """
    if isinstance(property_value, bool):
        raise ToolArgumentTypeError(f"Scalar '{property_key}' cannot be set to a boolean value.")

    data_type = _scalar_data_type(repo, property_key)
    if data_type in ("integer", "int"):
        _require_int(property_value, "property_value")
        bounded_val = _apply_scalar_bounds(repo, property_key, property_value)
    elif data_type in ("float", "number"):
        _require_number(property_value, "property_value")
        bounded_val = _apply_scalar_bounds(repo, property_key, property_value)
    else:
        if not isinstance(property_value, str):
            raise ToolArgumentTypeError(
                f"Scalar '{property_key}' requires a string value, got {property_value!r}."
            )
        if not property_value.strip():
            raise ValidationError(f"Scalar '{property_key}' requires a non-empty string.")
        bounded_val = property_value.strip()

    repo.set_cell("state_scalars", {"property_key": property_key}, "property_value", bounded_val)
    return True


@llm_tool(category="mutator", allowed_states={"docked", "enroute", "arriving"})
def set_game_epoch(repo, epoch: int) -> dict:
    """
    Sets the global game epoch (0-indexed day from 1905-01-01) in state_scalars.
    Emits a Horological anomaly warning if time moves backward.
    """
    epoch_int = _require_int(epoch, "epoch")
    if epoch_int < 0:
        raise ValidationError(f"Epoch must be a non-negative integer (days since 1905-01-01), got {epoch_int}.")

    warnings: list[str] = []
    current_epoch = _get_scalar_or_none(repo, "epoch")
    if current_epoch is not None and epoch_int < int(current_epoch):
        prev_epoch = int(current_epoch)
        warnings.append(
            f"Horological anomaly: date regressed from {epoch_to_date(prev_epoch)} "
            f"to {epoch_to_date(epoch_int)} ({epoch_int - prev_epoch} days). Consult the Royal Horological Office."
        )

    repo.set_cell("state_scalars", {"property_key": "epoch"}, "property_value", epoch_int)
    return {
        "epoch": epoch_int,
        "warnings": warnings,
    }


@llm_tool(category="query")
def convert_date_to_epoch(repo, iso_date: str) -> int:
    """
    Converts an ISO date string ('YYYY-MM-DD', >= 1905-01-01) into a 0-indexed High Wilderness
    epoch integer (365-day calendar, no leap years).
    """
    if not isinstance(iso_date, str):
        raise ToolArgumentTypeError(f"'iso_date' must be a string, got {type(iso_date).__name__}.")
    try:
        return date_to_epoch(iso_date)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc


@llm_tool(category="query")
def convert_epoch_to_date(repo, epoch: int) -> str:
    """
    Converts a 0-indexed High Wilderness epoch integer into an ISO date string ('YYYY-MM-DD').
    """
    epoch_int = _require_int(epoch, "epoch")
    try:
        return epoch_to_date(epoch_int)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc


@llm_tool(category="query")
def format_display_date(
    repo,
    iso_date: str | None = None,
    epoch: int | None = None,
    fmt: str = "%d %B, %Y",
) -> str:
    """
    Formats either an ISO date string ('YYYY-MM-DD') or a 0-indexed epoch integer for diegetic
    player presentation (default: '31 January, 1905'). Provide one of iso_date or epoch, not both.
    """
    if (iso_date is None and epoch is None) or (iso_date is not None and epoch is not None):
        raise ValidationError("Provide exactly one of 'iso_date' or 'epoch'.")
    if not isinstance(fmt, str) or not fmt.strip():
        raise ValidationError("'fmt' must be a non-empty strftime format string.")

    if epoch is not None:
        iso_str = convert_epoch_to_date(repo, epoch)
    else:
        if not isinstance(iso_date, str):
            raise ToolArgumentTypeError(f"'iso_date' must be a string, got {type(iso_date).__name__}.")
        iso_str = iso_date

    try:
        return format_iso_date(iso_str, fmt=fmt)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc


def _get_hold_qty(repo, good_key: str) -> int:
    """Returns current hold_qty for good_key in state_inventory, or 0 if not present."""
    try:
        return int(repo.get_row("state_inventory", {"good_key": good_key})["hold_qty"])
    except LookupError:
        return 0


def _commit_hold_change(repo, row: dict, good_key: str, new_hold_qty: int) -> None:
    """Updates hold_qty, deleting non-baseline rows when total stock hits 0."""
    new_total_qty = new_hold_qty + int(row["bank_qty"])
    if new_total_qty == 0 and good_key not in PERMANENT_BASELINES:
        repo.delete_row("state_inventory", {"good_key": good_key})
    else:
        new_mac = 0.0 if new_total_qty == 0 else float(row["average_unit_cost"])
        repo.update_row(
            "state_inventory",
            {"good_key": good_key},
            {"hold_qty": new_hold_qty, "average_unit_cost": new_mac},
        )


@llm_tool(category="mutator", allowed_states={"docked"})
def buy_goods(repo, good_key: str, qty: int, unit_price: float) -> bool:
    """
    Executes a market purchase into the vessel hold:
    - Validates good_key against ref_goods and sovereigns balance, deducting total cost
    - Calculates new Moving Average Unit Cost via compute_mac
    - Appends a new inventory row or updates existing hold_qty and average_unit_cost
    - Returns True on success
    """
    _validate_ref_key(repo, "ref_goods", "good_key", good_key, "good")
    qty = _require_int(qty, "qty")
    if qty <= 0:
        raise ValidationError(f"Purchase quantity for '{good_key}' must be a positive integer, got {qty}.")
    unit_price = _require_number(unit_price, "unit_price")
    if unit_price < 0:
        raise ValidationError(f"Unit price for '{good_key}' cannot be negative, got {unit_price}.")

    total_cost = int(round(qty * unit_price))

    sovereigns = int(repo.get_cell("state_scalars", {"property_key": "sovereigns"}, "property_value"))
    if sovereigns < total_cost:
        raise DomainRuleError(
            f"Insufficient sovereigns to buy {qty}x '{good_key}' at {unit_price} each: "
            f"need {total_cost}, have {sovereigns}."
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

    if total_cost > 0:
        adjust_scalar(repo, "sovereigns", -total_cost)
    return True


@llm_tool(category="mutator", allowed_states={"docked"})
def sell_goods(repo, good_key: str, qty: int, unit_price: float) -> bool:
    """
    Executes a market sale from the vessel hold:
    - Validates good_key against ref_goods and sufficient hold_qty
    - Deletes row if total stock (hold + bank) reaches 0 (unless in PERMANENT_BASELINES)
    - Resets average_unit_cost to 0.0 if total stock reaches 0; otherwise preserves existing MAC
    - Credits sale revenue to sovereigns
    - Returns True on success
    """
    _validate_ref_key(repo, "ref_goods", "good_key", good_key, "good")
    qty = _require_int(qty, "qty")
    if qty <= 0:
        raise ValidationError(f"Sale quantity for '{good_key}' must be a positive integer, got {qty}.")
    unit_price = _require_number(unit_price, "unit_price")
    if unit_price < 0:
        raise ValidationError(f"Unit sale price for '{good_key}' cannot be negative, got {unit_price}.")

    row = repo.get_row("state_inventory", {"good_key": good_key})
    hold_qty = int(row["hold_qty"])

    if hold_qty < qty:
        raise DomainRuleError(
            f"Insufficient hold quantity to sell {qty}x '{good_key}': only {hold_qty} in the hold."
        )

    _commit_hold_change(repo, row, good_key, hold_qty - qty)

    revenue = int(round(qty * unit_price))
    if revenue > 0:
        adjust_scalar(repo, "sovereigns", revenue)
    return True


@llm_tool(category="mutator", allowed_states={"docked", "enroute", "arriving"})
def adjust_hold_qty(repo, good_key: str, delta: int) -> bool:
    """
    Adjusts hold quantity for non-market events (salvage, transit consumption, event rewards)
    without altering Moving Average Unit Cost or sovereigns. Returns True on success.
    """
    _validate_ref_key(repo, "ref_goods", "good_key", good_key, "good")
    delta = _require_int(delta, "delta")
    if delta == 0:
        raise ValidationError(f"Delta for '{good_key}' must be a non-zero integer, got 0.")

    try:
        row = repo.get_row("state_inventory", {"good_key": good_key})
        hold_qty = int(row["hold_qty"])
        new_hold_qty = hold_qty + delta
        if new_hold_qty < 0:
            raise DomainRuleError(
                f"Insufficient hold quantity for '{good_key}': have {hold_qty}, attempted delta {delta}."
            )
        _commit_hold_change(repo, row, good_key, new_hold_qty)
    except LookupError as exc:
        if delta < 0:
            raise EntityNotFoundError(
                f"Cannot deduct {abs(delta)}x '{good_key}'; no stock is currently held."
            ) from exc
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


@llm_tool(category="mutator", allowed_states={"docked"})
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
    _validate_ref_key(repo, "ref_goods", "good_key", good_key, "good")
    qty = _require_int(qty, "qty")
    if qty <= 0:
        raise ValidationError(f"Transfer quantity for '{good_key}' must be positive, got {qty}.")

    row = repo.get_row("state_inventory", {"good_key": good_key})
    hold_qty = int(row["hold_qty"])
    bank_qty = int(row["bank_qty"])

    if direction == "deposit":
        if hold_qty < qty:
            raise DomainRuleError(
                f"Insufficient hold quantity to deposit {qty}x '{good_key}': only {hold_qty} in the hold."
            )
        hold_qty -= qty
        bank_qty += qty
    elif direction == "withdraw":
        if bank_qty < qty:
            raise DomainRuleError(
                f"Insufficient bank quantity to withdraw {qty}x '{good_key}': only {bank_qty} stored in the bank."
            )
        bank_qty -= qty
        hold_qty += qty
    else:
        raise ValidationError(
            f"Invalid transfer direction '{direction}'. Expected 'deposit' or 'withdraw'."
        )

    repo.update_row(
        "state_inventory",
        {"good_key": good_key},
        {"hold_qty": hold_qty, "bank_qty": bank_qty},
    )
    return True


@llm_tool(category="mutator", allowed_states={"docked"})
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
    target_ref = _validate_ref_key(repo, "ref_officers", "officer_key", officer_key, "officer")
    if officer_status not in VALID_OFFICER_STATUSES:
        raise ValidationError(
            f"Invalid officer_status '{officer_status}'. Expected one of {sorted(VALID_OFFICER_STATUSES)}."
        )

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
                raise DomainRuleError(
                    f"Cannot roster '{officer_key}' (Tier {target_tier}): higher-tier "
                    f"'{row['officer_key']}' (Tier {existing_tier}) of lineage '{target_lineage}' is already rostered."
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


@llm_tool(category="query")
def get_bridge_report(
    repo,
    include_inventory: bool = True,
    include_officers: bool = True,
    include_itinerary: bool = True,
    include_actions: bool = True,
) -> dict:
    """Returns a structured snapshot of current scalars, vitals, and requested state tables."""
    return {}


@llm_tool(category="mutator", allowed_states={"docked", "enroute", "arriving"})
def manage_itinerary(
    repo,
    operation: Literal["append", "insert", "remove", "clear"],
    location_key: str | None = None,
    position: int | None = None,
) -> bool:
    """Appends, inserts, removes, or clears waypoints in state_navigation_itinerary with contiguous sequence_order re-indexing."""
    return True


@llm_tool(category="mutator", allowed_states={"docked", "enroute", "arriving"})
def chart_discovered_location(
    repo,
    location_key: str,
    region_name: str,
    clock_bearing: int | None = None,
    ring_depth: Literal["center", "inner", "middle", "outer"] | None = None,
    notes: str | None = None,
) -> bool:
    """Records or updates a discovered port's region, clock bearing (1-12), and ring depth."""
    return True


@llm_tool(category="mutator", allowed_states={"docked"})
def log_bazaar_bargain(
    repo,
    location_key: str,
    good_key: str,
    unit_price: float,
    trade_side: Literal["buy", "sell"] = "buy",
    expiry_epoch: int | None = None,
) -> bool:
    """Logs a temporary port bazaar bargain or market opportunity."""
    return True


@llm_tool(category="mutator", allowed_states={"docked", "enroute", "arriving"})
def upsert_action(
    repo,
    title: str,
    action_type: Literal["ambition", "quest", "prospect", "passenger", "officer", "secondment", "todo"] = "todo",
    action_id: str | None = None,
    target_location_key: str | None = None,
    priority: Literal["critical", "high", "routine", "low"] = "routine",
    action_status: Literal["active", "ready", "blocked"] = "active",
    parent_action_id: str | None = None,
    deadline_epoch: int | None = None,
    good_key: str | None = None,
    qty: int | None = None,
    notes: str | None = None,
) -> str:
    """Creates or updates a row in state_action and returns its canonical action_id (e.g., 'ACT-1001')."""
    return ""


@llm_tool(category="mutator", allowed_states={"docked", "enroute", "arriving"})
def resolve_action(
    repo,
    action_id: str,
    terminal_status: Literal["completed", "cancelled", "failed"] = "completed",
    notes: str | None = None,
) -> bool:
    """Transitions a state_action row to a terminal status without deleting it and unlocks dependent subtasks."""
    return True


@llm_tool(category="query")
def publish_logbook(
    repo,
    narrative_counsel: str,
    action_notes: dict[str, str] | None = None,
    force_render: bool = True,
) -> str | None:
    """Wraps render_logbook(repo, prose_patch=..., force_render=...) to render logbook.j2."""
    return None


def _get_scalar_or_none(repo, property_key: str):
    """Returns a scalar value from state_scalars, or None if not present."""
    try:
        return repo.get_cell("state_scalars", {"property_key": property_key}, "property_value")
    except LookupError:
        return None


def _resolve_exclusive_pair(
    rel_val,
    abs_val,
    rel_name: str,
    abs_name: str,
    *,
    non_negative_abs: bool = True,
) -> tuple[Literal["relative", "absolute"], int]:
    """Validates a mutually exclusive (relative, absolute) integer parameter pair."""
    if rel_val is not None and abs_val is not None:
        raise ValidationError(f"Provide either '{rel_name}' or '{abs_name}', not both.")
    if rel_val is not None:
        return "relative", _require_int(rel_val, rel_name)
    if abs_val is not None:
        int_val = _require_int(abs_val, abs_name)
        if non_negative_abs and int_val < 0:
            raise ValidationError(f"'{abs_name}' cannot be negative, got {int_val}.")
        return "absolute", int_val
    return "relative", 0


@llm_tool(category="mutator", allowed_states={"docked"})
def depart_station(
    repo,
    narrative_counsel: str = "",
    action_notes: dict[str, str] | None = None,
) -> dict:
    """
    Validates departure prose inputs and delegates port departure (docked -> departing -> enroute)
    to GameFSM.
    """
    if not isinstance(narrative_counsel, str):
        raise ToolArgumentTypeError(
            f"'narrative_counsel' must be a string, got {type(narrative_counsel).__name__}."
        )
    if action_notes is not None and not isinstance(action_notes, dict):
        raise ToolArgumentTypeError(
            f"'action_notes' must be a dict or None, got {type(action_notes).__name__}."
        )

    prose_patch = {
        "narrative_counsel": narrative_counsel,
        "action_notes": action_notes or {},
    }
    return GameFSM(repo).depart(
        render_fn=lambda: render_logbook(repo, prose_patch=prose_patch),
    )


@llm_tool(category="mutator", allowed_states={"enroute"})
def arrive_station(
    repo,
    location_key: str,
    transit_days: int | None = None,
    epoch: int | None = None,
    fuel_burned: int | None = None,
    fuel: int | None = None,
    supplies_burned: int | None = None,
    supplies: int | None = None,
    hull_delta: int | None = None,
    current_hull: int | None = None,
    crew_delta: int | None = None,
    current_crew: int | None = None,
    terror_delta: int | None = None,
    terror_level: int | None = None,
    nightmares_delta: int | None = None,
    nightmares_level: int | None = None,
) -> dict:
    """
    Parses and validates arrival parameters (accepting relative deltas or absolute values while
    rejecting competing parameters for the same dimension) and delegates the arrival transition
    (enroute -> arriving -> docked) to GameFSM.
    """
    loc_row = _validate_ref_key(repo, "ref_locations", "location_key", location_key, "location")

    # 1. Validate & resolve time
    current_epoch = int(_get_scalar_or_none(repo, "epoch") or 0)
    time_mode, time_val = _resolve_exclusive_pair(
        transit_days, epoch, "transit_days", "epoch", non_negative_abs=True
    )
    target_epoch = current_epoch + time_val if time_mode == "relative" else time_val
    if target_epoch < 0:
        raise ValidationError(
            f"Resulting epoch ({target_epoch}) cannot precede the 1905-01-01 calendar anchor."
        )

    # 2. Validate & resolve consumables (fuel, supplies)
    consumable_deltas: list[tuple[str, int]] = []
    for good_key, rel_arg, abs_arg, rel_name, abs_name in (
        ("fuel", fuel_burned, fuel, "fuel_burned", "fuel"),
        ("supplies", supplies_burned, supplies, "supplies_burned", "supplies"),
    ):
        mode, val = _resolve_exclusive_pair(rel_arg, abs_arg, rel_name, abs_name, non_negative_abs=True)
        if mode == "relative" and val == 0:
            continue
        if mode == "relative" and val < 0:
            raise ValidationError(f"'{rel_name}' cannot be negative, got {val}.")
        current_qty = _get_hold_qty(repo, good_key)
        delta = -val if mode == "relative" else (val - current_qty)
        if current_qty + delta < 0:
            raise DomainRuleError(
                f"Insufficient {good_key} in hold: have {current_qty}, cannot apply delta {delta}."
            )
        if delta != 0:
            consumable_deltas.append((good_key, delta))

    # 3. Validate & resolve vitals
    vital_updates: list[tuple[str, str, int]] = []
    for rel_arg, abs_arg, rel_name, abs_name, scalar_key in (
        (hull_delta, current_hull, "hull_delta", "current_hull", "current_hull"),
        (crew_delta, current_crew, "crew_delta", "current_crew", "current_crew"),
        (terror_delta, terror_level, "terror_delta", "terror_level", "terror_level"),
        (nightmares_delta, nightmares_level, "nightmares_delta", "nightmares_level", "nightmares_level"),
    ):
        mode, val = _resolve_exclusive_pair(rel_arg, abs_arg, rel_name, abs_name, non_negative_abs=True)
        vital_updates.append((mode, scalar_key, val))

    fsm = GameFSM(repo)

    def _apply_arrival() -> None:
        if target_epoch != current_epoch:
            epoch_res = set_game_epoch(repo, target_epoch)
            fsm.warnings.extend(epoch_res["warnings"])
        for good_key, delta in consumable_deltas:
            adjust_hold_qty(repo, good_key, delta)
        for mode, scalar_key, val in vital_updates:
            if mode == "relative":
                if val != 0:
                    adjust_scalar(repo, scalar_key, val)
            else:
                set_scalar(repo, scalar_key, val)

        loc_region = loc_row.get("region_name") or loc_row.get("region")
        if isinstance(loc_region, str) and loc_region.strip() and _get_scalar_or_none(repo, "region_name") is not None:
            set_scalar(repo, "region_name", loc_region.strip())

    return fsm.arrive(location_key=location_key, on_arriving=_apply_arrival)
