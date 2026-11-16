#!/usr/bin/env python3
"""
@subsystem: repository_interface
@version: 1.2.0
@file: src/interfaces/repository.py
@description Abstract repository contract for Sunless Skies data management.
Enforces the 'no silent methods' rule: all mutations return True on success.
"""
from abc import ABC, abstractmethod
from typing import Any
import pandas as pd


class BaseRepository(ABC):
    """Abstract interface defining data contract for engine state and reference tables."""

    @abstractmethod
    def get_table(self, table_name: str) -> pd.DataFrame:
        """Fetches an entire table/tab as a Pandas DataFrame."""
        pass

    @abstractmethod
    def get_row(self, table_name: str, primary_key: dict) -> dict:
        """Fetches a single row matching the primary key dictionary as a dictionary."""
        pass

    @abstractmethod
    def append_row(self, table_name: str, row_data: dict) -> bool:
        """Appends a new row to the specified table. Returns True on success."""
        pass

    @abstractmethod
    def update_row(self, table_name: str, primary_key: dict, updates: dict) -> bool:
        """Updates multiple columns for a single row matching the primary key dictionary. Returns True on success."""
        pass

    @abstractmethod
    def delete_row(self, table_name: str, primary_key: dict) -> bool:
        """Deletes a row matching the primary key dictionary. Returns True on success."""
        pass

    @abstractmethod
    def get_cell(self, table_name: str, primary_key: dict, column: str) -> Any:
        """Gets a single cell value targeted by primary key and column name."""
        pass

    @abstractmethod
    def set_cell(self, table_name: str, primary_key: dict, column: str, value: Any) -> bool:
        """Sets a single cell value targeted by primary key and column. Returns True on success."""
        pass