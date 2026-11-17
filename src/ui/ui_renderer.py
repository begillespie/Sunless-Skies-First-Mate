#!/usr/bin/env python3
"""
@subsystem: ui_renderer
@version: 1.0.0
@file src/ui/ui_renderer.py
@description Pure Jinja2 template loader and renderer for Sunless Skies First Mate.
Enforces StrictUndefined so missing payload keys fail loudly during tests.
"""
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from src.ui.logbook_service import build_logbook_payload, should_render_logbook
import pprint

DEFAULT_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"


def get_jinja_env(template_dir: str | Path = DEFAULT_TEMPLATE_DIR) -> Environment:
    """Creates a strictly validated Jinja2 environment."""
    return Environment(
        loader=FileSystemLoader(str(template_dir)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


def render_template(
    template_name: str,
    payload: dict,
    template_dir: str | Path = DEFAULT_TEMPLATE_DIR,
) -> str:
    """Renders a named Jinja2 template against a complete data payload dictionary."""
    if not isinstance(payload, dict):
        raise TypeError(f"payload must be a dictionary, got {type(payload).__name__}.")
    env = get_jinja_env(template_dir)
    template = env.get_template(template_name)
    return template.render(**payload)


def render_logbook(
    repo,
    prose_patch: dict | None = None,
    force_render: bool = False,
    template_dir: str | Path = DEFAULT_TEMPLATE_DIR,
) -> str | None:
    """
    Top-level UI presentation entry point:
    1. Evaluates the FSM suppression gate (returns None when navigation_state == 'enroute'
       unless force_render=True).
    2. Assembles the calculated payload via build_logbook_payload(repo, prose_patch).
    3. Renders 'logbook.j2' with StrictUndefined validation.
    """
    if not force_render and not should_render_logbook(repo):
        return None

    payload = build_logbook_payload(repo, prose_patch=prose_patch)
#    pprint.pprint(payload)
    return render_template("logbook.j2", payload, template_dir=template_dir)
