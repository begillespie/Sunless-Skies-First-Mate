#!/usr/bin/env python3
"""
@subsystem: exceptions
@version: 1.0.0
@file: src/exceptions.py
@description: Domain-specific exception hierarchy for the Sunless Skies First Mate Engine.
All custom exceptions inherit from MinistryOfStandardsError as well as the corresponding
standard Python built-in exception for backward compatibility.
"""


class MinistryOfStandardsError(Exception):
    """Base exception for all Sunless Skies First Mate Engine errors."""


class DatastoreError(MinistryOfStandardsError, RuntimeError):
    """Tier 1 infrastructure failure: datastore unreachable, locked, or failed I/O."""


class UnknownToolError(MinistryOfStandardsError, KeyError):
    """Raised when an unexposed or unknown tool name is dispatched."""


class ToolArgumentTypeError(MinistryOfStandardsError, TypeError):
    """Raised when a tool argument has an invalid Python type (e.g. bool for int)."""


class ValidationError(MinistryOfStandardsError, ValueError):
    """Raised when a tool argument is malformed, empty, or out of valid range."""


class EntityNotFoundError(MinistryOfStandardsError, LookupError):
    """Raised when a requested key or record does not exist in reference or state tables."""


class DomainRuleError(MinistryOfStandardsError, ValueError):
    """Tier 2 domain invariant failure: insufficient resources, illegal state transition, or protected state."""


class InvalidTransitionError(DomainRuleError):
    """Raised when an FSM transition or state-restricted operation is illegal in the current navigation_state."""
