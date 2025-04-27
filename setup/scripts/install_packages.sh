#!/bin/bash

echo "📦 Installing system packages..."

cd /workspace/

apt update && apt install -y \
  git wget curl nano zip tar \
  ffmpeg p7zip-full lsof \
  libsm6 libxext6 psmisc

# Create and activate virtual environment
echo "🐍 Create and activate Python virtual environment"
python3 -m venv /workspace/venv
source /workspace/venv/bin/activate

# Upgrade python packages inside venv
echo "📦 Installing Python packages "
pip install --upgrade pip
pip install uv
uv pip install flask "huggingface_hub[hf_transfer]" --system

echo "✅ Python packages complete."