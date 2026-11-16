#!/usr/bin/env python3
"""
@subsystem: calendar
@version: 1.3.0
@file: /src/tools/engine_tools.py
@description: Convert between ISO and epoch dates respecting time laws in the High Wilderness.
"""
import re

MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
MONTH_NAMES = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
)

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
