#!/usr/bin/env python3
"""
@subsystem: logbook_service
@version: 1.1.0
@file: src/ui/logbook_service.py
@description: Pandas-powered Logbook Assembler for Sunless Skies First Mate.
Queries BaseRepository tables, performs relational joins across state_* and ref_*
tables, computes metrics via src/services/calculators.py, formats badges via
src/ui/ui_tools.py, and safely merges the LLM's creative prose patch.
"""
import pandas as pd

from src.state.game_fsm import GameFSM
from src.services.calculators import (
    ATTRIBUTE_KEYS,
    calculate_attribute_perks,
    compute_hold_utilization,
    exports_good
)
from src.services.calendar import epoch_to_date
from src.ui.ui_tools import (
    format_iso_date,
    format_officer_perks,
    nightmares_badge,
    reserve_badge,
    resupply_badge,
    terror_badge,
    vitals_badge,
)

BRIDGE_STATIONS = (
    "first_officer",
    "quartermaster",
    "signaller",
    "chief_engineer",
    "mascot",
)

ACTIVE_STATUSES = ["active", "ready", "blocked"]

ALLOWED_PROSE_KEYS = {"narrative_counsel", "action_notes"}

KINETIC_STATE_DISPLAY = {
    "docked": "🟢 Docked",
    "departing": "🟡 Departing",
    "enroute": "🚀 Enroute",
    "arriving": "🟡 Arriving",
}

PRIORITY_BADGE_MAP = {
    "high": "‼️",
    "routine": "",
    "low": "🔻"
}

def _safe_get_table(repo, table_name: str) -> pd.DataFrame:
    """Fetches a table from repo, returning an empty DataFrame if optional table is unseeded."""
    try:
        return repo.get_table(table_name)
    except (LookupError, RuntimeError):
        return pd.DataFrame()


