#!/usr/bin/env python3
"""
@subsystem: llm_tools_registry
@version: 1.0.0
@file: src/tools/registry.py
@description: Decorator and runtime dispatcher for the Sunless Skies LLM Tools API.
Introspects type hints to build JSON Schema declarations while stripping 'repo'
and enforcing an explicit allowlist of approved engine mutators/queries.
"""
import inspect
import types
from typing import Literal, Union, get_args, get_origin, get_type_hints

TOOL_REGISTRY: dict[str, dict] = {}


def _python_type_to_json_schema(hint) -> dict:
    """Converts Python type annotations (including Literal and Union) into JSON Schema."""
    origin = get_origin(hint)
    if origin is Literal:
        return {"type": "string", "enum": list(get_args(hint))}
    if origin in (Union, types.UnionType):
        args = [a for a in get_args(hint) if a is not type(None)]
        if set(args) <= {int, float}:
            return {"type": "number"}
        if len(args) == 1:
            return _python_type_to_json_schema(args[0])
    if hint is int:
        return {"type": "integer"}
    if hint is float:
        return {"type": "number"}
    if hint is bool:
        return {"type": "boolean"}
    return {"type": "string"}


def llm_tool(category: Literal["mutator", "query"] = "mutator"):
    """
    Registers a function in TOOL_REGISTRY for the LLM Tools API.
    Automatically strips the injected 'repo' argument from external schemas.
    """
    def decorator(fn):
        sig = inspect.signature(fn)
        hints = get_type_hints(fn)
        properties: dict[str, dict] = {}
        required: list[str] = []

        for param_name, param in sig.parameters.items():
            if param_name == "repo":
                continue
            hint = hints.get(param_name, str)
            properties[param_name] = _python_type_to_json_schema(hint)
            if param.default is inspect.Parameter.empty:
                required.append(param_name)

        TOOL_REGISTRY[fn.__name__] = {
            "fn": fn,
            "category": category,
            "declaration": {
                "name": fn.__name__,
                "description": inspect.cleandoc(fn.__doc__ or ""),
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }
        return fn

    return decorator


def get_tool_declarations(category: str | None = None) -> list[dict]:
    """Returns JSON Schema tool declarations for LLM function calling."""
    return [
        entry["declaration"]
        for entry in TOOL_REGISTRY.values()
        if category is None or entry["category"] == category
    ]


def dispatch_tool_call(repo, tool_name: str, arguments: dict | None = None):
    """
    Runtime entry point used by both production execution and Tier 3 write-interception tests.
    Injects the active repository instance and blocks unexposed functions.
    """
    if tool_name not in TOOL_REGISTRY:
        raise KeyError(f"Tool '{tool_name}' is not exposed in the LLM Tools API.")
    fn = TOOL_REGISTRY[tool_name]["fn"]
    kwargs = arguments or {}
    return fn(repo=repo, **kwargs)