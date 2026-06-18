"""
SkillPulse — Local Dev Server
Run: python server.py
Then open: http://localhost:3000
"""

import os
import json
import http.server
import socketserver
import urllib.request
import urllib.error
from pathlib import Path

def load_env():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

load_env()

PORT = 3000
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="public", **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/config.js":
            config = {
                "ANTHROPIC_API_KEY": API_KEY,
                "BRIGHT_DATA_TOKEN": os.environ.get("BRIGHT_DATA_TOKEN", ""),
            }
            body = f"window.ENV = {json.dumps(config)};".encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript")
            self.send_header("Content-Length", str(len(body)))
            self._cors()
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/api/chat":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

            # Detect provider from key prefix
            key = API_KEY
            if key.startswith("sk-ant-"):
                url = "https://api.anthropic.com/v1/messages"
                headers = {
                    "Content-Type": "application/json",
                    "x-api-key": key,
                    "anthropic-version": "2023-06-01",
                }
            else:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {key}",
                }

            try:
                req = urllib.request.Request(url, data=body, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=90) as resp:
                    result = resp.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(result)))
                self._cors()
                self.end_headers()
                self.wfile.write(result)
            except urllib.error.HTTPError as e:
                err = e.read()
                self.send_response(e.code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(err)))
                self._cors()
                self.end_headers()
                self.wfile.write(err)
            return

        self.send_response(404)
        self.end_headers()

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        print(f"  {args[0]} {args[1]}")

key_type = "OpenAI" if API_KEY.startswith("sk-") and not API_KEY.startswith("sk-ant-") else "Anthropic" if API_KEY.startswith("sk-ant-") else "missing"
print(f"\n🚀 SkillPulse running at http://localhost:{PORT}")
print(f"   API key: {'✓ ' + key_type if API_KEY.startswith('sk-') else '✗ check .env'}\n")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