def _clean_cell(val, default=None):
    """Converts Pandas NaN/NA values to clean Python defaults."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return default
    return val


def should_render_logbook(repo) -> bool:
    """
    FSM presentation gate: suppresses full logbook rendering when navigation_state
    is 'enroute' (mid-sky transit), returning True for 'docked', 'departing', and 'arriving'.
    """
    fsm = GameFSM(repo)
    return fsm.get_current_state() != "enroute"


def _load_key_value_dict(repo, table_name: str) -> dict:
    """Reads a property_key/property_value table into a flat dictionary."""
    df = _safe_get_table(repo, table_name)
    if df.empty or not {"property_key", "property_value"} <= set(df.columns):
        return {}
    return dict(zip(df["property_key"], df["property_value"]))


def _load_scalars_dict(repo) -> dict:
    """Reads state_scalars table into a flat key -> value dictionary."""
    return _load_key_value_dict(repo, "state_scalars")


def _assemble_header_vitals(repo, scalars: dict) -> dict:
    """Assembles ship header metadata, epoch-derived dates, and vital gauges with badges."""
    fsm_state = _load_key_value_dict(repo, "state_fsm")

    epoch = int(scalars.get("current_epoch", scalars.get("epoch", 0)))
    iso_date = epoch_to_date(epoch)
    formatted_date = format_iso_date(iso_date, "%d %B, %Y")

    nav_state = str(fsm_state.get("navigation_state", scalars.get("navigation_state", "docked")))
    kinetic_state = KINETIC_STATE_DISPLAY.get(nav_state, nav_state.title())

    current_location = str(
        fsm_state.get(
            "current_location",
            fsm_state.get(
                "current_location_key",
                scalars.get("current_location_key", scalars.get("current_location", "unknown")),
            ),
        )
    )
    location_name = current_location.replace("_", " ").title()
    ref_loc_df = _safe_get_table(repo, "ref_locations")
    if not ref_loc_df.empty and "location_key" in ref_loc_df.columns:
        loc_matches = ref_loc_df[ref_loc_df["location_key"] == current_location]
        if not loc_matches.empty:
            name_col = "display_name" if "display_name" in loc_matches.columns else "name"
            if name_col in loc_matches.columns:
                location_name = str(_clean_cell(loc_matches.iloc[0][name_col], location_name))

    current_hull = int(scalars.get("current_hull", 0))
    max_hull = int(scalars.get("max_hull", 100))
    current_crew = int(scalars.get("current_crew", 0))
    max_crew = int(scalars.get("max_crew", 20))
    terror_level = int(scalars.get("terror", scalars.get("terror_level", 0)))
    nightmares_level = int(scalars.get("nightmares", scalars.get("nightmares_level", 0)))

    return {
        "display_date": formatted_date,
        "iso_date": iso_date,
        "epoch": epoch,
        "current_location": current_location,
        "location_name": location_name,
        "navigation_state": nav_state,
        "kinetic_state": kinetic_state,
        "region_name": str(scalars.get("region_name", "The Reach")),
        "captain_name": str(scalars.get("captain_name", "Captain")),
        "first_mate_name": str(scalars.get("first_mate_name", "First Mate")),
        "vessel_name": str(scalars.get("vessel_name", "The Orphean")),
        "model": str(scalars.get("model", scalars.get("vessel_model", "Spatchcock-class"))),
        "sovereigns": int(scalars.get("sovereigns", 0)),
        "current_hull": current_hull,
        "max_hull": max_hull,
        "hull_badge": vitals_badge(current_hull, max_hull),
        "current_crew": current_crew,
        "max_crew": max_crew,
        "crew_badge": vitals_badge(current_crew, max_crew),
        "terror_level": terror_level,
        "terror_badge": terror_badge(terror_level),
        "nightmares_level": nightmares_level,
        "nightmares_badge": nightmares_badge(nightmares_level),
        }


def _assemble_attributes(repo, scalars: dict) -> dict:
    """Pairs base captain skills/affiliations with active officer perk totals."""
    totals = calculate_attribute_perks(repo)
    attrs: dict[str, int] = {}

    for attr in ATTRIBUTE_KEYS:
        base_val = int(scalars.get(attr, 0))
        total_val = int(totals.get(attr, base_val))
        attrs[attr] = base_val
        short_name = attr.split("_", 1)[1]
        attrs[f"{short_name}_total"] = total_val

    return attrs


def _assemble_officers(repo) -> dict:
    """
    Left-joins state_officers with ref_officers on officer_key.
    Routes 'active' officers to fixed bridge stations and 'seconded' officers
    to secondment_outlook.
    """
    officers_by_station: dict[str, dict] = {
        station: {
            "name": "🔘 Vacant",
            "skills": "—",
            "affiliation": "—",
        }
        for station in BRIDGE_STATIONS
    }
    secondment_outlook: list[dict] = []

    roster_df = _safe_get_table(repo, "state_officers")
    ref_df = _safe_get_table(repo, "ref_officers")
    actions_df = _safe_get_table(repo, "state_action")
    ref_loc_df = _safe_get_table(repo, "ref_locations")

    loc_name_map: dict[str, str] = {}
    if not ref_loc_df.empty and "location_key" in ref_loc_df.columns:
        loc_col = "display_name" if "display_name" in ref_loc_df.columns else "name"
        if loc_col in ref_loc_df.columns:
            loc_name_map = dict(zip(ref_loc_df["location_key"], ref_loc_df[loc_col]))

    secondment_actions: dict[str, dict] = {}
    if not actions_df.empty and "action_type" in actions_df.columns:
        sec_rows = actions_df[
            (actions_df["action_type"] == "secondment")
            & (actions_df["action_status"].isin(ACTIVE_STATUSES))
        ]
        for sr in sec_rows.to_dict(orient="records"):
            ent_key = _clean_cell(sr.get("target_entity_key"))
            if ent_key:
                secondment_actions[str(ent_key)] = sr

    if roster_df.empty:
        return {
            "officers": officers_by_station,
            "secondment_outlook": secondment_outlook,
        }

    if not ref_df.empty and "officer_key" in ref_df.columns:
        merged = roster_df.merge(ref_df, on="officer_key", how="left")
    else:
        merged = roster_df.copy()

    for r in merged.to_dict(orient="records"):
        status = str(_clean_cell(r.get("officer_status"), "unassigned"))
        station = str(_clean_cell(r.get("position_slot"), _clean_cell(r.get("station"), "")))
        officer_key = str(r["officer_key"])
        name = str(_clean_cell(r.get("lexical_name"), _clean_cell(r.get("name"), officer_key)))

        if status == "active" and station in officers_by_station:
            officers_by_station[station] = {
                "officer_key": officer_key,
                "name": name,
                "station": station,
                "status": status,
                "skills": format_officer_perks(r, "skill_"),
                "affiliation": format_officer_perks(r, "affiliation_"),
            }

        elif status == "seconded":
            sec_act = secondment_actions.get(officer_key, {})
            loc_key = _clean_cell(sec_act.get("target_location_key"))
            port = _clean_cell(r.get("secondment_port")) or (
                loc_name_map.get(str(loc_key), str(loc_key)) if loc_key else None
            )
            notes = _clean_cell(r.get("notes")) or _clean_cell(sec_act.get("notes"))
            if port and notes:
                status_note = f"{name} ({port}) — {notes}"
            elif notes:
                status_note = f"{name} — {notes}"
            elif port:
                status_note = f"{name} seconded at {port}"
            else:
                status_note = f"{name} — Seconded"

            secondment_outlook.append({
                "officer_key": officer_key,
                "name": name,
                "status_note": status_note,
            })

    return {
        "officers": officers_by_station,
        "secondment_outlook": secondment_outlook,
    }


def _assemble_inventory(repo, scalars: dict) -> dict:
    """
    Computes hold utilization and left-joins state_inventory with ref_goods
    to build the 6-column cargo ledger (aliasing average_unit_cost -> mac).
    """
    utilization = compute_hold_utilization(repo)
    hold_capacity = int(scalars.get("hold_capacity", 30))
    hidden_slots = int(scalars.get("hidden_slots", 0))
    standard_used = utilization["standard_hold_used"]
    hidden_used = utilization["hidden_hold_used"]
    reserve_fuel_min = int(scalars.get("reserve_fuel_min", 5))
    reserve_supplies_min = int(scalars.get("reserve_supplies_min", 5))

    inv_df = _safe_get_table(repo, "state_inventory")
    ref_goods_df = _safe_get_table(repo, "ref_goods")

    inventory_rows: list[dict] = []
    fuel_qty = 0
    supplies_qty = 0

    if not inv_df.empty:
        if not ref_goods_df.empty and "good_key" in ref_goods_df.columns:
            merged = inv_df.merge(ref_goods_df, on="good_key", how="left")
        else:
            merged = inv_df.copy()

        for r in merged.to_dict(orient="records"):
            display_name = str(r["display_name"])
            good_key = str(r["good_key"])
            hold_qty = int(_clean_cell(r.get("hold_qty"), 0))
            bank_qty = int(_clean_cell(r.get("bank_qty"), 0))
            mac = round(float(_clean_cell(r.get("average_unit_cost"), 0.0)), 2)
            is_contraband = bool(_clean_cell(r.get("is_contraband"), False))

            if good_key == "fuel":
                fuel_qty = hold_qty
            elif good_key == "supplies":
                supplies_qty = hold_qty

            explicit_status = _clean_cell(r.get("status"))
            if explicit_status:
                status_label = str(explicit_status)
            elif is_contraband:
                status_label = "Contraband"
            else:
                status_label = "Standard"

            dest_port = str(_clean_cell(r.get("destination_port"), "—"))
            display_name = str(
                _clean_cell(
                    r.get("display_name"),
                    _clean_cell(r.get("name"), display_name.replace("_", " ").title()),
                )
            )

            inventory_rows.append({
                "display_name": display_name,
                "name": display_name,
                "hold_qty": hold_qty,
                "bank_qty": bank_qty,
                "mac": mac,
                "is_contraband": is_contraband,
                "status": status_label,
                "destination_port": dest_port,
            })

    remaining_slots = max(0, hold_capacity - standard_used)
    capacity_badge = vitals_badge(remaining_slots, max(1, hold_capacity))

    return {
        "hold_capacity": hold_capacity,
        "hidden_slots": hidden_slots,
        "standard_hold_used": standard_used,
        "hidden_hold_used": hidden_used,
        "capacity_badge": capacity_badge,
        "fuel_qty": fuel_qty,
        "fuel_badge": reserve_badge(fuel_qty, reserve_fuel_min),
        "supplies_qty": supplies_qty,
        "supplies_badge": reserve_badge(supplies_qty, reserve_supplies_min),
        "inventory_rows": inventory_rows,
    }

def _assemble_navigation(repo) -> dict:
    """
    Vectorized Pandas assembler for itinerary legs, off-itinerary pinned objectives,
    and active passengers. Converts to plain dicts only at the final step.
    """
    itinerary_df = _safe_get_table(repo, "state_navigation_itinerary")
    ref_loc_df = _safe_get_table(repo, "ref_locations")
    actions_df = _safe_get_table(repo, "state_action")

    loc_name_map: dict[str, str] = {}
    if not ref_loc_df.empty and "location_key" in ref_loc_df.columns:
        loc_col = "display_name" if "display_name" in ref_loc_df.columns else "name"
        if loc_col in ref_loc_df.columns:
            loc_name_map = dict(zip(ref_loc_df["location_key"], ref_loc_df[loc_col]))

    if not actions_df.empty and "action_status" in actions_df.columns:
        active_actions_df = actions_df[actions_df["action_status"].isin(ACTIVE_STATUSES)].copy()
    else:
        active_actions_df = pd.DataFrame()

    if not active_actions_df.empty:
        active_actions_df["type"] = active_actions_df["action_type"].fillna("todo").astype(str).str.lower()
        active_actions_df["priority_badge"] = (
            active_actions_df["priority"].fillna("routine").astype(str).str.lower().map(PRIORITY_BADGE_MAP).fillna("")
        )
        active_actions_df["note"] = active_actions_df["notes"].fillna("").astype(str)
        active_actions_df["location_name"] = active_actions_df["target_location_key"].map(
            lambda k: loc_name_map.get(k, str(k).replace("_", " ").title()) if pd.notna(k) and str(k) else "—"
        )

    # 1. Assemble itinerary legs
    legs: list[dict] = []
    itinerary_keys: set[str] = set()
    if not itinerary_df.empty:
        itinerary_keys = set(itinerary_df["location_key"].dropna())

        actions_by_stop: dict[int, list[dict]] = {}
        if not active_actions_df.empty:
            itinerary_actions_df = itinerary_df.merge(
                active_actions_df,
                left_on="location_key",
                right_on="target_location_key",
                how="inner",
            )
            if not itinerary_actions_df.empty:
                action_cols = ["action_id", "type", "priority_badge", "title", "note"]
                actions_by_stop = {
                    int(stop): grp[action_cols].to_dict(orient="records")
                    for stop, grp in itinerary_actions_df.groupby("sequence_order", sort=False)
                }

        for row in itinerary_df.sort_values("sequence_order").itertuples(index=False):
            stop = int(row.sequence_order)
            loc_key = str(row.location_key)
            location_name = str(loc_name_map.get(loc_key, loc_key.replace("_", " ").title()))
            legs.append({
                "sequence_order": stop,
                "location_key": loc_key,
                "location_name": location_name,
                "resupply_badge": resupply_badge(
                    exports_good(repo, loc_key, "fuel"),
                    exports_good(repo, loc_key, "supplies"),
                ),
                "actions": actions_by_stop.get(stop, []),
            })

    # 2. Assemble pinned_objectives (is_pinned == True & target_location_key NOT IN itinerary)
    pinned_objectives: list[dict] = []
    if not active_actions_df.empty and "is_pinned" in active_actions_df.columns:
        is_pinned_mask = active_actions_df["is_pinned"].apply(
            lambda v: str(v).strip().lower() in ("true", "1", "yes") if isinstance(v, str) else bool(_clean_cell(v, False))
        )
        pinned_mask = is_pinned_mask & ~active_actions_df["target_location_key"].isin(itinerary_keys)
        pinned_df = active_actions_df.loc[
            pinned_mask, ["action_id", "title", "priority_badge", "note", "location_name"]
        ].rename(columns={"location_name": "port"})
        pinned_objectives = pinned_df.to_dict(orient="records")

    # 3. Assemble active_passengers (action_type == "passenger")
    active_passengers: list[dict] = []
    if not active_actions_df.empty:
        pax_df = active_actions_df[active_actions_df["type"] == "passenger"].copy()
        if not pax_df.empty:
            for r in pax_df.to_dict(orient="records"):
                raw_dl = _clean_cell(r.get("deadline_epoch"))
                deadline_str = ""
                if raw_dl is not None and str(raw_dl).strip() != "":
                    dl_int = int(float(raw_dl))
                    deadline_str = f"{format_iso_date(epoch_to_date(dl_int))} (Day {dl_int})"
                active_passengers.append({
                    "action_id": r["action_id"],
                    "name": r["title"],
                    "destination": r["location_name"],
                    "deadline": deadline_str,
                })

    return {
        "legs": legs,
        "pinned_objectives": pinned_objectives,
        "active_passengers": active_passengers,
    }


def _merge_prose_patch(payload: dict, prose_patch: dict | None) -> dict:
    """
    Safely merges the LLM's lightweight creative prose patch ('narrative_counsel'
    and 'action_notes') into the assembled payload while blocking attempts to
    override calculated datastore state keys.
    """
    patch = prose_patch or {}
    if not isinstance(patch, dict):
        raise TypeError(f"prose_patch must be a dictionary or None, got {type(patch).__name__}.")

    forbidden_keys = set(patch.keys()) - ALLOWED_PROSE_KEYS
    if forbidden_keys:
        raise ValueError(
            f"prose_patch contains protected state keys that cannot be overridden by LLM prose: {sorted(forbidden_keys)}"
        )

    payload["narrative_counsel"] = str(patch.get("narrative_counsel") or "").strip()

    action_notes = patch.get("action_notes") or {}
    if not isinstance(action_notes, dict):
        raise TypeError("prose_patch['action_notes'] must be a dictionary mapping leg key/order to note text.")

    for leg in payload.get("legs", []):
        for action in leg.get("actions", []):
            act_id = action.get("action_id")
            if act_id and act_id in action_notes:
                action["note"] = str(action_notes[act_id]).strip()

    return payload


def build_logbook_payload(repo, prose_patch: dict | None = None) -> dict:
    """
    Main assembler entry point: pulls all required tables from repo, runs Pandas
    joins and deterministic calculators, formats badges, merges the LLM prose patch,
    and returns the complete dictionary ready for Jinja2 rendering.
    """
    scalars = _load_scalars_dict(repo)

    payload: dict = {}
    payload.update(_assemble_header_vitals(repo, scalars))
    payload.update(_assemble_attributes(repo, scalars))
    payload.update(_assemble_officers(repo))
    payload.update(_assemble_inventory(repo, scalars))
    payload.update(_assemble_navigation(repo))

    return _merge_prose_patch(payload, prose_patch)