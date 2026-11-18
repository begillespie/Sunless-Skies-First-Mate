#!/usr/bin/env python3
"""
@subsystem: mcp_interface
@version: 1.0.0
@file: src/interfaces/mcp_interface.py
@description: Extensible Model Context Protocol (MCP) adapter interface and JSON-RPC 2.0
stdio server for Sunless Skies First Mate. Keeps repository credentials server-side.
"""
from abc import ABC, abstractmethod
import json
import sys

import src.tools.engine_tools  # noqa: F401 - ensures @llm_tool decorators populate TOOL_REGISTRY
from src.exceptions import DatastoreError, MinistryOfStandardsError
from src.interfaces.repository import BaseRepository
from src.tools.registry import dispatch_tool_call, get_tool_declarations

TELEGRAPH_SEVERED_ALERT = (
    "⚠️ EXECUTIVE OFFICER'S ALERT — TELEGRAPH LINK SEVERED. Captain, the bridge telegraph "
    "to our master ledger is dead or locked against my hand. I cannot verify our manifest "
    "or log new entries without risking phantom records."
)

MCP_PROTOCOL_VERSION = "2024-11-05"


class BaseMCPAdapter(ABC):
    """Abstract MCP adapter interface allowing different chat runners to host the engine."""

    def __init__(self, repo: BaseRepository):
        self.repo = repo

    @abstractmethod
    def list_tools(self, category: str | None = None) -> list[dict]:
        """Returns tool definitions formatted with MCP inputSchema declarations."""

    @abstractmethod
    def call_tool(self, name: str, arguments: dict | None = None) -> dict:
        """Executes a tool against the isolated repository and returns an MCP tool result."""

    @abstractmethod
    def serve(self) -> None:
        """Runs the adapter transport loop."""


class FirstMateMCPServer(BaseMCPAdapter):
    """Concrete MCP adapter supporting direct runner calls and JSON-RPC 2.0 stdio transport."""

    SERVER_INFO = {
        "name": "sunless-skies-first-mate",
        "version": "2.1.0",
    }

    def list_tools(self, category: str | None = None) -> list[dict]:
        """Converts TOOL_REGISTRY declarations into MCP tool entries."""
        return [
            {
                "name": decl["name"],
                "description": decl["description"],
                "inputSchema": decl["parameters"],
            }
            for decl in get_tool_declarations(category=category)
        ]

    def call_tool(self, name: str, arguments: dict | None = None) -> dict:
        """Dispatches a tool call against self.repo and translates Tier 1 / Tier 2 exceptions."""
        try:
            result = dispatch_tool_call(self.repo, name, arguments)
        except DatastoreError as exc:
            return {
                "content": [{"type": "text", "text": f"{TELEGRAPH_SEVERED_ALERT}\n({exc})"}],
                "isError": True,
                "errorTier": "infrastructure",
                "errorType": type(exc).__name__,
            }
        except MinistryOfStandardsError as exc:
            return {
                "content": [{"type": "text", "text": str(exc)}],
                "isError": True,
                "errorTier": "domain",
                "errorType": type(exc).__name__,
            }

        text = result if isinstance(result, str) else json.dumps(result)
        return {
            "content": [{"type": "text", "text": text}],
            "isError": False,
            "structuredContent": result,
        }

    def handle_jsonrpc_message(self, message: dict) -> dict | None:
        """Processes a single JSON-RPC 2.0 MCP request or notification."""
        if not isinstance(message, dict):
            return {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32600, "message": "Invalid Request"},
            }

        method = message.get("method")
        has_id = "id" in message
        msg_id = message.get("id")

        # Notifications carry no id and require no response
        if not has_id or method == "notifications/initialized":
            return None

        params = message.get("params") or {}

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": MCP_PROTOCOL_VERSION,
                    "capabilities": {"tools": {}},
                    "serverInfo": dict(self.SERVER_INFO),
                },
            }

        if method == "ping":
            return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"tools": self.list_tools()},
            }

        if method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments")
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": self.call_tool(tool_name, arguments),
            }

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }

    def serve(self, input_stream=None, output_stream=None) -> None:
        """Runs a line-delimited JSON-RPC 2.0 stdio transport loop."""
        in_stream = input_stream if input_stream is not None else sys.stdin
        out_stream = output_stream if output_stream is not None else sys.stdout

        for raw_line in in_stream:
            line = raw_line.strip()
            if not line:
                continue
            try:
                message = json.loads(line)
            except json.JSONDecodeError as exc:
                response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": f"Parse error: {exc}"},
                }
            else:
                response = self.handle_jsonrpc_message(message)

            if response is not None:
                out_stream.write(json.dumps(response) + "\n")
                out_stream.flush()
