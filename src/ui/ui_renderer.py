#!/usr/bin/env python3
"""
@subsystem: ui_renderer
@version: 1.0.0
@file: src/tools/ui_renderer.py
@descripton Assembles data payload and renders Jinja2 logbook template.
"""
from jinja2 import Environment
from pathlib import Path
from datetime import date
from ui.ui_tools import calculate_stats, vitals_badge, terror_badge, reserve_badge
from services.calculators import compute_hold_utilization

# formatted = "{dt.day} {dt:%B} {dt:%Y}".format(dt=date.fromisoformat("1907-02-08")) # date converter
