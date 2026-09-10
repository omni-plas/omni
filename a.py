"""Local, consent-based screen sharing server.

Run:
    python a.py

Open the printed URL in a browser. The host must explicitly press
"Start sharing" and approve the browser's screen-capture prompt.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
import json

HOST = "0.0.0.0"
PORT = 8000

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Local Screen Share</title>
<style>
body{font-family:system-ui,sans-serif;max-width:900px;margin:40px auto;padding:0 20px;background:#111;color:#eee}
button{padding:12px 18px;border:0;border-radius:10px;cursor:pointer;font-weight:700}
video{width:100%;max-height:75vh;background:#000;border-radius:14px;margin-top:20px}
#status{margin-top:12px;color:#bbb}.note{color:#aaa}
</style>
</head>
<body>
<h1>Local Screen Share</h1>
<p>On the device whose screen should be shared, press the button below and approve the browser's screen-sharing prompt.</p>
<button id="share">Start sharing this device</button>
<div id="status">Not sharing.</div>
<video id="screen" autoplay playsinline muted></video>
<script>
const button=document.getElementById('share');
const video=document.getElementById('screen');
const status=document.getElementById('status');
let stream=null;

button.onclick=async()=>{
  try {
    stream=await navigator.mediaDevices.getDisplayMedia({
      video:{cursor:'always'},
      audio:false
    });
    video.srcObject=stream;
    status.textContent='Screen sharing is active on this device. This page only previews the captured screen.';
    button.textContent='Stop sharing';
    stream.getVideoTracks()[0].addEventListener('ended', stop);
  } catch(e) {
    status.textContent='Screen sharing was cancelled or is not available in this browser.';
  }
};
function stop(){
  if(stream) stream.getTracks().forEach(t=>t.stop());
  stream=null; video.srcObject=null;
  button.textContent='Start sharing this device';
  status.textContent='Not sharing.';
}
button.addEventListener('dblclick',stop);
</script>
<p class="note">For viewing by another device, this simple version intentionally does not capture or transmit a screen without the host's explicit browser permission. A production multi-device version should use WebRTC signaling and authentication.</p>
</body>
</html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path != "/":
            self.send_error(404)
            return
        body = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Local screen-share page: http://127.0.0.1:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
