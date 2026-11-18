#!/usr/bin/env python3
"""
Unit tests for .env configuration loading and the extensible MCP server interface.
"""
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd

from src.config import (
    REPOSITORY_FACTORIES,
    EngineConfig,
    create_repository,
    load_dotenv,
    register_repository_backend,
)
from src.connectors.google_sheets_repo import GoogleSheetsRepository
from src.exceptions import DatastoreError, ValidationError
from src.interfaces.repository import BaseRepository
from src.interfaces.mcp_interface import (
    MCP_PROTOCOL_VERSION,
    TELEGRAPH_SEVERED_ALERT,
    BaseMCPAdapter,
    FirstMateMCPServer,
)


class _BrokenRepo(GoogleSheetsRepository):
    """Test repository that simulates an unreachable datastore."""

    def get_table(self, table_name: str) -> pd.DataFrame:
        raise DatastoreError(f"Simulated network outage fetching '{table_name}'")


class TestConfigAndMCPInterface(unittest.TestCase):

    def setUp(self):
        self.repo = GoogleSheetsRepository("mock_id")
        self.repo._cache["state_fsm"] = pd.DataFrame([
            {"property_key": "navigation_state", "property_value": "docked"},
            {"property_key": "current_location", "property_value": "new_winchester"},
            {"property_key": "last_location", "property_value": "new_winchester"},
        ])
        self.repo._cache["state_scalars"] = pd.DataFrame([
            {"property_key": "epoch", "property_value": 30},
            {"property_key": "sovereigns", "property_value": 500},
        ])
        self.repo._cache["ref_goods"] = pd.DataFrame([
            {"good_key": "fuel", "display_name": "Barrel of Fuel", "is_contraband": False},
        ])
        self.repo._cache["state_inventory"] = pd.DataFrame([
            {"good_key": "fuel", "hold_qty": 8, "bank_qty": 0, "average_unit_cost": 10.0},
        ])
        self.server = FirstMateMCPServer(self.repo)

    def test_dotenv_and_engine_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            env_file.write_text(
                '# comment line\n'
                'SUNLESS_SKIES_DATASTORE_URI="sheet_abc_123"\n'
                "export SUNLESS_SKIES_REPOSITORY_BACKEND='google_sheets'\n"
                'SUNLESS_SKIES_REPO_TIMEOUT=30\n',
                encoding="utf-8",
            )
            with patch.dict(os.environ, {}, clear=True):
                parsed = load_dotenv(env_file)
                self.assertEqual(parsed["SUNLESS_SKIES_DATASTORE_URI"], "sheet_abc_123")
                cfg = EngineConfig.from_env(env_file)
                self.assertEqual(cfg.datastore_uri, "sheet_abc_123")
                self.assertEqual(cfg.repository_backend, "google_sheets")
                self.assertEqual(cfg.options, {"timeout": "30"})

                repo = create_repository(cfg)
                self.assertIsInstance(repo, BaseRepository)
                self.assertIsInstance(repo, GoogleSheetsRepository)
                self.assertEqual(repo.spreadsheet_id, "sheet_abc_123")

        # Registering a custom backend works without modifying config.py
        class _PonyExpressRepo(GoogleSheetsRepository):
            def __init__(self, uri: str, options: dict[str, str]):
                super().__init__(uri)
                self.options = options

        register_repository_backend(
            "pony_express",
            lambda cfg: _PonyExpressRepo(cfg.datastore_uri, cfg.options),
        )
        self.addCleanup(REPOSITORY_FACTORIES.pop, "pony_express", None)
        custom_repo = create_repository(
            EngineConfig(
                datastore_uri="saddlebag://new-winchester",
                repository_backend="pony_express",
                options={"relay": "fast"},
            )
        )
        self.assertIsInstance(custom_repo, _PonyExpressRepo)
        self.assertEqual(custom_repo.spreadsheet_id, "saddlebag://new-winchester")
        self.assertEqual(custom_repo.options, {"relay": "fast"})

        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(DatastoreError):
                EngineConfig.from_env(Path(tmpdir) / "missing.env")

        with self.assertRaises(ValidationError):
            create_repository(EngineConfig(datastore_uri="abc", repository_backend="sqlite"))

    def test_list_tools_strips_repo_and_formats_mcp_schema(self):
        self.assertIsInstance(self.server, BaseMCPAdapter)
        tools = self.server.list_tools()
        self.assertTrue(len(tools) > 0)
        names = {tool["name"] for tool in tools}
        self.assertIn("buy_goods", names)
        self.assertIn("depart_station", names)
        self.assertIn("arrive_station", names)

        for tool in tools:
            self.assertIn("inputSchema", tool)
            self.assertNotIn("repo", tool["inputSchema"]["properties"])
            self.assertNotIn("repo", tool["inputSchema"]["required"])

    def test_call_tool_success_and_error_tiers(self):
        # Valid call succeeds
        ok_res = self.server.call_tool("adjust_scalar", {"property_key": "sovereigns", "delta": 50})
        self.assertFalse(ok_res["isError"])
        self.assertTrue(ok_res["structuredContent"])
        self.assertEqual(
            self.repo.get_cell("state_scalars", {"property_key": "sovereigns"}, "property_value"),
            550,
        )

        # Tier 2 domain error: buy_goods blocked while enroute
        self.repo.set_cell("state_fsm", {"property_key": "navigation_state"}, "property_value", "enroute")
        domain_err = self.server.call_tool("buy_goods", {"good_key": "fuel", "qty": 1, "unit_price": 10.0})
        self.assertTrue(domain_err["isError"])
        self.assertEqual(domain_err["errorTier"], "domain")
        self.assertEqual(domain_err["errorType"], "InvalidTransitionError")

        # Tier 2 unknown tool error
        unknown_err = self.server.call_tool("nonexistent_tool", {})
        self.assertTrue(unknown_err["isError"])
        self.assertEqual(unknown_err["errorTier"], "domain")
        self.assertEqual(unknown_err["errorType"], "UnknownToolError")

        # Tier 1 datastore error returns Telegraph Severed alert
        broken_server = FirstMateMCPServer(_BrokenRepo("broken_id"))
        infra_err = broken_server.call_tool("adjust_scalar", {"property_key": "sovereigns", "delta": 10})
        self.assertTrue(infra_err["isError"])
        self.assertEqual(infra_err["errorTier"], "infrastructure")
        self.assertEqual(infra_err["errorType"], "DatastoreError")
        self.assertIn(TELEGRAPH_SEVERED_ALERT, infra_err["content"][0]["text"])

    def test_jsonrpc_stdio_session(self):
        requests = [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": MCP_PROTOCOL_VERSION},
            },
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "convert_epoch_to_date",
                    "arguments": {"epoch": 30},
                },
            },
            {"jsonrpc": "2.0", "id": 4, "method": "unknown/method"},
        ]
        in_stream = io.StringIO("\n".join(json.dumps(r) for r in requests) + "\n")
        out_stream = io.StringIO()

        self.server.serve(input_stream=in_stream, output_stream=out_stream)

        responses = [json.loads(line) for line in out_stream.getvalue().splitlines() if line.strip()]
        # Notification produces no response, so 4 responses expected
        self.assertEqual(len(responses), 4)
        self.assertEqual(responses[0]["id"], 1)
        self.assertEqual(responses[0]["result"]["serverInfo"]["name"], "sunless-skies-first-mate")
        self.assertEqual(responses[1]["id"], 2)
        self.assertTrue(len(responses[1]["result"]["tools"]) > 0)
        self.assertEqual(responses[2]["id"], 3)
        self.assertFalse(responses[2]["result"]["isError"])
        self.assertEqual(responses[2]["result"]["content"][0]["text"], "1905-01-31")
        self.assertEqual(responses[3]["id"], 4)
        self.assertEqual(responses[3]["error"]["code"], -32601)


if __name__ == "__main__":
    unittest.main()
