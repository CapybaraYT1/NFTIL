from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import os

PORT = int(os.environ.get("PORT", 8080))

Handler = SimpleHTTPRequestHandler

with TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
