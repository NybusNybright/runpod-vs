import subprocess
import os
import signal
import webbrowser
from flask import Flask, render_template_string, redirect, url_for, request
from threading import Timer
from datetime import datetime

log_path = "/workspace/logs"
os.makedirs(log_path, exist_ok=True)

# Dual print to console and log file
def log_print(*args, **kwargs):
    print(*args, **kwargs)
    with open(os.path.join(log_path, "launcher.log"), "a") as f:
        print(*args, file=f, **kwargs)

log_print(f"\n\U0001F553 Launcher started at {datetime.now()}\n")

app = Flask(__name__, static_folder='static')

processes = {
    "comfy": None,
    "sd-webui": None
}

ports = {
    "comfy": 8188,
    "sd-webui": 6767,
    "jupyter": 8888,
    "launcher": 5555
}

html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>WebUI Launcher</title>
    <link rel="icon" href="/static/favicon.png" type="image/png">
    <style>
        body { font-family: sans-serif; text-align: center; margin-top: 30px; background-color: #111; color: white; }
        button {
            padding: 15px 30px;
            margin: 10px;
            font-size: 16px;
            border: none;
            cursor: pointer;
            border-radius: 8px;
            min-width: 150px;
        }
        .running { background-color: #4CAF50; color: white; }
        .stopped { background-color: #888; color: white; }
        .terminate { background-color: #f44336; color: white; }
        .open { background-color: #2196F3; color: white; }
        .refresh { background-color: #ff9800; color: white; }
        .jupyter { background-color: #9c27b0; color: white; }
        pre { background: #222; padding: 10px; border-radius: 8px; text-align: left; display: inline-block; white-space: pre-wrap; max-width: 80%%; overflow-wrap: break-word; }
        a { text-decoration: none; }
        .controls-row { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>WebUI Launcher 🚀</h1>
        <p><strong>RunPod ID:</strong> {{ RUNPOD_ID }} &nbsp;|&nbsp; <strong>IP:</strong> {{ PUBLIC_IP }} &nbsp;|&nbsp; <strong>Port:</strong> {{ TCP_PORT }}</p>

    {% for key in ["comfy", "sd-webui"] %}
        <form action="/launch/{{ key }}" method="post" style="display:inline;">
            <button class="{{ 'running' if running[key] else 'stopped' }}">Launch {{ key.title() }}</button>
        </form>
        <form action="/terminate/{{ key }}" method="post" style="display:inline;">
            <button class="terminate">Terminate {{ key.title() }}</button>
        </form>
        <button class="open" onclick="window.open('https://{{ RUNPOD_ID }}-{{ ports[key] }}.proxy.runpod.net', '_blank')">
            Open {{ key.title() }}
        </button>
        <br><br>
    {% endfor %}

    <h2>Open Ports</h2>
    <pre>{{ open_ports }}</pre>

    <div class="controls-row">
        <form action="/refresh_ports" method="get" style="display:inline;">
            <button class="refresh">Refresh Ports</button>
        </form>
        <form action="/terminate_launcher" method="post" style="display:inline;">
            <button class="terminate">Terminate Launcher</button>
        </form>
        <button class="jupyter" onclick="window.open('https://{{ RUNPOD_ID }}-8888.proxy.runpod.net', '_blank')">
            Open Jupyter
        </button>
    </div>

    <form action="/reset_ports" method="post" style="margin-top: 30px;">
        <button class="terminate">Reset Ports</button>
    </form>
</body>
</html>
'''

def kill_if_running(name):
    port = ports[name]
    try:
        if processes.get(name) and processes[name].poll() is None:
            os.killpg(os.getpgid(processes[name].pid), signal.SIGTERM)
            log_print(f"✅ Killed {name} (PID {processes[name].pid})")
        else:
            output = subprocess.check_output(["lsof", "-i", f":{port}"], stderr=subprocess.DEVNULL).decode()
            for line in output.splitlines()[1:]:
                pid = int(line.split()[1])
                log_print(f"🔪 Killing fallback {name} PID: {pid}")
                os.killpg(os.getpgid(pid), signal.SIGTERM)
    except Exception as e:
        log_print(f"⚠️ Could not terminate {name}: {e}")
    processes[name] = None

def get_open_ports():
    try:
        output = subprocess.check_output(["ss", "-tuln"], stderr=subprocess.DEVNULL).decode()
        filtered = []
        for line in output.splitlines():
            if any(f":{p} " in line for p in [ports["comfy"], ports["sd-webui"], ports["launcher"]]):
                parts = line.split()
                port = parts[4] if len(parts) > 4 else "?"
                pid_info = subprocess.getoutput(f"lsof -i :{port.split(':')[-1]} -sTCP:LISTEN -P -n | awk 'NR>1 {{print $2, $1}}'")
                for pid_line in pid_info.splitlines():
                    pid, cmd = pid_line.strip().split()[:2]
                    filtered.append(f"PID {pid} | {port} | {cmd}")
        return "\n".join(filtered) if filtered else "No relevant open ports."
    except Exception as e:
        return f"Error checking ports: {e}"

@app.route("/")
def index():
    pod_id = os.environ.get("RUNPOD_POD_ID")
    public_ip = os.environ.get("RUNPOD_PUBLIC_IP")
    tcp_port = os.environ.get("RUNPOD_TCP_PORT_22")
    print("🧠 Rendering WebUI with pod_id:", pod_id)
    open_port_text = get_open_ports()
    running = {
        "comfy": str(ports['comfy']) in open_port_text,
        "sd-webui": str(ports['sd-webui']) in open_port_text  # Changed 'forge' to 'sd-webui'
    }
    return render_template_string(
        html_template,
        processes=processes,
        ports=ports,
        open_ports=open_port_text,
        RUNPOD_ID=pod_id,
        PUBLIC_IP=public_ip,
        TCP_PORT=tcp_port,
        running=running
    )

@app.route("/refresh_ports")
def refresh_ports():
    return redirect(url_for("index"))

@app.route("/reset_ports", methods=["POST"])
def reset_ports():
    for port in ports.values():
        try:
            subprocess.run(["fuser", "-k", f"{port}/tcp"], check=False)
            log_print(f"🔪 Reset port {port}")
        except Exception as e:
            log_print(f"⚠️ Failed to reset port {port}: {e}")
    return redirect(url_for("index"))

@app.route("/launch/<name>", methods=["POST"])
def launch(name):
    if name not in ports:
        return redirect(url_for("index"))

    kill_if_running(name)

    try:
        if name == "comfy":
            cmd = [
                "/workspace/venv/bin/python",
                "/workspace/ComfyUI/main.py",
                "--listen",
                "--port", str(ports[name]),
                "--cuda-malloc"
            ]
        elif name == "sd-webui":
            cmd = [
                "/workspace/venv/bin/python",
                "/workspace/sd-webui/webui.py",
                "--listen",
                "--port", str(ports[name]),
                "--cuda-malloc"
            ]
        elif name == "jupyter":
            cmd = [
                "/workspace/venv/bin/jupyter",
                "lab",
                "--ip=0.0.0.0",
                "--port", str(ports[name]),
                "--no-browser"
            ]
        else:
            return redirect(url_for("index"))

        logfile = open(f"/workspace/logs/{name}.log", "a")
        log_print(f"🚀 Launching {name}: {' '.join(cmd)}")
        processes[name] = subprocess.Popen(cmd, preexec_fn=os.setsid, stdout=logfile, stderr=logfile)

    except Exception as e:
        log_print(f"❌ Failed to launch {name}: {e}")
        processes[name] = None

    return redirect(url_for("index"))

@app.route("/terminate/<name>", methods=["POST"])
def terminate(name):
    if name in processes:
        log_print(f"⛔ Terminating {name}...")
        kill_if_running(name)
    else:
        log_print(f"⚠️ Unknown process: {name}")
    return redirect(url_for("index"))

@app.route("/terminate_launcher", methods=["POST"])
def terminate_launcher():
    log_print("🛑 Terminating launcher via web button")
    os._exit(0)

if __name__ == "__main__":
    Timer(1.0, lambda: webbrowser.open_new("http://localhost:5555")).start()
    app.run(host="0.0.0.0", port=5555, debug=False, use_reloader=False)