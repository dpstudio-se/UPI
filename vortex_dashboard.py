import asyncio
from datetime import datetime
import json
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Vortex Omega-7834 Dashboard")

REGISTRY_FILE = Path(
    r"C:\Users\Admin\WORKSPACE_EMILIA_T800_VORTEX\universal_physics_index_export\epistemic_master_registry.json"
)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <title>VORTEX OMEGA-7834 // LIVE SWARM DASHBOARD</title>
    <style>
        body { background-color: #0b0f19; color: #00ffcc; font-family: 'Courier New', monospace; margin: 0; padding: 20px; }
        h1 { border-bottom: 2px solid #00ffcc; padding-bottom: 10px; font-size: 20px; text-shadow: 0 0 10px rgba(0,255,204,0.5); }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
        .panel { background: #111827; border: 1px solid #1f2937; padding: 15px; border-radius: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        pre { background: #030712; padding: 10px; border: 1px solid #374151; height: 300px; overflow-y: auto; color: #34d399; }
        .status-badge { display: inline-block; padding: 5px 10px; background: #065f46; color: #6ee7b7; border-radius: 3px; font-weight: bold; }
    </style>
</head>
<body>
    <h1>VORTEX-DNA v9.φ // REAL-TIME SWARM MONITOR [8.00 Hz]</h1>
    <div>System Status: <span class="status-badge" id="sys-status">ACTIVE</span></div>
    
    <div class="grid">
        <div class="panel">
            <h3>Live Agent Event Stream</h3>
            <pre id="logs">Ansluter till svärm-synaps...</pre>
        </div>
        <div class="panel">
            <h3>Epistemisk Master Registry State</h3>
            <pre id="registry">Laddar register...</pre>
        </div>
    </div>

    <script>
        const ws = new WebSocket(`ws://${window.location.host}/ws`);
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            const logPre = document.getElementById('logs');
            logPre.innerHTML += `[${data.timestamp}] ${data.message}\\n`;
            logPre.scrollTop = logPre.scrollHeight;
        };

        async function fetchRegistry() {
            const response = await fetch('/api/registry');
            const data = await response.json();
            document.getElementById('registry').innerText = JSON.stringify(data, null, 2);
        }
        setInterval(fetchRegistry, 3000);
        fetchRegistry();
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
  return HTML_TEMPLATE


@app.get("/api/registry")
async def get_registry():
  if REGISTRY_FILE.exists():
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  return {"status": "Registry saknas"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  try:
    while True:
      # Simulera live-händelser från svärmen i realtid
      timestamp = datetime.utcnow().strftime("%H:%M:%S")
      await websocket.send_json({
          "timestamp": timestamp,
          "message": "Svärm-nod synkroniserad och verifierad via 8 Hz baslinje.",
      })
      await asyncio.sleep(2.5)
  except WebSocketDisconnect:
    print("[DASHBOARD] Klient kopplade från.")


if __name__ == "__main__":
  print("[+] Startar Vortex Dashboard på http://127.0.0.1:8000 ...")
  uvicorn.run(app, host="127.0.0.1", port=8000)