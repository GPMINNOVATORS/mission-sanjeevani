"""Tiny control-room web dashboard (standard library only).

Run:  sanjeevani serve   then open http://127.0.0.1:8000
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .dispatch import DEMO_FLEET, plan_dispatch
from .models import PatientReport
from .triage import triage


def assess(payload: dict) -> dict:
    report = PatientReport.from_dict(payload)
    result = triage(report)
    plan = plan_dispatch(report, result, DEMO_FLEET)
    return {
        "level": result.level.name,
        "score": result.score,
        "reasons": result.reasons,
        "dispatch": {
            "dispatched": plan.dispatched,
            "drone_id": plan.drone_id,
            "payload": plan.payload,
            "distance_km": plan.distance_km,
            "eta_minutes": plan.eta_minutes,
            "needs_doctor_authorisation": plan.needs_doctor_authorisation,
            "notes": plan.notes,
        },
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE.encode(), "text/html; charset=utf-8")
        elif self.path == "/health":
            self._send(200, b'{"status":"ok"}', "application/json")
        else:
            self._send(404, b'{"error":"not found"}', "application/json")

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/assess":
            return self._send(404, b'{"error":"not found"}', "application/json")
        try:
            n = int(self.headers.get("Content-Length", 0))
            out = assess(json.loads(self.rfile.read(n)))
            self._send(200, json.dumps(out).encode(), "application/json")
        except (KeyError, ValueError, TypeError) as e:
            self._send(400, json.dumps({"error": f"bad request: {e}"}).encode(), "application/json")

    def log_message(self, *args) -> None:  # keep console quiet
        pass


def make_server(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), Handler)


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mission Sanjeevani: Control Room</title>
<style>
:root{color-scheme:light dark}
body{font-family:system-ui,sans-serif;max-width:860px;margin:0 auto;padding:16px;line-height:1.4}
h1{margin:.2em 0}.warn{background:#fff3cd;color:#664d03;padding:8px 12px;border-radius:8px;font-size:.9em}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:12px 0}
label{display:flex;flex-direction:column;font-size:.85em;gap:3px}
input,select{padding:7px;border-radius:6px;border:1px solid #8888;font-size:1em}
button{padding:9px 14px;border-radius:8px;border:0;background:#2e7d32;color:#fff;font-size:1em;cursor:pointer}
button.alt{background:#546e7a}.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0}
#out{margin-top:16px;padding:14px;border-radius:10px;border:2px solid #8888;display:none}
.badge{display:inline-block;padding:4px 12px;border-radius:20px;color:#fff;font-weight:700}
.GREEN{background:#2e7d32}.YELLOW{background:#b28704}.ORANGE{background:#ef6c00}.RED{background:#c62828}
</style></head><body>
<h1>🚁 Mission Sanjeevani <small style="font-weight:400">Control Room</small></h1>
<div class="warn">Research prototype. Not a medical device. Thresholds need clinical validation.</div>
<div class="row"><b>Try an example:</b>
<button class="alt" onclick="fill('stable')">Stable</button>
<button class="alt" onclick="fill('snakebite')">Snakebite</button>
<button class="alt" onclick="fill('accident')">Road accident</button>
<button class="alt" onclick="fill('pregnancy')">Pregnancy + bleeding</button></div>
<div class="grid">
<label>Complaint<select id="complaint"><option value="general">General</option><option value="snakebite">Snakebite</option><option value="road_accident">Road accident</option><option value="pregnancy">Pregnancy</option><option value="cardiac">Cardiac</option></select></label>
<label>Age<input id="age" type="number" value="30"></label>
<label>Heart rate (bpm)<input id="heart_rate" type="number" value="72"></label>
<label>Resp. rate (/min)<input id="resp_rate" type="number" value="16"></label>
<label>SpO₂ (%)<input id="spo2" type="number" value="98"></label>
<label>Systolic BP (mmHg)<input id="systolic_bp" type="number" value="120"></label>
<label>Temperature (°C)<input id="temperature_c" type="number" step="0.1" value="36.8"></label>
<label>Consciousness<select id="consciousness"><option>alert</option><option>confused</option><option>voice</option><option>pain</option><option>unresponsive</option></select></label>
<label>Latitude<input id="lat" type="number" step="0.01" value="25.55"></label>
<label>Longitude<input id="lon" type="number" step="0.01" value="85.20"></label>
</div>
<div class="row"><label style="flex-direction:row;gap:6px"><input id="heavy_bleeding" type="checkbox"> Heavy bleeding</label>
<label style="flex-direction:row;gap:6px"><input id="seizure" type="checkbox"> Seizure</label>
<button onclick="run()">Assess &amp; plan dispatch</button></div>
<div id="out"></div>
<script>
const $=id=>document.getElementById(id);
const P={
 stable:{complaint:'general',heart_rate:72,resp_rate:16,spo2:98,systolic_bp:120,temperature_c:36.8,consciousness:'alert',heavy_bleeding:false,seizure:false},
 snakebite:{complaint:'snakebite',heart_rate:112,resp_rate:22,spo2:94,systolic_bp:105,temperature_c:37.2,consciousness:'alert',heavy_bleeding:false,seizure:false},
 accident:{complaint:'road_accident',heart_rate:128,resp_rate:26,spo2:91,systolic_bp:88,temperature_c:36.4,consciousness:'confused',heavy_bleeding:true,seizure:false},
 pregnancy:{complaint:'pregnancy',heart_rate:118,resp_rate:22,spo2:96,systolic_bp:95,temperature_c:37.0,consciousness:'alert',heavy_bleeding:true,seizure:false}};
function fill(k){const p=P[k];for(const f in p){const e=$(f);if(e.type==='checkbox')e.checked=p[f];else e.value=p[f];}}
function add(parent,tag,text){const e=document.createElement(tag);e.textContent=text;parent.appendChild(e);return e;}
async function run(){
 const body={patient_id:'UI-'+Date.now(),complaint:$('complaint').value,age:+$('age').value||null,
  heavy_bleeding:$('heavy_bleeding').checked,seizure:$('seizure').checked,
  vitals:{heart_rate:+$('heart_rate').value,resp_rate:+$('resp_rate').value,spo2:+$('spo2').value,
   systolic_bp:+$('systolic_bp').value,temperature_c:+$('temperature_c').value,consciousness:$('consciousness').value},
  location:{lat:+$('lat').value,lon:+$('lon').value}};
 const out=$('out');out.style.display='block';out.replaceChildren();
 try{
  const r=await fetch('/api/assess',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  const d=await r.json();if(!r.ok)throw new Error(d.error);
  const h=add(out,'h2','Triage: ');const b=add(h,'span',d.level);b.className='badge '+d.level;add(h,'small',' (score '+d.score+')');
  if(d.reasons.length){const ul=add(out,'ul','');d.reasons.forEach(x=>add(ul,'li',x));}
  const x=d.dispatch;
  if(x.dispatched){add(out,'p','Dispatch: drone '+x.drone_id+' with '+x.payload+', '+x.distance_km+' km, ETA '+x.eta_minutes+' min.');}
  else{add(out,'p','No drone dispatch.');}
  const ul2=add(out,'ul','');x.notes.forEach(n=>add(ul2,'li',n));
 }catch(e){add(out,'p','Error: '+e.message);}
}
</script></body></html>
"""
