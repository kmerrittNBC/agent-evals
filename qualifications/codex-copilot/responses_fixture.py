"""Disposable, local Responses fixture for Codex provider configuration checks.

This is not a Copilot inference service. It emits a fixed response and records
only an allowlisted request summary, never headers or prompt bodies.
"""

from __future__ import annotations

import argparse
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from uuid import uuid4


def response(model: str) -> dict:
    response_id = f"resp_fixture_{uuid4().hex}"
    return {
        "id": response_id,
        "object": "response",
        "created_at": int(time.time()),
        "status": "completed",
        "model": model,
        "output": [
            {
                "id": f"msg_{uuid4().hex}",
                "type": "message",
                "status": "completed",
                "role": "assistant",
                "content": [
                    {"type": "output_text", "text": "Local fixture response. No Copilot inference occurred.", "annotations": []}
                ],
            }
        ],
        "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2},
    }


class Handler(BaseHTTPRequestHandler):
    server: "FixtureServer"

    def log_message(self, _format: str, *_args: object) -> None:
        # The standard handler logs request paths and remote addresses.
        return

    def do_GET(self) -> None:
        if self.path == "/health":
            self._json(200, {"status": "ready", "kind": "local-fixture"})
        elif self.path in ("/models", "/v1/models"):
            self._json(200, {"object": "list", "data": [
                {"id": model, "object": "model"} for model in self.server.models
            ]})
        else:
            self._json(404, {"error": {"message": "fixture path unavailable", "type": "invalid_request_error"}})

    def do_POST(self) -> None:
        if self.path not in ("/responses", "/v1/responses"):
            self._json(404, {"error": {"message": "fixture path unavailable", "type": "invalid_request_error"}})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 2_000_000:
                raise ValueError("invalid request size")
            body = json.loads(self.rfile.read(length))
            model = body.get("model")
            if model not in self.server.models:
                self._json(400, {"error": {"message": "model not pinned in fixture", "type": "invalid_request_error"}})
                return
            self.server.record({
                "model": model,
                "stream": body.get("stream") is True,
                "tool_count": len(body.get("tools") or []),
                "path": self.path,
            })
            result = response(model)
            if body.get("stream") is True:
                self._stream(result)
            else:
                self._json(200, result)
        except (ValueError, TypeError, json.JSONDecodeError):
            self._json(400, {"error": {"message": "invalid fixture request", "type": "invalid_request_error"}})

    def _json(self, code: int, body: dict) -> None:
        payload = json.dumps(body, separators=(",", ":")).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _stream(self, result: dict) -> None:
        item = result["output"][0]
        content = item["content"][0]
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        events = [
            ("response.created", {"type": "response.created", "response": {**result, "status": "in_progress", "output": []}}),
            ("response.output_item.added", {"type": "response.output_item.added", "output_index": 0, "item": {**item, "status": "in_progress", "content": []}}),
            ("response.content_part.added", {"type": "response.content_part.added", "output_index": 0, "content_index": 0, "part": {"type": "output_text", "text": "", "annotations": []}}),
            ("response.output_text.delta", {"type": "response.output_text.delta", "output_index": 0, "content_index": 0, "delta": content["text"]}),
            ("response.output_text.done", {"type": "response.output_text.done", "output_index": 0, "content_index": 0, "text": content["text"]}),
            ("response.content_part.done", {"type": "response.content_part.done", "output_index": 0, "content_index": 0, "part": content}),
            ("response.output_item.done", {"type": "response.output_item.done", "output_index": 0, "item": item}),
            ("response.completed", {"type": "response.completed", "response": result}),
        ]
        for name, data in events:
            self.wfile.write(f"event: {name}\ndata: {json.dumps(data, separators=(',', ':'))}\n\n".encode())
            self.wfile.flush()
        self.wfile.write(b"data: [DONE]\n\n")
        self.wfile.flush()


class FixtureServer(ThreadingHTTPServer):
    def __init__(self, port: int, models: tuple[str, ...], record_path: Path):
        super().__init__(("127.0.0.1", port), Handler)
        self.models = models
        self.record_path = record_path
        self.lock = threading.Lock()

    def record(self, value: dict) -> None:
        with self.lock:
            with self.record_path.open("a", encoding="utf-8") as file:
                file.write(json.dumps(value, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--record", type=Path, required=True)
    args = parser.parse_args()
    server = FixtureServer(args.port, ("gpt-6-sol", "gpt-6-luna"), args.record)
    print(json.dumps({"base_url": f"http://127.0.0.1:{server.server_port}/v1", "kind": "local-fixture"}), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
