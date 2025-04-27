# Install Comfy-cli
if [ ! -f /workspace/touch/comfycli-install ]; then
    echo "📦 Installing Comfy-CLI"
    uv pip install comfy-cli 
    comfy --skip-prompt install --nvidia
    touch /workspace/touch/comfycli-install
else
    echo "📁 Comfy-CLI already installed — skipping."
fi

# Now safe to make subfolders
mkdir -p /workspace/ComfyUI/custom_nodes /workspace/ComfyUI/scripts /workspace/ComfyUI/workflows

# Clone ComfyUI custom nodes
if [ ! -f /workspace/touch/comfyui-nodes ]; then
    echo "🧩 Installing ComfyUI nodes and LLM tools..."
    cd /workspace/ComfyUI/custom_nodes

    # 🧩 Node Packs / Node Collections
    (
    git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git &    # Big node pack for workflows
    git clone https://github.com/LucianoCirino/efficiency-nodes-comfyui.git &  # Speed-focused utility nodes
    git clone https://github.com/Ling-APE/ComfyUI-All-in-One-FluxDev-Workflow.git & # Combined node + workflow pack

    # 🧠 AI Enhancement / Interrogation / Prompt Tools
    git clone https://github.com/prodogape/ComfyUI-clip-interrogator.git &   # Auto caption and tagging tool
    git clone https://github.com/inflamously/comfyui-prompt-enhancer.git &    # Prompt enhancement tool

    # 🗣️ LLM / Text / SDXL Handling
    git clone https://github.com/SeargeDP/ComfyUI_Searge_LLM.git &      # LLM integration for Comfy
    git clone https://github.com/SeargeDP/SeargeSDXL.git &              # SDXL workflows and models

    # 🎨 IP Adapter Tools
    git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git &     # Improved image-to-image adapters
    wait
    )

    touch /workspace/touch/comfyui-nodes
else
    echo "📁 ComfyUI custom nodes already installed — skipping."
fi

# Clone ComfyUI scripts and workflows
if [ ! -f /workspace/touch/comfyui-scripts-workflows ]; then
    echo "📜 Installing ComfyUI scripts and SDXL workflows..."
    
    # 📜 Utility Scripts
    cd /workspace/ComfyUI/scripts
    (
    git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git &  # Extra utility scripts
    wait
    )

    # 🧩 Workflow Packs
    cd /workspace/ComfyUI/workflows
    (
    git clone https://github.com/cubiq/ComfyUI_Workflows.git &     # Workflow templates by Cubiq
    git clone https://github.com/LostDiffusion/ComfyUI-Workflows.git & # Advanced workflows by LostDiffusion
    wait
    )

    touch /workspace/touch/comfyui-scripts-workflows
else
    echo "📁 ComfyUI scripts and workflows already installed — skipping."
fi

# Install ComfyUI dependencies
if [ ! -f /workspace/touch/comfyui-install ]; then
    echo "📦 Installing ComfyUI Python dependencies..."
    cd /workspace/ComfyUI
    uv pip install -r requirements.txt
    touch /workspace/touch/comfyui-install
else
    echo "📁 ComfyUI requirements already installed — skipping."
fi

echo "✅ Comfy CLI + UI + custom nodes + workflows + scripts setup complete."
