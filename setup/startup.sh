#!/bin/bash

bash -c "
  echo '🚀 Initializing pod startup command'
  
  apt update && apt install -y \
  git wget curl nano zip tar \
  ffmpeg p7zip-full lsof \
  libsm6 libxext6 psmisc
  
  rm -rf /workspace/setup
  cd /workspace
  git clone https://${GIT_PAT}@github.com/NybusNybright/runpod-manual.git /workspace/temp

  if [ \$? -eq 0 ]; then
    echo '✅clone finished'
  else
    echo '❌ Git clone failed' && exit 1
  fi

  cp -r /workspace/temp/{*,.[!.]*} /workspace/
  rm -rf /workspace/temp

  echo '✅ Repo cloned and copied to /workspace/setup'
  bash /workspace/setup/setup.sh
"