from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
import html
import socket

HOST = "0.0.0.0"
PORT = 8000


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        user_agent = self.headers.get("User-Agent", "Unknown")
        path = urlparse(self.path).path

        if path != "/":
            self.send_error(404)
            return

        page = f"""<!doctype html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Omni Local</title>
  <style>
    body {{ font-family: sans-serif; max-width: 720px; margin: 60px auto; padding: 20px; text-align: center; }}
    .card {{ padding: 30px; border-radius: 18px; box-shadow: 0 4px 24px #0002; }}
    .ip {{ font-size: 2rem; direction: ltr; margin: 20px 0; }}
    .ua {{ word-break: break-word; color: #555; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>محیط محلی Omni</h1>
    <p>آدرس IP دستگاهی که این صفحه را باز کرده:</p>
    <div class="ip"><strong>{html.escape(client_ip)}</strong></div>
    <p class="ua">مرورگر/دستگاه: {html.escape(user_agent)}</p>
  </div>
</body>
</html>"""

        data = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}")


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    hostname = socket.gethostname()
    print("Omni local environment started.")
    print(f"Local:   http://127.0.0.1:{PORT}")
    print(f"Network: http://<THIS_DEVICE_IP>:{PORT}")
    print(f"Host:    {hostname}")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Omni local environment...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
