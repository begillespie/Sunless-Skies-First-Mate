#!/usr/bin/env python3
"""
@subsystem: mcp_entrypoint
@version: 1.0.0
@file: src/mcp_server.py
@description: Stdio MCP server entrypoint for Antigravity and compatible chat runners.
"""
from src.config import create_repository
from src.interfaces.mcp_interface import FirstMateMCPServer


def main(env_path: str | None = None) -> None:
    """Initializes the configured repository from .env and starts the stdio MCP server."""
    repo = create_repository(env_path=env_path)
    server = FirstMateMCPServer(repo)
    server.serve()


if __name__ == "__main__":
    main()
