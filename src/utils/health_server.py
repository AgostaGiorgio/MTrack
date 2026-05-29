# src/utils/health_server.py
import threading
from src.config.logger import *
from http.server import HTTPServer, BaseHTTPRequestHandler

logger = logging.getLogger(__name__)

class HealthHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        if self.path in ("/healthz", "/live"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        elif self.path == "/ready":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"READY")
        else:
            self.send_response(404)
            self.end_headers()

def start_health_server(port: int = 9090):
    def _run():
        try:
            httpd = HTTPServer(("0.0.0.0", port), HealthHandler)
            logger.info(f"Health server running on port {port}")
            httpd.serve_forever()
        except Exception as e:
            logger.exception(f"Health server failed: {e}")

    t = threading.Thread(target=_run, daemon=True)
    t.start()
