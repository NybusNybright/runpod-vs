import os
import json
from dotenv import load_dotenv
import http.client

# Load API key
load_dotenv("C:/Users/Home/.keys/keys.env")
api_key = os.getenv("RUNPOD_API")

# Request pod details
conn = http.client.HTTPSConnection("rest.runpod.io")
headers = { 'Authorization': f'Bearer {api_key}' }
conn.request("GET", "/v1/pods", headers=headers)

res = conn.getresponse()
data = json.loads(res.read().decode("utf-8"))
first_pod = data[0]  # Assumes one active pod

ip = first_pod["publicIp"]
port = first_pod["portMappings"]["22"]

# Create SSH config content
ssh_config = f"""Host runpod
  HostName {ip}
  User root
  Port {port}
  IdentityFile ~/.ssh/id_ed25519
"""

# Save to Windows SSH config
config_path = os.path.expanduser("C:/Users/Home/.ssh/config")
with open(config_path, "w") as f:
    f.write(ssh_config)

print(f"✅ SSH config saved to {config_path}")
