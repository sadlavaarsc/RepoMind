"""
MCP (Model Context Protocol) server for RepoMind
Provides tools for indexing and querying code repositories
"""
import os
from typing import Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server

from repomind.core import RepoMind
from repomind import __version__

# Initialize MCP server
server = Server("repomind")

# Global RepoMind instance
_repomind: Optional[RepoMind] = None


def get_repomind() -> RepoMind:
    """Get or create RepoMind instance."""
    global _repomind
    if _repomind is None:
        _repomind = RepoMind()
    return _repomind


@server.list_tools()
async def list_tools() -> list:
    """List available tools."""
    return [
        {
            "name": "index_repository",
            "description": "Index a code repository for querying",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Path to the repository directory"
                    }
                },
                "required": ["repo_path"]
            }
        },
        {
            "name": "query_repository",
            "description": "Query an indexed code repository",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Question about the repository"
                    }
                },
                "required": ["question"]
            }
        },
        {
            "name": "get_health",
            "description": "Check RepoMind service health",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "save_index",
            "description": "Save the current index to disk",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "index_path": {
                        "type": "string",
                        "description": "Path to save the index (optional, uses default if not provided)"
                    }
                }
            }
        },
        {
            "name": "load_index",
            "description": "Load an index from disk",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "index_path": {
                        "type": "string",
                        "description": "Path to load the index from"
                    }
                },
                "required": ["index_path"]
            }
        }
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> dict:
    """Handle tool calls."""
    try:
        if name == "get_health":
            return await handle_get_health()
        elif name == "index_repository":
            return await handle_index_repository(arguments)
        elif name == "query_repository":
            return await handle_query_repository(arguments)
        elif name == "save_index":
            return await handle_save_index(arguments)
        elif name == "load_index":
            return await handle_load_index(arguments)
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Unknown tool: {name}"
                    }
                ],
                "isError": True
            }
    except Exception as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error: {str(e)}"
                }
            ],
            "isError": True
        }


async def handle_get_health() -> dict:
    """Handle health check."""
    repomind = get_repomind()
    return {
        "content": [
            {
                "type": "text",
                "text": (
                    f"RepoMind MCP Server\n"
                    f"Version: {__version__}\n"
                    f"Status: healthy\n"
                    f"Indexed: {'Yes' if repomind.is_indexed else 'No'}"
                )
            }
        ]
    }


async def handle_index_repository(arguments: dict) -> dict:
    """Handle index_repository tool call."""
    repo_path = arguments.get("repo_path")

    if not repo_path:
        return {
            "content": [{"type": "text", "text": "Error: repo_path is required"}],
            "isError": True
        }

    if not os.path.exists(repo_path):
        return {
            "content": [{"type": "text", "text": f"Error: Repository path does not exist: {repo_path}"}],
            "isError": True
        }

    repomind = get_repomind()
    result = repomind.index_repository(repo_path)

    if not result["success"]:
        return {
            "content": [{"type": "text", "text": f"Indexing failed: {result['message']}"}],
            "isError": True
        }

    # Auto-save the index
    save_result = repomind.save_index()

    return {
        "content": [
            {
                "type": "text",
                "text": (
                    f"Successfully indexed repository!\n"
                    f"Path: {repo_path}\n"
                    f"Chunks: {result['num_chunks']}\n"
                    f"Index saved to: {save_result['index_path']}"
                )
            }
        ]
    }


async def handle_query_repository(arguments: dict) -> dict:
    """Handle query_repository tool call."""
    question = arguments.get("question")

    if not question:
        return {
            "content": [{"type": "text", "text": "Error: question is required"}],
            "isError": True
        }

    repomind = get_repomind()

    if not repomind.is_indexed:
        return {
            "content": [{"type": "text", "text": "Error: No index available. Please index a repository first using index_repository."}],
            "isError": True
        }

    result = repomind.query(question)

    sources_text = "\n".join(f"- {src}" for src in result["sources"])

    return {
        "content": [
            {
                "type": "text",
                "text": (
                    f"Answer:\n{result['answer']}\n\n"
                    f"Sources:\n{sources_text}\n\n"
                    f"Latency: {result['latency_ms']:.1f}ms"
                )
            }
        ]
    }


async def handle_save_index(arguments: dict) -> dict:
    """Handle save_index tool call."""
    index_path = arguments.get("index_path")

    repomind = get_repomind()

    if not repomind.is_indexed:
        return {
            "content": [{"type": "text", "text": "Error: No index available to save."}],
            "isError": True
        }

    result = repomind.save_index(index_path if index_path else None)

    return {
        "content": [
            {
                "type": "text",
                "text": f"Index saved successfully to: {result['index_path']}"
            }
        ]
    }


async def handle_load_index(arguments: dict) -> dict:
    """Handle load_index tool call."""
    index_path = arguments.get("index_path")

    if not index_path:
        return {
            "content": [{"type": "text", "text": "Error: index_path is required"}],
            "isError": True
        }

    repomind = get_repomind()
    result = repomind.load_index(index_path)

    if not result["success"]:
        return {
            "content": [{"type": "text", "text": f"Failed to load index: {result['message']}"}],
            "isError": True
        }

    return {
        "content": [
            {
                "type": "text",
                "text": (
                    f"Index loaded successfully!\n"
                    f"Path: {index_path}\n"
                    f"Chunks: {result.get('num_chunks', 'unknown')}"
                )
            }
        ]
    }


def create_mcp_server() -> Server:
    """Create and configure the MCP server."""
    return server


def run_mcp_server():
    """Run the MCP server using stdio transport."""
    import asyncio

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )

    asyncio.run(main())


if __name__ == "__main__":
    run_mcp_server()
