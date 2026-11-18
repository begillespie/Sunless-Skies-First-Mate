#!/usr/bin/env python3
"""
@subsystem: google_sheets_connector
@version: 1.3.0
@file: src/connectors/google_sheets_repo.py
@description: Concrete implementation of BaseRepository using Pandas and Google Sheets CSV exports.
"""
import io
import urllib.request
import pandas as pd
from typing import Any
from src.exceptions import DatastoreError, EntityNotFoundError
from src.interfaces.repository import BaseRepository


class GoogleSheetsRepository(BaseRepository):
    """
    Pulls data via Google Sheets CSV export endpoints and manages state in-memory via Pandas.
    """

    def __init__(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self._cache = {}

    def _fetch_sheet_as_df(self, sheet_name: str) -> pd.DataFrame:
        url = f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        try:
            req = urllib.request.urlopen(url)
            csv_data = req.read().decode("utf-8")
            return pd.read_csv(io.StringIO(csv_data))
        except Exception as e:
            raise DatastoreError(f"Failed to fetch sheet '{sheet_name}' from Google Sheets: {e}")

    def get_table(self, table_name: str) -> pd.DataFrame:
        if table_name not in self._cache:
            self._cache[table_name] = self._fetch_sheet_as_df(table_name)
        return self._cache[table_name]

    def get_row(self, table_name: str, primary_key: dict) -> dict:
        df = self.get_table(table_name)
        mask = pd.Series([True] * len(df))
        for pk_col, pk_val in primary_key.items():
            if pk_col not in df.columns:
                raise ValueError(f"Primary key column '{pk_col}' not found in table '{table_name}'.")
            mask &= (df[pk_col] == pk_val)

        matched_rows = df[mask]
        if matched_rows.empty:
            raise EntityNotFoundError(f"No row found matching primary key {primary_key} in table '{table_name}'.")

        return matched_rows.iloc[0].to_dict()

    def append_row(self, table_name: str, row_data: dict) -> bool:
        df = self.get_table(table_name)
        new_row_df = pd.DataFrame([row_data])
        self._cache[table_name] = pd.concat([df, new_row_df], ignore_index=True)
        return True

    def update_row(self, table_name: str, primary_key: dict, updates: dict) -> bool:
        df = self.get_table(table_name)
        for col in updates.keys():
            if col not in df.columns:
                raise ValueError(f"Update column '{col}' not found in table '{table_name}'.")

        mask = pd.Series([True] * len(df))
        for pk_col, pk_val in primary_key.items():
            if pk_col not in df.columns:
                raise ValueError(f"Primary key column '{pk_col}' not found in table '{table_name}'.")
            mask &= (df[pk_col] == pk_val)

        if not mask.any():
            raise EntityNotFoundError(f"No row found matching primary key {primary_key} in table '{table_name}'.")

        for col, val in updates.items():
            df.loc[mask, col] = val

        self._cache[table_name] = df
        return True

    def delete_row(self, table_name: str, primary_key: dict) -> bool:
        df = self.get_table(table_name)
        mask = pd.Series([True] * len(df))
        for pk_col, pk_val in primary_key.items():
            if pk_col not in df.columns:
                raise ValueError(f"Primary key column '{pk_col}' not found in table '{table_name}'.")
            mask &= (df[pk_col] == pk_val)

        if not mask.any():
            raise EntityNotFoundError(f"No row found matching primary key {primary_key} in table '{table_name}'.")

        self._cache[table_name] = df[~mask].reset_index(drop=True)
        return True

    def get_cell(self, table_name: str, primary_key: dict, column: str) -> Any:
        df = self.get_table(table_name)
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in table '{table_name}'.")

        mask = pd.Series([True] * len(df))
        for pk_col, pk_val in primary_key.items():
            if pk_col not in df.columns:
                raise ValueError(f"Primary key column '{pk_col}' not found in table '{table_name}'.")
            mask &= (df[pk_col] == pk_val)

        matched_rows = df[mask]
        if matched_rows.empty:
            raise EntityNotFoundError(f"No row found matching primary key {primary_key} in table '{table_name}'.")

        return matched_rows.iloc[0][column]

    def set_cell(self, table_name: str, primary_key: dict, column: str, value: Any) -> bool:
        df = self.get_table(table_name)
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in table '{table_name}'.")

        mask = pd.Series([True] * len(df))
        for pk_col, pk_val in primary_key.items():
            if pk_col not in df.columns:
                raise ValueError(f"Primary key column '{pk_col}' not found in table '{table_name}'.")
            mask &= (df[pk_col] == pk_val)

        if not mask.any():
            raise EntityNotFoundError(f"No row found matching primary key {primary_key} in table '{table_name}'.")

        df.loc[mask, column] = value
        self._cache[table_name] = df
        return True