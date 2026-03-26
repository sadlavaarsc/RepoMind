#!/usr/bin/env python
"""
Start the RepoMind MCP server.

Usage:
    python scripts/start_mcp_server.py
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repomind.mcp.server import run_mcp_server

if __name__ == "__main__":
    run_mcp_server()
