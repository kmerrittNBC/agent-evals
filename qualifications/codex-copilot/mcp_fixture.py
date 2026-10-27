"""Read-only, deterministic MCP stdio fixture for the frozen 50-tool catalog.

Run: python3 qualifications/codex-copilot/mcp_fixture.py
"""

import json
import sys
from pathlib import Path


CATALOG = json.loads(Path(__file__).with_name("mcp-catalog.json").read_text())
TOOLS = {tool["name"]: tool for tool in CATALOG["tools"]}


def respond(message):
    method = message.get("method")
    request_id = message.get("id")
    if request_id is None:
        return None
    if method == "initialize":
        result = {
            "protocolVersion": "2025-06-18",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "qualification-mcp-fixture", "version": "1.0.0"},
        }
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": [
            {key: tool[key] for key in ("name", "description", "inputSchema")}
            for tool in CATALOG["tools"]
        ]}
    elif method == "tools/call":
        params = message.get("params", {})
        tool = TOOLS.get(params.get("name"))
        if tool is None:
            return {"jsonrpc": "2.0", "id": request_id,
                    "error": {"code": -32602, "message": "Unknown tool"}}
        args = params.get("arguments", {})
        if not isinstance(args, dict) or not isinstance(args.get("query"), str):
            return {"jsonrpc": "2.0", "id": request_id,
                    "error": {"code": -32602, "message": "query must be a string"}}
        fixture = dict(tool["fixture_result"], query=args["query"])
        result = {"content": [{"type": "text", "text": json.dumps(fixture, sort_keys=True)}]}
    else:
        return {"jsonrpc": "2.0", "id": request_id,
                "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def main():
    for line in sys.stdin:
        try:
            message = json.loads(line)
            response = respond(message)
        except (ValueError, TypeError):
            response = {"jsonrpc": "2.0", "id": None,
                        "error": {"code": -32700, "message": "Invalid JSON"}}
        if response is not None:
            print(json.dumps(response, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    main()
