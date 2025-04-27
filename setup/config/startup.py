import os
import json
import subprocess
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv("C:/Users/Home/.keys/keys.env")
api_key = os.getenv("RUNPOD_API")

# Request pod details using requests
headers = {'Authorization': f'Bearer {api_key}'}
response = requests.get("https://rest.runpod.io/v1/pods", headers=headers)
response.raise_for_status()  # Raises error if bad response

api_data = response.json()[0]

pod_ip = api_data["publicIp"]
pod_port = api_data["portMappings"]["22"]

# Create SSH config content
ssh_config = f"""Host runpod
  HostName {pod_ip}
  User root
  Port {pod_port}
  IdentityFile ~/.ssh/id_ed25519
"""

# Save to Windows SSH config
config_path = os.path.expanduser("C:/Users/Home/.ssh/config")
with open(config_path, "w") as f:
    f.write(ssh_config)

print(f"✅ SSH config saved to {config_path}")

# Build SCP command
scp_command = [
    "scp",
    "-i", "C:/Users/Home/.ssh/id_ed25519",
    "-P", str(pod_port),
    "-o", "StrictHostKeyChecking=no",
    "-r",
    "C:/Users/Home/git/runpod-vs/setup",
    f"root@{pod_ip}:/workspace/"
]

print(f"🚀 Running SCP upload...")
subprocess.run(scp_command)

print("🎉 Upload completed.")

#Run Setup
ssh_command = [
    "ssh",
    "-i", "C:/Users/Home/.ssh/id_ed25519",
    "-p", str(pod_port),
    f"root@{pod_ip}",
    """
    cd /workspace/setup &&
    bash config/setup.sh
    """
]

print(f"🚀 Running config/setup.sh on the pod...")
subprocess.run(ssh_command)
print("🎉 setup.sh executed remotely.")
