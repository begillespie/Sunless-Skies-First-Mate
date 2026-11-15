#!/usr/bin/env python3
"""
@subsystem: engine_tools
@version: 1.2.0
@file: /src/tools/engine_tools.py
@description: Deterministic calculation and state-transfer engine for Sunless Skies First Mate.
"""
import re
from typing import Any, Dict, Iterable, Literal

MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
MONTH_NAMES = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
)

PERMANENT_BASELINES = {"fuel", "supplies"}
ISO_DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def date_to_epoch(iso_date: str) -> int:
    """
    Converts ISO date string 'YYYY-MM-DD' to 0-indexed epoch day (1905-01-01 = 0, no leap years).
    Validates format and enforces the 1905-01-01 lower boundary via string comparison.
    """
    if not isinstance(iso_date, str) or not ISO_DATE_REGEX.match(iso_date.strip()):
        raise ValueError(f"Invalid date format '{iso_date}'. Expected ISO format 'YYYY-MM-DD'.")
    
    clean_date = iso_date.strip()
    if clean_date < "1905-01-01":
        raise ValueError(f"Date '{clean_date}' is prior to High Wilderness epoch anchor (1905-01-01).")

    year, month, day = map(int, clean_date.split("-"))
    if not (1 <= month <= 12) or not (1 <= day <= MONTH_DAYS[month - 1]):
        raise ValueError(f"Invalid calendar date values in '{clean_date}'.")

    return (year - 1905) * 365 + sum(MONTH_DAYS[: month - 1]) + (day - 1)


