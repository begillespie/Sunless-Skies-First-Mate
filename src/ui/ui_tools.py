#!/usr/bin/env python3
"""
@subsystem: ui_tools
@version: 1.0.0
@file: src/tools/ui_tools.py
@descripton UI presentation formatting, conditional status badges, and dynamic stat perk aggregation.
"""
from typing import Dict, Iterable, List


ATTRIBUTE_KEYS = (
    "skill_iron",
    "skill_mirrors",
    "skill_hearts",
    "skill_veils",
    "affiliation_academe",
    "affiliation_bohemia",
    "affiliation_establishment",
    "affiliation_villainy",
)


def vitals_badge(current: int, maximum: int) -> str:
    """Crew & Hull badge (Rule 4.4.2.1): >70% 🟢, 31%-70% 🟡, <=30% 🔴."""
    if not isinstance(current, int) or not isinstance(maximum, int) or isinstance(current, bool) or isinstance(maximum, bool):
        raise TypeError("Current and maximum must be integers")
    if current < 0:
        raise ValueError("Current cannot be negative")
    if maximum <= 0:
        raise ValueError("Maximum must be positive")
    if maximum < current:
        raise ValueError("Maximum cannot be less than current")
    ratio = current / maximum if maximum > 0 else 0.0
    if ratio > 0.70:
        return "🟢"
    if ratio > 0.30:
        return "🟡"
    return "🔴"


def terror_badge(terror: int) -> str:
    """Terror badge (Rule 4.4.2.2): 0-39 🟢, 40-69 🟡, >=70 🔴."""
    if not isinstance(terror, int) or isinstance(terror, bool):
        raise TypeError("Terror must be an integer")
    if terror < 0 or terror > 100:
        raise ValueError("Terror must be between 0 and 100")
    return "🟢" if terror < 40 else ("🟡" if terror < 70 else "🔴")


def reserve_badge(hold_qty: int, reserve_min: int) -> str:
    """Fuel & Supplies reserve badge (Rule 4.4.2.5): >min 🟢, ==min ⚠️, <min 🚨.
    """
    if not isinstance(hold_qty, int) or not isinstance(reserve_min, int) or isinstance(hold_qty, bool) or isinstance(reserve_min, bool):
        raise TypeError("Hold quantity and reserve minimum must be integers")
    if hold_qty < 0:
        raise ValueError("Hold quantity cannot be negative")
    if reserve_min < 0:
        raise ValueError("Reserve minimum cannot be negative")
    if hold_qty > reserve_min:
        return "🟢"
    if hold_qty == reserve_min:
        return "⚠️"
    return "🚨"


def format_officer_perks(officer_row: dict, prefix: str) -> str:
    """Formats 'skill_*' or 'affiliation_*' columns into '+5 Iron, -1 Hearts'."""
    formatted = []
    for attr in ATTRIBUTE_KEYS:
        if attr.startswith(prefix):
            val = int(officer_row.get(attr, 0) or 0)
            if val != 0:
                sign = "+" if val > 0 else ""
                label = attr.removeprefix(prefix).title()
                formatted.append(f"{sign}{val} {label}")
    return ", ".join(formatted) if formatted else "—"


def calculate_stats(captain_stats: Dict[str, int], active_officers: List[Dict]) -> Dict[str, int]:
    """
    Calculates total ship aptitude stats (Base + Perks) for the 8 canonical attributes.
    - captain_stats: Dict with keys: iron, mirrors, hearts, veils, academe, bohemia, establishment, villainy (all ints >= 0).
    - active_officers: List of dicts for active officers, each containing officer_key, officer_status, and the 8 perk_ values.
                       (Enforces officer_status == 'active' and allows mascot_dilly.perk_hearts == -1).
    Returns a dict with the 8 total stat values.
    """
    if not isinstance(captain_stats, dict):
        raise TypeError("captain_stats must be a dictionary.")
    if not isinstance(active_officers, list):
        raise TypeError("active_officers must be a list of dictionaries.")

    stat_keys = ["iron", "mirrors", "hearts", "veils", "academe", "bohemia", "establishment", "villainy"]
    totals = {}
    
    # 1. Validate and load captain base stats
    for k in stat_keys:
        val = captain_stats.get(k, 0)
        if not isinstance(val, int) or isinstance(val, bool) or val < 0:
            raise ValueError(f"Captain base stat '{k}' must be a non-negative integer, got {val}")
        totals[k] = val

    # 2. Validate and aggregate active officers
    for officer in active_officers:
        if not isinstance(officer, dict):
            raise TypeError("Each officer record in active_officers must be a dictionary.")
        
        status = officer.get("officer_status")

        if officer.get("officer_status") == "active":
        
            key = officer.get("officer_key")
            if not isinstance(key, str) or not key.strip():
                raise ValueError("Officer record missing a valid string 'officer_key'.")

            for k in stat_keys:
                perk_val = officer.get(f"perk_{k}", 0)
                if not isinstance(perk_val, int) or isinstance(perk_val, bool):
                    raise ValueError(f"Perk '{k}' for officer '{key}' must be an integer.")
                
                # Allow mascot_dilly to have perk_hearts == -1; all other perks must be >= 0
                min_allowed = -1 if (key == "mascot_dilly" and k == "hearts") else 0
                if perk_val < min_allowed:
                    raise ValueError(f"Perk '{k}' for officer '{key}' is {perk_val}, which violates minimum bound {min_allowed}.")
                
                totals[k] += perk_val

    return totals
