#!/bin/bash

# Enable Hugging Face accelerated transfer
export HF_HUB_ENABLE_HF_TRANSFER=1

echo "🔥 Installing Stable Diffusion WebUI (SD WebUI)..."

# Create touch directory
mkdir -p /workspace/touch

# Activate venv
source /workspace/venv/bin/activate

# Clone SD WebUI repo if it doesn't exist
if [ ! -f /workspace/touch/sd-webui-clone ]; then
    echo "📥 Cloning SD WebUI repository..."
    git clone --recurse-submodules https://github.com/AUTOMATIC1111/stable-diffusion-webui.git /workspace/sd-webui
    touch /workspace/touch/sd-webui-clone
else
    echo "📁 SD WebUI repo already cloned — skipping."
fi

# Clone SD WebUI extensions
EXT_DIR="/workspace/sd-webui/extensions"

if [ ! -f /workspace/touch/sd-webui-extensions ]; then
    echo "🧩 Cloning SD WebUI extensions..."
    mkdir -p "$EXT_DIR"
    cd "$EXT_DIR"

    (
    # 🧩 Basic Extensions
    git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui-wildcards.git &     # Wildcards for prompts
    git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui-aesthetic-gradients.git &  # Aesthetic rating support

    # 🧩 UI / Browser Tools
    git clone https://github.com/BlafKing/sd-civitai-browser-plus.git &     # Enhanced Civitai browser
    git clone https://github.com/zanllp/sd-webui-infinite-image-browsing.git & # Infinite scrolling image browser

    # 🛠️ Utility / Model Handling
    git clone https://github.com/KohakuBlueleaf/a1111-sd-webui-locon.git &  # LoRA training / LoCon support
    git clone https://github.com/Bing-su/adetailer.git &                    # Automatic face/body fixing
    git clone https://github.com/deforum-art/sd-webui-deforum.git &          # Video animation (Deforum)
    git clone https://github.com/Uminosachi/sd-webui-inpaint-anything.git &  # Inpaint-anywhere tool
    git clone https://github.com/mcmonkeyprojects/sd-dynamic-thresholding.git & # Dynamic thresholding for generations
    git clone https://github.com/Mikubill/sd-webui-controlnet.git &          # ControlNet integration
    git clone https://github.com/civitai/sd_civitai_extension.git &          # Civitai integration

    wait
    )

    touch /workspace/touch/sd-webui-extensions
else
    echo "📁 WebUI extensions already installed — skipping."
fi

# Navigate to the WebUI directory
cd /workspace/sd-webui

# Install Python dependencies
if [ ! -f /workspace/touch/sd-webui-install ]; then
    echo "📦 Installing SD WebUI Python dependencies..."
    uv pip install -r requirements_versions.txt --system
    touch /workspace/touch/sd-webui-install
else
    echo "📁 SD WebUI dependencies already installed — skipping."
fi

echo "✅ SD WebUI setup complete."
