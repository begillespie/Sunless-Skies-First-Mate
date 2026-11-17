#!/usr/bin/env python3
"""
@subsystem: calculators
@version: 1.0.1
@file: /src/tools/calculators.py
@description: Deterministic state-transfer engine for Sunless Skies First Mate.
"""
import pandas as pd
import re
from typing import Any, Dict, Iterable, Literal
from src.interfaces.repository import *

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

def compute_mac(repo, good_key, acquired_qty: int, unit_price: float) -> float:
    """Recalculates Moving Average Unit Cost (Rule 3.1.3.1)."""
    
    if not isinstance(acquired_qty, int) or isinstance(acquired_qty, bool):
        raise TypeError("Acquired quantity must be an integer")
    if not isinstance(unit_price, (int, float)) or isinstance(unit_price, bool):
        raise TypeError("Unit price must be a number")

    try:
        row = repo.get_row("state_inventory", {"good_key": good_key})
    except(LookupError):
        return unit_price
    
    old_total_qty = row["hold_qty"] + row["bank_qty"]
    old_mac = row["average_unit_cost"]

    if not isinstance(old_total_qty, int) or isinstance(old_total_qty, bool):
        raise TypeError("Old total quantity must be an integer")
    if not isinstance(old_mac, (int, float)) or isinstance(old_mac, bool):
        raise TypeError("Old MAC must be a number")

    if old_total_qty < 0:
        raise ValueError("Old total quantity cannot be negative")
    if old_mac < 0:
        raise ValueError("Old MAC cannot be negative")
    if acquired_qty < 0:
        raise ValueError("Acquired quantity cannot be negative")
    if unit_price < 0:
        raise ValueError("Unit price cannot be negative")
    new_total = old_total_qty + acquired_qty
    if new_total <= 0:
        return 0.0
    return round(((old_total_qty * old_mac) + (acquired_qty * unit_price)) / new_total, 2)

def _get_scalar_cell(repo, key_name: str, default=0):
    """Reads a scalar value in data_package (property_key/property_value) schemas."""
    try:
        return repo.get_cell("state_scalars", {"property_key": key_name}, "property_value")
    except (LookupError, ValueError):
        return default


def compute_hold_utilization(repo) -> dict:
    """
    Computes standard hold and hidden hold utilization by querying the repository directly.
    - repo: data repository implementing the BaseRepository interface
    - returns: {"standard_hold_used": int, "hidden_hold_used": int} per Rule 3.1.2.2.
    """
    # 1. Fetch inventory and reference goods tables via repository
    inventory_df = repo.get_table("state_inventory")
    ref_goods_df = repo.get_table("ref_goods")
    
    # 2. Get hidden slots from scalar state
    try:
        hidden_slots = int(_get_scalar_cell(repo, "hidden_slots", 0))
    except ValueError:
        hidden_slots = 0

    if hidden_slots < 0:
        raise ValueError(f"hidden_slots must be a non-negative integer, got {hidden_slots}")

    # Merge inventory with reference goods to identify contraband items
    if "good_key" in inventory_df.columns and "good_key" in ref_goods_df.columns:
        merged_df = inventory_df.merge(ref_goods_df[["good_key", "is_contraband"]], on="good_key", how="left")
        # Default unmapped goods to not contraband
        merged_df["is_contraband"] = merged_df["is_contraband"].fillna(False).astype(bool)
    else:
        # Fallback if ref_goods lacks columns
        merged_df = inventory_df.copy()
        merged_df["is_contraband"] = False

    non_contraband = 0
    contraband = 0

    for idx, row in merged_df.iterrows():
        good_key = row.get("good_key")
        h_qty = row.get("hold_qty", 0)
        
        if not isinstance(h_qty, int) or isinstance(h_qty, bool) or h_qty < 0:
            raise ValueError(f"Inventory row for '{good_key}' has invalid 'hold_qty': {h_qty!r}. Must be a non-negative integer.")
        
        if not row["is_contraband"]:
            non_contraband += h_qty
        else:
            contraband += h_qty

    hidden_used = min(contraband, hidden_slots)
    spillover = max(0, contraband - hidden_slots)
    
    return {
        "standard_hold_used": non_contraband + spillover,
        "hidden_hold_used": hidden_used
    }


def calculate_attribute_perks(repo) -> dict[str, int]:
    """
    Read-only helper (zero side effects).
    Computes total values for all 8 skills and affiliations by adding active
    bridge officer perks from ref_officers to base values in state_scalars.
    """
    totals: dict[str, int] = {}
    for attr in ATTRIBUTE_KEYS:
        try:
            totals[attr] = int(_get_scalar_cell(repo, attr, 0))
        except ValueError:
            totals[attr] = 0

    roster_df = repo.get_table("state_officers")
    if roster_df.empty:
        return totals

    active_df = roster_df[roster_df["officer_status"] == "active"]
    if active_df.empty:
        return totals

    ref_df = repo.get_table("ref_officers")
    merged = active_df.merge(ref_df, on="officer_key", how="left")

    for attr in ATTRIBUTE_KEYS:
        short_name = attr.split("_", 1)[1]
        col = attr if attr in merged.columns else (short_name if short_name in merged.columns else None)
        if col is not None:
            totals[attr] += int(merged[col].fillna(0).sum())

    return totals

def exports_good(repo, location_key: str, good_key: str) -> bool:
    """
    Returns True if  location_key exports good_key
    """
    exports = set(repo.get_table("ref_location_goods").itertuples(index=False, name=None))
    try:
        return (location_key, good_key) in exports
    except:
        return False
