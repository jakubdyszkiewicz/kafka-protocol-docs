#!/usr/bin/env python3
"""
Simple HTTP server for Kafka Protocol Docs
Serves static files and provides an API endpoint to list message files
"""

import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # API endpoint to list all JSON files in messages directory
        if self.path == '/api/messages':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            messages_dir = 'messages'
            files = []

            if os.path.exists(messages_dir):
                for filename in os.listdir(messages_dir):
                    if filename.endswith('.json'):
                        files.append(filename)

            self.wfile.write(json.dumps(files).encode())
        else:
            # Serve static files normally
            super().do_GET()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print(f"Open http://localhost:{PORT}/ in your browser")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()
