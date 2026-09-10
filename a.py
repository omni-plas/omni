"""Consent-based local screen sharing over WebRTC.

Run by double-clicking a.py or with:
    python a.py

The program starts the local server and opens the browser automatically.
The page first shows Cancel and Start. Start asks the browser for explicit
screen-capture permission. For continuous sharing across navigation, choose
"Entire Screen" in the browser's native sharing dialog. Once the whole screen
is selected, changing apps, windows, or browser pages does not stop sharing.

The browser itself controls the final capture choice; Python/JavaScript cannot
silently select a screen or bypass the browser permission dialog.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import json
import secrets
import threading
import time
import webbrowser

HOST = "0.0.0.0"
PORT = 8000
ROOMS = {}
LOCK = threading.Lock()

HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Omni Screen Share</title>
<style>
body{font-family:system-ui,sans-serif;max-width:1000px;margin:32px auto;padding:0 18px;background:#111;color:#eee}
button,input{font:inherit;padding:12px 18px;border-radius:9px;border:1px solid #555}button{cursor:pointer;font-weight:700}
.actions{display:flex;gap:12px;margin:22px 0}.cancel{background:#222;color:#eee}.start{background:#eee;color:#111}
video{display:block;width:100%;max-height:75vh;background:#000;border-radius:14px;margin-top:18px}
#code{font-size:1.3rem;font-weight:700;letter-spacing:.15em}.muted{color:#aaa}.hidden{display:none}
</style></head>
<body>
<h1>Omni Screen Share</h1>
<div id="host">
  <p id="intro">Ready to share this device screen.</p>
  <div class="actions">
    <button id="cancel" class="cancel">Cancel</button>
    <button id="start" class="start">Start</button>
  </div>
  <p id="roomLine" class="hidden">Room code: <span id="code"></span></p>
  <p id="hostStatus" class="muted">Not sharing.</p>
  <video id="hostPreview" autoplay muted playsinline></video>
</div>
<div id="viewer" class="hidden">
  <p>Viewer mode. Enter the room code supplied by the host.</p>
  <input id="room" placeholder="Room code" maxlength="12" autocomplete="off">
  <button id="join">Join</button>
  <p id="viewerStatus" class="muted">Waiting.</p>
  <video id="remote" autoplay playsinline controls></video>
</div>
<script>
const qs=new URLSearchParams(location.search);
const isViewer=qs.has('room') || location.hash==='#viewer';
const host=document.querySelector('#host'), viewer=document.querySelector('#viewer');
if(isViewer){host.classList.add('hidden');viewer.classList.remove('hidden');
  if(qs.get('room')) document.querySelector('#room').value=qs.get('room');}

const state={pc:null,stream:null,room:null,client:null,closed:false};
const iceServers={iceServers:[{urls:['stun:stun.l.google.com:19302','stun:stun.cloudflare.com:3478']}]};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function api(path,body){
  const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  if(!r.ok) throw new Error(await r.text()); return r.json();
}
async function poll(room,client,handler){
  while(!state.closed){
    try{
      const r=await fetch(`/poll?room=${encodeURIComponent(room)}&client=${encodeURIComponent(client)}&t=${Date.now()}`);
      if(r.ok){const messages=await r.json(); for(const m of messages) await handler(m);}
    }catch(e){}
    await sleep(250);
  }
}
async function send(type,data){await api('/signal',{room:state.room,client:state.client,type,data});}

if(!isViewer){
  const status=document.querySelector('#hostStatus');
  const start=document.querySelector('#start');
  const cancel=document.querySelector('#cancel');

  cancel.onclick=()=>{
    state.closed=true;
    status.textContent='Sharing cancelled.';
    start.disabled=true;
    cancel.disabled=true;
  };

  start.onclick=async()=>{
    start.disabled=true;
    cancel.disabled=true;
    status.textContent='Opening the browser sharing permission…';
    try{
      // Asking for a display capture keeps the capture alive when the user
      // navigates to another page, provided the user selects Entire Screen.
      state.stream=await navigator.mediaDevices.getDisplayMedia({
        video:{cursor:'always'},
        audio:false,
        preferCurrentTab:false,
        selfBrowserSurface:'exclude',
        surfaceSwitching:'include'
      });
      document.querySelector('#hostPreview').srcObject=state.stream;
      const created=await api('/room',{action:'create'}); state.room=created.room; state.client=created.client;
      document.querySelector('#code').textContent=state.room;
      document.querySelector('#roomLine').classList.remove('hidden');
      document.querySelector('#intro').textContent='This device screen is ready to share.';
      status.textContent='Sharing is active. You can switch to another page or app; the selected screen remains shared.';
      state.pc=new RTCPeerConnection(iceServers);
      state.stream.getTracks().forEach(t=>state.pc.addTrack(t,state.stream));
      state.pc.onicecandidate=e=>{if(e.candidate) send('candidate',e.candidate).catch(()=>{});};
      state.stream.getVideoTracks()[0].onended=()=>{state.closed=true;status.textContent='Sharing stopped.';};
      poll(state.room,state.client,async m=>{
        if(m.type==='viewer-ready'){
          const offer=await state.pc.createOffer(); await state.pc.setLocalDescription(offer);
          await send('offer',state.pc.localDescription);
          status.textContent='Viewer connected. Your selected screen is being sent live.';
        }else if(m.type==='answer') await state.pc.setRemoteDescription(m.data);
        else if(m.type==='candidate') try{await state.pc.addIceCandidate(m.data);}catch(e){}
      });
    }catch(e){
      state.closed=false;
      start.disabled=false;
      cancel.disabled=false;
      status.textContent='Screen sharing was cancelled or is unavailable. '+e.message;
    }
  };
}else{
  const status=document.querySelector('#viewerStatus');
  document.querySelector('#join').onclick=async()=>{
    const room=document.querySelector('#room').value.trim().toUpperCase();
    if(!room){status.textContent='Enter a room code.';return;}
    document.querySelector('#join').disabled=true;
    try{
      const joined=await api('/room',{action:'join',room}); state.room=room;state.client=joined.client;
      state.pc=new RTCPeerConnection(iceServers);
      state.pc.ontrack=e=>{document.querySelector('#remote').srcObject=e.streams[0];status.textContent='Live screen connected.';};
      state.pc.onicecandidate=e=>{if(e.candidate) send('candidate',e.candidate).catch(()=>{});};
      poll(state.room,state.client,async m=>{
        if(m.type==='offer'){
          await state.pc.setRemoteDescription(m.data);
          const answer=await state.pc.createAnswer(); await state.pc.setLocalDescription(answer);
          await send('answer',state.pc.localDescription); status.textContent='Connected; waiting for video…';
        }else if(m.type==='candidate') try{await state.pc.addIceCandidate(m.data);}catch(e){}
      });
      await send('viewer-ready',{}); status.textContent='Waiting for host…';
    }catch(e){document.querySelector('#join').disabled=false;status.textContent='Could not join room: '+e.message;}
  };
}
</script></body></html>'''


def new_client():
    return secrets.token_urlsafe(9)


def new_room():
    return secrets.token_hex(3).upper()


def create_room():
    with LOCK:
        room=new_room()
        while room in ROOMS: room=new_room()
        client=new_client(); ROOMS[room]={'clients':{client:[]},'created':time.time()}
        return room,client


def join_room(room):
    with LOCK:
        if room not in ROOMS: raise KeyError('Room not found')
        if len(ROOMS[room]['clients']) >= 2: raise RuntimeError('Room is full')
        client=new_client(); ROOMS[room]['clients'][client]=[]
        return client


def post_message(room,client,kind,data):
    with LOCK:
        if room not in ROOMS or client not in ROOMS[room]['clients']:
            raise KeyError('Invalid room or client')
        for other,queue in ROOMS[room]['clients'].items():
            if other != client: queue.append({'type':kind,'data':data})


def get_messages(room,client):
    with LOCK:
        if room not in ROOMS or client not in ROOMS[room]['clients']:
            raise KeyError('Invalid room or client')
        q=ROOMS[room]['clients'][client]; ROOMS[room]['clients'][client]=[]
        return q


class Handler(BaseHTTPRequestHandler):
    def send_json(self,obj,status=200):
        body=json.dumps(obj,separators=(',',':')).encode()
        self.send_response(status); self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body))); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(body)

    def read_json(self):
        n=int(self.headers.get('Content-Length','0')); return json.loads(self.rfile.read(n) or b'{}')

    def do_GET(self):
        parsed=urlparse(self.path)
        if parsed.path=='/poll':
            q=parse_qs(parsed.query)
            try:self.send_json(get_messages(q['room'][0],q['client'][0]))
            except Exception as e:self.send_json({'error':str(e)},400)
            return
        if parsed.path!='/': self.send_error(404); return
        body=HTML.encode(); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_POST(self):
        if self.path not in ('/room','/signal'): self.send_error(404); return
        try:
            data=self.read_json()
            if self.path=='/room':
                if data.get('action')=='create': room,client=create_room(); self.send_json({'room':room,'client':client})
                elif data.get('action')=='join': self.send_json({'client':join_room(data['room'].upper())})
                else:self.send_json({'error':'unknown action'},400)
            else:
                post_message(data['room'],data['client'],data['type'],data.get('data'))
                self.send_json({'ok':True})
        except KeyError as e:self.send_json({'error':str(e)},404)
        except Exception as e:self.send_json({'error':str(e)},400)

    def log_message(self,fmt,*args): print(f'{self.address_string()} - {fmt % args}')


if __name__=='__main__':
    server=ThreadingHTTPServer((HOST,PORT),Handler)
    print(f'Omni Screen Share: http://127.0.0.1:{PORT}')
    try:
        webbrowser.open(f'http://127.0.0.1:{PORT}', new=2)
    except Exception as exc:
        print(f'Could not open browser automatically: {exc}')
    print('The viewer must use the host device IP and the room code.')
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
