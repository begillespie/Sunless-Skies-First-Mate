#!/usr/bin/env python3
"""
@subsystem: ui_tools
@version: 1.1.1
@file: src/tools/ui_tools.py
@descripton Stateless micro-formatters for Sunless Skies First Mate UI presentation.
"""
from datetime import date
import numbers

from src.services.calculators import ATTRIBUTE_KEYS
from src.services.calendar import ISO_DATE_REGEX

def vitals_badge(current: int | float, maximum: int | float) -> str:
    """
    Evaluates a current/maximum ratio (Hull, Crew) and returns a status indicator badge:
    - '🟢' when ratio >= 0.70
    - '🟡' when 0.25 <= ratio < 0.70
    - '🔴' when ratio < 0.25 or current <= 0
    """
    if not isinstance(current, numbers.Real) or isinstance(current, bool):
        raise TypeError(f"current must be numeric, got {current!r}")
    if not isinstance(maximum, numbers.Real) or isinstance(maximum, bool):
        raise TypeError(f"maximum must be numeric, got {maximum!r}")
    if maximum <= 0:
        raise ValueError(f"maximum must be positive, got {maximum}")
    if maximum < current:
        raise ValueError("Maximum cannot be less than current")

    if current <= 0:
        return "🔴"
    ratio = float(current) / float(maximum)
    if ratio < 0.25:
        return "🔴"
    if ratio < 0.70:
        return "🟡"
    return "🟢"


def terror_badge(terror_level: int) -> str:
    """
        Evaluates crew dread (0-100) and returns a threat badge:
        - '🚨' when terror_level >= 75
        - '⚠️' when terror_level >= 50
        - '🟡' when terror_level >= 25
        - '🟢' otherwise
        """
    if not isinstance(terror_level, numbers.Integral) or isinstance(terror_level, bool):
        raise TypeError(f"terror_level must be an integer, got {terror_level!r}")
    if terror_level < 0 or terror_level >100:
        raise ValueError("terror_level must be between 0 and 100.")

    if terror_level >= 75:
        return "🚨"
    if terror_level >= 50:
        return "🔴"
    if terror_level >= 25:
        return "🟡"
    return "🟢"


def nightmares_badge(nightmares_level: int) -> str:
    """
    Evaluates captain nightmares (0-4) and returns a threat badge:
    - '🚨' when nightmares_level >= 3
    - '🔴' when nightmares_level >= 2
    - '🟡' when nightmares_level >= 1
    - '🟢' otherwise
    """
    if not isinstance(nightmares_level, numbers.Integral) or isinstance(nightmares_level, bool):
        raise TypeError(f"nightmares_level must be an integer, got {nightmares_level!r}")
    if nightmares_level < 0 or nightmares_level > 4:
        raise ValueError("Nightmares must be between 0 and 4")

    if nightmares_level >= 3:
        return "🚨"
    if nightmares_level >= 2:
        return "🔴"
    if nightmares_level >= 1:
        return "🟡"
    return "🟢"


def reserve_badge(hold_qty: int, reserve_min: int) -> str:
    """
    Evaluates consumable reserve quantities (Fuel, Supplies) against a minimum safe threshold:
    - '🟢' when qty > threshold
    - '⚠️' when qty == threshold
    - '🔴' when threshold * 0.5 <= qty < threshold
    - '🚨' when qty <= 0 or qty < (threshold * 0.5)
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
    if hold_qty >= float(reserve_min) * 0.5:
        return "🔴"
    return "🚨"


def resupply_badge(has_fuel: bool, has_supplies: bool) -> str:
    """
    Evaluates resupply availability and returns a resupply badge:
    - '🔴' when no resupply is available
    - '🟡' when either fuel OR supplies are available
    - '🟢' when fuel AND supplies are available
    """ 
    if has_fuel and has_supplies:
        return "🟢"
    elif has_fuel or has_supplies:
        return "🟡"
    else:
        return "🔴"


def format_officer_perks(officer_row: dict, prefix: str) -> str:
    """
    Scans ATTRIBUTE_KEYS matching prefix ('skill_' or 'affiliation_') and formats
    non-zero modifiers into signed strings (e.g. '+5 Iron, -1 Hearts' or '—').
    """
    if prefix not in ("skill_", "affiliation_"):
        raise ValueError(f"Invalid prefix '{prefix}'. Expected 'skill_' or 'affiliation_'.")

    formatted: list[str] = []
    for attr in ATTRIBUTE_KEYS:
        if attr.startswith(prefix):
            short_name = attr[len(prefix):]
            raw_val = officer_row.get(attr, officer_row.get(short_name, 0))
            val = int(raw_val) if raw_val is not None and raw_val == raw_val else 0
            if val != 0:
                sign = "+" if val > 0 else ""
                label = short_name.replace("_", " ").title()
                formatted.append(f"{sign}{val} {label}")
    return ", ".join(formatted) if formatted else "—"


def format_iso_date(iso_date: str, fmt: str = "%d %B, %Y") -> str:
    """
    Formats a standardized ISO date string ('YYYY-MM-DD') using Python's built-in
    datetime.date.fromisoformat() and strftime(), stripping leading/trailing whitespace.
    """
    if not isinstance(iso_date, str) or not ISO_DATE_REGEX.match(iso_date.strip()):
        raise ValueError(f"Invalid ISO date string '{iso_date}'. Expected 'YYYY-MM-DD'.")

    parsed = date.fromisoformat(iso_date.strip())
    return parsed.strftime(fmt).lstrip("0")
