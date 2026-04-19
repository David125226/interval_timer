import http.server
import os
import socketserver
from pathlib import Path

PORT = 8000
web_dir = Path(__file__).resolve().parent
os.chdir(web_dir)

handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
    print(f"Serving interval timer at http://localhost:{PORT}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
