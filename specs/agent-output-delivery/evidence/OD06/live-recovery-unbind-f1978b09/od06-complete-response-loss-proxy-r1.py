#!/usr/bin/env python3
import hashlib
import http.client
import json
import os
import socket
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 10019
UPSTREAM_HOST = "127.0.0.1"
UPSTREAM_PORT = 10018
STATE = Path("/tmp/od06-complete-response-loss-r1.observation.json")
RELEASE = Path("/tmp/od06-complete-response-loss-r1.release")

HOP_BY_HOP = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade",
}

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *_):
        return

    def _close_without_response(self):
        self.close_connection = True
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            self.connection.close()
        except OSError:
            pass

    def _handle(self):
        if STATE.exists() and not RELEASE.exists():
            self._close_without_response()
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length) if length else None
        headers = {
            name: value for name, value in self.headers.items()
            if name.lower() not in HOP_BY_HOP and name.lower() != "host"
        }
        headers["Host"] = f"{UPSTREAM_HOST}:{UPSTREAM_PORT}"
        connection = http.client.HTTPConnection(UPSTREAM_HOST, UPSTREAM_PORT, timeout=30)
        try:
            connection.request(self.command, self.path, body=body, headers=headers)
            response = connection.getresponse()
            response_body = response.read()
            should_drop = (
                self.command == "POST"
                and self.path.startswith("/agent/output-uploads/")
                and self.path.endswith("/complete")
                and not STATE.exists()
            )
            if should_drop:
                observation = {
                    "fault": "drop_committed_complete_response_then_hold_transport",
                    "droppedAt": int(time.time() * 1000),
                    "method": self.command,
                    "path": self.path,
                    "upstreamStatus": response.status,
                    "upstreamBodyBytes": len(response_body),
                    "upstreamBodySha256": hashlib.sha256(response_body).hexdigest(),
                    "authorizationPersisted": False,
                    "requestBodyPersisted": False,
                }
                temporary = STATE.with_suffix(".tmp")
                temporary.write_text(json.dumps(observation, indent=2) + "\n")
                os.replace(temporary, STATE)
                self._close_without_response()
                return

            self.send_response(response.status, response.reason)
            for name, value in response.getheaders():
                if name.lower() in HOP_BY_HOP or name.lower() == "content-length":
                    continue
                self.send_header(name, value)
            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers()
            if response_body:
                self.wfile.write(response_body)
        finally:
            connection.close()

    do_GET = _handle
    do_POST = _handle
    do_PUT = _handle
    do_DELETE = _handle
    do_PATCH = _handle

if __name__ == "__main__":
    STATE.unlink(missing_ok=True)
    RELEASE.unlink(missing_ok=True)
    server = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), Handler)
    print(f"proxy_ready={LISTEN_HOST}:{LISTEN_PORT}", flush=True)
    server.serve_forever()