def epoch_to_date(epoch: int) -> str:
    """Converts 0-indexed epoch day to standardized ISO date string 'YYYY-MM-DD'."""
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
        raise ValueError(f"Epoch must be a non-negative integer, got {epoch}")
    
    year = 1905 + (epoch // 365)
    rem = epoch % 365
    for m_idx, m_days in enumerate(MONTH_DAYS):
        if rem < m_days:
            month = m_idx + 1
            day = rem + 1
            return f"{year:04d}-{month:02d}-{day:02d}"
        rem -= m_days
    raise RuntimeError("Unreachable calendar state")


def compute_mac(old_total_qty: int, old_mac: float, acquired_qty: int, unit_price: float) -> float:
    """Recalculates Moving Average Unit Cost (Rule 3.1.3.1)."""
    
    if not isinstance(old_total_qty, int) or isinstance(old_total_qty, bool):
        raise TypeError("Old total quantity must be an integer")
    if not isinstance(old_mac, (int, float)) or isinstance(old_mac, bool):
        raise TypeError("Old MAC must be a number")
    if not isinstance(acquired_qty, int) or isinstance(acquired_qty, bool):
        raise TypeError("Acquired quantity must be an integer")
    if not isinstance(unit_price, (int, float)) or isinstance(unit_price, bool):
        raise TypeError("Unit price must be a number")
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


def compute_hold_utilization_OLD(
    inventory_rows: Iterable[dict], contraband_keys: set[str], hidden_slots: int) -> dict:
    """
    Returns a structured dictionary for easy LLM parsing:
    {"standard_hold_used": int, "hidden_hold_used": int} per Rule 3.1.2.2.
    """
    if not isinstance(inventory_rows, Iterable):
        raise TypeError("inventory_rows must be an iterable of dictionaries")
    
    non_contraband = sum(int(r.get("hold_qty", 0)) for r in inventory_rows if r["good_key"] not in contraband_keys)
    contraband = sum(int(r.get("hold_qty", 0)) for r in inventory_rows if r["good_key"] in contraband_keys)
    hidden_used = min(contraband, hidden_slots)
    spillover = max(0, contraband - hidden_slots)
    
    return {
        "standard_hold_used": non_contraband + spillover,
        "hidden_hold_used": hidden_used
    }



def compute_hold_utilization(inventory_rows: Iterable[Dict[str, Any]], hidden_slots: int) -> dict:
    """
    Returns a structured dictionary for easy LLM parsing:
    {"standard_hold_used": int, "hidden_hold_used": int} per Rule 3.1.2.2.
    """
    if not isinstance(hidden_slots, int) or isinstance(hidden_slots, bool) or hidden_slots < 0:
        raise ValueError(f"hidden_slots must be a non-negative integer, got {hidden_slots}")
    
    contraband_keys = ["illicit_literature", "red_honey", "starshine"]  # Define contraband goods here; can be extended as needed.
    
    try:
        iterator = iter(inventory_rows)
    except TypeError:
        raise ValueError("inventory_rows must be an iterable collection of dictionaries.")

    non_contraband = 0
    contraband = 0

    for idx, r in enumerate(iterator):
        if not isinstance(r, dict):
            raise ValueError(f"Inventory row at index {idx} must be a dictionary, got {type(r).__name__}.")
        
        if "good_key" not in r or "hold_qty" not in r:
            raise ValueError(f"Inventory row at index {idx} is missing required keys ('good_key' or 'hold_qty').")
        
        good_key = r["good_key"]
        if not isinstance(good_key, str) or not good_key.strip():
            raise ValueError(f"Inventory row at index {idx} has invalid 'good_key': {good_key!r}")
        
        h_qty = r["hold_qty"]
        if not isinstance(h_qty, int) or isinstance(h_qty, bool) or h_qty < 0:
            raise ValueError(f"Inventory row for '{good_key}' has invalid 'hold_qty': {h_qty!r}. Must be a non-negative integer.")
        
        if good_key not in contraband_keys:
            non_contraband += h_qty
        else:
            contraband += h_qty

    hidden_used = min(contraband, hidden_slots)
    spillover = max(0, contraband - hidden_slots)
    
    return {
        "standard_hold_used": non_contraband + spillover,
        "hidden_hold_used": hidden_used
    }


def transfer_inventory(
    item_row: list,
    direction: Literal["deposit", "withdraw"],
    qty: int,
) -> str:
    """
    Simplifies bank transfers by operating on a single item row at a time.
    - item_row format: [good_key (str), hold_qty (int), bank_qty (int), average_unit_cost (float)]
    - direction: 'deposit' (Hold -> Bank) or 'withdraw' (Bank -> Hold)
    - qty: positive integer quantity to transfer
    - Capacity check is intentionally delayed until departure; returns updated line as a CSV string.
    """
    if not isinstance(item_row, list) or len(item_row) < 4:
        raise ValueError("Invalid item_row format. Expected [good_key, hold_qty, bank_qty, average_unit_cost]")
    if not isinstance(qty, int) or isinstance(qty, bool):
        raise TypeError("Transfer quantity must be an integer")
    
    if not isinstance(item_row[1], int) or not isinstance(item_row[2], int) or isinstance(item_row[1], bool) or isinstance(item_row[2], bool):
        raise TypeError("Hold and bank quantities must be integers")
    if not isinstance(item_row[3], (int, float)) or isinstance(item_row[3], bool):
        raise TypeError("Average unit cost must be a number")

    good_key, hold_qty, bank_qty, mac = item_row[0], int(item_row[1]), int(item_row[2]), float(item_row[3])
    
    if qty <= 0:
        raise ValueError(f"Transfer quantity must be positive, got {qty}")

    if direction == "deposit":
        if hold_qty < qty:
            raise ValueError(f"Insufficient hold quantity for deposit of '{good_key}': have {hold_qty}, trying to deposit {qty}.")
        hold_qty -= qty
        bank_qty += qty
    elif direction == "withdraw":
        if bank_qty < qty:
            raise ValueError(f"Insufficient bank quantity for withdrawal of '{good_key}': have {bank_qty}, trying to withdraw {qty}.")
        bank_qty -= qty
        hold_qty += qty
    else:
        raise ValueError(f"Invalid transfer direction '{direction}'. Expected 'deposit' or 'withdraw'.")

    updated_row = [good_key, hold_qty, bank_qty, f"{mac:.2f}"]
    return ",".join(map(str, updated_row))